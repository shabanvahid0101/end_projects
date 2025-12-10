import moviepy as mpy
video=mpy.VideoFileClip("asset/test_video.mp4")
audio=video.audio
audio.write_audiofile("asset/output_audio.mp3")