import curses


class MovieParser():
    def __init__(self, fn):
        self._size = 0
        self._file_name = fn
        self._frames = []
        self.read_file()

    def read_file(self):
        file = open(self._file_name, "r")
        self._width, self._height = [int(e) for e in file.readline()[:-1].split(",")]
        self._frame_rate, self._size = [int(e) for e in file.readline()[:-1].split(",")]
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

    def is_junk_line(self, s):
        return s == "\n"

    def get_lenght(self):
        return self._size

    def get_frame(self, i):
        return "Hello"


class MovieReader():
    def __init__(self, fn):
        self.movieparser = MovieParser(fn)
        self.win = curses.initscr()

    def play(self, loop=True):
        for i in range(self.movieparser.get_lenght()):
            self.display_frame(i)

    def display_frame(self, i):
        self.win.addstr(self.movieparser.get_frame(i))
        self.win.refresh()

    def clear_screen(self):
        self.win.clear()

    def close(self):
        curses.endwin()


a = MovieReader("ok")
a.win.addstr("ok")
