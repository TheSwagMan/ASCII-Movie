#! /usr/bin/python3
from moviepy.editor import VideoFileClip
from imgLib import SimplePicture,resize_raw_matrix,to_1D,SimpleTuple
import sys


def get_frame(n):
    return mym.get_frame(n / mym.fps)

if len(sys.argv)>1:
    sup=sys.argv[1]
else:
    sup="real_sample1.mp4"

one_over = 3
newsize = 35
mym = VideoFileClip(sup)
# frames = list(mym.iter_frames())
frate = mym.fps // one_over
outfile = open(sup + ".ascmov", "w")
noff = int(mym.duration * mym.fps / one_over)
first_frame = SimplePicture(get_frame(0).tolist(), dtype="2D").resize_height(newsize)
outfile.write(
    str(int(first_frame.get_height())) + "," + str(int(first_frame.get_width())) + "\n" + str(int(frate)) + "," + str(
        int(noff)) + "\n")
print("Loaded !\n")
for i in range(noff):
    print("\033[K", end="")
    print("\033[FWorking " + str(i + 1) + "/" + str(noff) + "...")
    raw_m=get_frame(int(i * one_over)).tolist()
    osize=SimpleTuple(len(raw_m),len(raw_m[0]))
    nsize=SimpleTuple(newsize,int(osize.get_val(1)/round(osize.get_val(0)/newsize)))
    print(osize.get_data(),nsize.get_data())
    mlsdc=to_1D(raw_m)
    p=resize_raw_matrix(mlsdc,osize.get_data(),nsize.get_data())
    tempimg = SimplePicture(p,dtype="A",size=nsize)

    tempimg.change_contrast(3).invert_color()
    ascimg = tempimg.to_ascii()
    # ascimg.save("temp_frames/ascii" + str(i) + ".txt")
    outfile.write(ascimg.to_string() + "\n")
outfile.close()
