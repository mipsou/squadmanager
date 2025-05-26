#!/usr/bin/env python3
"""
Bootstrap pour déverrouiller et lancer squadmanager sans verrou de fichiers.
Usage : python bootstrap_run.py
"""
import sys
import subprocess
import logging, os

# Configuration du logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bootstrap.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)

def kill_processes(names):
    logging.info(f"Tentative de suppression des processus: {names}")
    try:
        import psutil
    except ImportError:
        logging.error("Le module psutil est manquant. pip install psutil")
        sys.exit(1)
    for proc in psutil.process_iter(['name']):
        if proc.info.get('name') in names:
            logging.info(f"Arrêt du process {proc.info.get('name')} (PID {proc.pid})")
            try:
                proc.terminate()
                logging.info(f"Process {proc.pid} arrêté")
            except Exception as e:
                logging.error(f"Erreur en tuant {proc.pid}: {e}")

try:
    from elevate import elevate
except ImportError:
    print("pip install elevate pour UAC")
    sys.exit(1)

def main():
    logging.info("Élévation des privilèges via UAC")
    elevate()
    logging.info("Suppression des processus verrouillant")
    kill_processes(['squadmanager.exe', 'uv.exe', 'uvicorn.exe'])
    logging.info("Réinstallation du projet en mode editable")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], check=True)
    logging.info("Lancement de squadmanager run --once")
    subprocess.run([sys.executable, '-m', 'squadmanager.cli', 'run', '--once'], check=True)
    logging.info(f"Bootstrap terminé. Consultez le log ici : {log_file}")

if __name__ == '__main__':
    main()
