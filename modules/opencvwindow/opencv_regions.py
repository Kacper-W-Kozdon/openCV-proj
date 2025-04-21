import json
import os
import pathlib
import sys

import cv2 as cv

box_line_width = 3

file_path = os.path.dirname(os.path.realpath(__file__))


path_root = pathlib.Path(file_path).parent.parent.resolve()
print(path_root)


# mouse callback function
def draw_frame(event, x, y, flags, param):
    global ix, iy, ex, ey, drawing, mode, img, click_counter

    def connect_points(prev_point=None, current_point=None, click=None, image=None):
        if click == 0:
            image = imgbase.copy()
            return image

        cv.line(img, prev_point, current_point, (0, 0, 255), box_line_width)
        return img

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        img = imgbase.copy()
        ix, iy = x, y
        if mode is False:
            points[click_counter] = (ix, iy)
            img = connect_points(
                points[click_counter], points[click_counter - 1], click_counter, img
            )
            click_counter += 1
            click_counter = click_counter % 4

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing is True:
            img = imgbase.copy()
            if mode is True:
                cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), box_line_width)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode is True:
            cv.rectangle(img, (ix, iy), (x, y), (0, 0, 255), 3)
            ex, ey = x, y


def mainopencv(region_name: str = "region1", select_frame_or_points: str = "frame"):
    global mode, goal_config, region_file, imgbase

    region_file = f"{region_name}.png"

    mode = True if select_frame_or_points in ["frame"] else False

    path_imgbase = (
        f"{path_root}/vlcsnap-2025-03-18-18h48m58s510 (1).png"
        if mode
        else f"{path_root}/{region_file}"
    )
    # print(f"\n---BASE IMAGE:{path_imgbase}---\n")
    imgbase = cv.imread(f"{path_imgbase}")

    cv.namedWindow("image", cv.WINDOW_NORMAL)

    if (ratio := imgbase.shape[1] / imgbase.shape[0]) >= 1:
        cv.resizeWindow("image", canvas.get("height"), int(canvas.get("width") / ratio))
    else:
        cv.resizeWindow("image", int(canvas.get("height") * ratio), canvas.get("width"))

    cv.setMouseCallback("image", draw_frame)

    while 1:
        if img.shape != imgbase.shape:
            img_ = imgbase.copy()
        elif (img - imgbase).any():
            img_ = img
        else:
            img_ = imgbase.copy()

        assert (
            region_name in ["region1", "region2"]
        ), f"region_name variable incorrect, it should be 'region1' or 'region2', it was {region_name}"
        assert (
            select_frame_or_points in ["frame", "points"]
        ), f"select_frame_or_points variable incorrect, it should be 'frame' or 'points', it was {select_frame_or_points}"

        img_ = (
            img_
            if not mode
            else cv.putText(
                img_,
                region_name + select_frame_or_points,
                (10, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 0, 255),
                2,
                cv.LINE_AA,
                False,
            )
        )
        cv.imshow("image", img_)
        k = cv.waitKey(1) & 0xFF

        if k == ord("s"):
            region = img[
                (iy + box_line_width) : (ey - box_line_width),
                (ix + box_line_width) : (ex - box_line_width),
            ]
            cv.imwrite(f"{path_root}/{region_name}.png", region)

            goal_config[region_name] = {"frame_crop": ((ix, iy), (ex, ey))}

            with open("goal_config.json", "w", encoding="utf-8") as f:
                json.dump(goal_config, f, ensure_ascii=False, indent=4)

        elif k == 27:
            break
    cv.destroyAllWindows()


click_counter = 0
points = [None, None, None, None]
drawing = False  # true if mouse is pressed
mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1
ex, ey = -1, -1
region_file = "region1.png"

path = (
    f"{path_root}/vlcsnap-2025-03-18-18h48m58s510 (1).png"
    if mode
    else f"{path_root}/{region_file}"
)
imgbase = cv.imread(f"{path}")

canvas = {
    "width": imgbase.shape[0],
    "height": imgbase.shape[1],
    "anchor_y": 0,
    "anchor_x": 0,
}

img = imgbase.copy()
if img is None:
    sys.exit("Could not read the image.")


goal_config_file = pathlib.Path(f"{path}/goal_config.json")
if not goal_config_file.is_file():
    goal_config = dict()
else:
    with open(f"{path}/goal_config.json") as goal_config_json:
        goal_config = json.load(goal_config_json)
