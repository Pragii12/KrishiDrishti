"""Build the master table (and its supporting tables) from the raw data.

One master-table row = one crop x district x season x crop year, e.g.
"Wheat, Agra, Rabi, 2015-16". Each row carries the crop statistics plus the
weather of that season, the district's soil profile, the district's irrigation
and land use for that year, and mandi prices at harvest time.

Only the aggregation needed to fit the data to that grain is done here (daily
weather -> season, daily prices -> month / harvest window, soil test counts ->
shares). Ratios and other engineered features are left to preprocessing.
Missing information stays empty (null).

Outputs (data/processed/):
    master_table.csv          the master table
    master_table_columns.csv  what every column means and where it comes from
    price_monthly.csv         median mandi price per district x crop x month
    crop_master.csv           crop names across sources

Run from the repo root:
    python scripts/build_master_table.py
"""

from __future__ import annotations

import csv
import glob
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from download_mandi_prices import RENAMED, folder

RAW = Path("data/raw")
EXT = Path("data/external/up_crop_datasets_zip")
OUT = Path("data/processed")


def norm(text: str) -> str:
    return re.sub(r"[^a-z]", "", str(text).lower())


def to_number(series: pd.Series, dash_is_zero: bool = False) -> pd.Series:
    """'120,903.00' -> 120903.0. In DES Land Use Statistics '-' means nil."""
    s = series.astype(str).str.replace(",", "", regex=False).str.strip()
    if dash_is_zero:
        s = s.replace("-", "0")
    return pd.to_numeric(s.replace({"": None, "-": None, "nan": None}), errors="coerce")


# ---------------------------------------------------------------- districts
DISTRICTS = pd.read_csv(OUT / "district_master.csv")
TO_DES = {norm(r.district): r.district for r in DISTRICTS.itertuples()}
TO_DES |= {norm(r.current_official_name): r.district for r in DISTRICTS.itertuples()}
# LGD spellings used by the external package
TO_DES |= {"mahrajganj": "Maharajganj", "santkabirnagar": "Sant kabeer nagar",
           "shrawasti": "Shravasti", "lakhimpurkheri": "Kheri"}


def des_district(name: str) -> str | None:
    return TO_DES.get(norm(re.sub(r"^\d+\.\s*", "", str(name))))


