"""Download daily weather history for every UP district from NASA POWER.

NASA POWER is free and needs no API key. One request per district fetches
the whole date range. The API's JSON response is saved exactly as received,
with no renaming or cleaning (NASA marks missing values as -999).

Output: data/raw/weather_nasa_power/<DISTRICT>.json  (one file per district)

Run from the repo root:
    python scripts/download_weather.py
"""

from __future__ import annotations

import time
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

COORDS_FILE = Path("data/raw/up_district_coords.csv")
OUTPUT_DIR = Path("data/raw/weather_nasa_power")
BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
START, END = "19970101", "20251231"
RETRIES = 5

# PRECTOTCORR  precipitation, mm/day
# T2M, T2M_MAX, T2M_MIN  air temperature at 2 m, °C
# RH2M  relative humidity at 2 m, %
# ALLSKY_SFC_SW_DWN  sunlight reaching the ground, MJ/m²/day
PARAMETERS = ["PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN", "RH2M", "ALLSKY_SFC_SW_DWN"]


def fetch_district(lat: float, lon: float) -> bytes:
    """Return NASA's raw JSON response for one point."""
    params = urlencode({
        "parameters": ",".join(PARAMETERS),
        "community": "AG",
        "latitude": lat,
        "longitude": lon,
        "start": START,
        "end": END,
        "format": "JSON",
    })
    request = Request(f"{BASE_URL}?{params}", headers={"User-Agent": "KrishiDrishti/1.0"})

    for attempt in range(1, RETRIES + 1):
        try:
            with urlopen(request, timeout=180) as response:
                return response.read()
        except (HTTPError, URLError, OSError, HTTPException) as error:
            if attempt == RETRIES:
                raise RuntimeError(f"Failed after {RETRIES} attempts: {error}") from error
            pause = 2 ** attempt
            print(f"  problem ({error}); retrying in {pause}s...", flush=True)
            time.sleep(pause)

    raise AssertionError("Unreachable")


def main() -> None:
    coords = pd.read_csv(COORDS_FILE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, row in enumerate(coords.itertuples(), start=1):
        path = OUTPUT_DIR / f"{row.district_name}.json"
        if path.exists():  # already downloaded on an earlier run
            continue
        print(f"[{i}/{len(coords)}] {row.district_name}", flush=True)
        path.write_bytes(fetch_district(row.latitude, row.longitude))
        time.sleep(1)  # be polite to NASA's servers

    print(f"\nFinished. Raw weather files are in {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
