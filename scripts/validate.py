#!/usr/bin/env python3
"""Check every layout listed in layouts.json: files exist, XML parses,
ids and names are unique, and no stray layout folders are left unlisted."""
import sys
from collections import Counter

from common import LAYOUTS, layout_files, load_config, parse_keylayout

errors = []
cfg = load_config()
ids, names = Counter(), Counter()

for entry in cfg["layouts"]:
    kl, icns = layout_files(entry)
    if not kl.exists():
        errors.append(f"missing {kl.relative_to(LAYOUTS.parent)}")
        continue
    if not icns.exists():
        errors.append(f"missing {icns.relative_to(LAYOUTS.parent)}")
    try:
        root = parse_keylayout(kl)
    except Exception as e:  # noqa: BLE001
        errors.append(f"{kl.name}: XML parse error: {e}")
        continue
    if root.tag != "keyboard":
        errors.append(f"{kl.name}: root element is <{root.tag}>, expected <keyboard>")
        continue
    kid, name = root.get("id", ""), root.get("name", "")
    if not kid.lstrip("-").isdigit() or int(kid) >= 0:
        errors.append(f"{kl.name}: id {kid!r} must be a negative integer")
    if name != name.strip() or not name:
        errors.append(f"{kl.name}: name {name!r} is empty or has stray whitespace")
    ids[kid] += 1
    names[name] += 1
    print(f"ok  {entry['dir']:<22} id={kid:<7} name={name}")

errors += [f"duplicate id {k}" for k, n in ids.items() if n > 1]
errors += [f"duplicate name {k!r}" for k, n in names.items() if n > 1]

listed = {e["dir"] for e in cfg["layouts"]}
for d in LAYOUTS.iterdir():
    if d.is_dir() and d.name not in listed:
        errors.append(f"layouts/{d.name} is not listed in layouts.json")

if errors:
    print("\n".join("ERR " + e for e in errors), file=sys.stderr)
    sys.exit(1)
print(f"{len(listed)} layouts valid")
