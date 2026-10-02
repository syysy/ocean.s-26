# ocean.s-26
Source code of the Ocean.s-26 projects


# ICreate — Installation Désalinisation

## Prérequis
- Python 3.x
- make
- Arduino UNO branché en USB 
- port HDMI connecté à l'écran 
- Cable alimentaion atomiseur connecté (Cable rouge)

## Installation
```bash
make install
```

Crée le venv et installe `opencv-python`, `pyserial`, `screeninfo`.

## Lancement
```bash
make run
```

## Arrêt / Nettoyage
```bash
make clean
```

- Tue tous les processus occupant `/dev/cu.usbmodem*`
- Arrête `Controller.py`
- Supprime le venv

## Structure
```
Icreate/
├── Controller.py       # Script principal
├── Makefile
├── Accueil.png         # Écran d'accueil
├── Pompage.png         # Phase 1 — LED
├── sel.png             # Phase 2 — ATOM
├── lampe.png           # Phase 3 — LED2
├── arduino/
│   └── main.ino
└── venv/
```

## Dépannage

**Port série occupé** → `make clean` puis `make run`

**Mauvais port** → modifier `PORT` dans `Controller.py` (`/dev/cu.usbmodem1301` ou `1201`)

**Moniteur non détecté** → modifier `MONITOR_INDEX = 0` dans `Controller.py`