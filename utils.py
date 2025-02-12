import ctypes
import sys

# Check if script is running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Restart script as admin if not already
def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
