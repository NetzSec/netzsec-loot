# NetzSec Loot

<img alt="NetzSec Loot desktop app" src="https://github.com/user-attachments/assets/78107705-ba36-4904-ac86-09c11bf8d7bc" />

<p align="center">
  <img alt="Platforms" src="https://img.shields.io/badge/windows%20%C2%B7%20macOS%20%C2%B7%20linux-supported-555?style=for-the-badge">
  <img alt="Privacy" src="https://img.shields.io/badge/no%20accounts%20%C2%B7%20no%20logs-100%25%20local-4f46e5?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-4f46e5?style=for-the-badge">
</p>

A **free, offline** desktop app that turns the raw output of ESP32 pentest firmwares — **Marauder, Bruce, Ghost ESP, nyanBOX, OUI-SPY** — into validated, mapped, searchable intelligence. Point it at an SD card or folder and it checks every capture, throws out the junk, and makes the good stuff usable — no matter which firmware produced it. No account, no cloud, no telemetry.

> **➡️ [Download the latest version](https://github.com/NetzSec/netzsec-loot/releases/latest)**

---

## What it does

The problem: ESP32 firmwares are great at *capturing*, but they leave behind a chaotic SD card of `.pcap`, WiGLE `.csv`, `.hc22000`, `.sub`/`.ir`/`.nfc`, GPS logs and text logs — and half of them are silently broken. NetzSec Loot is the desktop tool that makes sense of it all.

- **🩺 Capture Doctor** — validates every file the moment you import it, and tells you *why* a file is bad (0-byte, corrupt, wrong format) instead of silently failing.
- **📶 Networks** — every Wi-Fi network across every capture, **deduplicated by BSSID** and enriched with the real **manufacturer** (built-in 52k-vendor OUI database), signal, channel, band and GPS. Filter, favorite, tag and export any slice.
- **📱 Devices** — client stations seen probing, with vendor lookup and automatic **randomized-MAC detection**.
- **🔑 Handshakes** — PMKID + EAPOL captures with real network names and a ready-to-paste **hashcat** command.
- **🔓 Cracked** — import a hashcat potfile; see recovered passwords with **strength analysis** and **reuse detection**.
- **📡 Signals** — Sub-GHz (frequency/band/protocol), IR (button counts) and NFC with the **tag technology decoded** (Mifare Classic, NTAG, DESFire…).
- **🗺️ Wardrive map** — a dark map plotting geolocated networks, colored by encryption, with per-security layer toggles.
- **📊 Analytics** — vendors, channels, bands, SSIDs, encryption/security posture, timelines, duplicates and auto-insights.
- **🧰 File tools** — dedupe/clean wordlists, merge or split big files, and merge multiple WiGLE CSVs into one clean log.
- **📤 Export** — WiGLE CSV, KML, CSV, JSON, HTML reports and combined `.hc22000` for cracking.
- **🔒 100% local** — no accounts, no telemetry, nothing leaves your machine. Every operation asks before it reads or writes a file.

---

## Supported firmwares & formats

| Firmwares | Capture formats |
| --- | --- |
| ESP32 Marauder · Bruce · Ghost ESP · nyanBOX · OUI-SPY | `.pcap` · `.pcapng` · WiGLE `.csv` · `.hc22000` · `.gpx` · `.nmea` · `.sub` · `.ir` · `.nfc` · logs |

NetzSec Loot **prepares and hands off** — it validates, organizes, maps and exports your captures for tools like hashcat. It is not a device flasher or a live device controller.

---

## Download & Install

All builds are published on the **[Releases page](https://github.com/NetzSec/netzsec-loot/releases)** — no compiling required.

1. Open the [latest release](https://github.com/NetzSec/netzsec-loot/releases/latest).
2. Download the installer for your OS:
   - **Windows** — `.exe`
   - **macOS** — `./netzec-loot`
   - **Linux** — `./netzec-loot` / `.deb` / `.rpm`
3. Run it and launch **NetzSec Loot**.
4. **Library → Import folder** and point it at your SD card or capture folder.

### Notes per platform
- **Windows** — SmartScreen may warn on first launch; choose *More info → Run anyway*.
- **macOS** — first launch: right-click the app → *Open* to bypass Gatekeeper.
- **Linux** — make the AppImage executable: `chmod +x NetzSec-Loot-*.AppImage`.

---

## Requirements

- Windows 10/11, macOS 12+, or a modern Linux distribution.
- Some capture files to work with (an SD card from an ESP32 device, or any folder of captures).
- No device, no internet connection, and no account required.

---

## Privacy

NetzSec Loot is privacy-first by design. Everything runs and stays **on your machine** — no accounts, no telemetry, no logs leaving your device, no cloud sync. The only network request the app ever makes is loading map tiles on the Map page.

---

## License

Released under the **[MIT License](LICENSE)**.

Bundled/third-party data and dependencies keep their own licenses — see **[THIRD_PARTY.md](THIRD_PARTY.md)** (notably the MAC-address vendor database and the open-source libraries this app is built on). **NetzSec** and **ZeroTrace** names and logos are trademarks and are **not** covered by the MIT license.

---

## Links & Support

- 📦 [Releases](https://github.com/NetzSec/netzsec-loot/releases)
- 🐞 [Report an issue](https://github.com/NetzSec/netzsec-loot/issues)
- 📱 NetzSec suite — *ZeroTrace is the hardware line; the ESP32 tools these captures come from.*

<sub>Free · local-only · no telemetry.</sub>
