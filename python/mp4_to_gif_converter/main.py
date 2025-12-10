from PIL import Image
# convert mp4 to gif
import imageio
input_path = "D:/code/end_project/python/Japanese_Vocabulary_Trainer/Recording 2025-12-10 212529.mp4"
output_path = "output.gif"
# تبدیل ویدئو به GIF
with imageio.get_writer(output_path, mode='I', duration=0.1) as writer:
    for frame in imageio.get_reader(input_path):
        writer.append_data(frame)
print("Conversion complete! GIF saved at:", output_path)