"""Find latitude/longitude for every UP district in the district master table.

Each district is located by its headquarters town using the free Open-Meteo
geocoding API (no key needed). Output: data/raw/up_district_coords.csv

Run from the repo root:
    python scripts/build_district_coords.py
"""

from __future__ import annotations

import csv
import json
import time
import unicodedata
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

# Upper-case district names (as in the old data.gov.in crop file), which also
# name the weather files.
MASTER_FILE = Path("data/processed/district_master.csv")
OUTPUT_FILE = Path("data/raw/up_district_coords.csv")
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

# District name in the crop data -> headquarters town to search for,
# where the two differ (renamed districts or districts named after a region).
HQ_TOWN = {
    "ALLAHABAD": "Prayagraj",
    "AMBEDKAR NAGAR": "Akbarpur",
    "AMETHI": "Gauriganj",
    "AMROHA": "Amroha",
    "CHITRAKOOT": "Karwi",
    "FAIZABAD": "Ayodhya",
    "GAUTAM BUDDHA NAGAR": "Greater Noida",
    "HAMIRPUR": "Hamirpur",
    "BARABANKI": "Bara Banki",
    "KANPUR DEHAT": "Akbarpur",
    "KANPUR NAGAR": "Kanpur",
    "KASGANJ": "Kasganj",
    "KAUSHAMBI": "Manjhanpur",
    "KHERI": "Lakhimpur",
    "KUSHI NAGAR": "Padrauna",
    "MAHARAJGANJ": "Maharajganj",
    "SAMBHAL": "Sambhal",
    "SANT KABEER NAGAR": "Khalilabad",
    "SANT RAVIDAS NAGAR": "Gyanpur",
    "SHRAVASTI": "Bhinga",
    "SIDDHARTH NAGAR": "Naugarh",
    "SONBHADRA": "Robertsganj",
}


def simplify(text: str) -> str:
    """Lowercase ASCII letters only, so 'Bānda District' compares like 'BANDA'."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return "".join(ch for ch in ascii_text.lower() if ch.isalpha())


def geocode(town: str, district: str) -> dict | None:
    """Return the best match for `town` inside Uttar Pradesh.

    Prefers places whose admin2 (district) field matches the district we want,
    because many town names repeat across districts. Falls back to the most
    populous place in UP with that name.
    """
    params = urlencode({"name": town, "count": 50, "countryCode": "IN"})
    request = Request(f"{GEOCODE_URL}?{params}", headers={"User-Agent": "KrishiDrishti/1.0"})
    with urlopen(request, timeout=30) as response:
        results = json.load(response).get("results", [])
    in_up = [r for r in results if r.get("admin1") == "Uttar Pradesh"]
    key = simplify(district)[:5]
    same_district = [r for r in in_up if key in simplify(r.get("admin2", ""))]
    candidates = same_district or in_up
    return max(candidates, key=lambda r: r.get("population") or 0) if candidates else None


def main() -> None:
    districts = sorted(pd.read_csv(MASTER_FILE)["nasa_weather_file"])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    missing = []
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["district_name", "hq_town", "latitude", "longitude", "matched_admin2"])
        for district in districts:
            town = HQ_TOWN.get(district, district.title())
            match = geocode(town, district)
            if match is None:
                missing.append(district)
                print(f"NOT FOUND: {district} (searched '{town}')")
                continue
            writer.writerow([district, town, match["latitude"], match["longitude"], match.get("admin2", "")])
            print(f"{district:22} -> {match['latitude']:.3f}, {match['longitude']:.3f}  ({match.get('admin2', '')})")
            time.sleep(0.2)

    print(f"\nSaved {len(districts) - len(missing)} / {len(districts)} districts to {OUTPUT_FILE}")
    if missing:
        print("Add these to HQ_TOWN with a better search name:", missing)


if __name__ == "__main__":
    main()
