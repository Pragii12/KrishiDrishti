# KrishiDrishti

Crop recommendation for farmers of Uttar Pradesh. For a district and a season it predicts the
yield and the harvest price of every candidate crop, estimates the cost of cultivation, and
ranks the crops by expected profit per hectare with a low-to-high range.

    profit = quantity sold x price + by-product - cost of cultivation

This is a prototype. The figures are district averages, not a forecast for a single farm.

## Folders

| Folder | Contents |
|---|---|
| `app/` | The Streamlit web application (`app.py`), its words in every language (`texts.py`) and the schemes (`schemes.py`) |
| `notebooks/` | The four notebooks, numbered in the order they are run |
| `src/` | `predict.py` (the only file an application calls), `rules.py`, `history.py` |
| `models/` | Saved models and tables written by the notebooks |
| `scripts/` | Download and build scripts for the data |
| `data/processed/` | Tables built by the scripts and read by the notebooks |
| `data/raw/`, `data/external/` | Downloaded source files (not in git; re-created by the scripts) |

## Notebooks

| Notebook | What it does | Writes |
|---|---|---|
| `1_Main.ipynb` | Yield model (t/ha per crop, district and season) | `models/model_a.joblib` |
| `2_PricingModel.ipynb` | Harvest price model (Rs per quintal) | `models/model_b.joblib` |
| `3_CostEstimate.ipynb` | Cost of cultivation and the profit range | `models/cost.joblib` |
| `4_AgronomyRules.ipynb` | Agronomy rules (irrigation, soil, how widely a crop is grown) | `models/rules.joblib` |

Both models are scikit-learn pipelines (ColumnTransformer + gradient boosting). They are split
into training and test years by time, never randomly, and chosen by cross-validation on the
training years.

| Model | Test years | Predictions within 20% of the actual value |
|---|---|---|
| Yield | 2020-21 to 2024-25 | 76% (90% on the 11 reliable crops) |
| Price | 2020-21 to 2025-26 | 88% |

## Web application

```
streamlit run app/app.py
```

Three pages with a navigation bar: Home (what the prototype is), Find Best Crop (district,
season, land size and irrigation give the three best crops with their profit in a bad and a good
year) and Farmer Schemes (eight central schemes with links to their official websites).
Languages: English, Hindi, Urdu, Bhojpuri and Awadhi. The page and language are kept in the
address, for example `?page=crops&lang=hi`.

This is a student prototype and not an official Government website. Its recommendations are
estimates for information only.

## Using the models

```python
from src.predict import districts, seasons, recommend_crops

recommend_crops("Agra", "Rabi", farmer_yields={"Wheat": 3.6}, irrigated=True)
```

Only the district and the season are required. The farmer's usual yield, whether the field can
be irrigated, and the soil card result are optional.

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`scripts/download_mandi_prices.py` needs a data.gov.in API key in the environment variable
`DATA_GOV_IN_API_KEY`. The key is never stored in this repository.

## Data sources

Directorate of Economics and Statistics (crop area, production, yield, irrigation, cost of
cultivation), Agmarknet through data.gov.in (mandi prices), NASA POWER (weather), Soil Health
Card scheme (soil), Government of India MSP notifications.

## Known limits

- Cost is one Uttar Pradesh average per crop, from a survey ending 2021-22.
- Potato prices are predicted poorly; 18 crops have a yield but no price.
- The crop lists for saline and alkaline soil sensitivity were typed in and are not yet verified.
- Yield is predicted for 2025-26, price and cost for 2026-27.
