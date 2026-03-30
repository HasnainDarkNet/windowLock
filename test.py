import socket
import tkinter as tk
import pyautogui
import keyboard
import os
import threading
import time
import random
import string

# ------------- CMD BANNER -------------
os.system("cls")
print(r"""
██████╗  █████╗ ██████╗ ██╗  ██╗███╗   ██╗███████╗████████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝████╗  ██║██╔════╝╚══██╔══╝
██╝  ██ ██ ██║█ █████╔╝█████╔╝ ██╔██╗ ██║█████╗     ██║   
██╔══██╗██╔══██║██╔══██╗██╔═██╗ ██║╚██╗██║██╔══╝     ██║   
██████║ ██║  ██║  ██║██║  ██║██║  ██╗██║ ╚████║███████╗   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   

                ★ DARKNET REMOTE LOCK SYSTEM ★
            [Hacker Mode - Matrix Style Animation]
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
animation_running = False

# ------------------------------------
def unlock_keys():
    """Unblock all keys"""
    try:
        keyboard.unblock_all_keys()
    except:
        pass

def matrix_animation(canvas, width, height):
    """Matrix code rain animation"""
    global animation_running
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    drops = [0] * (width // 20)
    font_size = 16
    
    def draw():
        if not animation_running:
            return
        canvas.delete("matrix")
        for i in range(len(drops)):
            char = random.choice(chars)
            x = i * 20 + 10
            y = drops[i] * font_size + 10
            if y < height:
                color = "#0f0" if random.random() > 0.7 else "#0a0"
                canvas.create_text(x, y, text=char, fill=color, font=("Courier", font_size, "bold"), tags="matrix")
                if random.random() > 0.95:
                    drops[i] = 0
                else:
                    drops[i] += 1
            else:
                drops[i] = 0
        canvas.after(50, draw)
    
    draw()

def glitch_effect(canvas, text_widget, count=0):
    """Glitch effect on text"""
    if not animation_running:
        return
    if count < 10:
        colors = ["red", "green", "yellow", "cyan", "magenta", "white"]
        if count % 2 == 0:
            text_widget.config(fg=random.choice(colors))
            canvas.config(bg="black")
        else:
            text_widget.config(fg="#0f0")
        canvas.after(100, glitch_effect, canvas, text_widget, count + 1)

def type_animation(label, text, index=0):
    """Typing animation effect"""
    if not animation_running:
        return
    if index < len(text):
        label.config(text=text[:index+1])
        label.after(50, type_animation, label, text, index+1)

def hacker_animation(win):
    """Full hacker animation on lock screen"""
    global animation_running
    animation_running = True
    
    # Create canvas for matrix rain
    canvas = tk.Canvas(win, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    # Glowing title
    title = tk.Label(
        canvas,
        text="⚠ SYSTEM BREACHED ⚠",
        fg="#0f0", bg="black",
        font=("Courier", 36, "bold")
    )
    title.place(relx=0.5, rely=0.15, anchor="center")
    
    # Subtitle with typing animation
    subtitle = tk.Label(
        canvas,
        text="",
        fg="#0f0", bg="black",
        font=("Courier", 18)
    )
    subtitle.place(relx=0.5, rely=0.25, anchor="center")
    type_animation(subtitle, ">>> REMOTE LOCK ACTIVE <<<")
    
    # Matrix rain
    width = win.winfo_screenwidth()
    height = win.winfo_screenheight()
    matrix_animation(canvas, width, height)
    
    # Hacker ASCII Art
    hacker_art = """
    ╔══════════════════════════════════════════════════════════╗
    ║  [*] TARGET: LOCALHOST                                   ║
    ║  [*] STATUS: LOCKED                                      ║
    ║  [*] ENCRYPTION: AES-256                                 ║
    ║  [*] FIREWALL: ACTIVE                                    ║
    ║  [*] INTRUSION DETECTION: ENABLED                        ║
    ║  [*] BACKDOOR: DEPLOYED                                  ║
    ╚══════════════════════════════════════════════════════════╝
    """
    
    ascii_label = tk.Label(
        canvas,
        text=hacker_art,
        fg="#0f0", bg="black",
        font=("Courier", 12)
    )
    ascii_label.place(relx=0.5, rely=0.4, anchor="center")
    
    # PIN Entry Frame with glow
    pin_frame = tk.Frame(canvas, bg="black")
    pin_frame.place(relx=0.5, rely=0.65, anchor="center")
    
    pin_label = tk.Label(
        pin_frame,
        text="[ ENTER UNLOCK KEY ]",
        fg="#0f0", bg="black",
        font=("Courier", 20, "bold")
    )
    pin_label.pack()
    
    entry = tk.Entry(
        pin_frame,
        show="*", 
        font=("Courier", 24),
        bg="black",
        fg="#0f0",
        insertbackground="#0f0",
        width=15,
        justify="center"
    )
    entry.pack(pady=10)
    entry.focus()
    
    status = tk.Label(
        pin_frame,
        text="",
        fg="#ff0", bg="black",
        font=("Courier", 14)
    )
    status.pack()
    
    # Glitch effect
    glitch_effect(canvas, title)
    
    return entry, status

def lock_screen():
    global is_locked, lock_window, animation_running
    
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
    
    # Start hacker animation
    entry, status = hacker_animation(win)
    
    def check():
        global is_locked, animation_running
        if entry.get() == UNLOCK_PIN:
            animation_running = False
            win.destroy()
            is_locked = False
            unlock_keys()
            print("\n[DarkNet] ✅ System UNLOCKED locally!")
        else:
            status.config(text="[!] ACCESS DENIED [!]")
            entry.delete(0, tk.END)
            entry.focus()
            # Flash effect
            for _ in range(3):
                status.config(fg="red")
                win.update()
                time.sleep(0.1)
                status.config(fg="#ff0")
                win.update()
                time.sleep(0.1)
    
    def remote_unlock(pin):
        global is_locked, animation_running
        if pin == UNLOCK_PIN:
            animation_running = False
            win.destroy()
            is_locked = False
            unlock_keys()
            return True
        return False
    
    win.remote_unlock = remote_unlock
    
    # Custom button with hacker style
    btn = tk.Button(
        win,
        text="[ UNLOCK ]",
        font=("Courier", 20, "bold"),
        command=check,
        bg="black",
        fg="#0f0",
        activebackground="#0a0",
        activeforeground="white",
        bd=2,
        relief="groove"
    )
    btn.place(relx=0.5, rely=0.85, anchor="center")
    
    entry.bind('<Return>', lambda e: check())
    win.protocol("WM_DELETE_WINDOW", lambda: None)
    
    print("\n[DarkNet] 🔒 System LOCKED! [HACKER MODE ACTIVE]")
    win.mainloop()
    
    # Cleanup
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
    global is_locked, lock_window, animation_running
    
    if lock_window:
        try:
            animation_running = False
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
                        print("[DarkNet] 🔒 Locking system... [HACKER MODE]")
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
