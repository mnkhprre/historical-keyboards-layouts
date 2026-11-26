#!/usr/bin/env python3
"""Build dist/HistoricalKeyboards.bundle containing every layout in layouts.json.

macOS pairs Foo.keylayout with Foo.icns by file name, and reads per-layout
metadata from KLInfo_<layout name> keys in Info.plist."""
import plistlib
import shutil
import sys
from pathlib import Path

from common import ROOT, layout_files, load_config, parse_keylayout


def strings_file(pairs):
    body = "".join(f'"{k}" = "{v}";\n' for k, v in pairs)
    return body.encode("utf-16")  # with BOM, as macOS expects


def main(out_dir: Path):
    cfg = load_config()
    meta = cfg["bundle"]
    bundle = out_dir / meta["file"]
    if bundle.exists():
        shutil.rmtree(bundle)
    res = bundle / "Contents" / "Resources"
    res.mkdir(parents=True)

    info = {
        "CFBundleIdentifier": meta["identifier"],
        "CFBundleName": meta["name"],
        "CFBundleVersion": meta["version"],
        "CFBundleShortVersionString": meta["version"],
        "CFBundlePackageType": "BNDL",
    }
    en, tr = [], []
    for entry in cfg["layouts"]:
        kl, icns = layout_files(entry)
        name = parse_keylayout(kl).get("name")
        shutil.copy2(kl, res / kl.name)
        shutil.copy2(icns, res / icns.name)
        info[f"KLInfo_{name}"] = {
            "TISInputSourceID": f'{meta["identifier"]}.{entry["dir"]}',
            "TISIntendedLanguage": entry["language"],
        }
        en.append((name, name))
        tr.append((name, entry.get("tr", name)))

    with open(bundle / "Contents" / "Info.plist", "wb") as f:
        plistlib.dump(info, f)
    with open(bundle / "Contents" / "version.plist", "wb") as f:
        plistlib.dump({"BuildVersion": "1", "CFBundleVersion": meta["version"],
                       "ProjectName": meta["name"]}, f)
    for lang, pairs in (("en", en), ("tr", tr)):
        d = res / f"{lang}.lproj"
        d.mkdir()
        (d / "InfoPlist.strings").write_bytes(strings_file(pairs))

    print(f"built {bundle.relative_to(ROOT) if bundle.is_relative_to(ROOT) else bundle}"
          f" with {len(cfg['layouts'])} layouts")
    return bundle


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist")
