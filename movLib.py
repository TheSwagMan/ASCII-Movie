#! /usr/bin/python3
from moviepy.editor import VideoFileClip
from imgLib import SimplePicture
import sys


def get_frame(n):
    return mym.get_frame(n / mym.fps)

one_over = 3
newsize = 35
mym = VideoFileClip(sys.argv[1])
# frames = list(mym.iter_frames())
frate = mym.fps // one_over
outfile = open(sys.argv[1] + ".ascmov", "w")
noff = int(mym.duration * mym.fps / one_over)
first_frame = SimplePicture(get_frame(0).tolist(), dtype="2D").resize_height(newsize)
outfile.write(
    str(int(first_frame.get_height())) + "," + str(int(first_frame.get_width())) + "\n" + str(int(frate)) + "," + str(
        int(noff)) + "\n")
print("Loaded !\n")
for i in range(noff):
    print("\033[K", end="")
    print("\033[FWorking " + str(i + 1) + "/" + str(noff) + "...")
    tempimg = SimplePicture(get_frame(int(i * one_over)).tolist(), dtype="2D")

    tempimg.resize_width(newsize).change_contrast(3).invert_color()
    ascimg = tempimg.to_ascii()
    # ascimg.save("temp_frames/ascii" + str(i) + ".txt")
    outfile.write(ascimg.to_string() + "\n")
outfile.close()
