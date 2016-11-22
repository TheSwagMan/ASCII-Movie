from PIL import ImageFont, Image, ImageDraw


class FontBenchmark():
    def __init__(self, fontname, ascii_range=(32, 127), size=250):
        self.fontname = fontname
        self.ascii_range = ascii_range
        self.size = size
        self.cs = []
        self.cval = []
        self.final_result=[]
        for cindex in range(self.ascii_range[0], self.ascii_range[1]):
            c = chr(cindex)
            self.cs.append(c)
            self.cval.append(self.char_mean(c))
        self.calculate_result()

    def calculate_result(self):
        raw_list = sorted(zip(self.cval, self.cs))
        mini = 255
        maxi = 0
        for e in raw_list:
            if e[0] < mini:
                mini = e[0]
            if e[0] > maxi:
                maxi = e[0]
        nomalized_list = []
        for e in raw_list:
            nomalized_list.append(((e[0] - mini) * 255 / (maxi - mini), e[1]))
        self.final_result=nomalized_list

    def char_mean(self, c):
        img = Image.new("RGB", (self.size, self.size), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.fontname, self.size)
        draw.text((0, 0), c, (0, 0, 0), font=font)
        mean_pix = 0
        for pix in img.getdata():
            mean_pix += pix[0]
        mean_pix /= img.height * img.width
        return mean_pix

    def get_result(self):
        return self.final_result



if __name__ == "__main__":
    print(FontBenchmark("fonts/UbuntuMono-R.ttf").get_result())
