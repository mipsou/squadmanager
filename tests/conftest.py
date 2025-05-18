import sys
from pathlib import Path

# Purge old 'dreamteam' paths to avoid conflits d'import
sys.path[:] = [p for p in sys.path if p and 'dreamteam' not in p.lower()]
# Add src directory to sys.path en première position
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
