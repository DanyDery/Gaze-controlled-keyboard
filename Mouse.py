from pynput import mouse

# pynput.mouse import Button, Controller

# mouse = Controller()  # init class for work with mouse
# mouse.position = (20, 10) # new coordinate
# mouse.move(20, 10) # refresh coordinate

# mouse.press(Button.left)  # press and hold lmb
# mouse.release(Button.left)  # let go lmb

# mouse.click(Button.left, 1)  # press 1 time lmb
# mouse.click(Button.left, 2)  # press 2 time lmb

# Button.left
# Button.right
# Button.middle

def on_move(x, y):
    print(x, y)


def on_click(x, y, button, pressed):
    pressed_status = 'Pressed' if pressed else 'Released'
    print(x, y, pressed_status, button)


# collect events until the stream ends
with mouse.Listener(
        on_move=on_move,
        on_click=on_click) as listener:
    listener.join()

# run the method to track the mouse
listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click)
listener.start()