"""Download historical daily mandi (market) prices for UP crops from data.gov.in.

Source: "Variety-wise Daily Market Prices Data of Commodity" (Agmarknet),
one row per market per day per variety. Prices are INR per quintal.
Rows are saved exactly as the API returns them, with every API column.

Why district-by-district: the API does not keep a fixed row order between
requests, so paging through hundreds of thousands of rows returns some pages
twice and skips others. Small slices (one crop in one district), sorted by
date, need only a few pages. Each slice is checked: the number of distinct
rows must equal the API's total, otherwise the slice is fetched again.

Agmarknet renamed six of the commodities on 5 November 2025. Rows before that
date carry the old name and rows after it the new one, so both are downloaded
(see RENAMED below).

Output:
    data/raw/mandi_prices/<commodity>/<District>.csv   one file per slice
    data/raw/mandi_prices/manifest.csv                 check result per slice

Re-running skips slices that are already saved, so it is safe after a failure.

Run in PowerShell from the repo root:
    $env:DATA_GOV_IN_API_KEY = "your-personal-api-key"
    python scripts/download_mandi_prices.py
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

RESOURCE_ID = "35985678-0d79-46b4-9ed6-6f13308a1d24"
BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"
OUTPUT_DIR = Path("data/raw/mandi_prices")
MANIFEST = OUTPUT_DIR / "manifest.csv"
STATE = "Uttar Pradesh"
PAGE_SIZE = 5_000
RETRIES = 10        # per request: the server and home internet both drop out
SLICE_ATTEMPTS = 4  # per slice: re-fetch if pages came back repeated

# Commodity names exactly as Agmarknet spells them.
# Paddy (not Rice) is what farmers sell. Sugarcane is skipped: it is sold to
# mills at a state-fixed price (SAP), so mandi data barely exists for it.
COMMODITIES = [
    "Wheat",
    "Paddy(Dhan)(Common)",
    "Maize",
    "Mustard",
    "Potato",
    "Bengal Gram(Gram)(Whole)",
    "Arhar (Tur/Red Gram)(Whole)",
    "Barley (Jau)",
    "Lentil (Masur)(Whole)",
    "Bajra(Pearl Millet/Cumbu)",
    "Black Gram (Urd Beans)(Whole)",
    "Green Gram (Moong)(Whole)",
    "Peas(Dry)",  # the pulse; "Peas Wet"/"Green Peas" are fresh vegetable peas
    "Sesamum(Sesame,Gingelly,Til)",
    "Jowar(Sorghum)",
]

# Old name -> the names Agmarknet has used for the same commodity since 5 November 2025.
# Several new names differ from the old one only by a space, so a new name is saved in
# "<folder of the old name>__renamed_<n>" and never overwrites the old files.
RENAMED = {
    "Paddy(Dhan)(Common)": ["Paddy(Common)"],
    "Arhar (Tur/Red Gram)(Whole)": ["Arhar(Tur/Red Gram)(Whole)", "Red gram/Arhar/Tur(whole)"],
    "Barley (Jau)": ["Barley(Jau)"],
    "Lentil (Masur)(Whole)": ["Lentil(Masur)(Whole)"],
    "Black Gram (Urd Beans)(Whole)": ["Black Gram(Urd Beans)(Whole)"],
    "Green Gram (Moong)(Whole)": ["Green Gram(Moong)(Whole)"],
}

# District names exactly as Agmarknet spells them for UP (taken from the data).
DISTRICTS = [
    "Agra", "Aligarh", "Ambedkarnagar", "Amethi", "Amroha", "Auraiya", "Ayodhya",
    "Azamgarh", "Badaun", "Baghpat", "Bahraich", "Ballia", "Balrampur", "Banda",
    "Barabanki", "Bareilly", "Basti", "Bhadohi(Sant Ravi Nagar)", "Bijnor",
    "Bulandshahar", "Chandauli", "Chitrakut", "Deoria", "Etah", "Etawah",
    "Farukhabad", "Fatehpur", "Firozabad", "Gautam Budh Nagar", "Ghaziabad",
    "Ghazipur", "Gonda", "Gorakhpur", "Hamirpur", "Hapur", "Hardoi", "Hathras",
    "Jalaun (Orai)", "Jaunpur", "Jhansi", "Kannuj", "Kanpur", "Kanpur Dehat",
    "Kasganj", "Kaushambi", "Khiri (Lakhimpur)", "Kushinagar", "Lakhimpur",
    "Lalitpur", "Lucknow", "Maharajganj", "Mahoba", "Mainpuri", "Mathura",
    "Mau(Maunathbhanjan)", "Meerut", "Mirzapur", "Muzaffarnagar", "Pillibhit",
    "Pratapgarh", "Prayagraj", "Raebarelli", "Rampur", "Saharanpur", "Sambhal",
    "Sant Kabir Nagar", "Shahjahanpur", "Shamli", "Shravasti", "Siddharth Nagar",
    "Sitapur", "Sonbhadra", "Unnao", "Varanasi",
]

MANIFEST_FIELDS = ["commodity", "district", "api_total", "rows_saved",
                   "distinct_rows", "attempts", "status"]


def slug(text: str) -> str:
    """'Bengal Gram(Gram)(Whole)' -> 'bengal_gram_gram_whole'"""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def folder(commodity: str) -> str:
    """Folder of a commodity name: its slug, or the old name's slug plus __renamed_<n>."""
    for old, names in RENAMED.items():
        if commodity in names:
            return f"{slug(old)}__renamed_{names.index(commodity) + 1}"
    return slug(commodity)


