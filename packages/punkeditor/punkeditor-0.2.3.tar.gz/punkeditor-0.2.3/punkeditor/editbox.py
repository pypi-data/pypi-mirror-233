import curses
from curses.textpad import Textbox


class EditBox(Textbox):

    """Modified curses textbox:

    LF (enter) - accept the result

    DEL - backspace

    Fix arrow-driven cursor movement logic

    Don't go to another line; no wrapping



    """

    @classmethod
    def keymap(cls):
        return {
            curses.KEY_LEFT:      cls.move_left,
            curses.KEY_RIGHT:     cls.move_right,
            curses.KEY_DOWN:      cls.move_down,
            curses.KEY_UP:        cls.move_up,
            curses.ascii.SOH:     cls.move_left_end,  # ^a
            curses.ascii.ENQ:     cls.move_right_end,  # ^e
            curses.ascii.BS:      cls.backspace,
            curses.KEY_BACKSPACE: cls.backspace,
            curses.ascii.DEL:     cls.backspace,
            curses.ascii.EOT:     cls.del_char,       # ^d
            curses.ascii.VT:      cls.kill_line,      # ^k
        }

    def del_char(self):
        self.win.delch()

    def move_left_end(self):
        (y, x) = self.win.getyx()
        self.win.move(y, 0)

    def move_left(self):
        (y, x) = self.win.getyx()
        if x > 0:
            self.win.move(y, x-1)
        elif y == 0:
            pass
        elif self.stripspaces:
            self.win.move(y-1, self._end_of_line(y-1))
        else:
            self.win.move(y-1, self.maxx)

    def backspace(self):
        self.move_left()
        self.del_char()

    def move_right_end(self):
        (y, x) = self.win.getyx()
        if self.stripspaces:
            self.win.move(y, self._end_of_line(y))
        else:
            self.win.move(y, self.maxx)

    def move_right(self):
        (y, x) = self.win.getyx()
        if x < self.maxx and x < self._end_of_line(y):
            self.win.move(y, x+1)
        elif y == self.maxy:
            pass
        else:
            self.win.move(y+1, 0)

    def kill_line(self):
        (y, x) = self.win.getyx()
        if x == 0 and self._end_of_line(y) == 0:
            self.win.deleteln()
        else:
            # first undo the effect of self._end_of_line
            self.win.move(y, x)
            self.win.clrtoeol()

    def move_down(self):
        (y, x) = self.win.getyx()
        if y < self.maxy:
            if x > self._end_of_line(y+1):
                self.win.move(y+1, self._end_of_line(y+1))
            else:
                self.win.move(y+1, x)

    def move_up(self):
        (y, x) = self.win.getyx()
        if y > 0:
            if x > self._end_of_line(y-1):
                self.win.move(y-1, self._end_of_line(y-1))
            else:
                self.win.move(y-1, x)

    def do_command(self, ch):
        "Process a single editing command."
        self._update_max_yx()
        (y, x) = self.win.getyx()
        self.lastcmd = ch
        if ch == curses.ascii.HT:
            return 0
        elif curses.ascii.isprint(ch):
            if x < self.maxx:
                self._insert_printable_char(ch)
        elif ch in self.keymap():
            self.keymap()[ch](self)
        return 1

    def _insert_printable_char(self, ch):
        self._update_max_yx()
        (y, x) = self.win.getyx()
        lastch = self.win.inch(y, self.maxx - 1)
        self.win.move(y, x)
        if curses.ascii.ascii(lastch) == curses.ascii.SP:
            backyx = None
            while x < self.maxx:
                oldch = self.win.inch()
                self.win.addch(ch)
                ch = oldch
                (y, x) = self.win.getyx()
                if backyx is None:
                    backyx = y, x
            if backyx is not None:
                self.win.move(*backyx)

    def gather(self):
        "Collect and return the contents of the window."
        result = ""
        self._update_max_yx()
        for y in range(self.maxy+1):
            self.win.move(y, 0)
            stop = self._end_of_line(y)
            if stop == 0 and self.stripspaces:
                continue
            for x in range(self.maxx+1):
                if self.stripspaces and x > stop:
                    break
                result = result + chr(curses.ascii.ascii(self.win.inch(y, x)))
            # if self.maxy > 0:
            #     result = result + " "
        return result
