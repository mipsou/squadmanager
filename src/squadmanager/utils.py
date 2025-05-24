import requests


def auto_detect_studio_url(ports=None):
    """Detecte localement un service CrewAI Studio sur localhost."""
    ports = ports or [8000, 8080, 3000, 5000]
    for port in ports:
        try:
            resp = requests.get(f"http://localhost:{port}/api/status", timeout=0.5)
            if resp.ok:
                return f"http://localhost:{port}"
        except requests.RequestException:
            pass
    return None


def parse_spec(text: str) -> dict:
    """
    Parse un cahier des charges en sections structurées.
    Sections commencées par un titre '# SectionName'.
    Retourne un dict section -> contenu texte.
    """
    result = {}
    current_key = None
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('#'):
            if current_key is not None:
                result[current_key] = '\n'.join(lines).strip()
            current_key = stripped.lstrip('#').strip()
            lines = []
        else:
            if current_key is None:
                continue
            if stripped == '':
                continue
            lines.append(line)
    if current_key is not None:
        result[current_key] = '\n'.join(lines).strip()
    return result
