from dotenv import load_dotenv
load_dotenv()

from typing import Callable
import os
import requests
import json

def download_bytes(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return response.content  

def get_video_for(image_file_getter: Callable[[], str], audio_path: str) -> bytes:

    image_path = image_file_getter()

    files = [
        ("input_face", open(image_path, "rb")),
        ("input_audio", open(audio_path, "rb")),
    ]
    payload = {}

    response = requests.post(
        "https://api.gooey.ai/v2/Lipsync/form/",
        headers={
            "Authorization": "Bearer " + os.environ["GOOEY_API_KEY"],
        },
        files=files,
        data={"json": json.dumps(payload)},
    )

    result = response.json()

    video_url = result['output']['output_video']

    video_bytes = download_bytes(video_url)

    return video_bytes


    
