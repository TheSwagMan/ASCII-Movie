#! /usr/bin/python3
from PIL import Image,ImageDraw,ImageFont
from symbolBenchmark import FontBenchmark
import os,sys
import pickle as pkl

class SimpleTuple():
    def __init__(self, *data):
        self._data = None
        self._size = None
        if data is None:
            data = []
        if len(data)>0:
            if type(data[0])==tuple or type(data[0])==list:
                self.set_data(list(data[0]))
                self.set_size(len(data[0]))
            else:
                self.set_data(data)
                self.set_size(len(data))

    def get_mul(self):
        m=1
        for e in self.get_data():
            m*=e
        return m

    def multiply(self,x):
        temp=[]
        for e in self.get_data():
            temp.append(e*x)
        self.set_data(temp)
        return self

    def multiply_n(self, x, n):
        self.set_data_n(self.get_data_n(n) * x, n)
        return self

    def add(self,x):
        temp=[]
        for e in self.get_data():
            temp.append(e+x)
        self.set_data(temp)
        return self

    def copy(self):
        return SimplePixel(self.get_data())

    def get_multiplied(self,x):
        return self.copy().multiply(x)

    def get_multiplied_n(self, x, n):
        return self.copy().multiply_n(x, n)

    def get_added(self,x):
        return self.copy().add(x)

    def __str__(self):
        return "(" + ",".join([str(i) for i in self.get_data()]) + ")"

    def set_data(self, data):
        if type(data)==tuple:
            data=list(data)
        self._data = data
        return self

    def set_data_n(self, v, n):
        self._data[n] = v
        return self

    def get_data(self) -> list:
        return self._data

    def get_data_n(self, n):
        return self._data[n]

    def get_data_as_int(self) -> list:
        temp=[]
        for e in self.get_data():
            temp.append(int(e))
        return temp

    def get_val(self, x) -> int:
        return self.get_data()[x]

    def set_val(self, x, v):
        self.get_data()[x] = v
        return self

    def set_size(self, size):
        self._size = size
        return self

    def get_size(self):
        return self._size

    def get_data_as_tuple(self):
        return tuple(k for k in self.get_data())

    def get_data_as_int_tuple(self):
        return tuple(k for k in self.get_data_as_int())

    def to_int(self):
        temp = []
        for e in self.get_data():
            temp.append(int(e))
        self.set_data(temp)
        return self

class SimplePixel(SimpleTuple):
    def __init__(self, data=None, size=()):
        super().__init__(data, size)

    def to_grey_scale(self):
        self.set_data([((self.get_val(0) + self.get_val(1) + self.get_val(2)) / 3) for i in range(3)])
        return self


class SimplePicture():
    def __init__(self, data=None, dtype="SP", size=SimpleTuple(),nwsize=100):
        self._data = None
        self._size = SimpleTuple()
        if data is None:
            data = []
        if dtype == "SP":
            self.set_data(data)
            self.set_size(size)
        if dtype == "A":
            self.set_data_from_array(data,size)
        if dtype == "2D":
            self.set_data_from_2d(data)

    def set_data_from_2d(self, data):
        size=SimpleTuple(len(data[0]), len(data))
        self.set_data_from_array(to_1D(data),size)
        return self

    def set_empty(self,size):
        self.set_size(size)
        temp=[]
        for i in range(self.get_size_mul()):
            temp.append(SimplePixel([0,0,0]))
        self.set_data(temp)

    def add_pixel(self,pix):
        self._data.append(pix)

    def clear(self):
        self.set_data([])

    def set_data_from_array(self, data,size):
        self.clear()
        self.set_size(size)
        for pix in data:
            self.add_pixel(SimplePixel(pix))
        return self

    def set_pixel(self, i, data):
        self._data[i] = data

    def set_data(self, data):
        self._data = data
        return self

    def set_size(self, size):
        self._size = size
        return self

    def get_data(self) -> list:
        return self._data

    def get_data_as_tuple(self):
        temp=[]
        for p in self.get_data():
            temp.append(p.get_data_as_tuple())
        return temp

    def get_data_as_int(self):
        temp=[]
        for p in self.get_data():
            temp.append(p.get_data_as_int())
        return temp

    def get_data_as_int_tuple(self):
        temp=[]
        for p in self.get_data():
            temp.append(p.get_data_as_int_tuple())
        return temp

    def get_size(self) -> SimpleTuple:
        return self._size

    def get_height(self) -> int:
        return self.get_size().get_val(1)

    def get_width(self) -> int:
        return self.get_size().get_val(0)

    def get_size_mul(self) -> int:
        return self.get_size().get_val(0) * self.get_size().get_val(1)

    def get_pixel(self, x, y=None):
        if y == None:
            return self.get_data()[x]
        else:
            return self.get_data()[x * self.get_width() + y]

    def get_pixel_as_int(self, x, y=None):
        if y == None:
            return SimplePixel(int(i) for i in self.get_pixel(x).get_data())
        else:
            return SimplePixel(int(i) for i in self.get_pixel(x * self.get_width() + y).get_data())

    def invert_color(self):
        temp = []
        for pix in self.get_data():
            temp.append(SimplePixel([255 - i for i in pix.get_data()]))
        self.set_data(temp)
        return self

    def import_Image(self,i):
        self.set_data_from_array(i.get)
        return self

    def resize_width(self,w):
        fact=round(self.get_width()/w)
        self.resize(SimpleTuple(w,int(self.get_height()/fact)))
        return self

    def resize_height(self,h):
        fact=round(self.get_height()/h)
        self.resize(SimpleTuple(int(self.get_width()/fact),h))
        return self

    def resize(self, size):
        """
        self.set_data(resize_raw_matrix(self.get_data(),self.get_size().get_data(),size.get_data()))
        self.set_size(size)
        """
        a=self.to_Image()
        a = a.resize(size.get_data_as_int_tuple())
        self.set_data_from_array(list(a.getdata()),size)
        """#"""
        return self


    def change_contrast(self, n):
        temp = []
        if n > 255:
            n = 255
        for pix in self.get_data():
            temppix = []
            for val in pix.get_data():
                val = ((val - 128) * n) + 128
                if val > 255:
                    val = 255
                if val < 0:
                    val = 0
                temppix.append(val)
            temp.append(SimplePixel(temppix))
        self.set_data(temp)
        return self

    def to_grey_scale(self):
        for pix in self.get_data():
            pix.to_grey_scale()
        return self

    def to_ascii(self,font="fonts/UbuntuMono-R.ttf"):
        ratio = int(round(self.get_size().get_val(0) / self.get_size().get_val(1)))
        corrected_size = self.get_size().get_multiplied_n(ratio, 0)
        greycopy = self.copy().to_grey_scale().resize(corrected_size)
        benchsavepath=font+".bench"
        if not os.path.exists(benchsavepath):
            bensh=FontBenchmark(font)
            benshfile=open(benchsavepath,"wb")
            pkl.dump(bensh, benshfile)
            benshfile.close()
        else:
            benshfile = open(benchsavepath,"rb")
            bensh = pkl.load(benshfile)
            benshfile.close()
        ascii_tab = bensh.get_result()

        temp = ""
        for i in range(greycopy.get_size_mul()):
            pix = greycopy.get_pixel(i).get_val(0)
            j = 0
            while ascii_tab[j][0] < pix and j < len(ascii_tab) - 1:
                j += 1
            if abs(ascii_tab[j - 1][0] - pix) < abs(ascii_tab[j][0] - pix):
                j -= 1
            temp += ascii_tab[j][1]
        return ASCIIPicture(temp, corrected_size)

    def to_Image(self):
        temp = Image.new("RGB", self.get_size().get_data_as_int_tuple())
        temp.putdata(self.get_data_as_int_tuple())
        return temp

    def copy(self):
        return SimplePicture(self.get_data(), dtype="SP", size=self.get_size())


