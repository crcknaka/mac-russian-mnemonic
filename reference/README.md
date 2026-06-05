# Reference data / Исходные данные

These files are the **source of truth** for the key mapping — the exact Windows
"Russian - Mnemonic" layout, dumped from `kbdrum.dll` (version 10.0.25393.1).

- `kbdrum.klc` — Microsoft Keyboard Layout Creator text dump (UTF-8 converted).
- `kbdrum.xml` — structured XML dump of the same layout.

Both were obtained from **[kbdlayout.info/kbdrum](https://kbdlayout.info/kbdrum/)**,
which generates them from the original `KBDTABLES` in Microsoft's `kbdrum.dll`.
They are included here only as a factual reference for reproducing the mapping.
The underlying layout is © Microsoft Corporation.

`generate_keylayout.py` in the repo root encodes this same mapping as a data
model and emits the macOS `.keylayout`.
