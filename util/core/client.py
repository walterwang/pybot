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
        inv_y = self.box['top'] + 223
        for column in range(7):
            for row in range(4):
                inv[inv_id] = [inv_x, inv_y]
                inv_x = inv_x + 37
                inv_id += 1
            inv_y = inv_y + 36
            inv_x = self.box['left'] + 552
        return inv

    def get_center(self):
        return (self.box['left'] + 254, self.box['top'] + 178)

    def get_client_box(self):
        return self.box




