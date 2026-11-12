"""Download district-wise irrigation and crop area data for UP from DES.

Source: Directorate of Economics & Statistics, Ministry of Agriculture,
Land Use Statistics "Grand Query" report at
https://data.desagri.gov.in/weblus/lus-grand-query-report (public, no login).

Three reports, each fetched once per agricultural year (1998-99 onwards):
    sources     net and gross irrigated area by source (canal, tank, tubewell, ...)
    crop_irr    irrigated area of every crop (and season, where reported)
    crop_area   area under every crop, net area sown, gross cropped area

The portal answers with an HTML table with nested column headers. In the crop
reports that header HTML is inconsistent (labels such as "Total" land under the
wrong column), so headers are stored exactly as printed instead of being
matched to columns here. For every request we save:
    data/raw/des_irrigation/html/<report>_<year>.html   the raw response
    data/raw/des_irrigation/<report>_values.csv         one row per district and
        year: State, District, Year, then col_001, col_002, ... in the portal's
        column order, values unchanged ("-" kept as "-")
    data/raw/des_irrigation/<report>_headers.csv        every header cell as
        printed, with its year, row, position, colspan and rowspan
Rows of a different shape (state totals) are not copied to the CSV; their count
is logged in manifest.csv and they remain in the raw HTML.

Re-running skips requests whose HTML file already exists.

Run from the repo root:
    python scripts/download_des_irrigation.py
"""

from __future__ import annotations

import csv
import html
import http.cookiejar
import re
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

FORM_URL = "https://data.desagri.gov.in/weblus/lus-grand-query-report"
REPORT_URL = "https://data.desagri.gov.in/lus/report/lus-grand-query"
OUTPUT_DIR = Path("data/raw/des_irrigation")
HTML_DIR = OUTPUT_DIR / "html"
UP_STATE_CODE = "9"
YEARS = range(1998, 2025)  # 1998-99 to 2024-25
RETRIES = 6

# The checkbox values the portal's own page sends when a whole section is
# ticked (captured from the page; ticking a box also ticks its parent chain,
# and the server needs all of them).
REPORTS = {
    "sources": {
        "fltrsourcemain[]": ["1", "4"],
        "fltrsourcesub[]": ["2", "11", "3", "12", "5", "17", "6", "18"],
        "fltrsourcechild[]": ["7", "8", "9", "10", "13", "14", "15", "16"],
        "fltrsourcechildtot[]": ["2", "3", "1", "5", "6", "4"],
    },
    "crop_irr": {
        "fltrcropemain[]": ["1", "2"],
        "fltrcropesub[]": ["7", "8", "9", "13", "15", "15", "14", "10", "21"],
        "fltrcrop[]": "1,3,4,5,6,2,7,8,13,14,10,62,66,44,38,39,40,41,42,12,47,43,71,51,52,53,54,55,56,57,58,50,59,45,48,49,60,61,9,15,16,17,18,24,23,25,26,27,28,29,30,34,35,36,33,63,37,31,32,64,65,69,11".split(","),
        "fltrcropseason[]": "1_K,1_R,1_A,1_W,1_S,3_K,3_R,3_S,8_K,8_R,8_S,10_K,10_R,10_S,60_K,60_R,60_Y".split(","),
        "fltrcroptotal[]": ["1", "3", "8", "10", "60"],
        "fltrcropesubtotal[]": ["7", "8", "9", "13", "14", "10"],
        "fltrcropefoodgrain[]": ["1"],
        "fltrsubsub[]": ["20", "19"],
        "fltrsubsubtotal[]": ["20", "19"],
        "fltrcropemaintotal[]": ["1", "11", "2", "irrigate"],
    },
    "crop_area": {
        "fltrundermain[]": ["1", "2", "croppedarea", "areamorethanone", "netareashown"],
        "fltrundersub[]": "7,8,9,13,15,14,10,11,16,12,21".split(","),
        "fltrundercrop[]": "1,3,4,5,6,2,7,8,13,14,10,62,66,38,39,40,41,42,12,47,43,71,51,52,53,54,55,56,57,58,50,59,45,46,48,49,60,9,15,19,16,17,18,24,22,21,23,20,25,26,27,28,29,30,67,68,34,63,35,36,31,32,33,37,64,65,69,70,11".split(","),
        "fltrundercropseason[]": "1_K,1_A,1_W,1_S,3_K,3_R,3_S,8_K,8_R,8_S,10_K,10_R,60_K,60_R,60_Y".split(","),
        "fltrundercroptotal[]": ["1", "3", "8", "10", "60"],
        "fltrundersubtotal[]": "7,8,9,13,15,14,10,11,16,12,21".split(","),
        "fltrunderextra[]": ["foodgrain", "fruitvegitable"],
        "fltrundersubsub[]": ["20", "19"],
        "fltrundersubsubtotal[]": ["20", "19"],
        "fltrundermaintotal[]": ["1", "2"],
    },
}

