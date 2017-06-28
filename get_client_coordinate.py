from contextlib import contextmanager
import Xlib
import Xlib.display

# Connect to the X server and get the root window
disp = Xlib.display.Display()
root = disp.screen().root

NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')  # UTF-8
WM_NAME = disp.intern_atom('WM_NAME')

last_seen = { 'xid': None, 'title': None }


@contextmanager

def _get_window_name_inner(win_obj):
    """Simplify dealing with _NET_WM_NAME (UTF-8) vs. WM_NAME (legacy)"""

    for atom in (NET_WM_NAME, WM_NAME):
        try:


            window_size = win_obj.translate_coords(disp.screen().root, 0, 0)

            print(window_size)
            #height: 536 width: 765


            window_name = win_obj.get_full_property(atom, 0)


        except UnicodeDecodeError:  # Apparently a Debian distro package bug
            title = "<could not decode characters>"
        else:
            if window_name:
                win_name = window_name.value
                if isinstance(win_name, bytes):
                    # Apparently COMPOUND_TEXT is so arcane that this is how
                    # tools like xprop deal with receiving it these days
                    win_name = win_name.decode('latin1', 'replace')
                return win_name
            else:
                title = "<unnamed window>"

    return "{} (XID: {})".format(title, win_obj.id)

