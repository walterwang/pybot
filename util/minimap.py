import cv2
import os
import mss
import util.gather_minimap_data as getmap
import numpy as np
import util.core.client as client
from util.core import mouse


class Minimap(object):
    # Load minimap icons:
    filepath = os.path.dirname(__file__)
    banktemplate = cv2.imread(os.path.join(filepath, 'templates/banktemplate.png'), 3)
    lunartemplate = cv2.imread(os.path.join(filepath, 'templates/lunaraltar.png'), 3)
    lunarbank = cv2.imread(os.path.join(filepath, 'templates/lunarbank.png'), 3)

    def __init__(self, sct, osclientbox, minimap_name, bw =True):
        filepath= os.path.dirname(__file__)
        minimappath= os.path.join(filepath, 'minimaps/'+ minimap_name)
        image = cv2.imread(minimappath)
        self.bw = bw
        if bw:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.edgedmap = cv2.Canny(gray, 50, 200)
        else:
            self.edgedmap = image
        self.sct = sct
        self.osclientbox = osclientbox

    def _match_location(self, template):
        if self.bw:
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.Canny(template, 50, 200)
            (tH, tW) = template.shape[:2]

            result = cv2.matchTemplate(self.edgedmap, template, cv2.TM_CCOEFF)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        else:
            result = cv2.matchTemplate(self.edgedmap, template, cv2.TM_CCOEFF)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        return maxLoc

    def get_minimap_xy(self):
        square_minimap, uncropped_map = getmap.get_map(self.sct, self.osclientbox, square=True)
        return self._match_location(square_minimap)

    def debug_minimap(self):

        while 1:
            square_minimap, uncropped_map = getmap.get_map(self.sct, self.osclientbox, square=True)
            loc = self._match_location(square_minimap)
            # x,y = self.find_lunaraltar()
            # print(x, y)
            # cv2.circle(uncropped_map, (x,y), 5, (0,0,255), 1)
            enlarged_uncropped_map = cv2.resize(uncropped_map, None, fx=3, fy=3, interpolation = cv2.INTER_CUBIC)

            cv2.putText(enlarged_uncropped_map, str(loc), (int(enlarged_uncropped_map.shape[1]/2), int(enlarged_uncropped_map.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('minimap_debug', enlarged_uncropped_map)
            # out.write(uncropped_map)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def find_bank(self):
        uncropped_map = getmap.get_map(self.sct, self.osclientbox)

        result = cv2.matchTemplate(uncropped_map, self.banktemplate, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        print("values:", maxVal, maxLoc)
        if maxVal >1000000:
            print("location of bank on minimap:", maxLoc)
            return maxLoc
        else:
            return None

    def find_lunarbank(self):
        uncropped_map = getmap.get_map(self.sct, self.osclientbox)

        result = cv2.matchTemplate(uncropped_map, self.lunarbank, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        print("values:", maxVal, maxLoc)
        if maxVal >500000:
            print("location of bank on minimap:", maxLoc)
            return maxLoc
        else:
            return None

    def find_lunaraltar(self):
        uncropped_map = getmap.get_map(self.sct, self.osclientbox)

        result = cv2.matchTemplate(uncropped_map, self.lunartemplate, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        print("values:", maxVal, maxLoc)
        if maxVal >100000:
            print("location of lunar latar on minimap:", maxLoc)
            return maxLoc
        else:
            return None



if __name__ == "__main__":

    client = client.Client()
    sct5 = mss.mss()
    n = 'lunarisle.png'
    m = Minimap(sct5, client.box, n, bw = False)
    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #out = cv2.VideoWriter('minimap_demo.mp4', fourcc, 30.0, (453, 453))
    m.debug_minimap()

    # print(get_minimap_xy(sct5, client))
    #out.release()
