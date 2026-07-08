# Third-party notices

NetzSec Loot is licensed under the [MIT License](LICENSE). It builds on
open-source libraries (listed in `go.mod` and `frontend/package.json`, each under
its own permissive MIT / BSD / ISC license) and bundles the two things below,
which keep their own terms.

The **NetzSec** and **ZeroTrace** names and logos are trademarks and are not
covered by the MIT license.

## MAC-address vendor database — `backend/loot/oui.txt`
Resolves manufacturers from MAC addresses, offline. Derived from the public
IEEE MA-L (OUI) registry (<https://regauth.standards.ieee.org/>), in the
`nmap-mac-prefixes` form produced by the Nmap Project
(<https://nmap.org/> · Nmap Public Source License).

## Map tiles
The Map page loads basemap tiles from **CARTO**
(<https://carto.com/attributions>); map data is **© OpenStreetMap contributors**,
under the ODbL (<https://www.openstreetmap.org/copyright>). This attribution is
shown on the map.
