#!/usr/bin/env python3
"""
audiotospeech.py

This module extracts audio from video files using the moviepy library.
"""

from moviepy import VideoFileClip
import os
import argparse

def extract_audio(input_video_path, output_audio_path):
    """
    Extract audio from a video file and save it to the specified output path.
    
    Args:
        input_video_path (str): Path to the input video file
        output_audio_path (str): Path to save the extracted audio
    
    Returns:
        None
    """
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)
    
    # Extract the audio
    audio = video_clip.audio
    
    # Write the audio to a file
    audio.write_audiofile(output_audio_path)
    
    # Close the clips to free up system resources
    video_clip.close()
    audio.close()
    
    return output_audio_path

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Extract audio from video files")
    parser.add_argument("input_path", help="Path to the input video file")
    parser.add_argument(
        "-o", 
        "--output", 
        help="Path to save the extracted audio (defaults to 'audio.mp3' in the same directory)"
    )
    
    args = parser.parse_args()
    
    # If output path is not specified, use a default name in the same directory
    if not args.output:
        args.output = os.path.join(os.path.dirname(args.input_path), "audio.mp3")
    
    # Extract the audio
    extract_audio(args.input_path, args.output)
    print(f"Audio extracted to {args.output}")

# Example usage
if __name__ == "__main__":
    main()