from pydantic import BaseModel
import uuid
import numpy as np
import os

import pymongo

from garbage.conversation.conversation import Conversation
from garbage.conversation.llm import new_conversation, mock_conversation
from garbage.conversation.voices import voices_on_file

from garbage.session.character import SessionCharacter

from garbage.image.generate import portrait_getter

from garbage.session.audio import AudioStore

from garbage.session.video import VideoStore
from garbage.video.gooey import get_video_for as gooey_get_video_for
from garbage.video.gooey import get_video_for as did_get_video_for

from garbage.session.image import ImageStore


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['garbage']
collection = db['sessions']

class Session(BaseModel):
    
    name: str

    character_a: SessionCharacter
    character_b: SessionCharacter
    
    conversation: Conversation

    audio: AudioStore = AudioStore()
    video: VideoStore = VideoStore()
    image: ImageStore = ImageStore()
    
    def base_path(self):
        return f'sessions/{self.name}'

    def run(self):
        
        print('generating audio clips')
        self.generate_audio_clips()
        self.save()
        
        print('joining audio clips')
        self.join_audio_clips()
        self.save()

        print('creating videos')
        self.create_videos()
        self.save()

        print('joining videos')
        self.concat_videos()
        self.save()

    def concat_videos(self):

        self.video.concat(self.base_path())

    def create_videos(self):

        # character A
        character_a_name = self.character_a.character.name
        image_file_getter_a = portrait_getter(self.character_a.character, self.base_path())
        character_a_audio_file = self.audio.joined_files[character_a_name].file

        # todo: set up using gooey vs did as a flag
        video_a_bytes = gooey_get_video_for(image_file_getter_a, character_a_audio_file)

        self.video.add_video_a(character_a_name, video_a_bytes, self.base_path())

        # character B
        character_b_name = self.character_b.character.name
        image_file_getter_b = portrait_getter(self.character_b.character, self.base_path())
        character_b_audio_file = self.audio.joined_files[character_b_name].file

        video_b_bytes = gooey_get_video_for(image_file_getter_b, character_b_audio_file)

        self.video.add_video_b(character_b_name, video_b_bytes, self.base_path())

        
   
    def join_audio_clips(self):
        self.audio.join(self.base_path())

    def generate_audio_clips(self):
        for message in self.conversation.messages:

            session_character = self.session_character_by_name(message.source)

            audio_bytes = session_character.audio_generation_func(message.content)

            self.audio.add(message.source, audio_bytes, self.base_path())

    def session_character_by_name(self, name:str ):

        if self.character_a.character.name == name:
            return self.character_a
        else:
            return self.character_b

    def store_images(self):
        self.image.set_image_a(
            self.character_a
        )
        self.image.set_image_b(
            self.character_b
        )

    def save(self):
        query = {
            'name': self.name
        }
        collection.update_one(query, {'$set': self.dict()}, upsert=True)

    @staticmethod
    def new() -> 'Session':

        # voice_a, voice_b = np.random.choice(voices_on_file, 2)
        # conversation = new_conversation(voice_a, voice_b)

        conversation = mock_conversation()

        # todo: make this a readable thing like twitch clips
        name = uuid.uuid4()
        print(f'Starting new session: {name}')

        print('Creating folders')
        os.mkdir(f'sessions/{name}')
        os.mkdir(f'sessions/{name}/audio')
        os.mkdir(f'sessions/{name}/audio/joined')
        os.mkdir(f'sessions/{name}/video')
        os.mkdir(f'sessions/{name}/image')

        print('Creating character portraits')
        session_character_a = SessionCharacter.new(conversation.character_a, f'sessions/{name}')
        session_character_b = SessionCharacter.new(conversation.character_b, f'sessions/{name}')

        new_instance = Session(
            character_a = session_character_a,
            character_b = session_character_b,
            conversation = conversation,
            name = str(name)
        )
        
        new_instance.store_images()
        new_instance.save()

        return new_instance

    @staticmethod
    def restart(name: str):
        pass
        # todo: implement python-statemachine for stages, makes reloading easier

if __name__ == '__main__':

    session = Session.new()

    session.run()