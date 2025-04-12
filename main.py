import os
import pathlib

from modules.gui.tkintergui import ControlsWindow

# from tkinter.ttk import *

file_path = os.path.dirname(os.path.realpath(__file__))
path = pathlib.Path(file_path).resolve()


if __name__ == "__main__":
    ControlsWindow()
