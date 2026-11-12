"""Read the official Cost of Cultivation workbooks into one table for Uttar Pradesh.

Input:  data/raw/cost_of_cultivation/*.xls, *.xlsx
        "Estimates of Cost of Cultivation/Production & Related Data", Directorate of Economics
        & Statistics, Ministry of Agriculture (desagri.gov.in). One workbook per crop year,
        one sheet per crop, one column per State.
Output: data/processed/cost_of_cultivation.csv, one row per crop and crop year, Uttar Pradesh only:
        crop, crop_as_printed, crop_year, crop_year_start,
        cost_a1, cost_a2, cost_a2_fl, cost_b1, cost_b2, cost_c1, cost_c2      (Rs per hectare)
        family_labour, operational_cost, fixed_cost                           (Rs per hectare)
        value_main_product, value_by_product                                  (Rs per hectare)
        derived_yield_qtl_per_ha, implicit_rate_rs_per_qtl, holdings_in_sample

Values are copied as printed. Nothing is calculated or filled: a figure the workbook does not
print is left empty (A2+FL is printed only from 2021-22). The State survey covers a sample of
holdings, so the figures are State averages, not district figures.

Run from the repo root:
    python scripts/build_cost_table.py
"""

from __future__ import annotations

import re
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore", message=".*xlrd engine.*")

RAW = Path("data/raw/cost_of_cultivation")
OUTPUT = Path("data/processed/cost_of_cultivation.csv")
STATE = "uttarpradesh"

# sheet name in the workbooks: crop name used in this project
CROPS = {
    "Paddy": "Rice", "Maize": "Maize", "Bajra": "Bajra", "Jowar": "Jowar", "Arhar": "Arhar/Tur", "Urad": "Urad",
    "Moong": "Moong(Green Gram)", "Sesamum": "Sesamum", "Groundnut": "Groundnut", "Wheat": "Wheat", "Barley": "Barley",
    "Gram": "Gram", "Lentil": "Masoor", "Peas": "Peas & beans (Pulses)", "R&M": "Rapeseed & Mustard",
    "Potato": "Potato", "Sugarcane": "Sugarcane",
}
CONCEPTS = {"A1": "cost_a1", "A2": "cost_a2", "A2+FL": "cost_a2_fl", "B1": "cost_b1", "B2": "cost_b2",
            "C1": "cost_c1", "C2": "cost_c2"}
ITEMS = {
    "valueofmainproduct": "value_main_product",
    "valueofbyproduct": "value_by_product",
    "operationalcost": "operational_cost",
    "fixedcosts": "fixed_cost",
    "fixedcost": "fixed_cost",
    "derivedyield": "derived_yield_qtl_per_ha",
    "implicitrate": "implicit_rate_rs_per_qtl",
    "numberofholdingsinsample": "holdings_in_sample",
}


def squeeze(value) -> str:
    return re.sub(r"[^a-z0-9+]", "", str(value).lower()) if isinstance(value, str) else ""


def read_sheet(sheet: pd.DataFrame) -> dict | None:
    state_col = next((c for r in range(min(8, len(sheet))) for c in range(sheet.shape[1])
                      if squeeze(sheet.iat[r, c]) == STATE), None)
    if state_col is None:
        return None

    row, block = {}, None
    for r in range(len(sheet)):
        labels = [str(v).strip() for v in sheet.iloc[r, :3] if isinstance(v, str)]
        text = squeeze(" ".join(labels))
        value = pd.to_numeric(sheet.iat[r, state_col], errors="coerce")
        if "costofcultivation" in text and "breakup" not in text:
            block = "cultivation"
        elif "costofproduction" in text:
            block = None
        elif "operationalcost" in text:
            block = "items"

        if block == "cultivation":
            concept = next((label for label in labels if label.upper() in CONCEPTS), None)
            if concept:
                row[CONCEPTS[concept.upper()]] = value
        if block == "items" and "humanlabour" in text and "family" in text:
            row["family_labour"] = value
        for key, name in ITEMS.items():
            if text.startswith(key) or re.sub(r"\(.*", "", text) == key:
                row.setdefault(name, value)
    return row


def main() -> None:
    rows = []
    for path in sorted(RAW.glob("*.xls*")):
        start = int(re.search(r"(\d{4})-\d{2}", path.name).group(1))
        for sheet_name, sheet in pd.read_excel(path, sheet_name=None, header=None).items():
            crop = CROPS.get(sheet_name.strip())
            if crop is None:
                continue
            values = read_sheet(sheet)
            if not values or pd.isna(values.get("cost_a2")):
                continue
            rows.append({"crop": crop, "crop_as_printed": sheet_name.strip(), "crop_year": f"{start}-{(start + 1) % 100:02d}",
                         "crop_year_start": start, **values})

    columns = ["crop", "crop_as_printed", "crop_year", "crop_year_start", *CONCEPTS.values(), "family_labour",
               "operational_cost", "fixed_cost", "value_main_product", "value_by_product",
               "derived_yield_qtl_per_ha", "implicit_rate_rs_per_qtl", "holdings_in_sample"]
    table = pd.DataFrame(rows).reindex(columns=columns).sort_values(["crop", "crop_year_start"]).reset_index(drop=True)

    checks = {
        "A1 <= A2": table["cost_a1"] <= table["cost_a2"] + 1,
        "B1 <= B2": table["cost_b1"] <= table["cost_b2"] + 1,
        "C1 <= C2": table["cost_c1"] <= table["cost_c2"] + 1,
        "B1 + family labour = C1": (table["cost_b1"] + table["family_labour"] - table["cost_c1"]).abs() <= 1,
        "operational + fixed = C2": (table["operational_cost"] + table["fixed_cost"] - table["cost_c2"]).abs() <= 1,
        "A2 + family labour = printed A2+FL": table["cost_a2_fl"].isna()
                                              | ((table["cost_a2"] + table["family_labour"] - table["cost_a2_fl"]).abs() <= 1),
    }
    failed = pd.DataFrame(checks)
    failed = failed.loc[~failed.all(axis=1)]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT, index=False)
    print(f"{len(table)} rows, {table.crop.nunique()} crops, crop years {table.crop_year.min()} to {table.crop_year.max()}")
    print(table.groupby("crop").agg(years=("crop_year_start", "size"), first=("crop_year", "min"), last=("crop_year", "max")).to_string())
    print(f"Empty cells: {table.drop(columns='cost_a2_fl').isna().sum().sum()} (A2+FL is printed in {table.cost_a2_fl.notna().sum()} rows)")
    print(f"Rows whose printed figures do not agree with each other (copied as printed): {len(failed)}")
    for index, row in failed.iterrows():
        print("   ", table.at[index, "crop"], table.at[index, "crop_year"], "fails:", ", ".join(row.index[~row]))
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
