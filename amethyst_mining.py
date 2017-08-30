# from transitions import Machine
from transitions.extensions import GraphMachine as Machine
from util.core.ssd import ssd_inference
from util.core import mouse, ocr, keyboard
import util.core.client as client
import util.autolog as autolog
import mss
import time
from util import template
from util.minimap import get_minimap_xy, move_minimap, find_bank, set_north

class AmethystBot(object):

    states = ['login', 'mine_amethyst', 'walking_to_bank', 'search_bankchest', 'walking_to_mine']

    transitions = [
        ['dc', 'mine_amethyst', 'login'],
        ['login_to_mining', 'login', 'mine_amethyst'],
        ['login_to_walking', 'login', 'walking_to_mine'],
        ['amethyst_mined', 'mine_amethyst', 'mine_amethyst'],
        ['inventory_full', 'mine_amethyst', 'walking_to_bank'],
        ['bank_reached', 'walking_to_bank', 'search_bankchest'],
        ['bank_found', 'search_bankchest', 'walking_to_mine'],
        ['mine_reached', 'walking_to_mine', 'mine_amethyst']

    ]

    def __init__(self, name):

        self.name = name
        self.total_amethyst_mined = 0
        self.script_runtime = 0

        self.osclient = client.Client()
        self.box = self.osclient.box
        self.sct = mss.mss()
        self.machine = Machine(model=self, states=AmethystBot.states, transitions=AmethystBot.transitions, initial='login', queued = True)

        self.machine.on_enter_mine_amethyst('onenter_amethyst')
        self.machine.on_enter_walking_to_bank('onenter_invfull')
        self.machine.on_enter_search_bankchest('onenter_bankchest')
        self.machine.on_enter_walking_to_mine('onenter_tomine')
        self.machine.on_enter_login('onenter_login')


    def onenter_amethyst(self):
        for i in range(0,10):
            rclasses, rbboxes, rcenter = ssd_inference.get_objects(self.sct, self.osclient, object_id=[4])
            for c in rcenter:
                text_found = mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], self.box, target_text="rys")
                if text_found:
                    for i in range(1,20):
                        time.sleep(4)
                        if "manage" in ocr.get_lastchat(self.box):
                            print("managed to mine a rock")
                            return self.amethyst_mined()

                        if "currently" in ocr.get_lastchat(self.box):
                            print("no_rocks")
                            return self.amethyst_mined()

                        if "full" in ocr.get_dialogue(self.box):
                            print("inv is full")
                            return self.inventory_full()
            keyboard.hold_key("RIGHT_KEY", 5)
            keyboard.hold_key("UP_KEY", 5)
        print('found nothing, checking to see if dc')
        if autolog.checkloginscreen(box=self.box):
            self.dc()

    def onenter_invfull(self):
        print("entering invful")
        time.sleep(2)
        set_north(self.sct, self.box)
        time.sleep(2)
        minimap_xy = get_minimap_xy(self.sct, self.osclient)
        print("x,y coordinates", minimap_xy[0],' ', minimap_xy[1])

        if minimap_xy[1]<280:
            move_minimap(self.osclient, -10,-65)
            time.sleep(10)
            bankx, banky = find_bank(self.sct, self.box)
            move_minimap(self.osclient, bankx-75, banky-75)
            time.sleep(3)
            return self.bank_reached()
    def onenter_login(self):
        time.sleep(9)
        print('minimap, coordiante', get_minimap_xy(self.sct, self.osclient))
        if get_minimap_xy(self.sct, self.osclient)[1]>180:
            self.login_to_mining()
        else:
            self.login_to_walking()


    def onenter_bankchest(self):
        for i in range(0,4):
            keyboard.hold_key("RIGHT_KEY", 10)
            keyboard.hold_key("UP_KEY", 10)
            rclasses, rbboxes, rcenter = ssd_inference.get_objects(self.sct, self.osclient, object_id=[2,3])
            for c in rcenter:
                text_found = mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], self.box, target_text="Bank")
                if text_found:
                    time.sleep(3)
                    if template.click_deposit(self.sct, self.box):
                        set_north(self.sct, self.box)
                        return self.bank_found()
        print('bankchest cant be found')
    def onenter_tomine(self):
        print("walking to mine")
        set_north(self.sct, self.box)
        move_minimap(self.osclient, 10, 70)
        time.sleep(12)
        self.mine_reached()

        # return self.amethyst_mined()
        # print("recursive hell initiated")


pybot = AmethystBot("mysuperbot")

# graph_pic = pybot.get_graph().draw(format='png', prog='dot')
# import cv2
# import numpy as np
# g = np.fromstring(graph_pic, np.uint8)
# img = cv2.imdecode(g, cv2.IMREAD_COLOR)
# cv2.imshow("dynamicgraph", img)
# cv2.waitKey(0)

pybot.login_to_mining()







#

#
# labels = {
#     0: 'none',
#     1: 'depleted',
#     2: 'bankchest',
#     3: 'depositbox',
#     4: 'amethyst',
#     5: 'mithril',
#     6: 'adamantite',
#     8: 'coal',
#     9: 'iron',
#     15: 'spooky_ghost'
#
# }
#