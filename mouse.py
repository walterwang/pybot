import time
import uinput
import cv2
import random

from Xlib import display

device = uinput.Device([
        uinput.BTN_LEFT,
        uinput.BTN_RIGHT,
        uinput.REL_X,
        uinput.REL_Y
        ])

def move_mouse_abs(abs_x, abs_y):
    qp = display.Display().screen().root.query_pointer()
    device.emit(uinput.REL_X, abs_x-qp.root_x)
    device.emit(uinput.REL_Y, abs_y-qp.root_y)

def mclick_abs(abs_x, abs_y, click = "left", e = 0):
    if e != 0:
        mouse_err= random.randint(0,e)
    qp = display.Display().screen().root.query_pointer()
    device.emit(uinput.REL_X, abs_x-qp.root_x+e)
    device.emit(uinput.REL_Y, abs_y-qp.root_y+e)
    time.sleep(.1)
    if click == "left":
        device.emit_click(uinput.BTN_LEFT, 1)
    else:
        device.emit_click(uinput.BTN_RIGHT, 1)

def random_pause(seconds, range = 0):
    if (seconds-range) < 0:
        min_pause=0
    else:
        min_pause =seconds-range

    sleep_time = random.randint(min_pause*10, (seconds+range)*10)/10
    time.sleep(sleep_time)

# for i in range(100):
#
#     mclick_abs(2141, 714)
#     random_pause(8, 2)
#
#     mclick_abs(2508, 730, click ='right')
#     random_pause(1, 1)
#
#     mclick_abs(2497, 775)
#     random_pause(1, 1)


# 2141 714
# 2508 730
# 2497 775