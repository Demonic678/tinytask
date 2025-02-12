import mouse

def on_click(event):
    print(f"Mouse Click: {event.button} at ({event.x}, {event.y})")

mouse.on_click(on_click)  # Listen for mouse clicks

print("Click anywhere. Press Ctrl+C to exit.")
mouse.wait()  # Keep script running
