import cv2
import os
import mss
import util.gather_minimap_data as getmap
import numpy as np
import util.core.client as client
from util.core import mouse

filepath= os.path.dirname(__file__)
minimappath= os.path.join(filepath, "training_data/minimaps/miningguild.png")
image = cv2.imread(minimappath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edgedmap = cv2.Canny(gray, 50, 200)

banktemplate = cv2.imread(os.path.join(filepath,'banktemplate.png'),3)

def _match_location(template):

    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]

    result = cv2.matchTemplate(edgedmap, template, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    return (maxLoc)

def get_minimap_xy(sct, osclient):
    square_minimap, uncropped_map = getmap.get_map(sct, osclient.box, square=True)
    return _match_location(square_minimap)

def debug_minimap():

    while 1:
        square_minimap, uncropped_map = getmap.get_map(sct5, client.box, square=True)
        loc = _match_location(square_minimap)
        enlarged_uncropped_map = cv2.resize(uncropped_map, None, fx=3, fy=3, interpolation = cv2.INTER_CUBIC)
        cv2.putText(enlarged_uncropped_map, str(loc), (int(enlarged_uncropped_map.shape[1]/2), int(enlarged_uncropped_map.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('minimap_debug', enlarged_uncropped_map)
        # out.write(uncropped_map)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def move_minimap(osclient, mx , my):
    minimap_center_x = 75 + 562 # change this to osclient map offset to be compatible to other clients
    minimap_center_y = 75 + 4
    mouse.mclick_onclient(osclient.box, minimap_center_x+mx, minimap_center_y+my)


def find_bank(sct, osclientbox):
    uncropped_map = getmap.get_map(sct, osclientbox)

    result = cv2.matchTemplate(uncropped_map, banktemplate, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    print("values:", maxVal, maxLoc)
    if maxVal >1000000:
        print("location of bank on minimap:", maxLoc)
        return maxLoc
    else:
        return None
def set_north(sct, osclientbox):
    mouse.mclick_onclient(osclientbox, 560, 20)


if __name__ == "__main__":

    client = client.Client()
    sct5 = mss.mss()
    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #out = cv2.VideoWriter('minimap_demo.mp4', fourcc, 30.0, (453, 453))
    debug_minimap()

    # print(get_minimap_xy(sct5, client))
    #out.release()
