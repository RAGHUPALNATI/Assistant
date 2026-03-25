import ctypes
import os
import platform

def lock_pc():
    """
    Locks the workstation.
    Supported on Windows, macOS, and some Linux distributions.
    """
    system = platform.system()
    
    try:
        if system == "Windows":
            # Direct Windows API call (equivalent to Win + L)
            ctypes.windll.user32.LockWorkStation()
            print("PC Locked (Windows)")
            return True
            
        elif system == "Darwin": # macOS
            # Using AppleScript to lock or sleep screen
            os.system('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend')
            print("System Locked (macOS)")
            return True
            
        elif system == "Linux":
            # Common Linux lock commands (Desktop dependent)
            commands = [
                'xdg-screensaver lock',
                'gnome-screensaver-command -l',
                'dbus-send --type=method_call --dest=org.gnome.ScreenSaver /org/gnome/ScreenSaver org.gnome.ScreenSaver.Lock',
                'loginctl lock-session'
            ]
            for cmd in commands:
                if os.system(cmd) == 0:
                    print(f"System Locked (Linux via {cmd})")
                    return True
            return False
            
    except Exception as e:
        print(f"Failed to lock PC: {e}")
        return False
    
    return False