HEADER_FIELDS = ["year", "header_row", "position", "text", "colspan", "rowspan"]
MANIFEST_FIELDS = ["report", "year", "data_rows", "value_columns", "other_rows_skipped"]

opener = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))
HEADERS = {"User-Agent": "KrishiDrishti/1.0", "Referer": FORM_URL, "X-Requested-With": "XMLHttpRequest"}


def fetch(url: str, data: bytes | None = None) -> str:
    request = Request(url, data=data, headers=HEADERS)
    for attempt in range(1, RETRIES + 1):
        try:
            with opener.open(request, timeout=600) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception as error:  # network errors, timeouts, cut-off responses
            if attempt == RETRIES:
                raise RuntimeError(f"Gave up on {url}: {error}") from error
            pause = min(2 ** attempt, 120)
            print(f"    {error}; retrying in {pause}s...", flush=True)
            time.sleep(pause)
    raise AssertionError("Unreachable")


def cell_text(cell: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", cell))).strip()


def parse(page: str) -> tuple[list[list[str]], list[list[str]], int]:
    """Return (header cells as printed, district data rows, number of other rows).

    Header cells: [header_row, position, text, colspan, rowspan].
    Data rows: [State, District, Year, value, value, ...], the most common row
    shape in the table body (one row per district).
    """
    page = re.sub(r"<style.*?</style>|<!--.*?-->", "", page, flags=re.S)
    thead = re.search(r"<thead.*?</thead>", page, re.S)
    tbody = re.search(r"<tbody.*?</tbody>", page, re.S)
    if not thead or not tbody:
        return [], [], 0

    headers = []
    for r, tr in enumerate(re.findall(r"<tr.*?</tr>", thead.group(0), re.S), start=1):
        for p, (attrs, inner) in enumerate(re.findall(r"<th([^>]*)>(.*?)</th>", tr, re.S), start=1):
            colspan = (re.search(r'colspan="?(\d+)', attrs) or [None, "1"])[1]
            rowspan = (re.search(r'rowspan="?(\d+)', attrs) or [None, "1"])[1]
            headers.append([str(r), str(p), cell_text(inner), colspan, rowspan])

    body = [[cell_text(td) for td in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
            for tr in re.findall(r"<tr.*?</tr>", tbody.group(0), re.S)]
    body = [cells for cells in body if cells]
    if not body:
        return headers, [], 0
    width = Counter(len(cells) for cells in body).most_common(1)[0][0]
    rows = [cells for cells in body if len(cells) == width and len(cells) >= 4]
    return headers, rows, len(body) - len(rows)


def append_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    page = fetch(FORM_URL)
    token = re.search(r'id="hdnrltoken"[^>]*value="([^"]+)"', page).group(1)

    for report, boxes in REPORTS.items():
        values_file = OUTPUT_DIR / f"{report}_values.csv"
        headers_file = OUTPUT_DIR / f"{report}_headers.csv"
        for year in YEARS:
            raw_file = HTML_DIR / f"{report}_{year}.html"
            if raw_file.exists():
                continue
            form = {
                "btnValue": "2", "fltrdatatype": "district_data", "fltrreporttype": "horizontal_year",
                "fltrstates[]": [UP_STATE_CODE], "fltrdistricts[]": ["all"],
                "fromfltryear": str(year), "tofltryear": str(year),
                "units": "1", "unittxt": "Hectare", "fltrrptformat": "scrview",
                "_token": token, **boxes,
            }
            page = fetch(REPORT_URL, urlencode(form, doseq=True).encode())
            headers, rows, skipped = parse(page)
            value_columns = len(rows[0]) - 3 if rows else 0

            # Save the CSVs first, then the raw HTML: an existing HTML file means "done".
            # A year can have a different number of columns, so every row is padded
            # to the widest layout seen so far (new columns go in a new header row).
            append_csv(headers_file, HEADER_FIELDS, [[f"{year}-{year + 1}", *h] for h in headers])
            append_csv(values_file, ["State", "District", "Year"] + [f"col_{i:03d}" for i in range(1, 400)],
                       [cells + [""] * (402 - len(cells)) for cells in rows])
            append_csv(OUTPUT_DIR / "manifest.csv", MANIFEST_FIELDS,
                       [[report, f"{year}-{year + 1}", str(len(rows)), str(value_columns), str(skipped)]])
            raw_file.write_text(page, encoding="utf-8")
            print(f"{report} {year}-{year + 1}: {len(rows)} district rows, {value_columns} value columns, "
                  f"{skipped} other rows", flush=True)
            time.sleep(1)

    # Drop trailing col_ columns that are empty in every row (formatting only).
    for report in REPORTS:
        values_file = OUTPUT_DIR / f"{report}_values.csv"
        with values_file.open(encoding="utf-8") as f:
            table = list(csv.reader(f))
        used = max(max((i for i, v in enumerate(row) if v != ""), default=0) for row in table[1:]) + 1
        with values_file.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(row[:used] for row in table)

    print(f"\nFinished. Files are in {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    main()
