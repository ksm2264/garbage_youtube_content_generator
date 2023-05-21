from pydantic import BaseModel
from moviepy.editor import VideoFileClip, clips_array

class VideoFile(BaseModel):

    speaker: str
    file: str

class VideoStore(BaseModel):
    
    video_a: VideoFile = None
    video_b: VideoFile = None

    final: str = None

    def add_video_a(self, speaker: str, video_a_bytes: bytes, base_path: str):

        video_path = f'{base_path}/video/{speaker}.mp4'

        with open(video_path, 'wb') as f:
            f.write(video_a_bytes)

        video_file = VideoFile(
            speaker = speaker,
            file = video_path
        )

        self.video_a = video_file

    def add_video_b(self, speaker: str, video_b_bytes: bytes, base_path: str):

        video_path = f'{base_path}/video/{speaker}.mp4'

        
        with open(video_path, 'wb') as f:
            f.write(video_b_bytes)

        clip = VideoFileClip(video_path)
        clip.write_videofile(video_path, codec='libx264')

        video_file = VideoFile(
            speaker = speaker,
            file = video_path
        )

        self.video_b = video_file

    def concat(self, base_path: str):

            # Load video clips
        clip1 = VideoFileClip(self.video_a.file)
        clip2 = VideoFileClip(self.video_b.file)

        # Create a new video clip that plays the two clips side by side
        final_clip = clips_array([[clip1, clip2]])


        output_path = f'{base_path}/video/final.mp4'
        # Write the result to a file
        final_clip.write_videofile(output_path, codec='libx264')

        self.final = output_path

