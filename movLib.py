#! /usr/bin/python3
from moviepy.editor import VideoFileClip
from imgLib import SimplePicture

one_over = 5
mym = VideoFileClip("sample2.mp4")
frate = mym.fps // one_over
frames = list(mym.iter_frames())
outfile = open("film-test.ascmov", "w")
noff = len(frames) // one_over
first_frame = SimplePicture(frames[0].tolist(), dtype="2D")
outfile.write(
    str(int(first_frame.get_height())) + "," + str(int(first_frame.get_width())) + "\n" + str(int(frate)) + "," + str(
        int(noff)) + "\n")
print("Loaded !\n")
for i in range(noff):
    print("\033[K", end="")
    print("\033[FWorking " + str(i + 1) + "/" + str(noff) + "...")
    tempimg = SimplePicture(frames[i * one_over].tolist(), dtype="2D")
    tempimg.resize_height(50).change_contrast(2).invert_color()
    ascimg = tempimg.to_ascii()
    ascimg.save("temp_frames/ascii" + str(i) + ".txt")
    outfile.write(ascimg.to_string() + "\n")
outfile.close()
