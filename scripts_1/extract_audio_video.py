import ffmpeg
import os

# Input path (your downloaded sample video)
input_path = r'D:\Audio_Cloning_Project\Input_video\sample_input.mp4'
# Output directory
output_dir = r'D:\Audio_Cloning_Project\Output_audio_video'
os.makedirs(output_dir, exist_ok=True)

# Output file paths
audio_output = os.path.join(output_dir, 'sample_audio.wav')
video_output = os.path.join(output_dir, 'sample_video.mp4')

# Extract audio (WAV format)
ffmpeg.input(input_path).output(audio_output, format='wav').run(overwrite_output=True)

# Extract video only (no audio)
ffmpeg.input(input_path).output(video_output, **{'an': None}).run(overwrite_output=True)
