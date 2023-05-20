from pydantic import BaseModel
from typing import Callable, Any
import uuid
import numpy as np

from garbage.conversation.models import Character
from garbage.conversation.generator import ConversationGenerator
from garbage.conversation.random_characters import new_characters
from garbage.conversation.character.best_voice import get_best_voice_name, possible_voices

from garbage.image.generate import generate

from garbage.audio.clone import generate_audio_for_name

from garbage.video.clip import create_video_clip
from garbage.video.join import join_video_clips

class SessionCharacter(BaseModel):

    image_path: str
    character: Character
    audio_generation_func: Callable

    def get_audio_bytes(self, text: str) -> bytes:

        audio = self.audio_generation_func(text)

        return audio

    @staticmethod
    def new(character: Character) -> 'SessionCharacter':

        image_path = generate(character)

        voice_name = get_best_voice_name(character)

        audio_generation_func = lambda text : generate_audio_for_name(voice_name, text)

        new_instance = SessionCharacter(
            image_path = image_path,
            audio_generation_func=audio_generation_func,
            character=character
        )

        return new_instance

class Session(BaseModel):

    character_a: SessionCharacter
    character_b: SessionCharacter
    generator: Any
    name: str
    current_step: int = 0

    def step(self):
        
        next_msg, name = self.generator.next()

        session_character = self.session_character_by_name(name)

        audio_bytes = session_character.audio_generation_func(next_msg)

        create_video_clip(audio_bytes, session_character.image_path, self.output_path(), f'{self.current_step}.mp4')

        self.current_step+=1

    def output_path(self):
        return f'video_clips/{self.name}'

    def session_character_by_name(self, name:str ):

        if self.character_a.character.name == name:
            return self.character_a
        else:
            return self.character_b

    def end(self):
        join_video_clips(self.output_path())

    @staticmethod
    def new() -> 'Session':

        # character_a = new_character()
        # character_b = new_character()

        characters = np.random.choice(possible_voices, 2)

        character_a, character_b = new_characters(f'{characters[0]} and {characters[1]}')

        generator = ConversationGenerator(character_a, character_b)

        session_character_a = SessionCharacter.new(character_a)
        session_character_b = SessionCharacter.new(character_b)

        new_instance = Session(
            character_a = session_character_a,
            character_b = session_character_b,
            generator=generator,
            name = f'{character_a.name}_{character_b.name}_{uuid.uuid4()}'
        )
        return new_instance


