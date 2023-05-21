from pydub import AudioSegment
from typing import Dict, List
from pydantic import BaseModel
import pymongo
import numpy as np

class AudioFile(BaseModel):

    speaker: str
    file: str

class AudioStore(BaseModel):

    files : list[AudioFile] = []
    index: int = 0
    
    joined_files: dict[str, AudioFile] = {}

    def add(self, speaker: str, audio_bytes: bytes, base_path: str):

        audio_path = f'{base_path}/audio/{speaker}_{self.index}.mp3'

        with open(audio_path, 'wb') as f:
            f.write(audio_bytes)

        file = AudioFile(
            speaker = speaker,
            file = audio_path
        )

        self.files.append(file)
        
        self.index += 1

    def join(self, base_path: str):

        unique_speakers = np.unique([audio_file.speaker for audio_file in self.files])

         # Create a dict to hold the final audio for each speaker
        speaker_audio: Dict[str, AudioSegment] = {}

        # For each audio file (sorted by the order they were added)...
        for audio_file in self.files:
            # Load the file as an AudioSegment
            audio_segment = AudioSegment.from_mp3(audio_file.file)
            quiet_segment = AudioSegment.silent(len(audio_segment))

            pause_segment = AudioSegment.silent(250)

            for speaker in unique_speakers:
                if audio_file.speaker == speaker:
                    
                    if speaker not in speaker_audio:
                        speaker_audio[speaker] = audio_segment

                    else:
                        speaker_audio[speaker] += audio_segment

                else:

                    if speaker not in speaker_audio:
                        speaker_audio[speaker] = quiet_segment
                    else:
                        speaker_audio[speaker] += quiet_segment

                speaker_audio[speaker] += pause_segment

        for speaker in unique_speakers:
            audio_path = f"{base_path}/audio/joined/{speaker}.mp3"
            
            speaker_audio[speaker].export(audio_path, format='mp3')

            self.joined_files[speaker] = (AudioFile(
                speaker = speaker,
                file = audio_path
            ))


    @staticmethod
    def from_session(session_name: str):

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['garbage']
        collection = db['sessions']

        query = {
            "name":f'sessions/{session_name}'
        }

        session = collection.find_one(query)

        audio_files = []

        for file in session['audio']['files']:
            
            speaker = file['speaker']
            file_name = file['file']

            audio_file = AudioFile(
                speaker = speaker,
                file = file_name
            )

            audio_files.append(audio_file)

        audio_store = AudioStore(files = audio_files)

        return audio_store
    
if __name__ == '__main__':

    uuid = '424c1131-1e06-424e-9753-db3f90c1cb5e'

    audio = AudioStore.from_session(uuid)

    base_path = f'sessions/{uuid}'

    audio.join(base_path)
