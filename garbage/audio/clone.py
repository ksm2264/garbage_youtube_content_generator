from elevenlabs import set_api_key
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('ELEVENLABS_API_KEY')
set_api_key(api_key)

from elevenlabs import clone, generate, play, voices
import glob

def retrieve(name: str):

    my_voices = voices()

    filtered = [voice for voice in my_voices if voice.name == name]

    if len(filtered) == 1:
        return filtered[0]
    else:
        return None

def clone_voice(name:str):
        
    voice = retrieve(name)

    if voice :
        return voice
    
    my_voices = voices()

    if len(my_voices.voices) == 19:
        print('deleting')
        my_voices.voices[-1].delete()
        my_voices.voices[-2].delete()

    voice = clone(
        name=name,
        files=glob.glob(f'audio_clips/{name}/*.mp3'),
    )

    return voice

def generate_audio(voice, text):
    audio = generate(text=text, voice=voice)

    return audio

def generate_audio_for_name(voice_name: str, text):

    voice = clone_voice(voice_name)

    audio = generate_audio(voice, text)

    return audio

if __name__ == '__main__':

    voice = clone_voice('troll')

    text = "Hi! I'm a cloned voice!"

    audio = generate_audio(voice, text)

    play(audio)