# ---------------------------------------------------------------- crops
# crop (DES name): group, LUS irrigation crop per season, Agmarknet commodity.
# The commodity is the name used until 5 November 2025; the names used since then are in
# RENAMED (download_mandi_prices.py) and are read as the same commodity.
# LUS crops were matched to their raw columns by identical values (two years).
CROPS = {
    "Rice": ("Cereals", {"Kharif": "Rice|Autumn", "Summer": "Rice|Summer"}, "Paddy(Dhan)(Common)"),
    "Wheat": ("Cereals", {"Rabi": "Wheat"}, "Wheat"),
    "Maize": ("Cereals", {"*": "Maize"}, "Maize"),
    "Bajra": ("Cereals", {"Kharif": "Bajra"}, "Bajra(Pearl Millet/Cumbu)"),
    "Jowar": ("Cereals", {"Kharif": "Jowar|Kharif"}, "Jowar(Sorghum)"),
    "Barley": ("Cereals", {"Rabi": "Barley"}, "Barley (Jau)"),
    "Ragi": ("Cereals", {}, None),
    "Small millets": ("Cereals", {}, None),
    "Arhar/Tur": ("Pulses", {"Kharif": "Arhar(Tur)"}, "Arhar (Tur/Red Gram)(Whole)"),
    "Gram": ("Pulses", {"Rabi": "Gram"}, "Bengal Gram(Gram)(Whole)"),
    "Masoor": ("Pulses", {"Rabi": "Other Pulses|Rabi"}, "Lentil (Masur)(Whole)"),
    "Moong(Green Gram)": ("Pulses", {"Kharif": "Other Pulses|Kharif", "Rabi": "Other Pulses|Rabi"}, "Green Gram (Moong)(Whole)"),
    "Urad": ("Pulses", {"Kharif": "Other Pulses|Kharif", "Rabi": "Other Pulses|Rabi"}, "Black Gram (Urd Beans)(Whole)"),
    "Moth": ("Pulses", {"Kharif": "Other Pulses|Kharif"}, None),
    "Peas & beans (Pulses)": ("Pulses", {"Rabi": "Other Pulses|Rabi"}, "Peas(Dry)"),
    "Other Kharif pulses": ("Pulses", {"Kharif": "Other Pulses|Kharif"}, None),
    "Other  Rabi pulses": ("Pulses", {"Rabi": "Other Pulses|Rabi"}, None),
    "Rapeseed &Mustard": ("Oilseeds", {"Rabi": "Rapeseed and Mustard"}, "Mustard"),
    "Sesamum": ("Oilseeds", {"Kharif": "Sesamum"}, "Sesamum(Sesame,Gingelly,Til)"),
    "Groundnut": ("Oilseeds", {"Kharif": "Groundnut"}, None),
    "Linseed": ("Oilseeds", {"Rabi": "Linseed"}, None),
    "Soyabean": ("Oilseeds", {}, None),
    "Sunflower": ("Oilseeds", {"*": "Sunflower"}, None),
    "Castor seed": ("Oilseeds", {}, None),
    "Sugarcane": ("Cash crops", {"*": "Sugarcane"}, None),
    "Cotton(lint)": ("Cash crops", {}, None),
    "Jute": ("Cash crops", {}, None),
    "Sannhamp": ("Cash crops", {}, None),
    "Tobacco": ("Cash crops", {"*": "Tobacco"}, None),
    "Guar seed": ("Cash crops", {}, None),
    "Potato": ("Vegetables & spices", {}, "Potato"),
    "Onion": ("Vegetables & spices", {}, None),
    "Garlic": ("Vegetables & spices", {}, None),
    "Sweet potato": ("Vegetables & spices", {}, None),
    "Banana": ("Vegetables & spices", {}, None),
    "Coriander": ("Vegetables & spices", {}, None),
    "Dry chillies": ("Vegetables & spices", {}, None),
    "Ginger": ("Vegetables & spices", {}, None),
    "Turmeric": ("Vegetables & spices", {}, None),
}
# Raw LUS value column for each LUS crop (crop_area table, crop_irr table)
LUS_COLUMNS = {
    "Rice|Autumn": ("col_002", "col_001"), "Rice|Summer": ("col_004", "col_003"),
    "Jowar|Kharif": ("col_006", "col_005"), "Bajra": ("col_010", "col_009"),
    "Maize": ("col_012", "col_011"), "Wheat": ("col_016", "col_015"),
    "Barley": ("col_018", "col_017"), "Gram": ("col_025", "col_024"),
    "Arhar(Tur)": ("col_027", "col_026"), "Other Pulses|Kharif": ("col_029", "col_028"),
    "Other Pulses|Rabi": ("col_030", "col_029"), "Sugarcane": ("col_035", "col_034"),
    "Groundnut": ("col_101", "col_095"), "Sesamum": ("col_105", "col_097"),
    "Rapeseed and Mustard": ("col_107", "col_099"), "Linseed": ("col_109", "col_101"),
    "Sunflower": ("col_117", "col_105"), "Tobacco": ("col_142", "col_123"),
}
CROP_KEY = {norm(c): c for c in CROPS}

# DES changed the season under which some crops are reported (mostly around 2004)
# although the crop is grown at the same time of year. Each is given the one season
# that matches its growing period, so it always gets the same weather window.
SEASON_FIX = {
    "Potato": "Rabi", "Garlic": "Rabi", "Coriander": "Rabi", "Peas & beans (Pulses)": "Rabi",
    "Dry chillies": "Kharif", "Guar seed": "Kharif", "Sweet potato": "Kharif", "Sannhamp": "Kharif",
    "Moth": "Kharif", "Castor seed": "Kharif", "Ragi": "Kharif",
    "Sunflower": "Summer",
    "Sugarcane": "Whole Year", "Banana": "Whole Year", "Turmeric": "Whole Year",
}


