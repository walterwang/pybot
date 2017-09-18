from ewmh import EWMH


class Client(object):

    def __init__(self, client_name = "osbuddy"):
        if client_name == "osbuddy":
            self.win_offset_x = 18
            self.win_offset_y = 48
        self.ewmh = EWMH()
        self.box = self.set_box(self.ewmh)
        self.client_name = client_name
        self.inv = self.get_inventory()
        self.center = self.get_center()
        self.lunarmagic = self.get_lunarmagic()
        self.bankspace = self.get_bankcoord()
        self.invbox= self.get_invbox()

    def frame(self, client, ewmh):
        frame = client
        while frame.query_tree().parent != ewmh.root:
            frame = frame.query_tree().parent
        return frame

    def set_box(self, ewmh):
        wins = ewmh.getClientList()
        box = {}
        for client in wins:
            if "OSBuddy" in str(ewmh.getWmName(client)):
                ewmh.setActiveWindow(client)
                ewmh.display.flush()
                frame_data = self.frame(client, self.ewmh).get_geometry()._data
                box['top'] = frame_data['y'] + self.win_offset_y
                box['left'] = frame_data['x'] + self.win_offset_x
                box['width'] = 512
                box['height'] = 333
                return box

    def get_inventory(self):
        inv = {}
        inv_id = 0
        inv_x = self.box['left'] + 575
        inv_y = self.box['top'] + 230
        for column in range(7):
            for row in range(4):
                inv[inv_id] = [inv_x, inv_y]
                inv_x = inv_x + 41
                inv_id += 1
            inv_y = inv_y + 36
            inv_x = inv_x -164
        return inv
    def get_lunarmagic(self):
        lunarmagic = {}
        lunar_id = 0
        lunarx=self.box['left'] + 563
        lunary=self.box['top'] + 221
        for column in range(8):
            for row in range(6):
                lunarmagic[lunar_id] = [lunarx, lunary]
                lunarx = lunarx + 30
                lunar_id += 1
            lunary = lunary + 35
            lunarx = lunarx - 150
        return lunarmagic

    def get_bankcoord(self):
        bankspace = {}
        bank_id = 0
        bankx=self.box['left'] + 84
        banky=self.box['top'] + 95
        for column in range(6):
            for row in range(8):
                bankspace[bank_id] = [bankx, banky]
                bankx = bankx + 48
                bank_id += 1
            banky = banky + 37
            bankx = bankx - 336
        return bankspace

    def get_center(self):
        return (self.box['left'] + 254, self.box['top'] + 178)

    def get_client_box(self):
        return self.box

    def get_invbox(self):
        invbox = {}
        invbox['top'] = self.box['top'] +206
        invbox['left'] = self.box['left'] +550
        invbox['width'] = 175
        invbox['height'] = 255
        return invbox
if __name__ == '__main__':
    osclient = Client()
    print(osclient.lunarmagic)