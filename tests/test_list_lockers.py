import os
import sys
import psutil

def test_module_not_locked():
    """
    Vérifie qu'aucun processus ne verrouille le module md.cp311-win_amd64.pyd
    """
    target = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..',
        '.venv', 'Lib', 'site-packages',
        'charset_normalizer', 'md.cp311-win_amd64.pyd'
    ))
    lockers = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.pid == os.getpid():
            continue
        try:
            for m in proc.memory_maps():
                if target.lower() in m.path.lower():
                    lockers.append((proc.pid, proc.name()))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    assert not lockers, f"Le module est encore chargé par: {lockers}"
