import cv2
import mss
from util.gather_minimap_data import get_map
import numpy as np
import util.core.client as client


def get_location(template):

    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]

    image = cv2.imread("training_data/minimaps/miningguild.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edgedmap = cv2.Canny(gray, 50, 200)

    result = cv2.matchTemplate(edgedmap, template, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    return (maxLoc)


def debug_minimap(out):

    while 1:
        square_minimap, uncropped_map = get_map(sct5, client.box, square=True)
        loc = get_location(square_minimap)
        uncropped_map = cv2.resize(uncropped_map, None, fx=3, fy=3, interpolation = cv2.INTER_CUBIC)
        cv2.putText(uncropped_map, str(loc), (int(uncropped_map.shape[1]/2), int(uncropped_map.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # cv2.imshow('minimap_debug', uncropped_map)
        out.write(uncropped_map)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

            break


if __name__ == "__main__":

    client = client.Client()
    sct5 = mss.mss()
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('minimap_demo.mp4', fourcc, 30.0, (453, 453))
    debug_minimap(out)
    out.release()
