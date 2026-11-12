"""Download the official Cost of Cultivation / Production files from DES.

Source: Economics, Statistics & Evaluation Division, Ministry of Agriculture,
"Archive Cost of Cultivation/Production & Related Data" at
https://desagri.gov.in/document-report-category/cost-of-cultivation-production-related-data-archive/
(public, no login). The page lists one document per year through a year filter.

Every file offered for a single crop year is saved unchanged in
    data/raw/cost_of_cultivation/
and listed in manifest.csv (year, title, url, file, bytes).

Re-running skips files that are already downloaded.

Run from the repo root:
    python scripts/download_cost_of_cultivation.py
"""

from __future__ import annotations

import csv
import html
import re
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PAGE_URL = "https://desagri.gov.in/document-report-category/cost-of-cultivation-production-related-data-archive/"
AJAX_URL = "https://desagri.gov.in/wp-admin/admin-ajax.php"
OUTPUT_DIR = Path("data/raw/cost_of_cultivation")
HEADERS = {"User-Agent": "Mozilla/5.0 KrishiDrishti/1.0", "X-Requested-With": "XMLHttpRequest", "Referer": PAGE_URL}
DATA_FILE = re.compile(r"\.(xls|xlsx|csv)$", re.I)


def fetch(url: str, data: bytes | None = None) -> bytes:
    with urlopen(Request(url, data=data, headers=HEADERS), timeout=120) as response:
        return response.read()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    page = fetch(PAGE_URL).decode("utf-8", "replace")
    select_tag = re.search(r'<select[^>]*id="year_filter_sess"[^>]*>', page).group(0)
    category = re.search(r'data-cat="(\d+)"', select_tag).group(1)
    options = re.findall(r'<option[^>]*value="(\d+)"[^>]*>([^<]*)', page.split(select_tag, 1)[1].split("</select>", 1)[0])

    manifest = []
    for value, label in options:
        label = label.strip()
        if not re.fullmatch(r"\d{4}-\d{2}", label):  # single crop years only
            continue
        form = urlencode({"action": "yearFilter", "year_sess_catId": value, "cat_id": category,
                          "tax_id": "document-report-category"}).encode()
        listing = fetch(AJAX_URL, form).decode("utf-8", "replace")
        for row in re.findall(r"<tr.*?</tr>", listing, re.S):
            cells = re.findall(r"<td.*?</td>", row, re.S)
            links = [u for u in re.findall(r'href="([^"]+)"', row) if DATA_FILE.search(u)]
            if not cells or not links:
                continue
            title = html.unescape(re.sub(r"<[^>]+>|\s+", " ", cells[0])).strip()
            for url in links:
                url = url.replace("http://", "https://")
                target = OUTPUT_DIR / url.rsplit("/", 1)[-1]
                if not target.exists():
                    target.write_bytes(fetch(url))
                    time.sleep(1)
                manifest.append([label, title, url, target.name, target.stat().st_size])
                print(f"{label}: {target.name} ({target.stat().st_size:,} bytes)", flush=True)
        time.sleep(0.5)

    with (OUTPUT_DIR / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["crop_year", "title", "url", "file", "bytes"])
        writer.writerows(sorted(manifest))
    print(f"\nFinished. {len(manifest)} files are in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
