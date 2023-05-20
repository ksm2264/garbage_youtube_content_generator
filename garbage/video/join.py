import os
from moviepy.editor import concatenate_videoclips, VideoFileClip

def join_video_clips(directory):
    # List all .mp4 files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
    
    # Sort the files in numerical order
    files.sort(key=lambda x: int(x.split('.')[0]))

    # Load and concatenate the video clips
    clips = [VideoFileClip(os.path.join(directory, f)) for f in files]
    final_clip = concatenate_videoclips(clips)

    # Write the result to file
    final_clip.write_videofile(os.path.join(directory, 'final.mp4'), codec='libx264')


if __name__ == '__main__':

    join_video_clips('video_clips/Gandalf_Harry Potter_a384319c-7a5e-45bf-8b7b-1fc22cff11ca')
