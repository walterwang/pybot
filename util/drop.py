import util.core.mouse as mouse
import time

def drop_item(inv_id, inv):
    ix, iy =inv[inv_id]
    mouse.mclick_abs(ix, iy, click='right')
    time.sleep(0.3)
    mouse.mclick_abs(ix, iy + 42)