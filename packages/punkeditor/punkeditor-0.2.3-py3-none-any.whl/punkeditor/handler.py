import sys

from wizlib.command_handler import CommandHandler
from punkeditor.command import PunkEditorCommand


class PunkEditorHandler(CommandHandler):

    @classmethod
    def shell(cls):
        super().shell(PunkEditorCommand)
