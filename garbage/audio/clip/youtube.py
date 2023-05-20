import os
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import AudioFileClip

def download_youtube_video(url, target_path):
    yt = YouTube(url)
    stream = yt.streams.first()
    stream.download(target_path)
    return os.path.join(target_path, stream.default_filename)

def cut_into_clips(video_path, target_path, clip_length=12):
    try:
        start_time = 0
        end_time = clip_length
        clip_index = 0

        while end_time <= 120:  # 2 minutes in seconds
            target_file = os.path.join(target_path, f'clip_{clip_index}.mp4')
            ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=target_file)

            # Convert the clip to mp3
            audioclip = AudioFileClip(target_file)
            audioclip.write_audiofile(os.path.join(target_path, f'clip_{clip_index}.mp3'))

            clip_index += 1
            start_time = end_time
            end_time += clip_length

    except Exception as e:
        print(e)

def create_clips(youtube_url, name: str):
    target_directory = f'audio_clips/{name}'
    video_file = download_youtube_video(youtube_url, target_directory)
    cut_into_clips(video_file, target_directory)


def main():
    youtube_url = 'https://www.youtube.com/watch?v=0n-X9B-oTWk'
    name = 'dwarf'

    create_clips(youtube_url, name)
    
    
if __name__ == "__main__":
    main()