class ASCIIPicture():
    def __init__(self, data=None, size=()):
        super().__init__()
        if data is None:
            data = []
        self._data = data
        self._size = size

    def set_data_from_2d(self, data):
        temp = []
        for line in data:
            for elem in line:
                temp.append(elem)
        self.set_data(temp)
        return self

    def set_data(self, data):
        self._data = data
        return self

    def set_size(self, size):
        self._size = size
        return self

    def get_data(self) -> list:
        return self._data

    def get_size(self) -> SimpleTuple:
        return self._size

    def get_height(self) -> int:
        return self.get_size().get_val(0)

    def get_width(self) -> int:
        return self.get_size().get_val(0)

    def get_size_mul(self) -> int:
        return self.get_size().get_mul()

    def get_pixel(self, x, y=None):
        if y == None:
            return self.get_data()[x]
        else:
            return self.get_data()[x * self.get_height() + y]

    def set_pixel(self, i, data):
        self._data[i] = data

    def __str__(self):
        return self.to_string()

    def save(self, filepath):
        file = open(filepath, "w")
        file.write(self.to_string())
        return self

    def to_string(self):
        temp = ""
        for i in range(self.get_size_mul()):
            c = self.get_pixel(i)
            temp += c
            if i % self.get_size().get_val(0) == self.get_size().get_val(0) - 1:
                temp += "\n"
        return temp

    def to_Image(self,font="fonts/UbuntuMono-R.ttf",fontsize=12,bg=SimpleTuple(255,255,255),fg=SimpleTuple(0,0,0)):
        corrrect_fonsize=0.8*fontsize
        img = Image.new("RGB", self.get_size().get_multiplied(corrrect_fonsize).get_added(-corrrect_fonsize).get_data_as_int_tuple(), bg.get_data_as_tuple())
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font, fontsize)
        for i in range(self.get_size_mul()):
            draw.text((int((i%self.get_width())*corrrect_fonsize), int((i//self.get_height())*corrrect_fonsize)), self.get_pixel(i), fg.get_data_as_tuple(), font=font)
        return img

def resize_raw_matrix(mat,osize,nsize):
    fact = round(osize[0] / nsize[0])
    resized = []
    for i in range(nsize[1]):
        for j in range(nsize[0]):
            resized.append(mat[i * fact*osize[0]+ j * fact])
    return resized

def to_1D(m):
    temp=[]
    for l in m:
        temp+=l
    return temp


import time
if __name__ == "__main__":
    # MAIN PROG
    if len(sys.argv)>1:
        fname = sys.argv[1]
    else:
        fname="swag.jpg"
    k=time.time()
    img1 = Image.open(fname)
    print(1,time.time() - k)
    k=time.time()
    raw_img_rbg = list(img1.getdata())
    print(2,time.time() - k)
    k=time.time()
    size = SimpleTuple(img1.width, img1.height)
    print(3,time.time() - k)
    k=time.time()
    myimg = SimplePicture(raw_img_rbg, "A", size)
    print(4,time.time() - k)
    k=time.time()
    ok = myimg.resize_width(100).change_contrast(2).invert_color().to_ascii().save(fname + ".asciip")
    print(5,time.time()-k)
    # MATRIX COLORS : fg=SimpleTuple(127,255,0),bg=SimpleTuple(0,0,0)
    """
    TODO :
    - crop
    - better resize

    """