def lus_crop_for(crop: str, season: str) -> str | None:
    rule = CROPS[crop][1]
    return rule.get(season) or rule.get("*")


# ---------------------------------------------------------------- 1. crop statistics
def load_crop_statistics() -> pd.DataFrame:
    des = pd.read_csv(RAW / "des_crop_production/up_crop_production_1997_2022.csv", dtype=str)
    des = pd.DataFrame({
        "crop_year": des.Year.str[:4] + "-" + des.Year.str[-2:],
        "district": des.District.map(des_district),
        "season": des.Season.str.strip(),
        "crop": des.Crop.str.strip(),
        "area_ha": to_number(des["Area (Hectare)"]),
        "production_t": to_number(des["Production (Tonnes)"]),
        "yield_t_per_ha": to_number(des["Yield (Tonne/Hectare)"]),
        "data_source": "DES crop statistics (raw)",
    })
    # 2023-24 and 2024-25 are only in the external package (from UPAg)
    ext = pd.read_csv(EXT / "up_district_season_crop_apy_1997_2025.csv")
    ext = ext[ext.fiscal_year.isin(["2023-24", "2024-25"])]
    ext = pd.DataFrame({
        "crop_year": ext.fiscal_year,
        "district": ext.district_as_per_lgd.map(des_district),
        "season": ext.season,
        "crop": ext.crop.map(lambda c: CROP_KEY.get(norm(c), c)),
        "area_ha": ext.area,
        "production_t": ext.production,
        "yield_t_per_ha": (ext.crop_yield / 1000).round(2),  # kg/ha -> t/ha
        "data_source": "External package (UPAg via India Data Portal)",
    })
    rows = pd.concat([des, ext], ignore_index=True)
    rows.insert(1, "crop_year_start", rows.crop_year.str[:4].astype(int))
    assert rows.district.notna().all(), "unmapped district"
    assert rows.crop.isin(list(CROPS)).all(), f"unmapped crop: {set(rows.crop) - set(CROPS)}"
    fix = rows.crop.map(SEASON_FIX)
    print(f"  season label harmonised in {(fix.notna() & (fix != rows.season)).sum():,} rows")
    rows["season"] = fix.fillna(rows.season)
    # where a district-year reported the crop under both labels, keep the larger-area row
    key = ["crop_year", "district", "season", "crop"]
    before = len(rows)
    rows = rows.sort_values("area_ha", ascending=False).drop_duplicates(key).sort_index()
    print(f"  {before - len(rows)} duplicate rows dropped after harmonising")
    rows["crop_group"] = rows.crop.map(lambda c: CROPS[c][0])
    return rows


# ---------------------------------------------------------------- 2. weather
# Season windows for crop year Y-(Y+1); the crop-year convention matches DES.
SEASON_WINDOWS = {
    "Kharif": [(0, m) for m in range(6, 11)],                         # Jun-Oct Y
    "Rabi": [(0, 11), (0, 12), (1, 1), (1, 2), (1, 3)],               # Nov Y - Mar Y+1
    "Summer": [(1, 4), (1, 5), (1, 6)],                               # Apr-Jun Y+1
    "Whole Year": [(0, m) for m in range(7, 13)] + [(1, m) for m in range(1, 7)],  # Jul Y - Jun Y+1
}


def assign_windows(frame: pd.DataFrame, windows: dict, year_col: str, month_col: str) -> pd.DataFrame:
    """Copy each row once per window it falls in, tagged with season and crop_year_start."""
    parts = []
    for season, window in windows.items():
        for dy, m in window:
            part = frame[frame[month_col] == m].copy()
            part["season"] = season
            part["crop_year_start"] = part[year_col] - dy
            parts.append(part)
    return pd.concat(parts, ignore_index=True)


