import tomllib
import re
from pathlib import Path

def version_tuple(v: str):
    return tuple(int(x) for x in v.split('.'))


def test_requirements_in_sync():
    root = Path(__file__).resolve().parents[1]
    py = root / 'pyproject.toml'
    req = root / 'requirements.txt'
    py_data = tomllib.loads(py.read_text(encoding='utf-8'))
    deps = py_data['project']['dependencies']

    data = req.read_bytes()
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        text = data.decode('utf-16')
    pinned_lines = text.splitlines()
    pinned = {}
    for line in pinned_lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '==' in line:
            pkg, ver = line.split('==', 1)
            pinned[pkg.lower()] = ver

    for dep in deps:
        m = re.match(r'^([A-Za-z0-9_\-]+)(.+)$', dep)
        assert m, f"Impossible de parser la dépendance '{dep}'"
        name = m.group(1).lower()
        spec_str = m.group(2)
        assert name in pinned, f"{name} absent de requirements.txt"
        pv = version_tuple(pinned[name])
        for piece in spec_str.split(','):
            piece = piece.strip()
            if not piece:
                continue
            if piece.startswith('>='):
                cv = version_tuple(piece[2:])
                assert pv >= cv, f"{name}=={pinned[name]} ne satisfait pas '{piece}'"
            elif piece.startswith('>'):
                cv = version_tuple(piece[1:])
                assert pv > cv, f"{name}=={pinned[name]} ne satisfait pas '{piece}'"
            elif piece.startswith('<='):
                cv = version_tuple(piece[2:])
                assert pv <= cv, f"{name}=={pinned[name]} ne satisfait pas '{piece}'"
            elif piece.startswith('<'):
                cv = version_tuple(piece[1:])
                assert pv < cv, f"{name}=={pinned[name]} ne satisfait pas '{piece}'"
            else:
                # ignore other specifiers
                pass
