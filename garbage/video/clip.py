from moviepy.editor import *
import os

from garbage.video.wav_2_lip import wav_2_lip
from garbage.video.talking_face import get_video_for

def create_video_clip(audio_bytes, image_path, output_folder, output_filename):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    temp_audio_path = "temp_audio.mp3"
    with open(temp_audio_path, 'wb') as f:
        f.write(audio_bytes)

    video_bytes = get_video_for(image_path, temp_audio_path)

    os.remove(temp_audio_path)

    temp_file_path = "temp_video.mp4"
    with open(temp_file_path, 'wb') as f:
        f.write(video_bytes)

    # Read the video bytes into a VideoFileClip
    video_clip = VideoFileClip(temp_file_path)

    output_path = os.path.join(output_folder, output_filename)

    # Write the video clip to the output file using the libx264 codec
    video_clip.write_videofile(output_path, codec='libx264')
    print(f"Video written to {output_path}")

    # Remove the temporary file
    os.remove(temp_file_path)