def load_weather() -> pd.DataFrame:
    frames = []
    for row in DISTRICTS.itertuples():
        data = json.load(open(RAW / f"weather_nasa_power/{row.nasa_weather_file}.json"))
        p = data["properties"]["parameter"]
        d = pd.DataFrame(p).replace(-999.0, np.nan)
        d.index = pd.to_datetime(d.index, format="%Y%m%d")
        d["district"] = row.district
        frames.append(d)
    daily = pd.concat(frames)
    daily["y"], daily["m"] = daily.index.year, daily.index.month
    daily["rainy"] = daily.PRECTOTCORR >= 2.5          # IMD rainy day
    daily["heavy"] = daily.PRECTOTCORR >= 64.5         # IMD heavy rain
    daily["hot35"] = daily.T2M_MAX >= 35
    daily["hot40"] = daily.T2M_MAX >= 40
    daily["cold5"] = daily.T2M_MIN <= 5
    daily["frost2"] = daily.T2M_MIN <= 2

    g = assign_windows(daily, SEASON_WINDOWS, "y", "m").groupby(["district", "season", "crop_year_start"])
    weather = pd.DataFrame({
        "w_rain_total_mm": g.PRECTOTCORR.sum(min_count=1),
        "w_rainy_days": g.rainy.sum(),
        "w_heavy_rain_days": g.heavy.sum(),
        "w_max_1day_rain_mm": g.PRECTOTCORR.max(),
        "w_temp_mean_c": g.T2M.mean(),
        "w_tmax_mean_c": g.T2M_MAX.mean(),
        "w_tmin_mean_c": g.T2M_MIN.mean(),
        "w_hot_days_tmax_ge_35": g.hot35.sum(),
        "w_hot_days_tmax_ge_40": g.hot40.sum(),
        "w_cold_days_tmin_le_5": g.cold5.sum(),
        "w_frost_risk_days_tmin_le_2": g.frost2.sum(),
        "w_humidity_mean_pct": g.RH2M.mean(),
        "w_solar_mean_mj_m2_day": g.ALLSKY_SFC_SW_DWN.mean(),
        "w_days_in_window": g.T2M.count(),
    }).reset_index()

    # Soil moisture is not in our raw download; take it from the external
    # package's monthly district averages (NASA POWER), averaged over the window.
    ext = pd.read_csv(EXT / "up_district_climate_monthly_1997_2025.csv")
    ext["district"] = ext.district_as_per_lgd.map(des_district)
    g = assign_windows(ext, SEASON_WINDOWS, "year", "month").groupby(["district", "season", "crop_year_start"])
    moisture = pd.DataFrame({
        "w_soil_wetness_surface_0to1": g.soil_wetness_surface_0to1.mean(),
        "w_soil_wetness_root_zone_0to1": g.soil_wetness_root_zone_0to1.mean(),
    }).reset_index()
    weather = weather.merge(moisture, on=["district", "season", "crop_year_start"], how="left")
    # only complete windows (the last crop year's Summer may run past the data)
    full = weather.w_days_in_window >= weather.groupby("season").w_days_in_window.transform("max") - 1
    return weather[full].drop(columns="w_days_in_window").round(3)


