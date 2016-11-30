import curses, time
from imgLib import SimpleTuple

class MovieParser():
    def __init__(self, fn):
        self._size = 0
        self._file_name = fn
        self._frames = []
        self.read_file()

    def read_file(self):
        file = open(self._file_name, "r")
        self._size = SimpleTuple([int(e) for e in file.readline()[:-1].split(",")])
        self._frame_rate, self._lenght = [int(e) for e in file.readline()[:-1].split(",")]
        tline = file.readline()
        while self.is_junk_line(tline):
            tline = file.readline()
        temp_frame = tline
        for line in file.readlines():
            if self.is_junk_line(line):
                self._frames.append(temp_frame)
                temp_frame = ""
            else:
                temp_frame += line
        self._frames.append(temp_frame)

    def is_junk_line(self, s):
        return s == "\n"

    def get_lenght(self):
        return self._lenght

    def get_frame(self, i):
        return self._frames[i]

    def get_frame_rate(self):
        return self._frame_rate

    def get_size(self):
        return self._size


class MovieReader():
    def __init__(self, fn):
        self.movieparser = MovieParser(fn)
        self.win = curses.initscr()

    def play(self, loop=True):
        temploop = loop
        loop = True
        while loop:
            for i in range(self.movieparser.get_lenght()):
                self.display_frame(i)
                time.sleep(1 / self.movieparser.get_frame_rate())
            if not temploop:
                loop = False

    def display_frame(self, i):
        self.clear_screen()
        try:
            y, x = self.win.getmaxyx()
            print(y, x, self.movieparser.get_size())
            self.win.addstr(self.movieparser.get_frame(i))
            self.win.refresh()
        except:
            print("Error !")

    def clear_screen(self):
        self.win.clear()

    def close(self):
        curses.endwin()


if __name__ == "__main__":
    a = MovieReader("film-test.ascmov")
    try:
        a.play()
    except:
        a.close()
        exit(1)
