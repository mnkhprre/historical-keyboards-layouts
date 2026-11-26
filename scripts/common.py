"""Shared helpers for validate.py and build_bundle.py."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYOUTS = ROOT / "layouts"

# .keylayout files are XML 1.1 and contain control-character references
# (e.g. &#x0008; for backspace) that XML 1.0 parsers reject. Neutralise them
# before parsing; the source files are never modified.
_CTRL_REF = re.compile(r"&#(x0*[0-8bcef]|x0*1[0-9a-f]|0*(?:[0-8]|1[124-9]|2[0-9]|3[01]));", re.I)


def load_config():
    return json.loads((ROOT / "layouts.json").read_text(encoding="utf-8"))


def parse_keylayout(path: Path) -> ET.Element:
    text = path.read_text(encoding="utf-8")
    text = text.replace('<?xml version="1.1"', '<?xml version="1.0"', 1)
    text = re.sub(r"<!DOCTYPE[^>]*>", "", text, count=1)
    text = _CTRL_REF.sub("&#xFFFD;", text)
    return ET.fromstring(text.encode("utf-8"))


def layout_files(entry):
    d = LAYOUTS / entry["dir"]
    return d / f'{entry["dir"]}.keylayout', d / f'{entry["dir"]}.icns'
