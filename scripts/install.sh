#!/usr/bin/env bash
# Build the bundle and install it for the current user.
# Usage: scripts/install.sh            install
#        scripts/install.sh --uninstall remove
set -euo pipefail
cd "$(dirname "$0")/.."
DEST="$HOME/Library/Keyboard Layouts"
BUNDLE="HistoricalKeyboards.bundle"

if [[ "${1:-}" == "--uninstall" ]]; then
  rm -rf "$DEST/$BUNDLE"
  echo "Removed $DEST/$BUNDLE. Log out and back in to finish."
  exit 0
fi

python3 scripts/validate.py
python3 scripts/build_bundle.py
mkdir -p "$DEST"
rm -rf "$DEST/$BUNDLE"
cp -R "dist/$BUNDLE" "$DEST/"
echo "Installed to $DEST/$BUNDLE"
echo "Log out and back in, then add the layouts in System Settings > Keyboard > Input Sources (under 'Others')."
