import mouse
import keyboard
import json
import time
import pygetwindow as gw

# Store recorded actions
recorded_actions = []
start_time = None
recording = False

# Mouse movement handler (smooth tracking)
def on_move(event):
    if recording:
        timestamp = time.time() - start_time
        recorded_actions.append({
            "type": "mouse_move",
            "x": event.x,
            "y": event.y,
            "time": timestamp
        })

# Mouse click handler (left/right click)
def on_click(event):
    if recording and event.event_type in ["down", "up"]:
        timestamp = time.time() - start_time
        recorded_actions.append({
            "type": "mouse_click",
            "x": mouse.get_position()[0],
            "y": mouse.get_position()[1],
            "button": event.button,
            "pressed": event.event_type == "down",
            "time": timestamp
        })

# Keyboard press handler (ignores hotkeys)
def on_key(event):
    if recording and event.name not in ["f11", "f12", "f10"]:  # Ignore hotkeys
        timestamp = time.time() - start_time
        recorded_actions.append({
            "type": "keyboard",
            "key": event.name,
            "time": timestamp
        })

# Window switch handler
def on_window_switch(event):
    if recording:
        timestamp = time.time() - start_time
        window = gw.getActiveWindow()
        if window:
            recorded_actions.append({
                "type": "switch_window",
                "title": window.title,
                "time": timestamp
            })

# Start recording
def start_recording():
    global start_time, recording
    if recording:
        return
    recorded_actions.clear()
    start_time = time.time()
    recording = True
    mouse.hook(on_click)  # Capture clicks
    mouse.hook(on_move)   # Capture movements
    keyboard.hook(on_key) # Capture keys
    keyboard.hook(on_window_switch) # Capture window switches
    print("Recording started... Press F12 to stop.")

# Stop recording
def stop_recording():
    global recording
    if not recording:
        return
    recording = False
    mouse.unhook(on_click)
    mouse.unhook(on_move)
    keyboard.unhook(on_key)
    keyboard.unhook(on_window_switch)

    # Save to file
    with open("macro.json", "w") as f:
        json.dump(recorded_actions, f, indent=4)
    print("Recording saved.")

# Hotkey bindings
keyboard.add_hotkey("f11", start_recording)
keyboard.add_hotkey("f12", stop_recording)

print("Press F11 to start recording, F12 to stop.")
keyboard.wait("esc")  # Keep script running