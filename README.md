# How to Build an AI Video Agent with Python and the Shotstack API

### Create Promo Template with the following JSON:

```json
{
  "timeline": {
    "background": "#404548",
    "tracks": [
      {
        "clips": [
          {
            "asset": {
              "type": "text",
              "text": "{{ CTA }}",
              "alignment": {
                "horizontal": "center",
                "vertical": "center"
              },
              "font": {
                "color": "#000000",
                "family": "Montserrat ExtraBold",
                "size": "66",
                "lineHeight": 1
              },
              "width": 535,
              "height": 163,
              "background": {
                "color": "#ffffff",
                "borderRadius": 73
              },
              "stroke": {
                "color": "#ffffff",
                "width": 0
              }
            },
            "start": 1.955,
            "length": "auto",
            "offset": {
              "x": 0,
              "y": 0.066
            },
            "position": "center",
            "fit": "none",
            "scale": 1,
            "transition": {
              "in": "slideUp"
            }
          }
        ]
      },
      {
        "clips": [
          {
            "length": 3.97,
            "asset": {
              "type": "image",
              "src": "{{ PRODUCT_IMAGE }}"
            },
            "start": 1.03,
            "offset": {
              "x": -0.014,
              "y": -0.188
            },
            "scale": 0.367,
            "position": "center",
            "transition": {
              "in": "slideUp"
            }
          }
        ]
      },
      {
        "clips": [
          {
            "length": 5,
            "asset": {
              "type": "image",
              "src": "https://templates.shotstack.io/grey-minimalist-product-ad/4ee059ca-2fcd-4bfe-9de9-d940238c49d4/source.png"
            },
            "start": 0,
            "offset": {
              "x": 0,
              "y": -0.344
            },
            "scale": 0.535,
            "position": "center"
          }
        ]
      },
      {
        "clips": [
          {
            "asset": {
              "type": "text",
              "text": "{{ PRODUCT_NAME }}",
              "alignment": {
                "horizontal": "center",
                "vertical": "center"
              },
              "font": {
                "color": "#ffffff",
                "family": "Montserrat ExtraBold",
                "size": "150",
                "lineHeight": 1
              },
              "width": 800,
              "height": 422,
              "stroke": {
                "color": "#0055ff",
                "width": 0
              }
            },
            "start": 0,
            "length": 5,
            "offset": {
              "x": 0,
              "y": 0.338
            },
            "position": "center",
            "fit": "none",
            "scale": 1,
            "transition": {
              "in": "slideUpFast"
            }
          }
        ]
      },
      {
        "clips": [
          {
            "fit": "none",
            "scale": 1,
            "asset": {
              "type": "text",
              "text": "{{ PRODUCT_FEATURE }}",
              "alignment": {
                "horizontal": "center",
                "vertical": "center"
              },
              "font": {
                "color": "#ffffff",
                "family": "Montserrat ExtraBold",
                "size": 46,
                "lineHeight": 1
              },
              "width": 728,
              "height": 72
            },
            "start": 0.25,
            "length": 4.75,
            "offset": {
              "x": 0,
              "y": 0.207
            },
            "position": "center",
            "transition": {
              "in": "slideUpFast"
            }
          }
        ]
      },
      {
        "clips": [
          {
            "length": 5,
            "asset": {
              "type": "image",
              "src": "https://templates.shotstack.io/grey-minimalist-product-ad/cfd0e601-9e06-47b7-9d3d-c79e2ae51711/source.png"
            },
            "start": 0,
            "offset": {
              "x": 0,
              "y": -0.471
            },
            "scale": 0.741,
            "position": "center"
          }
        ]
      }
    ]
  },
  "output": {
    "format": "mp4",
    "fps": 25,
    "size": {
      "width": 1080,
      "height": 1920
    }
  }
}
```

### Create General Template with the following JSON:

```sh
{
  "timeline": {
    "soundtrack": {
      "src": "{{ MUSIC_URL }}",
      "effect": "fadeInFadeOut"
    },
    "background": "#FFFFFF",
    "tracks": [
      {
        "clips": [
          {
            "asset": {
              "type": "rich-text",
              "text": "{{ TEXT_1 }}",
              "font": {
                "family": "Montserrat",
                "size": 48,
                "color": "#ffffff"
              },
              "animation": {
                "preset": "typewriter"
              }
            },
            "start": 0,
            "length": 4
          },
          {
            "asset": {
              "type": "rich-text",
              "text": "{{ TEXT_2 }}",
              "font": {
                "family": "Montserrat",
                "size": 48,
                "color": "#ffffff"
              },
              "animation": {
                "preset": "typewriter"
              }
            },
            "start": "auto",
            "length": 4
          }
        ]
      },
      {
        "clips": [
          {
            "asset": {
              "type": "video",
              "src": "{{ VIDEO_URL }}",
              "volume": 1
            },
            "start": 0,
            "length": "auto"
          }
        ]
      }
    ]
  },
  "output": {
    "format": "mp4",
    "fps": 25,
    "size": {
      "width": 1280,
      "height": 720
    }
  }
}
```

### Place your template IDs in the Python file:

```json
TEMPLATE_IDS = {
    "promo":   "YOUR_PROMO_TEMPLATE_UUID",
    "general": "YOUR_GENERAL_TEMPLATE_UUID",
}
```

### Install the required packages:

```sh
pip install anthropic requests
```

### Export your API keys as environment variables:

```sh
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export SHOTSTACK_API_KEY="your-shotstack-api-key"
```

### Run:

```sh
python ai_agent.py
```
