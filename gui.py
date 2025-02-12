import tkinter as tk
import subprocess
import utils
import keyboard
import time  # Import the time module
import json
import os

recording_process = None
playback_process = None
window_titles = ["Roblox Game 1", "Roblox Game 2", "Roblox Game 3", "Roblox Game 4"]
max_loops = 10
end_time = None

# Run as admin
if not utils.is_admin():
    utils.run_as_admin()

# Load recorded actions
if os.path.exists("macro.json") and os.stat("macro.json").st_size != 0:
    with open("macro.json", "r") as f:
        recorded_actions = json.load(f)
else:
    recorded_actions = []

# Start or stop recording
def toggle_recording():
    global recording_process
    if recording_process is None:
        recording_process = subprocess.Popen(["python", "record.py"])
        start_button.config(text="Recording... (Press F11 to Stop)", state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
    else:
        recording_process.terminate()
        recording_process = None
        start_button.config(text="Start Recording", state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

# Play or stop macro
def toggle_playback():
    global playback_process
    if playback_process is None:
        playback_process = subprocess.Popen(["python", "playback.py", str(max_loops)])
        play_button.config(text="Playing... (Press F10 to Stop)", state=tk.DISABLED)
        stop_play_button.config(state=tk.NORMAL)
    else:
        playback_process.terminate()
        playback_process = None
        play_button.config(text="Play Macro", state=tk.NORMAL)
        stop_play_button.config(state=tk.DISABLED)

# Settings window
def open_settings():
    settings = tk.Toplevel(root)
    settings.title("Settings")
    settings.geometry("300x200")

    tk.Label(settings, text="Hotkeys:").pack()
    tk.Label(settings, text="F11 - Start/Stop Recording").pack()
    tk.Label(settings, text="F10 - Play/Stop Macro").pack()

    tk.Label(settings, text="Loop Count:").pack()
    loop_count_entry = tk.Entry(settings)
    loop_count_entry.insert(0, str(max_loops))  # Default to current max_loops
    loop_count_entry.pack()

    # Calculate total duration of all loops
    def calculate_total_duration():
        if recorded_actions:
            total_seconds = max(action["time"] for action in recorded_actions) * max_loops
        else:
            total_seconds = 0
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)} hours {int(minutes)} minutes {seconds:.2f} seconds"

    total_duration_label = tk.Label(settings, text=f"Total Duration: {calculate_total_duration()}")
    total_duration_label.pack()

    def apply_settings():
        global max_loops, end_time
        loop_count = loop_count_entry.get()
        if loop_count:
            max_loops = int(loop_count)
            total_duration_label.config(text=f"Total Duration: {calculate_total_duration()}")
        print(f"Settings applied: max_loops={max_loops}")

    apply_button = tk.Button(settings, text="Apply", command=apply_settings)
    apply_button.pack()

    for i, title in enumerate(window_titles):
        tk.Label(settings, text=f"Window {i+1} Title:").pack()
        entry = tk.Entry(settings)
        entry.insert(0, title)
        entry.pack()
        entry.bind("<FocusOut>", lambda e, i=i: update_window_title(i, e.widget.get()))

def update_window_title(index, title):
    window_titles[index] = title

# Bind hotkeys to GUI
keyboard.add_hotkey("f11", toggle_recording)
keyboard.add_hotkey("f10", toggle_playback)

root = tk.Tk()
root.title("Macro Recorder")

# Buttons
start_button = tk.Button(root, text="Start Recording", command=toggle_recording)
start_button.pack()

stop_button = tk.Button(root, text="Stop Recording", command=toggle_recording, state=tk.DISABLED)
stop_button.pack()

play_button = tk.Button(root, text="Play Macro", command=toggle_playback)
play_button.pack()

stop_play_button = tk.Button(root, text="Stop Playback", command=toggle_playback, state=tk.DISABLED)
stop_play_button.pack()

settings_button = tk.Button(root, text="Settings", command=open_settings)
settings_button.pack()

root.mainloop()