# ---------------------------------------------------------------- 3. soil
def load_soil() -> pd.DataFrame:
    """Static district profile: share of samples in each class, all cycles pooled."""
    counts: dict[str, dict[str, int]] = {}
    for f in sorted(glob.glob(str(RAW / "soil_health_card/*.json"))):
        for rec in json.load(open(f, encoding="utf-8"))["data"]["getNutrientDashboardForPortal"] or []:
            district = des_district(rec["district"]["name"])
            c = counts.setdefault(district, {})
            for nutrient, classes in rec["results"].items():
                for cls, n in classes.items():
                    c[f"{nutrient}|{cls}"] = c.get(f"{nutrient}|{cls}", 0) + n
    names = {"n": "n", "p": "p", "k": "k", "OC": "oc", "pH": "ph", "EC": "ec",
             "S": "s", "Zn": "zn", "Fe": "fe", "Cu": "cu", "B": "b", "Mn": "mn"}
    keep = {"Low", "Medium", "High", "Acidic", "Neutral", "Alkaline", "Saline", "Deficient"}
    rows = []
    for district, c in counts.items():
        row = {"district": district, "soil_samples_tested": sum(v for k, v in c.items() if k.startswith("n|"))}
        for nutrient, short in names.items():
            total = sum(v for k, v in c.items() if k.split("|")[0] == nutrient)
            for k, v in c.items():
                nut, cls = k.split("|")
                if nut == nutrient and cls in keep and total:
                    row[f"soil_{short}_{cls.lower()}_share"] = round(v / total, 4)
        rows.append(row)
    soil = pd.DataFrame(rows)

    # Spread across villages (external package, village level, 2023-25)
    v = pd.read_csv(EXT / "up_soil_health_village_nutrient_status_2023_2025.csv")
    v["district"] = v.district_as_per_lgd.map(des_district)
    spread = v.groupby("district").agg(
        soil_villages_tested=("village_lgd_code", "nunique"),
        soil_village_sd_n_low_pct=("pct_nitrogen_low", "std"),
        soil_village_sd_p_low_pct=("pct_phosphorus_low", "std"),
        soil_village_sd_k_low_pct=("pct_potassium_low", "std"),
        soil_village_sd_oc_low_pct=("pct_organic_carbon_low", "std"),
        soil_village_sd_zn_deficient_pct=("pct_zinc_deficient", "std"),
        soil_village_sd_ph_alkaline_pct=("pct_ph_alkaline", "std"),
    ).round(3).reset_index()
    return soil.merge(spread, on="district", how="left")


# ---------------------------------------------------------------- 4. irrigation & land use
def load_irrigation() -> tuple[pd.DataFrame, pd.DataFrame]:
    """District-year totals, and crop-wise LUS area / irrigated area."""
    def read(name):
        t = pd.read_csv(RAW / f"des_irrigation/{name}_values.csv", dtype=str)
        t["district"] = t.District.map(des_district)
        t["crop_year"] = t.Year.str[:4] + "-" + t.Year.str[-2:]
        return t[t.district.notna()]  # drops the pre-2000 Uttarakhand districts

    src, area, irr = read("sources"), read("crop_area"), read("crop_irr")
    # sources: 9 net-irrigated columns, then the same 9 for gross irrigated
    district = pd.DataFrame({
        "district": src.district, "crop_year": src.crop_year,
        "irr_net_irrigated_area_ha": to_number(src.col_009, True),
        "irr_gross_irrigated_area_ha": to_number(src.col_018, True),
        "irr_nia_canal_ha": to_number(src.col_003, True),
        "irr_nia_tank_ha": to_number(src.col_004, True),
        "irr_nia_tubewell_ha": to_number(src.col_005, True),
        "irr_nia_other_wells_ha": to_number(src.col_006, True),
        "irr_nia_other_sources_ha": to_number(src.col_008, True),
    })
    land = pd.DataFrame({
        "district": area.district, "crop_year": area.crop_year,
        "land_net_sown_area_ha": to_number(area.col_169, True),
        "land_gross_cropped_area_ha": to_number(area.col_167, True),
    })
    district = district.merge(land, on=["district", "crop_year"], how="outer")

    crop_rows = []
    for lus_crop, (area_col, irr_col) in LUS_COLUMNS.items():
        a = pd.DataFrame({"district": area.district, "crop_year": area.crop_year,
                          "irr_lus_crop_area_ha": to_number(area[area_col], True)})
        i = pd.DataFrame({"district": irr.district, "crop_year": irr.crop_year,
                          "irr_lus_crop_irrigated_ha": to_number(irr[irr_col], True)})
        crop_rows.append(a.merge(i, on=["district", "crop_year"], how="outer").assign(lus_crop=lus_crop))
    return district, pd.concat(crop_rows, ignore_index=True)


# ---------------------------------------------------------------- 5. prices
HARVEST_WINDOWS = {  # (year offset from crop-year start, month)
    "Kharif": [(0, 10), (0, 11), (0, 12)],   # Oct-Dec Y
    "Rabi": [(1, 3), (1, 4), (1, 5)],        # Mar-May Y+1
    "Summer": [(1, 6), (1, 7), (1, 8)],      # Jun-Aug Y+1
}


