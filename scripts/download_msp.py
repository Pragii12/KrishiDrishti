"""Download the official Minimum Support Price (MSP) statements from DES.

Source: Economics, Statistics & Evaluation Division, Ministry of Agriculture
(desagri.gov.in). Three published PDF statements are saved unchanged in
    data/raw/msp/
and listed in manifest.csv (title, url, file, bytes).

Re-running skips files that are already downloaded.

Run from the repo root:
    python scripts/download_msp.py
"""

from __future__ import annotations

import csv
from pathlib import Path
from urllib.request import Request, urlopen

OUTPUT_DIR = Path("data/raw/msp")
HEADERS = {"User-Agent": "Mozilla/5.0 KrishiDrishti/1.0"}
STATEMENTS = [
    ("MSP of Kharif and Rabi crops since 1995-96, marketing season-wise (RTI reply, 2026)",
     "https://desagri.gov.in/wp-content/uploads/2026/05/RTI-reply-of-Sandeep-Rathore.pdf"),
    ("MSP statement, marketing season-wise, as on 12.12.2025",
     "https://desagri.gov.in/wp-content/uploads/2025/12/MSP-Statement_English_As-on-12.12.2025.pdf"),
    ("MSP according to crop year, as on 22.01.2025",
     "https://desagri.gov.in/wp-content/uploads/2025/02/MSP_for-website_English-version.pdf"),
]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for title, url in STATEMENTS:
        target = OUTPUT_DIR / url.rsplit("/", 1)[-1]
        if not target.exists():
            with urlopen(Request(url, headers=HEADERS), timeout=120) as response:
                target.write_bytes(response.read())
        manifest.append([title, url, target.name, target.stat().st_size])
        print(f"{target.name} ({target.stat().st_size:,} bytes)", flush=True)

    with (OUTPUT_DIR / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "url", "file", "bytes"])
        writer.writerows(manifest)
    print(f"\nFinished. {len(manifest)} files are in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
