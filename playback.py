import pyautogui
import keyboard
import json
import time
import os
import pygetwindow as gw
import sys

# Check if macro file exists
if not os.path.exists("macro.json") or os.stat("macro.json").st_size == 0:
    print("Error: No recorded macro found!")
    exit()

# Load recorded macro
with open("macro.json", "r") as f:
    recorded_actions = json.load(f)

# Function to switch to a specific window
def switch_to_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    if window:
        window[0].activate()
    else:
        print(f"Window with title '{window_title}' not found!")

# Loop control variables
loop_count = 0
max_loops = int(sys.argv[1]) if len(sys.argv) > 1 else 3  # Default to 3 loops if not provided
end_time = None
stop_looping = False

def set_end_time(duration):
    global end_time
    end_time = time.time() + int(duration)

def stop_loop():
    global stop_looping
    stop_looping = True

# Calculate total duration of all loops
total_duration = sum(action["time"] for action in recorded_actions) * max_loops

# Start playback loop
while not stop_looping:
    start_time = time.time()

    for action in recorded_actions:
        while time.time() - start_time < action["time"]:
            if stop_looping:
                break  # Exit inner loop if stop_looping is True
            pass  # Wait until it's time to execute

        if stop_looping:
            break  # Exit outer loop if stop_looping is True

        try:
            if action["type"] == "mouse_move":
                pyautogui.moveTo(action["x"], action["y"], duration=0.001, _pause=False)
            elif action["type"] == "mouse_click":
                pyautogui.click(action["x"], action["y"], button=action["button"])
            elif action["type"] == "keyboard":
                keyboard.press_and_release(action["key"])
            elif action["type"] == "switch_window":
                switch_to_window(action["title"])
            else:
                print(f"Unknown action type: {action['type']}")
        except Exception as e:
            print(f"Error executing action {action}: {e}")

    loop_count += 1
    remaining_loops = max_loops - loop_count
    print(f"Playback loop {loop_count} complete. {remaining_loops} remaining")

    if max_loops is not None and loop_count >= max_loops:
        break
    if end_time is not None and time.time() >= end_time:
        break

print("Playback stopped.")
