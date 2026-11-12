"""Download district-level soil test results for UP from the Soil Health Card portal.

Source: soilhealth.dac.gov.in (Ministry of Agriculture), via the same public
GraphQL API its Nutrient Dashboard uses. No key needed.

For each district and testing cycle, the API gives how many soil samples fell
into each class (e.g. nitrogen Low/Medium/High). The classes are assigned by
the portal, not by us. The JSON response is saved exactly as received.

Output: data/raw/soil_health_card/up_<cycle>.json  (one file per cycle)

Run from the repo root:
    python scripts/download_soil_health.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

API_URL = "https://soilhealth4.dac.gov.in/"
UP_STATE_ID = "63f600f38cec41e6c9607e6b"  # from the API's getState query
CYCLES = ["2023-24", "2024-25", "2025-26"]  # earlier cycles return no data
OUTPUT_DIR = Path("data/raw/soil_health_card")

QUERY = """
query($state: ID, $cycle: String) {
  getNutrientDashboardForPortal(state: $state, cycle: $cycle)
}
"""


def fetch_cycle(cycle: str) -> bytes:
    """Return the API's raw JSON response for one testing cycle."""
    body = json.dumps({"query": QUERY, "variables": {"state": UP_STATE_ID, "cycle": cycle}}).encode()
    request = Request(API_URL, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": "KrishiDrishti/1.0",
    })
    with urlopen(request, timeout=180) as response:
        return response.read()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for cycle in CYCLES:
        raw = fetch_cycle(cycle)
        records = json.loads(raw)["data"]["getNutrientDashboardForPortal"] or []
        path = OUTPUT_DIR / f"up_{cycle}.json"
        path.write_bytes(raw)
        print(f"{cycle}: {len(records)} records -> {path}")
        time.sleep(1)


if __name__ == "__main__":
    main()
