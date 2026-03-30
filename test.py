import socket
import tkinter as tk
import pyautogui
import keyboard
import os
import threading
import time

# ------------- CMD BANNER -------------
os.system("cls")
print(r"""
██████╗  █████╗ ██████╗ ██╗  ██╗███╗   ██╗███████╗████████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝████╗  ██║██╔════╝╚══██╔══╝
██████╔╝███████║██████╔╝█████╔╝ ██╔██╗ ██║█████╗     ██║   
██╔══██╗██╔══██║██╔══██╗██╔═██╗ ██║╚██╗██║██╔══╝     ██║   
██║  ██║██║  ██║██║  ██║██║  ██╗██║ ╚████║███████╗   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   

                ★ DARKNET REMOTE LOCK SYSTEM ★
            [Auto-Restart Mode - Continuous Operation]
""")

# ------------- SETTINGS -------------
PORT = 9095
UNLOCK_PIN = "1234"

pyautogui.FAILSAFE = False

# Global variables
is_locked = False
lock_window = None
server_running = True
lock_thread = None

# ------------------------------------
def unlock_keys():
    """Unblock all keys"""
    try:
        keyboard.unblock_all_keys()
    except:
        pass

def lock_screen():
    global is_locked, lock_window
    
    # Double check to prevent double lock
    if is_locked:
        print("\n[DarkNet] ⚠ System already locked!")
        return
    
    is_locked = True
    
    # Block keys
    keys = ["alt", "tab", "alt+tab", "win", "ctrl+esc", "alt+f4"]
    for k in keys:
        try:
            keyboard.block_key(k)
        except:
            pass

    win = tk.Tk()
    lock_window = win
    win.attributes("-fullscreen", True)
    win.attributes("-topmost", True)
    win.configure(bg="black")
    win.overrideredirect(True)

    title = tk.Label(
        win,
        text="DarkNet LOCKED SYSTEM",
        fg="red", bg="black",
        font=("Arial", 40, "bold")
    )
    title.pack(pady=20)

    label = tk.Label(
        win, text="ENTER PIN TO UNLOCK",
        fg="white", bg="black",
        font=("Arial", 30)
    )
    label.pack(pady=30)

    entry = tk.Entry(win, show="*", font=("Arial", 30))
    entry.pack()
    
    status = tk.Label(
        win, text="", fg="yellow", bg="black",
        font=("Arial", 16)
    )
    status.pack(pady=10)

    def check():
        global is_locked
        if entry.get() == UNLOCK_PIN:
            win.destroy()
            is_locked = False
            unlock_keys()
            print("\n[DarkNet] ✅ System UNLOCKED locally!")
        else:
            status.config(text="❌ WRONG PIN! Try again")
            entry.delete(0, tk.END)
            entry.focus()
    
    def remote_unlock(pin):
        global is_locked
        if pin == UNLOCK_PIN:
            win.destroy()
            is_locked = False
            unlock_keys()
            return True
        return False
    
    win.remote_unlock = remote_unlock

    btn = tk.Button(win, text="UNLOCK", font=("Arial", 30), command=check)
    btn.pack(pady=30)
    
    entry.bind('<Return>', lambda e: check())
    win.protocol("WM_DELETE_WINDOW", lambda: None)

    print("\n[DarkNet] 🔒 System LOCKED!")
    win.mainloop()
    
    # Cleanup after window closes
    is_locked = False
    lock_window = None
    unlock_keys()
    print("\n[DarkNet] 🔓 System UNLOCKED!")
    print("[DarkNet] ✅ Server ready for next LOCK command!")

def remote_unlock_with_pin(pin):
    """Remote unlock using PIN"""
    global is_locked, lock_window
    
    print(f"[DarkNet] Remote unlock attempt - Current locked state: {is_locked}")
    
    if not is_locked:
        return "ALREADY_UNLOCKED"
    
    if pin == UNLOCK_PIN:
        if lock_window:
            try:
                if hasattr(lock_window, 'remote_unlock'):
                    if lock_window.remote_unlock(pin):
                        # Wait a bit for window to close
                        time.sleep(0.5)
                        return "UNLOCKED"
                else:
                    unlock_system()
                    return "UNLOCKED"
            except Exception as e:
                print(f"[DarkNet] Remote unlock error: {e}")
                unlock_system()
                return "UNLOCKED"
        else:
            unlock_system()
            return "UNLOCKED"
    else:
        return "WRONG_PIN"

