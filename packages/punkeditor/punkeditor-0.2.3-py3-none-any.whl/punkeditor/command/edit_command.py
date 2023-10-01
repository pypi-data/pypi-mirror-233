from dataclasses import dataclass
from argparse import ArgumentParser
import os
import curses

from punkeditor.command import PunkEditorCommand
from punkeditor.editbox import EditBox


@dataclass
class EditCommand(PunkEditorCommand):

    name = 'edit'
    width:int = None
    height:int = None

    @classmethod
    def add_args(self, parser):
        parser.add_argument('--width', type=int)
        parser.add_argument('--height', type=int)
        

    def loop(self, window: curses.window):
        window.bkgd(' ')
        window.refresh()
        wmaxy, wmaxx = window.getmaxyx()
        width = self.width or wmaxx - 2
        height = self.height or wmaxy - 2
        bx = int((wmaxx - width) / 2)
        by = int((wmaxy - height) / 2)
        bwindow = window.subwin(height + 2, \
                width + 2, by - 1, bx - 1)
        bwindow.border()
        bwindow.refresh()
        twindow = window.subwin(height, width, by, bx)
        box = EditBox(twindow, insert_mode=True)
        self.result = box.edit()

    def execute(self):
        curses.wrapper(self.loop)
        return self.result
