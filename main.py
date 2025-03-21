import json
import pathlib
import sys
from functools import wraps
from tkinter import NW, Button, Canvas, Frame, Tk

import cv2 as cv
from PIL import Image, ImageTk

# from tkinter.ttk import *


path = pathlib.Path().resolve()

imgbase = cv.imread(f"{path}/vlcsnap-2025-03-18-18h48m58s510 (1).png")
img = imgbase.copy()
if img is None:
    sys.exit("Could not read the image.")

# cv.imshow("Display window", img)
# k = cv.waitKey(0)

# if k == ord("s"):
#     cv.imwrite("starry_night.png", img)


# Create a black image, a window and bind the function to window
# img = np.zeros((512,512,3), np.uint8)

# while(1):
#     cv.imshow('image',img)
#     if cv.waitKey(20) & 0xFF == 27:
#         break
# cv.destroyAllWindows()


def region_wrapper(func):
    def outer(_self, **kwargs):
        region_name = kwargs.get("region_name")

        @wraps(func)
        def inner(*args, **kwargs):
            return func(_self, region_name=region_name)

        return inner

    return outer


class ControlsWindow:
    def __init__(self):
        self.main_window()

    def Close(self):
        self.root.destroy()

    @region_wrapper
    def select_region(self, region_name: str = "region1"):
        return mainopencv(region_name=region_name)

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


drawing = False  # true if mouse is pressed
mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1
ex, ey = -1, -1
goal_config_file = pathlib.Path(f"{path}/goal_config.json")
if not goal_config_file.is_file():
    goal_config = dict()
else:
    with open(f"{path}/goal_config.json") as goal_config_json:
        goal_config = json.load(goal_config_json)


# mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, ex, ey, drawing, mode, img

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        img = imgbase.copy()
        ix, iy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing is True:
            img = imgbase.copy()
            if mode is True:
                cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 3)
            else:
                r = int(((x - ix) ** 2 + (y - iy) ** 2) ** (0.5))
                cv.circle(img, (ix, iy), r, (0, 0, 255), 3)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        r = ((x - ix) ** 2 + (y - iy) ** 2) ** (0.5)
        if mode is True:
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 3)
            ex, ey = x, y
        else:
            cv.circle(img, (ix, iy), r, (0, 0, 255), 3)


def mainopencv(region_name: str = "region1"):
    global mode, goal_config

    cv.namedWindow("image")
    cv.setMouseCallback("image", draw_circle)

    while 1:
        if (img - imgbase).any():
            img_ = img
        else:
            img_ = imgbase.copy()
        img_ = cv.putText(
            img_,
            region_name,
            (10, 50),
            cv.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 255),
            2,
            cv.LINE_AA,
            False,
        )
        cv.imshow("image", img_)
        k = cv.waitKey(1) & 0xFF
        if k == ord("m"):
            mode = not mode
        elif k == ord("s"):
            region = img[iy:ey, ix:ex]
            cv.imwrite(f"{path}/{region_name}.png", region)

            goal_config[region_name] = {"frame_crop": ((ix, iy), (ex, ey))}

            with open("goal_config.json", "w", encoding="utf-8") as f:
                json.dump(goal_config, f, ensure_ascii=False, indent=4)

        elif k == 27:
            break
    cv.destroyAllWindows()


if __name__ == "__main__":
    ControlsWindow()
