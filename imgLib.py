from PIL import Image,ImageDraw,ImageFont
from symbolBenchmark import FontBenchmark
import os
import pickle as pkl

class SimpleTuple():
    def __init__(self, *data):
        self._data = None
        self._size = None
        if data is None:
            data = []
        if len(data)>0:
            if type(data[0])==tuple or type(data[0])==list:
                self.set_data(data[0])
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

    def get_added(self,x):
        return self.copy().add(x)

    def __str__(self):
        return "(" + ",".join([str(i) for i in self.get_data()]) + ")"

    def set_data(self, data):
        self._data = data
        return self

    def get_data(self) -> list:
        return self._data

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

    def get_size(self):
        return self._size

    def get_data_as_tuple(self):
        return tuple(k for k in self.get_data())

    def get_data_as_int_tuple(self):
        return tuple(k for k in self.get_data_as_int())

    def to_int(self):
        for e in self.get_data():
            e=int(e)


class SimplePixel(SimpleTuple):
    def __init__(self, data=None, size=()):
        super().__init__(data, size)

    def to_grey_scale(self):
        self.set_data([((self.get_val(0) + self.get_val(1) + self.get_val(2)) / 3) for i in range(3)])
        return self


class SimplePicture():
    def __init__(self, data=None, dtype="SP", size=SimpleTuple()):
        self._data = None
        self._size = None
        if data is None:
            data = []
        if dtype == "SP":
            self.set_data(data)
            self.set_size(size)
        if dtype == "A":
            self.set_data_from_array(data)
            self.set_size(size)
        if dtype == "2D":
            self.set_data_from_2d(data)

    def set_data_from_2d(self, data):
        temp = []
        for line in data:
            for elem in line:
                temp.append(SimplePixel(elem))
        self.set_data(temp)
        self.set_size(SimpleTuple(len(data[0]), len(data)))
        return self

    def set_data_from_array(self, data):
        temp = []
        for pix in data:
            temp.append(SimplePixel(pix))
        self.set_data(temp)
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
            temp.append(p.get_data_as_tuple())
        return temp

    def get_size(self) -> SimpleTuple:
        return self._size

    def get_height(self) -> int:
        return self.get_size().get_val(0)

    def get_width(self) -> int:
        return self.get_size().get_val(1)

    def get_size_mul(self) -> int:
        return self.get_size().get_val(0) * self.get_size().get_val(1)

    def get_pixel(self, x, y=None):
        if y == None:
            return self.get_data()[x]
        else:
            return self.get_data()[x * self.get_height() + y]

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
        h=int(self.get_height()*(w/self.get_width()))
        self.resize(SimpleTuple(h,w))
        return self

    def resize_height(self,h):
        w=int(self.get_width()*(h/self.get_height()))
        self.resize(SimpleTuple(h,w))
        return self

    def resize(self, size):
        a=self.to_Image()
        a=a.resize(size.get_data_as_tuple())
        self.set_data_from_array(list(a.getdata()))
        self.set_size(size)
        """
        to finish

        temp = []
        n = SimpleTuple(self.get_height() // size.get_val(0), self.get_width() // size.get_val(1))
        rest = SimpleTuple(self.get_height() - n.get_val(0) * size.get_val(0), self.get_width() - n.get_val(1) * size.get_val(1))
        offset = (
            (rest.get_val(0) // 2, rest.get_val(0) // 2 + rest.get_val(0) % 2),
            (rest.get_val(1) // 2, rest.get_val(1) // 2 + rest.get_val(1) % 2)
        )
        print(n,rest,offset)
        for i in range(0,size.get_mul()):
            p = [0, 0, 0]
            if i<size.get_val(0):
                print(i,"first line")
            elif i>size.get_mul()-size.get_val(0)-1:
                print(i,"last lin")
            elif i % size.get_val(0) == 0:
                print(i,"first col")
            elif i % size.get_val(0) == size.get_val(0) - 1:
                print(i,"last col")
            else:
                print(i,"middle")
            for k in range(n.get_val(0)):
                for l in range(n.get_val(1)):
                    index = i * n.get_val(0) + k + l * self.get_width() + i // size.get_val(0) * self.get_width()
                    cp = self.get_pixel(index)
                    p[0] += cp.get_val(0)
                    p[1] += cp.get_val(1)
                    p[2] += cp.get_val(2)
            p[0] /= n.get_mul()
            p[1] /= n.get_mul()
            p[2] /= n.get_mul()

            temp.append(SimplePixel(p))
        self.set_size(size)
        self.set_data(temp)
        """
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
        greycopy = self.copy().to_grey_scale()
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
        return ASCIIPicture(temp, self.get_size())

    def to_Image(self):
        temp = Image.new("RGB", self.get_size().get_data_as_tuple())
        temp.putdata(self.get_data_as_int_tuple())
        """
        for i in range(self.get_size_mul()):

            #temp.putpixel((i%self.get_width(),i%self.get_height()), (self.get_pixel_as_int(i).get_data_as_tuple()))
        """
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
        print(self._data, "\n", temp)
        return temp

    def to_Image(self,font="fonts/UbuntuMono-R.ttf",fontsize=12,bg=SimpleTuple(255,255,255),fg=SimpleTuple(0,0,0)):
        corrrect_fonsize=0.8*fontsize
        img = Image.new("RGB", self.get_size().get_multiplied(corrrect_fonsize).get_added(-corrrect_fonsize).get_data_as_int_tuple(), bg.get_data_as_tuple())
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font, fontsize)
        for i in range(self.get_size_mul()):
            draw.text((int((i%self.get_width())*corrrect_fonsize), int((i//self.get_height())*corrrect_fonsize)), self.get_pixel(i), fg.get_data_as_tuple(), font=font)
        return img


if __name__ == "__main__":
    # MAIN PROG
    fname = "swag.jpg"
    img1 = Image.open(fname)
    raw_img_rbg = list(img1.getdata())
    size = SimpleTuple(img1.width, img1.height)
    myimg = SimplePicture(raw_img_rbg, "A", size)
    ok = myimg.resize_width(100).change_contrast(2).invert_color().to_ascii().save(fname + ".asciip")

    # MATRIX COLORS : fg=SimpleTuple(127,255,0),bg=SimpleTuple(0,0,0)
    """
    TODO :
    - crop
    - better resize

    """
