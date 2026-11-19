# Map fix: CARTO API key patch

## The problem

The Map page shows black tiles reading **"API KEY REQUIRED · carto.com/basemaps/apikey"**.

NetzSec Loot draws its basemap from CARTO's raster tiles using a hardcoded, keyless URL:

```
https://{s}.basemaps.cartocdn.com/{dark_all|light_all|rastertiles/voyager}/{z}/{x}/{y}{r}.png
```

Since **25 September 2026**, CARTO only serves raster tiles to requests that carry a `?key=` parameter
([CARTO basemaps FAQ](https://docs.carto.com/faqs/carto-basemaps)). The app has no setting for a map key
(nothing in `zerotrace-settings.json` is read for it), and its source isn't published, so the fix has to be
applied to the installed binary.

## What the patch does

`patch-map-key.py` copies the binary and appends `?key=<your key>` to that one tile URL inside the embedded
frontend JavaScript. The embedded file can't change size, so the script frees the room in the same module by
rewriting a duplicated colour table into an equivalent form:

```js
k={Open:"#ef4444",WEP:"#f59e0b",WPA:"#eab308",WPA2:"#22c55e",WPA3:"#3b82f6",Other:"#9ca3af"}
k={...x,Other:"#9ca3af"}   // x already holds the first five entries; same object, same order
```

Leftover bytes become spaces. Safety checks:

- the input binary is never modified; output goes to a separate file
- each matched snippet must appear exactly once, in the expected order, inside one embedded file; otherwise it stops
- refuses an already-patched binary
- the key must be URL-safe characters only
- output is byte-for-byte identical except for the edited span, and the edited JavaScript is syntax-checked with `node --check` when Node.js is installed

## Usage (Linux)

1. Get a free key at <https://carto.com/basemaps/apikey>. Leave it **unrestricted**: website restrictions rely
   on a `Referer`, and the app's webview origin is not a normal web host.
2. Save the key on one line in `~/.config/NetzSec Loot/carto-key.txt`.
3. Run the patch (Python 3; Node.js optional for the syntax check):

   ```sh
   python3 -I patch-map-key.py
   ```

   Defaults: input `/usr/local/bin/netzsec-loot`, output
   `~/.local/share/netzsec-loot-patch/netzsec-loot.patched`. Override with `--input`, `--output`, `--key-file`.
4. Close NetzSec Loot, keep a backup, and install:

   ```sh
   cp /usr/local/bin/netzsec-loot ~/.local/share/netzsec-loot-patch/netzsec-loot.original
   sudo install -m 755 ~/.local/share/netzsec-loot-patch/netzsec-loot.patched /usr/local/bin/netzsec-loot
   ```

To undo, install the `.original` copy the same way.

## Notes

- **Updates remove the patch.** Re-run the script on the new binary. If the frontend code changed, the script
  stops with a "found 0" or "found 2" error rather than guessing.
- **Don't share the patched binary**: your key is embedded in it in plain text.
- `dpkg --verify` will report the binary as modified; that's expected.
- Tested on the Linux amd64 build, package version `0.0.0~dev.7a85d25-1`
  (original binary sha256 `b2273f6f0e2e8c971189a763b876179278e762a8881adac351120833558e23f6`).
  Windows and macOS builds are untested; the default paths are Linux-only.
- CARTO requires attribution ("© OpenStreetMap contributors, © CARTO"), which the app already shows.
  Free tier: up to 5M requests/month non-commercial, 1M commercial.
