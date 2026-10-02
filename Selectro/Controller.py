import cv2
import serial
import time
from screeninfo import get_monitors

# ===== CONFIGURATION =====
PORT = "/dev/cu.usbmodem1301"
BAUD = 9600

IMAGE_ACCUEIL = "Accueil.png"       # Étape 0 - écran d'accueil / idle

# Une image par étape
IMAGES = {
    "LED":  "Pompage.png",   # Étape 1 - LEDs eau
    "ATOM": "sel.png",   # Étape 2 - Brumificateur
    "LED2": "lampe.png",   # Étape 3 - Lampe
    "IDLE": None,                # Étape 0 - retour accueil
}

TIMEOUT_INACTIVITE = 300   # 5 minutes → retour écran d'accueil
MONITOR_INDEX = 1          # 0 = principal, 1 = secondaire


def main():
    # 1. Setup écran
    monitors = get_monitors()
    target = monitors[MONITOR_INDEX] if MONITOR_INDEX < len(monitors) else monitors[0]

    window_name = "Affichage_Permanent"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, target.x, target.y)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def load_and_resize(path):
        img = cv2.imread(path)
        if img is not None:
            return cv2.resize(img, (target.width, target.height))
        print(f"[WARN] Fichier introuvable : {path}")
        return None

    # Préchargement de toutes les images
    accueil_img = load_and_resize(IMAGE_ACCUEIL)
    step_images = {}
    for key, path in IMAGES.items():
        if path:
            step_images[key] = load_and_resize(path)
        else:
            step_images[key] = None 

    # Affichage écran d'accueil au démarrage
    if accueil_img is not None:
        cv2.imshow(window_name, accueil_img)

    ser = None
    last_activity_time = time.time()
    is_on_welcome_screen = True

    print("Système prêt. Écran d'accueil affiché. En attente de signal...")

    try:
        while True:
            # 2. Reconnexion série automatique
            if ser is None or not ser.is_open:
                try:
                    ser = serial.Serial(PORT, BAUD, timeout=0.1)
                    time.sleep(2)
                    ser.reset_input_buffer()
                    print("--- Connexion Arduino OK ---")
                except Exception:
                    time.sleep(1)
                    pass

            # 3. Lecture des commandes série
            if ser and ser.is_open:
                try:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8', errors='ignore').strip()
                        print(f"Signal reçu : {line}")

                        if line == "IDLE":
                            # Retour écran d'accueil immédiat
                            if accueil_img is not None:
                                cv2.imshow(window_name, accueil_img)
                            is_on_welcome_screen = True

                        elif line in step_images:
                            img = step_images[line]
                            if img is not None:
                                cv2.imshow(window_name, img)
                                last_activity_time = time.time()
                                is_on_welcome_screen = False
                            else:
                                # Fallback sur accueil si image manquante
                                if accueil_img is not None:
                                    cv2.imshow(window_name, accueil_img)
                                is_on_welcome_screen = True

                except (serial.SerialException, OSError):
                    print("Arduino déconnecté.")
                    if ser:
                        ser.close()
                    ser = None

            # 4. Timeout inactivité → retour accueil
            current_time = time.time()
            if not is_on_welcome_screen and (current_time - last_activity_time > TIMEOUT_INACTIVITE):
                print("Inactivité détectée : retour à l'écran d'accueil.")
                if accueil_img is not None:
                    cv2.imshow(window_name, accueil_img)
                is_on_welcome_screen = True

            # 5. Maintenance fenêtre (Échap pour quitter)
            if cv2.waitKey(30) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Fermeture...")
    finally:
        if ser:
            ser.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()