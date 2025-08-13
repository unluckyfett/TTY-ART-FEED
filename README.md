# TTY Art feed

A single‑page web app that turns vintage **RTTY/TTY art** into **AFSK WAV audio** you can play to a teletype, radio modem, or software decoder. It works fully offline with a bundled archive and includes SFW/NSFW filtering, art‑set selection, a per‑piece **MARK lead‑in** (to wake auto‑starts), and automatic WAV splitting by time/size.

> **Credit:** All artwork is sourced from the excellent [TEXTFILES.COM Artscene RTTY Collection](http://artscene.textfiles.com/rtty/COLLECTION/). Huge thanks to the collectors and curators who archived it.

> **Disclaimer:** This app aggregates third‑party art. Some pieces may be insensitive or politically incorrect. Best‑effort NSFW filtering is provided but **not guaranteed**; viewer discretion is advised. Views expressed in the artwork are those of the original creators and do not necessarily reflect the author’s views.

---

## Quick start (GitHub Pages)

Live Demo:https://unluckyfett.github.io/TTY-ART-FEED/

1. Put the app at the repo root:

   * `index.html` (the file in this repo)
   * `rtty_offline/` (folder; see below)
2. Enable **GitHub Pages** → *Settings → Pages* → deploy from the `main` branch.
3. Visit your Pages URL and click **Build WAV**.

> The app is completely client‑side. No server or APIs are required.

---

## Folder layout

```
repo/
├─ index.html                  # RTTY Art WAV Builder UI (this app)
└─ rtty_offline/
   ├─ manifest.json            # list of bundled artworks
   ├─ nsfw_list.json           # optional manual NSFW overrides
   ├─ ARTWORK-01/
   │  ├─ 000
   │  ├─ 001
   │  └─ ...
   ├─ ARTWORK-02/
   │  └─ ...
   └─ ... (up to ARTWORK-08)
```

### `manifest.json` formats

The app accepts **any** of these shapes:

**Simple array** (recommended):

```json
[
  "ARTWORK-01/000",
  "ARTWORK-01/001",
  "ARTWORK-02/045"
]
```

**Object with items (+optional base):**

```json
{
  "base": "rtty_offline",
  "items": ["ARTWORK-01/000", "ARTWORK-02/045"]
}
```

**Grouped by folder:**

```json
{
  "base": "rtty_offline",
  "ARTWORK-01": ["000","001"],
  "ARTWORK-02": ["045"]
}
```

All entries must match `ARTWORK-0[1-8]/[0-9][0-9][0-9]` and the files must exist in `rtty_offline/`.

### `nsfw_list.json` (optional)

SFW mode **always** excludes whole sets **ARTWORK‑04**, **ARTWORK‑07**, **ARTWORK‑08**. You can add specific files from any set to exclude in SFW by listing them here. Two accepted formats:

**JSON array**:

```json
["ARTWORK-01/123", "ARTWORK-05/007"]
```

**Plain text** (newline separated):

```
ARTWORK-01/123
ARTWORK-05/007
```

Place this file at: `rtty_offline/nsfw_list.json`. It’s optional; if missing, the app continues without overrides.

---

## Using the app

1. **Art set** – choose a collection (01–08) or **All**.
2. **Content filter** – SFW or NSFW. In SFW, sets 04/07/08 and any file in `nsfw_list.json` are excluded.
3. **Count** – how many artworks to include (randomized, de‑duplicated).
4. **Gap (min)** – silence between pieces.
5. **Mark lead‑in (sec)** – continuous MARK tone before each piece to wake auto‑starts (default 5s).
6. **AFSK** – Baud (default **45.45**), Mark/Space (default **2125/2295 Hz**), Stop Bits (default **1.5**).
7. **Time limits** – optional *Max minutes per item*, *Max minutes total* (default **1440**), and *Split every* (default **1440**). WAVs split to respect both your split size and RIFF limits.
8. Hit **Build WAV**. You’ll see a live **Preview** of normalized art and one or more WAV download links. The first segment auto‑loads into the player.

> Tip: The **Run self‑test** button validates Baudot mapping, AFSK streaming, CR→CRLF normalization, and WAV headers.

---

## Browser notes

* Audio generation uses the Web Audio sample rate when available; otherwise **48 kHz**.
* Modern desktop browsers recommended. Mobile works, but large WAVs may be memory‑heavy.
* Autoplay: browsers require a user gesture; clicking **Build WAV** satisfies this. The **Mark lead‑in** helps wake external decoders.

---

## Troubleshooting

* **“idle” forever / no downloads** → Check the browser console and ensure `rtty_offline/manifest.json` is reachable and has valid entries.
* **“No items to process”** → Your filters removed everything (e.g., SFW + restrictive Art set). Try NSFW or a different set/count.
* **Segments stop early** → You hit *Max minutes total*; increase it or reduce Count.
* **“Invalid array length” (very large builds)** → Reduce *Split every* minutes (creates more, smaller WAV files) and/or lower Count.
* **NSFW overrides not applied** → Confirm the path format (e.g., `ARTWORK-01/123`). Reload after editing `nsfw_list.json`.

---

## Developing / Updating content

You can populate `rtty_offline/` by hand (download from the archive) or with your own scripts. After adding/removing files, update `manifest.json` accordingly. No build step is required—the app loads the manifest at runtime.

If you host behind a CDN or different path, keep `manifest.json` in `rtty_offline/` so the app derives a correct base URL automatically.

---

## License & attribution

* UI code: © 2025 Frankie Caswell — Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
* Source artwork: © respective creators; archived at [TEXTFILES.COM](http://artscene.textfiles.com/). This project is unaffiliated and provided for historical/educational purposes only.

---

## Acknowledgements

Thanks to the vintage computing and radio communities keeping this history alive, and special thanks to the TEXTFILES.COM maintainers.
