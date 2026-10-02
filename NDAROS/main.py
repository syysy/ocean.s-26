import serial
import serial.tools.list_ports
import time
import sys
import webbrowser
import subprocess
import atexit
import signal
import os

from Context import Context
from State import AlertState

# Détecter automatiquement le port série
def get_auto_port():
    ports = list(serial.tools.list_ports.comports())
    keywords = ["arduino", "ch340", "ch341", "ftdi", "usb serial", "usb-serial", "cdc"]
    
    # 1. Recherche ciblée par mot-clé
    for p in ports:
        desc = (p.description or "").lower()
        mfg = (p.manufacturer or "").lower()
        hwid = (p.hwid or "").lower()
        if any(kw in desc or kw in mfg or kw in hwid for kw in keywords):
            print(f"Port Arduino détecté : {p.device} ({p.description})")
            return p.device

    # 2. Repli sur le premier port disponible
    if ports:
        print(f"Port détecté par défaut : {ports[0].device} ({ports[0].description})")
        return ports[0].device

    print("Aucun port série détecté.", file=sys.stderr)
    return None

PORT = get_auto_port()
BAUD = 9600
TIMEOUT = 1

arduino = None

def cleanup():
    global arduino
    if arduino and arduino.is_open:
        print("Closing serial port...")
        arduino.close()

def signal_handler(sig, frame):
    cleanup()
    sys.exit(0)

atexit.register(cleanup)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def connect_arduino(port=PORT, baud=BAUD, timeout=TIMEOUT, retries=5):
    for attempt in range(retries):
        try:
            arduino = serial.Serial(port=port, baudrate=baud, timeout=timeout)
            time.sleep(2)  # Wait for Arduino to initialize
            return arduino
        except Exception as e:
            if attempt < retries - 1:
                print(f"Connection failed (attempt {attempt+1}/{retries}), retrying in 2s...", file=sys.stderr)
                time.sleep(2)
            else:
                print(f"Error opening serial port {port}: {e}", file=sys.stderr)
                return None

def open_browser_fullscreen():
    """Ouvrir le navigateur en fullscreen"""
    time.sleep(2)  # Attendre que Flask soit complètement prêt
    webbrowser.open("http://localhost:5000")
    time.sleep(1)
    # Forcer fullscreen (Linux avec F11)
    try:
        subprocess.run(['xdotool', 'key', 'F11'], timeout=2, capture_output=True)
    except Exception as e:
        print(f"Warning: Could not set fullscreen: {e}")

def main():
    global arduino
    try:
        arduino = connect_arduino()
        if not arduino:
            print("Could not connect to Arduino. Continuing anyway...", file=sys.stderr)
        
        context = Context(arduino) if arduino else None
        
        if not context:
            print("Cannot start without Arduino connection", file=sys.stderr)
            sys.exit(1)
        
        browser_thread = subprocess.Popen(['python', '-c', 
            'import time, webbrowser, subprocess; '
            'time.sleep(2); '
            'webbrowser.open("http://localhost:5000"); '
            'time.sleep(1); '
            'subprocess.run(["xdotool", "key", "F11"], capture_output=True)'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        context.execute()
        
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    finally:
        cleanup()

if __name__ == "__main__":
    main()