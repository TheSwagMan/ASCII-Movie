from moviepy.editor import VideoFileClip
from imgLib import SimplePicture
from os import listdir, remove
from PIL import Image

one_over = 5
mym = VideoFileClip("sample2.mp4")
frames = list(mym.iter_frames())
print("Loaded !\n")
noff = len(frames) // one_over
for i in range(noff):
    print("\033[K", end="")
    print("\033[FWorking " + str(i + 1) + "/" + str(noff) + "...")
    tempimg = SimplePicture(frames[i * one_over].tolist(), dtype="2D")
    tempimg.resize_width(60).change_contrast(2).invert_color()
    tempimg.to_ascii().save("temp_frames/ascii" + str(i) + ".txt")

exit()
mym.write_images_sequence("temp_frames/frame%05d.png", verbose=False)
for imname in listdir("temp_frames"):
    tempimg = SimplePicture(Image.open("temp_frames/" + imname).getdata(), dtype="A")
    remove("temp_frames/" + imname)
    tempimg.to_ascii().save("temp_frames/ascii" + imname + ".txt")
