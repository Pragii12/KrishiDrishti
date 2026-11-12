"""The one place a user interface talks to the saved models.

notebooks/1_Main.ipynb trains the yield model and writes models/model_a.joblib.
notebooks/2_PricingModel.ipynb trains the price model and writes models/model_b.joblib.
notebooks/3_CostEstimate.ipynb projects the cost of cultivation, builds the profit range and writes
models/cost.joblib.
notebooks/4_AgronomyRules.ipynb builds the agronomy rules and writes models/rules.joblib.
Each model file holds the fitted pipeline together with everything needed to use
it: the feature rows for the next season, the prediction range of every crop and
the list of reliable crops. A user interface only calls the functions below,
so retraining or changing a model in its notebook needs no change here or in
the interface.

    from src.predict import districts, seasons, predict_yields, predict_prices, estimate_costs, check_crops, recommend_crops
    recommend_crops("Agra", "Rabi", farmer_yields={"Wheat": 3.6}, irrigated=True)
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from . import history  # noqa: F401  (the saved model is a src.history.HistoryAdjustedRegressor)
from . import rules

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model_a.joblib"
PRICE_MODEL_PATH = MODEL_PATH.with_name("model_b.joblib")
COST_PATH = MODEL_PATH.with_name("cost.joblib")
RULES_PATH = MODEL_PATH.with_name("rules.joblib")
FARM_FACTOR_LIMITS = (0.5, 2.0)
# Yield statistics count rice as milled rice, while mandis and the MSP price it as paddy.
# Official conversion: rice is two thirds of paddy, so 1 tonne of rice is sold as 1.5 tonnes of paddy.
SOLD_TONNES_PER_TONNE_OF_YIELD = {"Rice": 1.5}


@lru_cache(maxsize=4)
def load_model(path: str | Path = MODEL_PATH) -> dict:
    return joblib.load(path)


def districts() -> list[str]:
    return sorted(load_model()["next_season"]["district"].unique())


def seasons(district: str) -> list[str]:
    rows = load_model()["next_season"]
    return sorted(rows.loc[rows["district"] == district, "season"].unique())


def farm_adjust(table: pd.DataFrame, farmer_yields: dict[str, float] | None) -> pd.DataFrame:
    """Scale district predictions by how the farmer's usual yield compares with the district's.

    `table` is indexed by crop and has recent_average_t_ha, predicted_t_ha and the range columns.
    Crops the farmer has grown use their own ratio; the other crops use the average of those
    ratios, so that all crops are compared on the same footing.
    """
    table = table.copy()
    own = (pd.Series(farmer_yields or {}, dtype=float) / table["recent_average_t_ha"]).dropna().clip(*FARM_FACTOR_LIMITS)
    farm_factor = own.mean() if len(own) else 1.0
    table["farm_factor"] = own.reindex(table.index).fillna(farm_factor).round(2)
    table["basis"] = np.where(table.index.isin(own.index), "farmer's own yield",
                              "farmer's other crops" if len(own) else "district average")
    for col in ["predicted_t_ha", "range_low_t_ha", "range_high_t_ha"]:
        table["farm_" + col] = (table[col] * table["farm_factor"]).round(2)
    return table


def predict_yields(district: str, season: str, farmer_yields: dict[str, float] | None = None) -> pd.DataFrame:
    """Expected yield of every candidate crop for the next season, best first.

    farmer_yields: optional {crop: the farmer's usual yield in t/ha}.
    """
    bundle = load_model()
    rows = bundle["next_season"]
    rows = rows[(rows["district"] == district) & (rows["season"] == season)]
    if rows.empty:
        return pd.DataFrame()

    predicted = bundle["model"].predict(rows[bundle["feature_columns"]])
    ranges = bundle["crop_range"].reindex(rows["crop"])
    low = ranges["low"].fillna(bundle["pooled_range"]["low"]).to_numpy()
    high = ranges["high"].fillna(bundle["pooled_range"]["high"]).to_numpy()
    table = pd.DataFrame({
        "crop": rows["crop"].to_numpy(),
        "crop_year": bundle["next_season_label"],
        "recent_average_t_ha": rows["yield_recent_mean"].round(2).to_numpy(),
        "predicted_t_ha": predicted.round(2),
        "range_low_t_ha": (predicted * np.exp(low)).round(2),
        "range_high_t_ha": (predicted * np.exp(high)).round(2),
        "reliable": rows["crop"].isin(bundle["reliable_crops"]).to_numpy(),
    }).set_index("crop")
    return farm_adjust(table, farmer_yields).sort_values("farm_predicted_t_ha", ascending=False)


def predict_prices(district: str, season: str) -> pd.DataFrame:
    """Expected harvest price (Rs per quintal) of every priced crop for the next season."""
    bundle = load_model(PRICE_MODEL_PATH)
    rows = bundle["next_season"]
    rows = rows[(rows["district"] == district) & (rows["season"] == season)]
    if rows.empty:
        return pd.DataFrame()

    predicted = bundle["model"].predict(rows[bundle["feature_columns"]])
    ranges = bundle["crop_range"].reindex(rows["crop"])
    low = ranges["low"].fillna(bundle["pooled_range"]["low"]).to_numpy()
    high = ranges["high"].fillna(bundle["pooled_range"]["high"]).to_numpy()
    table = pd.DataFrame({
        "crop": rows["crop"].to_numpy(),
        "price_year": bundle["next_season_label"],
        "last_harvest_price": rows["price_last_harvest"].round(0).to_numpy(),
        "predicted_price": predicted.round(0),
        "price_range_low": (predicted * np.exp(low)).round(0),
        "price_range_high": (predicted * np.exp(high)).round(0),
        "price_basis": np.where(rows["last_is_district"] == 1, "district mandis", "state average"),
        "price_reliable": rows["crop"].isin(bundle["reliable_crops"]).to_numpy(),
    }).set_index("crop")
    return table.sort_values("predicted_price", ascending=False)


def estimate_costs() -> pd.DataFrame:
    """Expected cost of cultivation (Rs per hectare) of every surveyed crop for the coming season.

    The figures are Uttar Pradesh averages from the official cost survey, projected to the coming
    season. cost_rs_per_ha is the paid-out cost plus the value of the family's own labour (A2+FL).
    """
    bundle = load_model(COST_PATH)
    return bundle["cost"].assign(cost_year=bundle["cost_year_label"])


def profit_range(earnings: float, cost: float, revenue_error, cost_error, interval=(0.10, 0.90)) -> np.ndarray:
    """Low and high end of the profit when every past revenue error meets every past cost error.

    earnings is the revenue plus the by-product. The errors are log(actual / predicted), listed
    at evenly spaced levels, so every combination is equally likely.
    """
    outcomes = earnings * np.exp(np.asarray(revenue_error))[:, None] - cost * np.exp(np.asarray(cost_error))[None, :]
    return np.quantile(outcomes, interval)


def add_profit_range(table: pd.DataFrame, ranges: dict) -> pd.DataFrame:
    """Add profit_range_low and profit_range_high to the crops that have a profit."""
    table = table.assign(profit_range_low=np.nan, profit_range_high=np.nan)
    revenue_error, cost_error = ranges["revenue_error"], ranges["cost_error"]
    for crop, row in table.dropna(subset=["profit_rs_per_ha"]).iterrows():
        errors = revenue_error[crop] if crop in revenue_error else revenue_error["other crops"]
        low, high = profit_range(row["revenue_rs_per_ha"] + row["byproduct_rs_per_ha"], row["cost_rs_per_ha"],
                                 errors, cost_error[crop], ranges["interval"])
        table.loc[crop, ["profit_range_low", "profit_range_high"]] = round(low, -2), round(high, -2)
    return table


def check_crops(district: str, season: str, irrigated: bool | None = None, soil: dict | None = None) -> pd.DataFrame:
    """Agronomy rules for every candidate crop: area_share, irrigation_need, suitable and advice.

    irrigated: whether the farmer's field can be irrigated (True, False, or None when not known).
    soil: optional {"saline": bool, "alkaline": bool} from the farmer's soil health card.
    """
    crops = predict_yields(district, season).index
    return rules.check(load_model(RULES_PATH), district, season, crops, irrigated, soil)


def add_rules(table: pd.DataFrame, district: str, season: str, irrigated: bool | None, soil: dict | None) -> pd.DataFrame:
    """Add suitable and advice; crops that are not suitable move to the end, the order is otherwise kept."""
    try:
        checks = check_crops(district, season, irrigated, soil)
    except FileNotFoundError:
        return table
    table = table.join(checks[["suitable", "advice"]], how="left")
    return table.sort_values("suitable", ascending=False, kind="stable")


def recommend_crops(district: str, season: str, farmer_yields: dict[str, float] | None = None,
                    irrigated: bool | None = None, soil: dict | None = None) -> pd.DataFrame:
    """Candidate crops ranked by expected profit per hectare.

    irrigated and soil are passed to the agronomy rules (see check_crops), which add the columns
    suitable and advice. Crops that are not suitable are listed last.

    profit = quantity sold x price + value of the by-product - cost of cultivation.
    The quantity sold (sold_t_ha) is the yield, except for rice, which is sold as paddy.
    profit_range_low and profit_range_high are built to hold 8 in 10 outcomes of a district
    average; a single farm varies more than that.
    Crops with no cost survey come next, ranked by revenue; crops with no mandi price data are
    listed last, with their yield only.
    """
    yields = predict_yields(district, season, farmer_yields)
    if yields.empty:
        return yields
    yields = yields.rename(columns={"crop_year": "yield_year", "reliable": "yield_reliable"})
    try:
        prices = predict_prices(district, season)
    except FileNotFoundError:
        prices = pd.DataFrame()
    if prices.empty:
        return add_rules(yields, district, season, irrigated, soil)

    table = yields.join(prices, how="left")
    sold = table.index.map(lambda crop: SOLD_TONNES_PER_TONNE_OF_YIELD.get(crop, 1.0))
    table["sold_t_ha"] = (table["farm_predicted_t_ha"] * sold).round(2)
    table["revenue_rs_per_ha"] = (table["sold_t_ha"] * 10 * table["predicted_price"]).round(-2)
    columns = ["yield_year", "farm_predicted_t_ha", "farm_range_low_t_ha", "farm_range_high_t_ha", "yield_reliable", "basis",
               "sold_t_ha",
               "price_year", "predicted_price", "price_range_low", "price_range_high", "price_reliable", "price_basis",
               "revenue_rs_per_ha"]
    try:
        costs = estimate_costs()
    except FileNotFoundError:
        table = table[columns].sort_values("revenue_rs_per_ha", ascending=False, na_position="last")
        return add_rules(table, district, season, irrigated, soil)

    table = table.join(costs[["cost_year", "cost_rs_per_ha", "byproduct_share", "cost_reliable"]], how="left")
    table["byproduct_rs_per_ha"] = (table["revenue_rs_per_ha"] * table["byproduct_share"]).round(-2)
    table["profit_rs_per_ha"] = (table["revenue_rs_per_ha"] + table["byproduct_rs_per_ha"] - table["cost_rs_per_ha"]).round(-2)
    columns += ["byproduct_rs_per_ha", "cost_year", "cost_rs_per_ha", "cost_reliable", "profit_rs_per_ha"]
    ranges = load_model(COST_PATH).get("profit_range")
    if ranges:
        table = add_profit_range(table, ranges)
        columns += ["profit_range_low", "profit_range_high"]
    table = table[columns].sort_values(["profit_rs_per_ha", "revenue_rs_per_ha"], ascending=False, na_position="last")
    return add_rules(table, district, season, irrigated, soil)
