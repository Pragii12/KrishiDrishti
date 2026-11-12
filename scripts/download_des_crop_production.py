"""Download district-wise crop Area, Production and Yield for UP from DES.

Source: Directorate of Economics & Statistics, Ministry of Agriculture,
"Area, Production & Yield (APY) Statistics" report at
https://data.desagri.gov.in/website/crops-apy-report-web (public, no login).
This is the official source behind the data.gov.in crop production dataset,
but it is updated further: 1997-98 to 2022-23.

The portal answers one report request with an HTML table. For every crop and
season we add its table rows, unchanged (numbers kept as text, e.g. "120,903.00"), to
    data/raw/des_crop_production/up_crop_production_1997_2022.csv
and record the request in manifest.csv.

Re-running skips crop/season requests already listed in manifest.csv.

Run from the repo root:
    python scripts/download_des_crop_production.py
"""

from __future__ import annotations

import csv
import html
import http.cookiejar
import re
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

FORM_URL = "https://data.desagri.gov.in/website/crops-apy-report-web"
REPORT_URL = "https://data.desagri.gov.in/report/crop/horizontal_crop_vertical_year"
OUTPUT_DIR = Path("data/raw/des_crop_production")
CSV_FILE = OUTPUT_DIR / "up_crop_production_1997_2022.csv"
MANIFEST = OUTPUT_DIR / "manifest.csv"
UP_STATE_CODE = "9"
START_YEAR, END_YEAR = "1997", "2022"  # 1997-98 to 2022-23
SEASONS = {"R": "Rabi", "K": "Kharif", "S": "Summer", "Y": "Whole Year", "A": "Autumn", "W": "Winter"}
RETRIES = 6

CSV_FIELDS = ["State", "District", "Year", "Crop", "Season",
              "Area (Hectare)", "Production (Tonnes)", "Yield (Tonne/Hectare)"]

opener = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))
HEADERS = {"User-Agent": "KrishiDrishti/1.0", "Referer": FORM_URL}


def fetch(url: str, data: bytes | None = None, extra: dict | None = None) -> str:
    request = Request(url, data=data, headers={**HEADERS, **(extra or {})})
    for attempt in range(1, RETRIES + 1):
        try:
            with opener.open(request, timeout=300) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception as error:  # network errors, timeouts, cut-off responses
            if attempt == RETRIES:
                raise RuntimeError(f"Gave up on {url}: {error}") from error
            pause = min(2 ** attempt, 120)
            print(f"    {error}; retrying in {pause}s...", flush=True)
            time.sleep(pause)
    raise AssertionError("Unreachable")


def read_form() -> tuple[str, dict[str, str]]:
    """Open the report page (sets the session cookie) and return (token, crops)."""
    page = fetch(FORM_URL)
    token = re.search(r'name="_token" value="([^"]+)"', page).group(1)
    select = re.search(r'id="fltrcrops".*?</select>', page, re.S).group(0)
    crops = {code: html.unescape(name).strip()
             for code, name in re.findall(r'<option value="(\d+)"[^>]*>([^<]*)', select)}
    return token, crops


def parse_rows(page: str, crop: str, season: str) -> list[dict]:
    """Read the report table. State and District cells span several rows."""
    page = re.sub(r"<!--.*?-->", "", page, flags=re.S)
    body = page.split("<tbody>", 1)[1] if "<tbody>" in page else ""
    rows, state, district = [], "", ""
    for tr in re.findall(r"<tr.*?</tr>", body, re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", td)).strip()
                 for td in re.findall(r"<td.*?</td>", tr, re.S)]
        if len(cells) < 4 or not re.fullmatch(r"\d{4} - \d{4}", cells[-4]):
            continue
        leading = cells[:-4]  # 0, 1 or 2 spanning cells: state and/or district
        if len(leading) == 2:
            state, district = leading
        elif len(leading) == 1:
            district = leading[0]
        year, area, production, yield_ = cells[-4:]
        rows.append({"State": state, "District": district, "Year": year,
                     "Crop": crop, "Season": season, "Area (Hectare)": area,
                     "Production (Tonnes)": production, "Yield (Tonne/Hectare)": yield_})
    return rows


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    done: set[tuple[str, str]] = set()
    if MANIFEST.exists():
        with MANIFEST.open(encoding="utf-8") as f:
            done = {(row["crop_code"], row["season"]) for row in csv.DictReader(f)}
    token, crops = read_form()
    print(f"Portal lists {len(crops)} crops.", flush=True)

    for code, crop in crops.items():
        for season_code, season in SEASONS.items():
            if (code, season) in done:
                continue
            form = urlencode({
                "_token": token,
                "reportformat": "horizontal_crop_vertical_year",
                "fltrstates[]": UP_STATE_CODE,
                "fltrcrops[]": code,
                "fltrseason[]": season_code,
                "fltrstartyear": START_YEAR,
                "fltrendyear": END_YEAR,
                "fltrrptformat": "scrview",
            }).encode()
            page = fetch(REPORT_URL, form, {"X-Requested-With": "XMLHttpRequest"})
            rows = parse_rows(page, crop, season)

            # Save rows first, then the manifest entry that marks the request done.
            new_csv = not CSV_FILE.exists()
            with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
                if new_csv:
                    writer.writeheader()
                writer.writerows(rows)
            new_manifest = not MANIFEST.exists()
            with MANIFEST.open("a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if new_manifest:
                    writer.writerow(["crop_code", "crop", "season", "rows"])
                writer.writerow([code, crop, season, len(rows)])

            if rows:
                print(f"{crop} / {season}: {len(rows):,} rows", flush=True)
            time.sleep(1)

    print(f"\nFinished. Rows are in {CSV_FILE}", flush=True)


if __name__ == "__main__":
    main()
