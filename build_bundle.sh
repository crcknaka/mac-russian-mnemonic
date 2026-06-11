#!/bin/bash
# Build a keyboard-layout BUNDLE that tags the layout as Russian (ru) so that
# macOS lists it under "Russian" and Dictation/voice typing can follow it.
#
# Structure mirrors known-working bundles (Ukelele / kirelagin). The two things
# that commonly make a bundle NOT appear in Input Sources:
#   * CFBundleIdentifier MUST contain ".keyboardlayout." (not ".keylayout.")
#   * a version.plist + en.lproj/InfoPlist.strings should be present
set -e

HERE="$(cd "$(dirname "$0")" && pwd)"
LAYOUT="Russian – Mnemonic.keylayout"
LAYOUT_NAME="Russian – Mnemonic"           # MUST match <keyboard name=...>
BUNDLE="Russian Mnemonic.bundle"
BID="com.local.keyboardlayout.RussianMnemonic"   # note: .keyboardlayout.

cd "$HERE"
[ -f "$LAYOUT" ] || python3 generate_keylayout.py

rm -rf "$BUNDLE"
mkdir -p "$BUNDLE/Contents/Resources/en.lproj"
cp "$LAYOUT" "$BUNDLE/Contents/Resources/"

# Menu-bar icon: an .icns named exactly like the layout is picked up by macOS.
ICON="${LAYOUT_NAME}.icns"
if [ -f "$ICON" ]; then
  cp "$ICON" "$BUNDLE/Contents/Resources/"
  echo "Included icon: $ICON"
else
  echo "No $ICON found — bundle will use the default text badge."
fi

cat > "$BUNDLE/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleIdentifier</key>
	<string>${BID}</string>
	<key>CFBundleName</key>
	<string>Russian Mnemonic</string>
	<key>CFBundleVersion</key>
	<string>1.0</string>
	<key>KLInfo_${LAYOUT_NAME}</key>
	<dict>
		<key>TISInputSourceID</key>
		<string>${BID}</string>
		<key>TISIntendedLanguage</key>
		<string>ru</string>
		<!-- Makes "Use Caps Lock to switch to and from ABC" available with just
		     this layout + an ABC/Latin one. macOS only sets the per-source
		     CapsLock-switch flag (read by LoadKeyboardLayoutXML from this
		     KLInfo dict) when this key is true; without it the layout is not a
		     valid non-Latin switch partner and the option never appears. -->
		<key>TICapsLockLanguageSwitchCapable</key>
		<true/>
	</dict>
</dict>
</plist>
PLIST

cat > "$BUNDLE/Contents/version.plist" <<'VPLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>ProjectName</key>
	<string>Russian Mnemonic</string>
	<key>SourceVersion</key>
	<string>1.0</string>
	<key>BuildVersion</key>
	<string>1</string>
</dict>
</plist>
VPLIST

printf '"%s" = "%s";\n' "$LAYOUT_NAME" "$LAYOUT_NAME" \
  > "$BUNDLE/Contents/Resources/en.lproj/InfoPlist.strings"

plutil -lint "$BUNDLE/Contents/Info.plist"
plutil -lint "$BUNDLE/Contents/version.plist"
echo "Built $BUNDLE"
