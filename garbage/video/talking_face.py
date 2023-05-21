from dotenv import load_dotenv
load_dotenv()

import requests
import os
import sys

from typing import Callable

import time

api_key = os.environ.get('CREATIVE_REALITY_API_TOKEN')


def upload_image(image_path: str) -> str:

    image_path
    url = "https://api.d-id.com/images"

    files = {"image": (image_path, open(image_path, "rb"), "image/png")}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {api_key}"
    }

    response = requests.post(url, headers=headers,files = files)

    response_dict = response.json()

    return response_dict['url']

def upload_audio(audio_path: str) -> str:

    import requests

    url = "https://api.d-id.com/audios"

    files = {"audio": (audio_path, open(audio_path, "rb"), "audio/mpeg")}
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {api_key}"
    }

    response = requests.post(url, files=files, headers=headers)

    response_dict = response.json()

    return response_dict['url']

def create_talk(image_url: str, audio_url: str) -> str:

    url = " https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "audio",
            "subtitles": "false",
            "ssml": "false",
            "reduce_noise": "false",
            "audio_url": audio_url
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": image_url
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {api_key}"
    }

    response = requests.post(url, json=payload, headers=headers)

    response_dict = response.json()

    return response_dict['id']

def get_talk(talk_id:str, retry_counter: int = 0) -> str:

    import requests

    url = f"https://api.d-id.com/talks/{talk_id}"

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {api_key}"
    }

    response = requests.get(url, headers=headers)

    response_dict = response.json()

    if response_dict['status'] == 'error':
        if response_dict['error']['kind'] == 'FaceError':
            print('face detect error, recreating face')
            return False, None

    if 'result_url' not in response_dict:
        print(f'video not ready yet, retrying: {retry_counter}')
        time.sleep(2)
        retry_counter +=1
        return get_talk(talk_id, retry_counter)
    
    return  True, response_dict['result_url']

def download_bytes(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return response.content  

def get_video_for(image_file_getter: Callable[[], str], audio_path: str) -> bytes:
    
    img_path = image_file_getter()

    image_url = upload_image(img_path)
    audio_url = upload_audio(audio_path)

    talk_id = create_talk(image_url, audio_url)

    print(f'waiting for talk: {talk_id}')

    success, vid_url = get_talk(talk_id)

    if success :
        video_bytes = download_bytes(vid_url)
        return video_bytes
    else :
        return get_video_for(image_file_getter, audio_path)
    

if __name__ == '__main__':

    image_url = 's3://d-id-images-prod/google-oauth2|107689569745182731627/img_oERlqmaMJBEAMvxBfaWti/Alaric.png'
    audio_url = 's3://d-id-audios-prod/google-oauth2|107689569745182731627/M0pH_Se8s_x9ZjZcaHcxI/temp_audio.wav'

    talk_id = create_talk(image_url, audio_url)

    vid_url = get_talk(talk_id)

    print(vid_url)

    