import base64
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

from garbage.conversation.models import Character 
from garbage.conversation.random_character import new_character 

from garbage.image.template import prompt

engine_id = "stable-diffusion-512-v2-1"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv('STABILITY_API_KEY')

if api_key is None:
    raise Exception("Missing Stability API key.")

def generate(character: Character) -> str:

    formatted = prompt.format(
        race = character.race,
        occupation = character.occupation
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
        img_path = f"images/{character.name}.png"
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))

    return img_path

if __name__ == '__main__':

    character = Character(
        name='bob',
        race='Elf',
        occupation='Wizard',
        emotional_state='',
        obssessed_with=[],
        has_distate_for=[]

    )

    generate(character)