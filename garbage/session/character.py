from pydantic import BaseModel
from typing import Callable

from garbage.image.generate import generate
from garbage.conversation.conversation import Character
from garbage.audio.clone import generate_audio_for_name

class SessionCharacter(BaseModel):

    image_path: str
    character: Character
    audio_generation_func: Callable

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        # Remove the function from the dict
        d.pop('audio_generation_func', None)

        return d

    def get_audio_bytes(self, text: str) -> bytes:

        audio = self.audio_generation_func(text)

        return audio

    @staticmethod
    def new(character: Character, base_path: str) -> 'SessionCharacter':

        image_path = generate(character, base_path)

        audio_generation_func = lambda text : generate_audio_for_name(character.race, text)

        new_instance = SessionCharacter(
            image_path = image_path,
            audio_generation_func=audio_generation_func,
            character=character
        )

        return new_instance