def get_page(api_key: str, filters: dict, offset: int, limit: int = PAGE_SIZE) -> dict:
    """Return one JSON page, retrying temporary failures with growing pauses."""
    params = {"api-key": api_key, "format": "json", "limit": limit, "offset": offset,
              "sort[Arrival_Date]": "asc"}
    params.update({f"filters[{k}]": v for k, v in filters.items()})
    request = Request(f"{BASE_URL}?{urlencode(params)}", headers={"User-Agent": "KrishiDrishti/1.0"})

    for attempt in range(1, RETRIES + 1):
        try:
            with urlopen(request, timeout=180) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504}:
                raise RuntimeError(f"HTTP {error.code} for {filters} at offset {offset}") from error
            problem = f"HTTP {error.code}"
        # OSError covers dropped connections and timeouts;
        # HTTPException covers responses cut off midway (IncompleteRead).
        except (URLError, OSError, HTTPException, json.JSONDecodeError) as error:
            problem = str(error)

        if attempt == RETRIES:
            raise RuntimeError(f"Gave up on {filters} at offset {offset}: {problem}")
        pause = min(2 ** attempt, 120)
        print(f"    {problem}; retrying in {pause}s...", flush=True)
        time.sleep(pause)

    raise AssertionError("Unreachable")


def fetch_slice(api_key: str, filters: dict) -> tuple[list[dict], list[str], int]:
    """Fetch every page of one slice. Returns (records, API field order, API total)."""
    records: list[dict] = []
    fields: list[str] = []
    total = 0
    offset = 0
    while True:
        page = get_page(api_key, filters, offset)
        total = int(page.get("total", 0))
        fields = fields or [f["id"] for f in page.get("field", [])]
        batch = page.get("records", [])
        if not batch:
            break
        records.extend(batch)
        offset += len(batch)
        if offset >= total:
            break
        time.sleep(0.5)
    return records, fields, total


def distinct_count(records: list[dict]) -> int:
    return len({tuple(sorted(r.items())) for r in records})


def done_slices() -> set[tuple[str, str]]:
    if not MANIFEST.exists():
        return set()
    with MANIFEST.open(encoding="utf-8") as f:
        return {(row["commodity"], row["district"]) for row in csv.DictReader(f)}


def record_in_manifest(row: dict) -> None:
    new_file = not MANIFEST.exists()
    with MANIFEST.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


def download_slice(api_key: str, commodity: str, district: str) -> None:
    filters = {"State": STATE, "Commodity": commodity, "District": district}
    best: list[dict] = []
    fields: list[str] = []
    total = 0
    attempts = 0

    for attempts in range(1, SLICE_ATTEMPTS + 1):
        records, fields, total = fetch_slice(api_key, filters)
        if distinct_count(records) > distinct_count(best):
            best = records
        if distinct_count(best) >= total:
            break
        print(f"    {commodity} / {district}: {distinct_count(best):,} distinct of "
              f"{total:,}; fetching the slice again", flush=True)

    distinct = distinct_count(best)
    status = "complete" if distinct >= total else "incomplete"
    if best:
        path = OUTPUT_DIR / folder(commodity) / f"{district}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields or list(best[0]))
            writer.writeheader()
            writer.writerows(best)

    record_in_manifest({"commodity": commodity, "district": district, "api_total": total,
                        "rows_saved": len(best), "distinct_rows": distinct,
                        "attempts": attempts, "status": status})
    print(f"  {commodity} / {district}: {len(best):,} rows, {status}", flush=True)


def main() -> None:
    api_key = os.getenv("DATA_GOV_IN_API_KEY")
    if not api_key:
        sys.exit('API key not found. In PowerShell run:  $env:DATA_GOV_IN_API_KEY = "your-key"')

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    done = done_slices()
    for commodity in COMMODITIES + [name for names in RENAMED.values() for name in names]:
        print(f"{commodity}", flush=True)
        for district in DISTRICTS:
            if (commodity, district) not in done:
                download_slice(api_key, commodity, district)

    print(f"\nFinished. Check {MANIFEST} for any slice marked incomplete.")


if __name__ == "__main__":
    main()
