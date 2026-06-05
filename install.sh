#!/bin/bash
# Install the Russian – Mnemonic keyboard layout for the current user.
# Default = bare .keylayout (most reliable; shows up under "Others").
# Pass --bundle to install the language-tagged bundle instead (enables
# Russian Dictation to follow the layout, but is pickier on some macOS builds).
set -e

HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/Library/Keyboard Layouts"
LAYOUT="Russian – Mnemonic.keylayout"
BUNDLE="Russian Mnemonic.bundle"

cd "$HERE"
python3 generate_keylayout.py
mkdir -p "$DEST"

# Always clear previous installs of either form to avoid duplicates/conflicts.
rm -f  "$DEST/$LAYOUT"
rm -rf "$DEST/$BUNDLE"

if [ "$1" = "--bundle" ]; then
  ./build_bundle.sh
  cp -R "$BUNDLE" "$DEST/"
  echo "Installed (bundle): $DEST/$BUNDLE"
else
  cp "$LAYOUT" "$DEST/"
  echo "Installed (single file): $DEST/$LAYOUT"
fi

echo
echo "Next steps:"
echo "  1. LOG OUT and back in (or reboot) — macOS only reloads layouts at login."
echo "  2. System Settings → Keyboard → Text Input → Input Sources → Edit… → +"
echo "     Search 'Mnemonic'. Single file = under 'Others'; bundle = under 'Russian'."
echo "  3. Switch input source with Ctrl+Space."
