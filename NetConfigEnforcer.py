import os
import subprocess
import sys
import ctypes
import platform
import random 
from time import sleep

# --- Admin Functions ---
def is_admin():
    """Check administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() if platform.system() == 'Windows' else os.getuid() == 0
    except:
        return False

def run_as_admin():
    """Elevate privileges with UAC prompt"""
    if platform.system() == 'Windows':
        try:
            script = os.path.abspath(sys.argv[0])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}"', None, 1
            )
            sys.exit(0)
        except Exception as e:
            print(f"⛔ Elevation failed: {e}")
            sys.exit(1)

# --- Network Functions ---
def get_network_interfaces():
    """Get active network interfaces"""
    interfaces = []
    try:
        result = subprocess.run(
            ['netsh', 'interface', 'show', 'interface'],
            capture_output=True,
            text=True,
            check=True
        )
        
        for line in result.stdout.split('\n'):
            if 'Connected' in line and 'Dedicated' in line:
                parts = line.split('   ')
                if len(parts) >= 4:
                    interface = parts[-1].strip()
                    if interface:
                        interfaces.append(interface)
        
        return interfaces if interfaces else ['Ethernet']
    
    except subprocess.CalledProcessError as e:
        print(f"🔧 Interface detection error: {e.stderr}")
        return ['Ethernet']

def apply_manual_settings(interface):
    """Set static IP configuration"""
    try:
        last_octet = random.randint(100, 195) 
        ip_address = f"192.168.1.{last_octet}"
        
        print("\n⚙️ Applying static configuration...")
        commands = [
            ['netsh', 'interface', 'ip', 'set', 'address',
             f'name={interface}', 'source=static',
             f'addr={ip_address}', 'mask=255.255.255.0', 'gateway=192.168.1.254'],
            
            ['netsh', 'interface', 'ip', 'set', 'dns',
             f'name={interface}', 'source=static', 'addr=8.8.8.8', 'validate=no'],
            
            ['netsh', 'interface', 'ip', 'add', 'dns',
             f'name={interface}', 'addr=4.2.2.4', 'index=2', 'validate=no']
        ]
        
        for cmd in commands:
            subprocess.run(cmd, check=True)
            sleep(0.5)
        
        print("\n✅ Successfully applied:")
        print(f"IP: {ip_address}\nMask: 255.255.255.0\nGateway: 192.168.1.254") 
        print("DNS: 8.8.8.8, 4.2.2.4")
    
    except subprocess.CalledProcessError as e:
        print(f"⛔ Configuration failed: {e.stderr}")

def apply_automatic_settings(interface):
    """Enable DHCP configuration"""
    try:
        print("\n⚙️ Configuring DHCP...")
        commands = [
            ['netsh', 'interface', 'ip', 'set', 'address',
             f'name={interface}', 'source=dhcp'],
            
            ['netsh', 'interface', 'ip', 'set', 'dns',
             f'name={interface}', 'source=dhcp']
        ]
        
        for cmd in commands:
            subprocess.run(cmd, check=True)
            sleep(0.5)
        
        print("\n✅ DHCP configuration successful!")
    
    except subprocess.CalledProcessError as e:
        print(f"⛔ DHCP failed: {e.stderr}")

# --- UI Functions ---
def show_menu(interfaces, current_interface):
    """Display interactive menu"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("┌───────────────────────────────────┐")
    print("│      NETWORK CONFIG MANAGER       │")
    print("├───────────────────────────────────┤")
    print(f"│ Current Interface: {current_interface.ljust(15)}│")
    print("├───────────────────────────────────┤")
    print("│ 1. Set Static IP                 │")
    print("│ 2. Enable DHCP                   │")
    print("│ 0. Exit                          │")
    print("└───────────────────────────────────┘")
    return input("\nSelect option (0-2): ").strip()

# --- Main Program ---
def main():
    if not is_admin():
        print("\n🔒 Administrator privileges required!")
        if platform.system() == 'Windows':
            run_as_admin()
        else:
            print("🚫 Run with sudo/root privileges")
            sys.exit(1)
    
    interfaces = get_network_interfaces()
    if not interfaces:
        print("⚠️ No network interfaces found!")
        sys.exit(1)
    
    current_interface = interfaces[0]
    
    while True:
        try:
            choice = show_menu(interfaces, current_interface)
            
            if choice == '1':
                apply_manual_settings(current_interface)
            elif choice == '2':
                apply_automatic_settings(current_interface)
            elif choice == '0':
                print("\n👋 Goodbye!")
                break
            else:
                print("⛔ Invalid choice")
            
            input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n🚫 Operation cancelled")
            break
        except Exception as e:
            print(f"💥 Critical error: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💀 Fatal error: {str(e)}")
    finally:
        if platform.system() == 'Windows':
            input("Press Enter to exit...")
