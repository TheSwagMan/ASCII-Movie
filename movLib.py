from moviepy.editor import *
import os, imgLib
from PIL import Image

mym = VideoFileClip("sample.mp4", verbose=False)
frames = list(mym.iter_frames())
for i in range(len(frames)):
    if i > 50:
        break
    tempimg = imgLib.SimplePicture(list(frames[i]), dtype="A")
    print(tempimg)
    tempimg.resize_width(70)
    print(tempimg)
    tempimg.to_ascii().save("temp_frames/ascii" + str(i) + ".txt")

exit()
mym.write_images_sequence("temp_frames/frame%05d.png", verbose=False)
for imname in os.listdir("temp_frames"):
    tempimg = imgLib.SimplePicture(Image.open("temp_frames/" + imname).getdata(), dtype="A")
    os.remove("temp_frames/" + imname)
    tempimg.to_ascii().save("temp_frames/ascii" + imname + ".txt")
