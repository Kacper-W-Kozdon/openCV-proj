import pathlib
from tkinter import NW, Button, Canvas, Frame, Tk

from PIL import Image, ImageTk

from ..utils import region_wrapper

path = pathlib.Path().resolve()


class ControlsWindow:
    def __init__(self):
        self.main_window()

    def Close(self):
        self.root.destroy()

    @region_wrapper
    def select_region(self, region_name: str = "region1", fun_=None):
        if fun_:
            return fun_(region_name=region_name)

    def update_canvas(self):
        self.canvas_region1.delete("all")
        self.canvas_region2.delete("all")
        my_file = pathlib.Path(f"{path}/region1.png")

        if my_file.is_file():
            img_region1 = ImageTk.PhotoImage(Image.open(f"{path}/region1.png"))
            self.canvas_region1.create_image(10, 10, anchor=NW, image=img_region1)

        my_file = pathlib.Path(f"{path}/region2.png")
        print(my_file.is_file())
        if my_file.is_file():
            img_region2 = ImageTk.PhotoImage(Image.open(f"{path}/region2.png"))
            self.canvas_region2.create_image(10, 10, anchor=NW, image=img_region2)

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

        self.canvas_region1 = Canvas(self.root, bg="black", height=200, width=200)
        self.canvas_region1.pack(in_=self.top, side="left")

        my_file = pathlib.Path(f"{path}/region1.png")
        if my_file.is_file():
            img_region1 = ImageTk.PhotoImage(Image.open(f"{path}/region1.png"))
            self.canvas_region1.create_image(10, 10, anchor=NW, image=img_region1)

        self.canvas_region2 = Canvas(self.root, bg="black", height=200, width=200)
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

        region2_button = Button(
            self.root,
            text="Select region 2",
            command=self.select_region(region_name="region2"),
        )
        region2_button.pack(in_=self.bottom, side="right")

        self.update_canvas()