def unlock_system():
    """Unlock system remotely"""
    global is_locked, lock_window
    
    if lock_window:
        try:
            lock_window.destroy()
        except:
            pass
    
    is_locked = False
    lock_window = None
    unlock_keys()
    
    print("\n[DarkNet] 🔓 System UNLOCKED remotely!")
    print("[DarkNet] ✅ Server ready for next LOCK command!")

def get_status():
    """Get current status"""
    return "LOCKED" if is_locked else "UNLOCKED"

# ---------------- SOCKET LISTENER ----------------
def start_server():
    global server_running, is_locked
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", PORT))
        sock.listen(5)
        
        print(f"\n[DarkNet] ✅ Server running on port {PORT}")
        print(f"[DarkNet] 🔑 Unlock PIN: {UNLOCK_PIN}")
        print("\n[DarkNet] 📡 Available commands:")
        print("   LOCK                    - Lock system")
        print("   UNLOCK_PIN:<pin>        - Unlock with PIN")
        print("   STATUS                  - Check status")
        print("\n[DarkNet] 🔄 AUTO-RESTART MODE ACTIVE:")
        print("   • After unlock, server continues running")
        print("   • Lock again anytime without restart")
        print("   • LOCK → UNLOCK → LOCK → UNLOCK (infinite)")
        print(f"\n[DarkNet] 📊 Current Status: {get_status()}")
        print("\n[DarkNet] ⏳ Waiting for commands...\n")
        print("="*60)
        
        while server_running:
            try:
                conn, addr = sock.accept()
                data = conn.recv(1024).decode().strip()
                
                print(f"\n[DarkNet] 📨 Received: {data} from {addr[0]}")
                print(f"[DarkNet] 📊 Current Status before command: {get_status()}")
                
                # LOCK command
                if data == "LOCK":
                    if is_locked:
                        conn.send(b"ALREADY_LOCKED")
                        print("[DarkNet] ⚠ System already locked!")
                    else:
                        conn.send(b"LOCKING")
                        print("[DarkNet] 🔒 Locking system...")
                        # Start lock screen in new thread
                        new_lock_thread = threading.Thread(target=lock_screen, daemon=True)
                        new_lock_thread.start()
                
                # UNLOCK with PIN command
                elif data.startswith("UNLOCK_PIN:"):
                    pin = data.split(":")[1] if ":" in data else ""
                    print(f"[DarkNet] 🔑 Unlock attempt with PIN: {pin}")
                    result = remote_unlock_with_pin(pin)
                    conn.send(result.encode())
                    if result == "UNLOCKED":
                        print("[DarkNet] ✅ System unlocked remotely!")
                        print("[DarkNet] ✅ Ready for next LOCK command")
                    elif result == "WRONG_PIN":
                        print("[DarkNet] ❌ Wrong PIN attempted!")
                    elif result == "ALREADY_UNLOCKED":
                        print("[DarkNet] ℹ System already unlocked!")
                
                # STATUS command
                elif data == "STATUS":
                    status = get_status()
                    conn.send(status.encode())
                    print(f"[DarkNet] 📊 Status: {status}")
                
                else:
                    conn.send(b"UNKNOWN_COMMAND")
                    print(f"[DarkNet] ❓ Unknown command: {data}")
                
                print(f"[DarkNet] 📊 Current Status after command: {get_status()}")
                conn.close()
                
            except Exception as e:
                print(f"[DarkNet] ⚠ Error: {e}")
                try:
                    conn.close()
                except:
                    pass
                    
    except Exception as e:
        print(f"[DarkNet] ❌ Server error: {e}")
    finally:
        try:
            sock.close()
        except:
            pass

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n[DarkNet] 🛑 Server stopped by user")
        server_running = False
        unlock_keys()