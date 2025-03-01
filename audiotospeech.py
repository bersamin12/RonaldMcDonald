from moviepy import VideoFileClip
import os 
input_path = os.path.join("src", "vid2.mp4")

def extract_audio(input_video_path, output_audio_path):
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)
    
    # Extract the audio
    audio = video_clip.audio
    
    # Write the audio to a file
    audio.write_audiofile(output_audio_path)
    
    # Close the clips to free up system resources
    video_clip.close()
    audio.close()

# Example usage
if __name__ == "__main__":
    output_path = os.path.join("src", "audio.mp3")
    extract_audio(input_path, output_path)

