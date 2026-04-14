import os
import time

import anthropic
import requests

# -- Configuration -------------------------------------------------------------
SHOTSTACK_API_KEY = os.environ.get("SHOTSTACK_API_KEY")
SHOTSTACK_BASE_URL = "https://api.shotstack.io/edit/stage"

TEMPLATE_IDS = {
    "promo":   "YOUR_PROMO_TEMPLATE_UUID",
    "general": "YOUR_GENERAL_TEMPLATE_UUID",
}

# -- System Prompt -------------------------------------------------------------
system_prompt = """
You are an AI video agent. You can render two types of video using Shotstack templates.

PROMO
  Use for: product promotions, product launches, and promotional announcements.
  Merge fields:
    - PRODUCT_NAME: the name of the product
    - PRODUCT_FEATURE: a short description of the product's key feature
    - CTA: the call-to-action text (e.g. "Shop Now", "Order Now")
    - PRODUCT_IMAGE: a publicly accessible URL of the product image

GENERAL
  Use for: general announcements, event videos, or any non-product content.
  Merge fields:
    - DISPLAY_TEXT: the main text to display in the video
    - IMAGE_URL: a publicly accessible URL to use as the background image
    - MUSIC_URL: a publicly accessible URL of the background music track
    - DURATION: the duration of the video in seconds (must be a positive number)

When the user requests a video:
1. Determine whether their intent is 'promo' or 'general'. If it is not clear, ask for clarification.
2. Extract the required merge field values from their message.
3. If any required value is missing, ask the user for it before proceeding.
4. Call the render_video tool with the correct video_type and populated merge fields.
"""

# -- Tool Definition -----------------------------------------------------------
video_tool = {
    "name": "render_video",
    "description": "Renders a video from a Shotstack template. Use this when the user asks to create or generate a video.",
    "input_schema": {
        "type": "object",
        "properties": {
            "video_type": {
                "type": "string",
                "enum": ["promo", "general"],
                "description": (
                    "The type of video to render. Use 'promo' for product promotions and launches. "
                    "Use 'general' for announcements, event videos, or any non-product content."
                ),
            },
            "merge_fields": {
                "type": "array",
                "description": "Array of find/replace pairs to populate the template placeholders.",
                "items": {
                    "type": "object",
                    "properties": {
                        "find": {"type": "string"},
                        "replace": {"type": "string"},
                    },
                    "required": ["find", "replace"],
                },
            },
            "output_format": {
                "type": "string",
                "enum": ["mp4", "gif"],
                "description": "Output format. Default to 'mp4'.",
            },
        },
        "required": ["video_type", "merge_fields", "output_format"],
    },
}

# -- Shotstack Function --------------------------------------------------------
def render_video(video_type: str, merge_fields: list[dict], output_format: str = "mp4") -> str:
    template_id = TEMPLATE_IDS.get(video_type)
    if not template_id:
        raise ValueError(f"Unknown video_type: {video_type!r}")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": SHOTSTACK_API_KEY,
    }

    payload = {
        "id": template_id,
        "merge": merge_fields,
        "output": {"format": output_format},
    }

    response = requests.post(
        f"{SHOTSTACK_BASE_URL}/templates/render",
        json=payload,
        headers=headers,
    )

    if response.status_code != 201:
        raise Exception(f"Shotstack API error ({response.status_code}): {response.text}")

    render_id = response.json()["response"]["id"]
    print(f"[Shotstack] Render queued: {render_id}")

    max_attempts = 60
    attempts = 0

    while attempts < max_attempts:
        time.sleep(5)
        attempts += 1

        status_data = requests.get(
            f"{SHOTSTACK_BASE_URL}/render/{render_id}",
            headers=headers,
        ).json()["response"]

        status = status_data["status"]
        print(f"[Shotstack] Status: {status} (attempt {attempts})")

        if status == "done":
            return status_data["url"]
        if status == "failed":
            raise Exception(f"Render failed: {status_data.get('error', 'check assets and payload')}")

    raise Exception(f"Render timed out after 5 minutes. Render ID: {render_id}")


# -- Agent Loop ----------------------------------------------------------------
client = anthropic.Anthropic()


def run_agent(user_message: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=system_prompt,
        tools=[video_tool],
        messages=[{"role": "user", "content": user_message}],
    )

    if response.stop_reason == "tool_use":
        tool_use_block = next(b for b in response.content if b.type == "tool_use")
        tool_input = tool_use_block.input

        print(f"[Agent] Tool call: render_video")
        print(f"[Agent] video_type: {tool_input['video_type']}")

        try:
            video_url = render_video(
                video_type=tool_input["video_type"],
                merge_fields=tool_input["merge_fields"],
                output_format=tool_input.get("output_format", "mp4"),
            )

            final_response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                system=system_prompt,
                tools=[video_tool],
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": response.content},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use_block.id,
                                "content": f"The video is ready: {video_url}",
                            }
                        ],
                    },
                ],
            )
            return final_response.content[0].text

        except Exception as e:
            return f"Error rendering video: {str(e)}"

    return response.content[0].text


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Video Agent ready. Describe the video you want to create.")
    print("Type 'quit' to exit.\n")

    conversation_history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue

        conversation_history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=system_prompt,
            tools=[video_tool],
            messages=conversation_history,
        )

        if response.stop_reason == "tool_use":
            tool_use_block = next(b for b in response.content if b.type == "tool_use")
            tool_input = tool_use_block.input

            print(f"\n[Agent] Tool call: render_video")
            print(f"[Agent] video_type: {tool_input['video_type']}\n")

            try:
                video_url = render_video(
                    video_type=tool_input["video_type"],
                    merge_fields=tool_input["merge_fields"],
                    output_format=tool_input.get("output_format", "mp4"),
                )

                conversation_history.append({"role": "assistant", "content": response.content})
                conversation_history.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": f"The video is ready: {video_url}",
                    }],
                })

                final_response = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=1024,
                    system=system_prompt,
                    tools=[video_tool],
                    messages=conversation_history,
                )

                reply = final_response.content[0].text
                print(f"\nAgent: {reply}\n")
                break  # video rendered — exit the loop

            except Exception as e:
                print(f"\nAgent: Error rendering video: {e}\n")
                break

        else:
            reply = response.content[0].text
            conversation_history.append({"role": "assistant", "content": reply})
            print(f"\nAgent: {reply}\n")