def load_prices() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    mandi_to_des = {}
    for r in DISTRICTS.itertuples():
        for name in str(r.mandi).split("; "):
            if name and name != "nan":
                mandi_to_des[name] = r.district
    frames = []
    for crop, (_, _, commodity) in CROPS.items():
        if not commodity:
            continue
        for name in [commodity] + RENAMED.get(commodity, []):
            for f in glob.glob(str(RAW / f"mandi_prices/{folder(name)}/*.csv")):
                d = pd.read_csv(f, usecols=["Commodity", "District", "Market", "Arrival_Date", "Modal_Price"], dtype=str)
                d["crop"] = crop
                frames.append(d)
    p = pd.concat(frames, ignore_index=True)
    p["district"] = p.District.map(mandi_to_des)
    p["date"] = pd.to_datetime(p.Arrival_Date, format="%d/%m/%Y", errors="coerce")
    p["price"] = pd.to_numeric(p.Modal_Price, errors="coerce")
    p = p[(p.price > 0) & p.date.notna() & p.district.notna()]  # 0 is not a price
    p["year"], p["month"] = p.date.dt.year, p.date.dt.month

    monthly = (p.groupby(["district", "crop", "year", "month"])
                .agg(commodity=("Commodity", lambda names: "; ".join(sorted(names.unique()))),
                     modal_price_median=("price", "median"), records=("price", "size"), markets=("Market", "nunique"))
                .reset_index())
    monthly = monthly[["district", "crop", "commodity", "year", "month", "modal_price_median", "records", "markets"]]

    windowed = assign_windows(p[["district", "crop", "price", "year", "month"]], HARVEST_WINDOWS, "year", "month")
    district = (windowed.groupby(["district", "crop", "season", "crop_year_start"])
                .agg(price_harvest_district_median=("price", "median"), price_harvest_district_records=("price", "size"))
                .reset_index())
    # the state price applies to every district, including ones without a mandi
    state = (windowed.groupby(["crop", "season", "crop_year_start"])
             .agg(price_harvest_state_median=("price", "median")).reset_index())
    return monthly, district, state


# ---------------------------------------------------------------- column guide
COLUMN_GUIDE = [  # (prefix or exact name, group, source, meaning, caution)
    ("crop_year", "key", "DES", "Agricultural year, e.g. 2015-16 (Jul 2015 - Jun 2016)", ""),
    ("crop_year_start", "key", "DES", "First calendar year of the crop year", ""),
    ("district", "key", "district_master", "Standard (DES) district name", "drop before training"),
    ("season", "key", "DES", "Kharif / Rabi / Summer / Whole Year", ""),
    ("crop", "key", "DES", "Crop name (DES spelling)", ""),
    ("crop_group", "key", "crop_master", "Cereals, Pulses, Oilseeds, Cash crops, Vegetables & spices", ""),
    ("area_ha", "crop statistics", "DES / UPAg", "Area under the crop, hectares", "LEAKAGE: yield is computed from it"),
    ("production_t", "crop statistics", "DES / UPAg", "Production, tonnes", "LEAKAGE: yield is computed from it"),
    ("yield_t_per_ha", "TARGET", "DES / UPAg", "Yield, tonnes per hectare (as published)", "target of the yield model"),
    ("data_source", "crop statistics", "", "Which source the crop row came from", "drop before training"),
    ("loc_", "location", "geocoder", "Latitude/longitude of the district HQ town", ""),
    ("w_", "weather", "NASA POWER daily (soil wetness: external package)",
     "Season weather; window for crop year Y: Kharif Jun-Oct Y, Rabi Nov Y-Mar Y+1, Summer Apr-Jun Y+1, Whole Year Jul Y-Jun Y+1", ""),
    ("soil_village", "soil", "external package (village level, 2023-25)", "Standard deviation across villages of the % of samples in a class", "static per district"),
    ("soil_villages_tested", "soil", "external package", "Villages with soil tests", "static per district"),
    ("soil_samples_tested", "soil", "Soil Health Card API", "Soil samples tested, 2023-24 to 2025-26", "static per district"),
    ("soil_", "soil", "Soil Health Card API", "Share (0-1) of tested samples in the class, cycles 2023-24 to 2025-26 pooled", "static per district"),
    ("irr_lus_crop", "irrigation", "DES Land Use Statistics", "Area / irrigated area of this crop (or its LUS group) in the district, ha", "LUS area differs a little from DES area"),
    ("irr_", "irrigation", "DES Land Use Statistics", "District net/gross irrigated area and net irrigated area by source, ha", ""),
    ("land_", "land use", "DES Land Use Statistics", "District net sown area and gross cropped area, ha", ""),
    ("price_harvest_district", "price", "Agmarknet", "Median daily modal price (Rs/quintal) in the district's mandis in the harvest window: Kharif Oct-Dec Y, Rabi Mar-May Y+1, Summer Jun-Aug Y+1", "LEAKAGE for the yield model (known only after harvest)"),
    ("price_harvest_state", "price", "Agmarknet", "Same, all UP mandis together", "LEAKAGE for the yield model (known only after harvest)"),
]


