"""Agronomy rules applied to the candidate crops after the models have made their predictions.

notebooks/4_AgronomyRules.ipynb builds the rule tables and writes models/rules.joblib. The rules do not
change any prediction. They mark a crop as not suitable (it needs irrigation and the farm has
none) or attach a note to it (rarely grown in the district, sensitive to the soil, old yield data).
"""

from __future__ import annotations

import pandas as pd

SOIL_KINDS = ("saline", "alkaline")


def irrigation_need(rules: dict, crop: str, season: str) -> str:
    if crop in rules["typed_irrigation"]:
        return rules["typed_irrigation"][crop]
    table = rules["irrigation"]
    return table.loc[(crop, season), "irrigation_need"] if (crop, season) in table.index else "not known"


def check(rules: dict, district: str, season: str, crops, irrigated: bool | None = None,
          soil: dict | None = None) -> pd.DataFrame:
    """One row per crop: area_share, irrigation_need, suitable and advice.

    irrigated: True or False when the farmer has said whether the field can be irrigated.
    soil: optional {"saline": bool, "alkaline": bool} from the farmer's own soil health card;
    without it the district's soil health card shares are used.
    """
    grown, tolerance = rules["grown"], rules["tolerance"]
    district_soil = rules["district_soil"]
    rows = []
    for crop in crops:
        notes, suitable = [], True
        key = (district, season, crop)
        share = grown.loc[key, "area_share"] if key in grown.index else float("nan")
        if key in grown.index and grown.loc[key, "rarely_grown"]:
            notes.append(f"rarely grown here (under {rules['thresholds']['min_area_share']:.0%} of the district's {season} area)")

        need = irrigation_need(rules, crop, season)
        if need == "needs irrigation":
            if irrigated is False:
                suitable = False
                notes.append("needs irrigation, which the farm does not have")
            elif irrigated is None:
                notes.append("needs irrigation")

        for kind in SOIL_KINDS:
            sensitive = crop in tolerance.index and tolerance.loc[crop, f"sensitive_to_{kind}"] is True
            if not sensitive:
                continue
            if soil is not None:
                if soil.get(kind):
                    notes.append(f"sensitive to {kind} soil, which the farm's soil card shows")
            elif district in district_soil.index and district_soil.loc[district, f"{kind}_common"]:
                notes.append(f"sensitive to {kind} soil, found in {district_soil.loc[district, f'{kind}_share']:.0%} of the district's soil samples")

        last = rules["last_yield_year"].get(crop)
        if last is not None and last < rules["latest_year"] - 1:
            notes.append(f"official yield data ends {last}-{(last + 1) % 100:02d}")

        rows.append({"crop": crop, "area_share": round(float(share), 4), "irrigation_need": need,
                     "suitable": suitable, "advice": "; ".join(notes)})
    return pd.DataFrame(rows).set_index("crop")
