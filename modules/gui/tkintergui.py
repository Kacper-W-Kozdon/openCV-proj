import os
import pathlib
from tkinter import NW, Button, Canvas, Frame, Tk

import cv2 as cv
import numpy as np
from PIL import Image, ImageTk

from ..opencvwindow import mainopencv
from ..utils import region_wrapper

file_path = os.path.dirname(os.path.realpath(__file__))
path = pathlib.Path(file_path).parent.parent.resolve()
select_region_fun = mainopencv

canvas = {"height": 200, "width": 200, "anchor_y": 0, "anchor_x": 0}


class ControlsWindow:
    def __init__(self):
        self.main_window()

    def Close(self):
        self.root.destroy()

    @region_wrapper
    def select_region(
        self,
        region_name: str = "region1",
        select_frame_or_points: str = "frame",
        fun_=select_region_fun,
    ):
        if fun_:
            return fun_(
                region_name=region_name, select_frame_or_points=select_frame_or_points
            )

    def update_canvas(self):
        self.canvas_region1.delete("all")
        self.canvas_region2.delete("all")
        my_file = pathlib.Path(f"{path}/region1.png")

        if my_file.is_file():
            img1 = cv.imread(f"{path}/region1.png")
            height, width, channels = img1.shape
            if (ratio := height / width) >= 1:
                dsize = (canvas.get("height"), int(width / ratio))
            else:
                dsize = (int(height / ratio), canvas.get("width"))

            resized_image1 = cv.resize(
                img1, dsize, dst=None, fx=None, fy=None, interpolation=cv.INTER_LINEAR
            )
            resized_image1 = np.flip(resized_image1, 2)

            img_region1_array = Image.fromarray(resized_image1, mode="RGB")
            img_region1 = img_region1_array.convert("RGB")
            img_region1 = ImageTk.PhotoImage(img_region1)

            self.canvas_region1.create_image(
                canvas.get("anchor_y"),
                canvas.get("anchor_x"),
                anchor=NW,
                image=img_region1,
            )

        my_file = pathlib.Path(f"{path}/region2.png")
        print(my_file.is_file())
        if my_file.is_file():
            img2 = cv.imread(f"{path}/region2.png")
            height, width, channels = img2.shape
            if (ratio := height / width) >= 1:
                dsize = (canvas.get("height"), int(width / ratio))
            else:
                dsize = (int(height / ratio), canvas.get("width"))

            resized_image2 = cv.resize(
                img2, dsize, dst=None, fx=None, fy=None, interpolation=cv.INTER_LINEAR
            )
            resized_image2 = np.flip(resized_image2, 2)

            img_region2_array = Image.fromarray(resized_image2, mode="RGB")
            img_region2 = img_region2_array.convert("RGB")
            img_region2 = ImageTk.PhotoImage(img_region2)

            self.canvas_region2.create_image(
                canvas.get("anchor_y"),
                canvas.get("anchor_x"),
                anchor=NW,
                image=img_region2,
            )

        self.canvas_region1.update()
        self.canvas_region2.update()
        self.root.after(1000, self.update_canvas)
        self.root.mainloop()

    def main_window(self):
        self.root = Tk()
        self.root.geometry("512x512")
        self.top = Frame(self.root)
        self.bottom = Frame(self.root)
        self.top.pack(side="top", pady=10)
        self.bottom.pack(side="top", fill="both")

        # Button for closing
        exit_button = Button(self.root, text="Exit", command=self.Close)
        exit_button.pack(in_=self.top, pady=10)

        self.canvas_region1 = Canvas(
            self.root,
            bg="black",
            height=canvas.get("height"),
            width=canvas.get("width"),
        )
        self.canvas_region1.pack(in_=self.top, side="left")

        my_file = pathlib.Path(f"{path}/region1.png")
        if my_file.is_file():
            img_region1 = ImageTk.PhotoImage(Image.open(f"{path}/region1.png"))
            self.canvas_region1.create_image(10, 10, anchor=NW, image=img_region1)

        self.canvas_region2 = Canvas(
            self.root,
            bg="black",
            height=canvas.get("height"),
            width=canvas.get("width"),
        )
        self.canvas_region2.pack(in_=self.top, side="left")

        my_file = pathlib.Path(f"{path}/region2.png")
        if my_file.is_file():
            img_region2 = ImageTk.PhotoImage(Image.open(f"{path}/region2.png"))
            self.canvas_region2.create_image(10, 10, anchor=NW, image=img_region2)

        region1_button = Button(
            self.root,
            text="Select region 1",
            command=self.select_region(region_name="region1"),
        )
        region1_button.pack(in_=self.bottom, side="left")

        region1_points_button = Button(
            self.root,
            text="Select region 1",
            command=self.select_region(
                region_name="region1", select_frame_or_points="points"
            ),
        )
        region1_points_button.pack(in_=self.bottom, side="left")

        region2_button = Button(
            self.root,
            text="Select region 2",
            command=self.select_region(region_name="region2"),
        )
        region2_button.pack(in_=self.bottom, side="right")

        region2_points_button = Button(
            self.root,
            text="Select region 2",
            command=self.select_region(
                region_name="region2", select_frame_or_points="points"
            ),
        )
        region2_points_button.pack(in_=self.bottom, side="right")

        self.update_canvas()