def describe_columns(master: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in master.columns:
        # the longest guide entry that the column name starts with
        matches = [g for g in COLUMN_GUIDE if col.startswith(g[0])]
        key, group, source, meaning, caution = max(matches, key=lambda g: len(g[0]), default=("", "", "", "", ""))
        rows.append({"column": col, "group": group, "source": source, "meaning": meaning, "caution": caution,
                     "missing_pct": round(master[col].isna().mean() * 100, 1)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- assemble
def main() -> None:
    print("crop statistics...", flush=True)
    master = load_crop_statistics()
    print("weather...", flush=True)
    weather = load_weather()
    print("soil...", flush=True)
    soil = load_soil()
    print("irrigation...", flush=True)
    irr_district, irr_crop = load_irrigation()
    print("prices...", flush=True)
    monthly, harvest_district, harvest_state = load_prices()

    coords = pd.read_csv(RAW / "up_district_coords.csv").rename(columns={"district_name": "nasa_weather_file"})
    coords = coords.merge(DISTRICTS[["district", "nasa_weather_file"]], on="nasa_weather_file")
    coords = coords[["district", "latitude", "longitude"]].rename(columns={"latitude": "loc_hq_latitude", "longitude": "loc_hq_longitude"})

    master["lus_crop"] = [lus_crop_for(c, s) for c, s in zip(master.crop, master.season)]
    n = len(master)
    master = (master
              .merge(coords, on="district", how="left")
              .merge(weather, on=["district", "season", "crop_year_start"], how="left")
              .merge(soil, on="district", how="left")
              .merge(irr_district, on=["district", "crop_year"], how="left")
              .merge(irr_crop, on=["district", "crop_year", "lus_crop"], how="left")
              .merge(harvest_district, on=["district", "crop", "season", "crop_year_start"], how="left")
              .merge(harvest_state, on=["crop", "season", "crop_year_start"], how="left"))
    assert len(master) == n, "a join duplicated rows"
    master = master.drop(columns="lus_crop")  # the crop -> LUS mapping is listed in crop_master.csv
    master = master.sort_values(["crop_year_start", "district", "season", "crop"]).reset_index(drop=True)

    crop_master = pd.DataFrame([{"crop": c, "crop_group": g, "lus_irrigation_crop": "; ".join(f"{k}: {v}" for k, v in rule.items()),
                                 "mandi_commodity": "; ".join([commodity] + RENAMED.get(commodity, [])) if commodity else ""} for c, (g, rule, commodity) in CROPS.items()])

    OUT.mkdir(exist_ok=True)
    master.to_csv(OUT / "master_table.csv", index=False)
    describe_columns(master).to_csv(OUT / "master_table_columns.csv", index=False)
    monthly.sort_values(["crop", "district", "year", "month"]).to_csv(OUT / "price_monthly.csv", index=False)
    crop_master.to_csv(OUT / "crop_master.csv", index=False)
    print(f"\nmaster_table.csv: {master.shape[0]:,} rows x {master.shape[1]} columns")
    print(f"price_monthly.csv: {len(monthly):,} rows")


if __name__ == "__main__":
    main()
