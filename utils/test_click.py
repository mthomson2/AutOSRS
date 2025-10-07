from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at (X: {x}, Y: {y})")

# Start listening for mouse events
with mouse.Listener(on_click=on_click) as listener:
    listener.join()