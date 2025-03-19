import cv2 as cv
import sys
import pathlib
import numpy as np

path = pathlib.Path().resolve()
 
imgbase = cv.imread(f"{path}/vlcsnap-2025-03-18-18h48m58s510 (1).png") 
img = imgbase.copy()
if img is None:
    sys.exit("Could not read the image.")
 
# cv.imshow("Display window", img)
# k = cv.waitKey(0)
 
# if k == ord("s"):
#     cv.imwrite("starry_night.png", img)

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
 
# mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, img
    

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv.EVENT_MOUSEMOVE:
        
        if drawing == True:
            img = imgbase.copy()
            if mode == True:
                cv.rectangle(img,(ix,iy),(x,y),(0,255,0), 3)
            else:
                r = int(((x - ix)**2 + (y - iy)**2)**(0.5))
                cv.circle(img,(ix,iy),r,(0,0,255), 3)

            # cv.imshow('image', img)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        r = ((x - ix)**2 + (y - iy)**2)**(0.5)
        if mode == True:
            cv.rectangle(imgbase,(ix, iy),(x, y),(0,255,0), 3)
        else:
            cv.circle(imgbase,(ix, iy),r,(0,0,255), 3)

    
 
# Create a black image, a window and bind the function to window
# img = np.zeros((512,512,3), np.uint8)
 
# while(1):
#     cv.imshow('image',img)
#     if cv.waitKey(20) & 0xFF == 27:
#         break
# cv.destroyAllWindows()

def main():

    global mode

    cv.namedWindow('image')
    cv.setMouseCallback('image',draw_circle)

    while(1):
        if (img-imgbase).any():
            img_ = img
        else:
            img_ = imgbase
            
        cv.imshow('image', img_)
        k = cv.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()