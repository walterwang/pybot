from util.core import client, mouse
import mss, time
from util.template import Template
from util.minimap import Minimap
from util.core.ocr import Ocr
from util.core.ssd.ssd_inference import SSD
from util.core.mouse import Mouse
from util.autolog import Autolog
from transitions import Machine
from util.path_matrix import get_path
import util.core.keyboard as keyboard

# from transitions.extensions import GraphMachine as Machine

class AstralBot(object):

    states = ['s_login', 's_walkaltar', 's_findaltar', 's_telebank', 's_findbank']

    transitions = [['t_dc', '*', 's_login'],
                   ['t_teleport', '*', 's_telebank'],
                   ['t_login2telebank', 's_login', 's_telebank'],
                   ['t_telebank2findbank', 's_telebank', 's_findbank'],
                   ['t_findbank2walkaltar', 's_findbank', 's_walkaltar'],
                   ['t_walkaltar2walkaltar', 's_walkaltar', 's_walkaltar'],
                   ['t_walkaltar2findaltar', 's_walkaltar', 's_findaltar'],
                   ['t_findaltar2telebank', 's_findaltar', 's_telebank']]

    def __init__(self, name):
        self.name = name
        self.osclient = client.Client()
        self.astral_runes = 0
        self.staminapot = 0
        self.box = self.osclient.box
        self.sct = mss.mss()
        self.machine = Machine(model=self, states=AstralBot.states, transitions=AstralBot.transitions,
                               initial='s_telebank', queued=True)
        self.minimap = Minimap(self.sct, self.box, 'lunarisle.png', bw = False)
        self.ocr = Ocr(self.sct, self.box)
        self.mouse = Mouse(self.sct, self.box)
        self.template = Template(self.sct, self.box)
        self.autolog = Autolog(self.sct, self.box)
        self.ssd_inference = SSD(ckpt_filename= '/home/walter/Documents/others_git/SSD-Tensorflow/checkpoints/astrals/astrals_model.ckpt', n_classes=3)
        self.walkingpath = get_path()
        self.did_not_find_bank = 0


        # self.machine.on_enter_s_login('onenter_s_login')
        self.machine.on_enter_s_walkaltar('onenter_s_walkaltar')
        self.machine.on_enter_s_findaltar('onenter_s_findaltar')
        self.machine.on_enter_s_telebank('onenter_s_telebank')
        self.machine.on_enter_s_findbank('onenter_s_findbank')

        self.rctrips = 0

    def onenter_s_walkaltar(self):
        minimap_xy = self.minimap.get_minimap_xy()
        print(minimap_xy)
        if minimap_xy[0] >239  and minimap_xy[1]> 240:
            #self.mouse.move_minimap(5, 0)
            print("destination reached")
            time.sleep(1)
            return self.t_walkaltar2findaltar()
        else:
            move_x, move_y = self.walkingpath[minimap_xy[0]][minimap_xy[1]]
            self.mouse.move_minimap(int(move_x), int(move_y))
            time.sleep(1.5)
            return self.t_walkaltar2walkaltar()

    def empty_pouch(self, pouchpos):
        ix, iy = self.osclient.inv[pouchpos]
        self.mouse.mclick_abs(ix, iy, click='right')
        time.sleep(0.2)
        self.mouse.mclick_abs(ix, iy + 42)

    def repair_pouch(self):
        # cosmicx, cosmicy = self.osclient.bankspace[2]
        # self.mouse.mclick_abs(cosmicx, cosmicy, click='left')
        # time.sleep(.3)
        keyboard.send_key('ESC')
        time.sleep(.5)
        keyboard.send_key('F3')
        lx, ly = self.osclient.lunarmagic[5]
        time.sleep(.3)
        self.mouse.mclick_abs(lx, ly)
        time.sleep(1)
        self.mouse.mclick_onclient(247,117)
        time.sleep(6)
        keyboard.send_key('SPACE')
        time.sleep(2)
        keyboard.send_key('SPACE')
        time.sleep(2)
        keyboard.send_key('SPACE')
        time.sleep(2)
        keyboard.send_key('ESC')
        return

    def onenter_s_findaltar(self):
        time.sleep(2)
        rclasses, rbboxes, rcenter = self.ssd_inference.get_objects(self.sct, self.osclient, object_id=[3])
        text_found = False
        for c in rcenter:
            text_found = self.mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], target_text=['une', '3','ra'], textcolor = 200)
        if text_found:
            time.sleep(5)
            self.empty_pouch(0)
            time.sleep(0.5)
            self.empty_pouch(1)
        rclasses, rbboxes, rcenter = self.ssd_inference.get_objects(self.sct, self.osclient, object_id=[3])
        for c in rcenter:
            text_found = self.mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], target_text=['une', '3','ra'], textcolor = 200)
        time.sleep(3)
        if text_found:
            self.empty_pouch(2)
            time.sleep(0.5)
            self.empty_pouch(3)
        time.sleep(0.2)
        for c in rcenter:
            text_found = self.mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], target_text=['une', '3','ra'], textcolor = 200)
        #put rune in pouch
        time.sleep(2.5)
        ix, iy = self.osclient.inv[4]
        self.mouse.mclick_abs(ix, iy)
        time.sleep(.2)
        ix, iy = self.osclient.inv[5]
        time.sleep(1)
        self.mouse.mclick_abs(ix, iy)
        self.rctrips += 1

        return self.t_findaltar2telebank()

    def onenter_s_telebank(self):
        keyboard.send_key('F3')
        lx, ly = self.osclient.lunarmagic[8]
        time.sleep(.3)
        self.mouse.mclick_abs(lx, ly)
        time.sleep(1)
        keyboard.send_key('ESC')
        print('missed banks', self.did_not_find_bank)
        print('rc trips: ', self.rctrips)

        return self.t_telebank2findbank()

    def onenter_s_findbank(self):

        time.sleep(2)
        bankx, banky = self.minimap.find_lunarbank()
        self.mouse.move_minimap(bankx - 75+5, banky - 75+10)
        time.sleep(6)


        #self.mouse.move_minimap(-15, 0)


        if (self.rctrips + 1) % 11 == 0:  # check for npc repair
            print("pouch repair npc contact")
            time.sleep(2)
            self.repair_pouch()
            time.sleep(2)

        rclasses, rbboxes, rcenter = self.ssd_inference.get_objects(self.sct, self.osclient, object_id=[1, 2])
        text_found = False

        for c in rcenter:
            text_found = self.mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], target_text=['ank'])
            if text_found:



                print('withdraw everything')
                time.sleep(2)
                ess_x, ess_y = self.osclient.bankspace[0]
                self.mouse.mclick_abs(ess_x, ess_y, click='right')
                time.sleep(.2)
                self.mouse.mclick_abs(ess_x, ess_y+100)
                time.sleep(.3)
                keyboard.send_key('ESC')
                time.sleep(.3)
                lx, ly = self.osclient.inv[0]
                self.mouse.mclick_abs(lx, ly)
                lx, ly = self.osclient.inv[1]
                self.mouse.mclick_abs(lx, ly)
                break
        print('find bank again')
        rclasses, rbboxes, rcenter = self.ssd_inference.get_objects(self.sct, self.osclient, object_id=[1, 2])
        for c in rcenter:
            text_found = False
            text_found = self.mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], target_text=['ank'])
            if text_found:
                print('withdraw again')
                time.sleep(3)
                ess_x, ess_y = self.osclient.bankspace[0]
                self.mouse.mclick_abs(ess_x, ess_y, click='right')
                time.sleep(.2)
                self.mouse.mclick_abs(ess_x, ess_y + 100)
                time.sleep(.3)
                keyboard.send_key('ESC')
                time.sleep(.5)
                lx, ly = self.osclient.inv[2]
                self.mouse.mclick_abs(lx, ly)
                lx, ly = self.osclient.inv[3]
                self.mouse.mclick_abs(lx, ly)
                time.sleep(1)
                break
        rclasses, rbboxes, rcenter = self.ssd_inference.get_objects(self.sct, self.osclient, object_id=[1, 2])
        for c in rcenter:
            text_found = False
            text_found = self.mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], target_text=['ank'])
            if text_found:
                time.sleep(3)
                # print('last time opening bank')
                # self.mouse.mclick_onclient(c[0], c[1])

                if self.ocr.get_run_energy() < 75:
                    stam_x, stam_y = self.osclient.bankspace[1 + self.staminapot%4]
                    self.mouse.mclick_abs(stam_x, stam_y)
                    self.staminapot += 1
                    time.sleep(.3)
                    keyboard.send_key('ESC')
                    time.sleep(1)
                    px, py = self.template.click_pot()

                    print('drinking stam')
                    time.sleep(.5)
                    rclasses, rbboxes, rcenter = self.ssd_inference.get_objects(self.sct, self.osclient, object_id=[1, 2])
                    for c in rcenter:
                        text_found = self.mouse.ocr_click(c[0] + self.box['left'], c[1] + self.box['top'], target_text=['ank'])
                        time.sleep(.5)
                        if text_found:
                            time.sleep(2.5)
                            if px*py != 0:
                                self.mouse.mclick_abs(px, py)
                            time.sleep(.2)
                            #self.template.click_pot()
                            self.template.click_deposit()
                            break

                ess_x, ess_y = self.osclient.bankspace[0]
                self.mouse.mclick_abs(ess_x, ess_y, click='right')
                time.sleep(.2)
                self.mouse.mclick_abs(ess_x, ess_y + 100)
                time.sleep(.3)
                return self.t_findbank2walkaltar()

        # self.mouse.move_minimap(-5,0)
        print('did not find bank, teleport again')
        self.did_not_find_bank += 1
        self.t_teleport()

pybot = AstralBot("mysuperbot")
# pybot.t_walkaltar2findaltar()
pybot.t_telebank2findbank()