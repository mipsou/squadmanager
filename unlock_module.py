#!/usr/bin/env python3
"""
Script pour débloquer le module verrouillé md.cp311-win_amd64.pyd en élevant les privilèges via UAC.
Usage :
  pip install psutil elevate
  python unlock_module.py
"""
import os
import sys

# Monte en privilèges (UAC)
try:
    from elevate import elevate
except ImportError:
    print("Merci d'installer le package 'elevate' (pip install elevate)")
    sys.exit(1)
elevate()

try:
    import psutil
except ImportError:
    print("Merci d'installer le package 'psutil' (pip install psutil)")
    sys.exit(1)

# Chemin absolu du module à débloquer
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(SCRIPT_DIR, '.venv', 'Lib', 'site-packages',
                      'charset_normalizer', 'md.cp311-win_amd64.pyd')

print(f"Recherche des processus verrouillant : {TARGET}")
lockers = []
for proc in psutil.process_iter(['pid', 'name']):
    try:
        for m in proc.memory_maps():
            if m.path and TARGET.lower() in m.path.lower():
                lockers.append((proc.pid, proc.name()))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

if not lockers:
    print("Aucun processus ne verrouille le module.")
    sys.exit(0)

print("Processus à tuer :")
for pid, name in lockers:
    print(f"  - {name} (PID {pid})")
    try:
        p = psutil.Process(pid)
        p.terminate()
    except Exception as e:
        print(f"Erreur en tuant PID {pid}: {e}")

print("Opération terminée.")
