# TTY Art feed

A single‑page web app that turns vintage **RTTY/TTY art** into **AFSK WAV audio** you can play to a teletype, radio modem, or software decoder. It works fully offline with a bundled archive and includes SFW/NSFW filtering, art‑set selection, a per‑piece **MARK lead‑in** (to wake auto‑starts), and automatic WAV splitting by time/size.

> **Credit:** All artwork is sourced from the excellent [TEXTFILES.COM Artscene RTTY Collection](http://artscene.textfiles.com/rtty/COLLECTION/). Huge thanks to the collectors and curators who archived it.

> **Disclaimer:** This app aggregates third‑party art. Some pieces may be insensitive or politically incorrect. Best‑effort NSFW filtering is provided but **not guaranteed**; viewer discretion is advised. Views expressed in the artwork are those of the original creators and do not necessarily reflect the author’s views.

---

Live Demo:https://unluckyfett.github.io/TTY-ART-FEED/

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

## License & attribution

* UI code: © 2025 Frankie Caswell — Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
* Source artwork: © respective creators; archived at [TEXTFILES.COM](http://artscene.textfiles.com/). This project is unaffiliated and provided for historical/educational purposes only.

---

## Acknowledgements

Thanks to the vintage computing and radio communities keeping this history alive, and special thanks to the TEXTFILES.COM maintainers.
