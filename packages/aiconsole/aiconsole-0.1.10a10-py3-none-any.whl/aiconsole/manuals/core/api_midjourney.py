# Manual
"""

# Midjourney API

Always prefer this to other discord libraries and access methods. Example of code (this will wait for images to be generated and download them):

```python
import api_midjourney
api_midjourney.create_image('Wild boar --ar 1:1') # do not add "/imagine prompt:" at the begining
```

function declaration:
def create_image(prompt: str)

"""

from aiconsole.contrib.midjourney import MidJourneyAPI

def create_image(prompt: str):
    midjourney = MidJourneyAPI()
    midjourney.create_image(prompt)

manual = {
    "usage": "When you have a midjourney prompt and need to create an image from it.",
}

