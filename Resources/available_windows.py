from Xlib.display import Display


display = Display()
root = display.screen().root
children = root.query_tree().children
for w in children:
    print(w.get_wm_name())