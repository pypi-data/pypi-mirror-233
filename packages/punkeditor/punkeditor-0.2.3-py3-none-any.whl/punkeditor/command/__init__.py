from dataclasses import dataclass

from wizlib.command_handler import Command
from wizlib.config_machine import ConfigMachine


@dataclass
class PunkEditorCommand(ConfigMachine, Command):

    appname = 'punkeditor'
    default = 'edit'
