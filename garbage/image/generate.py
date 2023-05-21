import base64
import os
import requests
from dotenv import load_dotenv
load_dotenv()

from typing import Callable

from garbage.conversation.conversation import Character 

from garbage.image.template import prompt

engine_id = "stable-diffusion-512-v2-1"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv('STABILITY_API_KEY')

if api_key is None:
    raise Exception("Missing Stability API key.")

def portrait_getter(character: Character, base_path: str) -> Callable[[], str]:

    getter_func = lambda :generate(character, base_path)

    return getter_func

def generate(character: Character, base_path: str) -> str:

    formatted = prompt.format(
        race = character.race,
    )

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": formatted
                }
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 100,
            "stype_preset": 'fantasy-art'
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        img_path = f"{base_path}/image/{character.name}.png"
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))

    return img_path

if __name__ == '__main__':

    character = Character(
        name='bob',
        voice='Elf'
    )

    generate(character)