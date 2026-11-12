"""Read the official MSP statement (PDF) into a table.

Input:  data/raw/msp/RTI-reply-of-Sandeep-Rathore.pdf
        "Minimum Support Price of Kharif Crops & Rabi Crops since 1995-96 to 2026-27
        (Marketing Season-wise)", Ministry of Agriculture (desagri.gov.in).
Output: data/processed/msp.csv, one row per crop and marketing season:
        crop, commodity_as_printed, season, marketing_season, crop_year_start, msp_rs_per_quintal

Values are copied as printed, including any Central bonus the statement includes in the figure.
Footnote marks next to a number are removed. The "Special drought relief price" column of
2002-03 is not copied. A Kharif marketing season KMS Y-(Y+1) belongs to crop year Y; a Rabi
marketing season RMS (Y+1)-(Y+2) sells the crop sown in crop year Y.

The result is checked against the two other statements in data/raw/msp/.

Run from the repo root:
    python scripts/build_msp_table.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import pypdf

RAW = Path("data/raw/msp")
OUTPUT = Path("data/processed/msp.csv")

# first crop year of each page's columns, and whether its second column is the drought relief price
PAGES = {1: (1995, 7, False), 2: (2002, 6, True), 3: (2008, 10, False), 4: (2018, 8, False)}

# crop name used in this project: (season, line start as printed, in upper case)
CROPS = {
    "Rice": ("Kharif", ["PADDY COMMON"]),
    "Jowar": ("Kharif", ["JOWAR HYBRID", "JOWAR"]),
    "Bajra": ("Kharif", ["BAJRA"]),
    "Maize": ("Kharif", ["MAIZE"]),
    "Arhar/Tur": ("Kharif", ["ARHAR(TUR)", "TUR(ARHAR)"]),
    "Moong(Green Gram)": ("Kharif", ["MOONG"]),
    "Urad": ("Kharif", ["URAD"]),
    "Sesamum": ("Kharif", ["SESAMUM"]),
    "Groundnut": ("Kharif", ["GROUNDNUT IN SHELL", "GROUNDNUT"]),
    "Wheat": ("Rabi", ["WHEAT"]),
    "Barley": ("Rabi", ["BARLEY"]),
    "Gram": ("Rabi", ["GRAM"]),
    "Masoor": ("Rabi", ["MASUR(LENTIL)", "MASUR (LENTIL)"]),
    "Rapeseed & Mustard": ("Rabi", ["RAPESEED/MUSTARD", "RAPESEED & MUSTARD"]),
}


def numbers(text: str) -> list[float | None]:
    values = []
    for token in text.split():
        if token == "-":
            values.append(None)
        elif re.match(r"\d", token):
            values.append(float(re.match(r"\d+", token).group(0)))
    return values


def main() -> None:
    pages = [p.extract_text() or "" for p in pypdf.PdfReader(RAW / "RTI-reply-of-Sandeep-Rathore.pdf").pages]
    rows = []
    for page_no, (first_year, n_years, has_relief) in PAGES.items():
        lines = [re.sub(r"^\d+\s+", "", line.strip()) for line in pages[page_no].splitlines()]
        for crop, (season, labels) in CROPS.items():
            line = next((l for label in labels for l in lines if l.upper().startswith(label + " ")), None)
            if line is None:
                continue
            label = next(label for label in labels if line.upper().startswith(label + " "))
            values = numbers(line[len(label):])
            if has_relief:
                del values[1]
            assert len(values) == n_years, (page_no + 1, crop, line)
            for offset, value in enumerate(values):
                year = first_year + offset
                season_label = (f"KMS {year}-{(year + 1) % 100:02d}" if season == "Kharif"
                                else f"RMS {year + 1}-{(year + 2) % 100:02d}")
                rows.append([crop, line[:len(label)], season, season_label, year, value])

    table = pd.DataFrame(rows, columns=["crop", "commodity_as_printed", "season", "marketing_season",
                                        "crop_year_start", "msp_rs_per_quintal"]).dropna(subset=["msp_rs_per_quintal"])
    table = table.sort_values(["crop", "crop_year_start"]).reset_index(drop=True)

    # check against the statement "as on 12.12.2025" (KMS 2021-22 to 2025-26, RMS 2022-23 to 2026-27)
    check = (pypdf.PdfReader(RAW / "MSP-Statement_English_As-on-12.12.2025.pdf").pages[0].extract_text() or "")
    check = re.sub(r"\s+", " ", check)
    expected = {"Rice": r"Paddy \(Common\)", "Bajra": "Bajra", "Maize": "Maize", "Arhar/Tur": "Arhar", "Moong(Green Gram)": "Moong",
                "Urad": "Urad", "Sesamum": "Sesamum", "Groundnut": "Groundnut", "Wheat": "Wheat", "Barley": "Barley",
                "Gram": "Gram", "Masoor": "Masur"}
    checked = 0
    for crop, pattern in expected.items():
        found = re.search(pattern + r"((?: \d{3,5}){5})", check)
        assert found, crop
        printed = [float(v) for v in found.group(1).split()]
        ours = table[(table.crop == crop) & table.crop_year_start.between(2021, 2025)].msp_rs_per_quintal.tolist()
        assert printed == ours, (crop, printed, ours)
        checked += len(ours)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT, index=False)
    print(f"{len(table)} rows, {table.crop.nunique()} crops, crop years {table.crop_year_start.min()}-{table.crop_year_start.max()}")
    print(f"{checked} values match the second official statement")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
