# PlayStation 4, PlayStation 5, Vita and Nintendo Switch 2

ROMarr recognizes PS4 (ps4), PS5 (ps5) and PlayStation Vita (psvita).
These are acquisition and library organization targets. They do not add
browser emulation or turn ROMarr into software that runs on the console.

PS4 and PS5 accept complete .pkg files; Vita accepts .vpk, .pkg and intact
.zip packages. The shared .pkg extension does not identify the console:
select the platform explicitly. Search still needs a configured indexer or
source that actually provides compatible results. ROMarr supplies no keys,
licenses, firmware, or guaranteed source catalogue.

Use your existing download client and library importer. DAT verification is
only possible when a matching DAT is loaded; an imported file without a DAT
match remains unknown, never automatically verified. Console installation
and external playback depend on the user's own device and software.
Folder dumps, split packages, updates/DLC relationships and installation on
hardware are not implemented by these platform declarations.

## Nintendo Switch 2

Nintendo Switch 2 (switch-2) is separate from the Switch (switch). It
accepts .nup packages and imports them as they are; ROMarr does not split
or install them. Switch requests reject titles naming the Switch 2 or .nup;
Switch 2 requests reject NSP, XCI, NSZ and XCZ releases. A title naming only
"Switch" is still accepted for a Switch 2 request, as "Xbox" is for Xbox 360
and "PlayStation" for PS2, so check such results. TitleDB and the NSP/XCI
game-folder routing are Switch-only.
