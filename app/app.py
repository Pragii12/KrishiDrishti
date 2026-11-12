"""KrishiDrishti web application (prototype).

Run from the project folder:

    streamlit run app/app.py

The application only calls src/predict.py; every word it shows is in app/texts.py.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "app"))

from src.predict import districts, predict_yields, recommend_crops, seasons  # noqa: E402
from texts import LANGUAGES, RIGHT_TO_LEFT, crop_name, district_name, season_name, t  # noqa: E402

HECTARES_PER_ACRE = 0.4047
TONNES_PER_HA_PER_QUINTAL_PER_ACRE = 0.1 / HECTARES_PER_ACRE
RICE_PER_PADDY = 2 / 3
SEASON_ORDER = ["Kharif", "Rabi", "Summer", "Whole Year"]
TOP_CROPS = 3

GREEN, DARK_GREEN, PALE_GREEN, AMBER, PALE_AMBER = "#15803d", "#14532d", "#ecfdf3", "#b45309", "#fff7ed"

STYLE = f"""
<style>
:root {{ color-scheme: light; }}
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
.stApp {{ background: #ffffff; color: #1f2937; }}
.block-container {{ max-width: 980px; padding-top: 1.2rem; padding-bottom: 3rem; }}
.kd-header {{ background: {GREEN}; color: #ffffff; border-radius: 10px; padding: 18px 22px; margin-bottom: 6px; }}
.kd-header h1 {{ color: #ffffff; font-size: 1.9rem; margin: 0; padding: 0; }}
.kd-header p {{ color: #dcfce7; font-size: 1.05rem; margin: 4px 0 0 0; }}
.kd-steps {{ background: {PALE_GREEN}; border: 1px solid #bbf7d0; border-radius: 10px; padding: 14px 20px; font-size: 1.05rem; }}
.kd-steps b {{ color: {DARK_GREEN}; }}
.kd-steps ol {{ margin: 6px 0 0 0; padding-inline-start: 22px; }}
h3 {{ color: {DARK_GREEN}; border-bottom: 3px solid {GREEN}; padding-bottom: 4px; }}
.kd-card {{ border: 1px solid #d1d5db; border-top: 6px solid {GREEN}; border-radius: 10px; padding: 16px; background: #ffffff;
            height: 100%; margin-bottom: 14px; }}
.kd-rank {{ display: inline-block; background: {GREEN}; color: #ffffff; border-radius: 50%; width: 32px; height: 32px;
            line-height: 32px; text-align: center; font-weight: 700; margin-inline-end: 8px; }}
.kd-crop {{ font-size: 1.5rem; font-weight: 700; color: #111827; }}
.kd-label {{ color: #4b5563; font-size: 0.95rem; margin-top: 12px; }}
.kd-profit {{ font-size: 1.9rem; font-weight: 700; color: {DARK_GREEN}; line-height: 1.2; }}
.kd-range {{ display: flex; gap: 8px; margin-top: 12px; }}
.kd-range div {{ flex: 1; background: #f3f4f6; border-radius: 8px; padding: 8px 10px; font-size: 0.9rem; color: #4b5563; }}
.kd-range span {{ display: block; font-size: 1.1rem; font-weight: 700; color: #111827; }}
.kd-tag {{ border-radius: 8px; padding: 8px 10px; margin-top: 12px; font-weight: 600; font-size: 0.95rem; }}
.kd-safe {{ background: {PALE_GREEN}; color: {DARK_GREEN}; }}
.kd-risk {{ background: {PALE_AMBER}; color: {AMBER}; }}
.kd-note {{ color: #4b5563; font-size: 0.92rem; margin-top: 8px; }}
.kd-foot {{ color: #6b7280; font-size: 0.9rem; border-top: 1px solid #e5e7eb; margin-top: 28px; padding-top: 10px; }}
div.stButton > button {{ background: {GREEN}; color: #ffffff; border: 0; font-size: 1.15rem; font-weight: 700; padding: 0.7rem 1rem; }}
div.stButton > button p {{ font-size: 1.15rem; font-weight: 700; }}
div.stButton > button:hover, div.stButton > button:focus {{ background: {DARK_GREEN}; color: #ffffff; }}
label, .stRadio p, .stCheckbox p {{ font-size: 1.02rem !important; }}
</style>
"""


def rupees(value: float) -> str:
    """Rupees with Indian digit grouping, rounded to the nearest hundred: 134800 -> Rs 1,34,800."""
    value = int(round(value, -2))
    sign, digits = ("-" if value < 0 else ""), str(abs(value))
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return f"{sign}₹ {','.join(groups + [tail])}"


def notes_for(advice: str, lang: str) -> list[str]:
    """The agronomy advice of src/rules.py as short sentences in the chosen language."""
    notes = []
    for marker, key in [("rarely grown", "note_rare"), ("needs irrigation", "note_water"),
                        ("saline soil", "note_saline"), ("alkaline soil", "note_alkaline"),
                        ("yield data ends", "note_old")]:
        if marker in advice:
            notes.append(t(key, lang))
    return notes


def card(rank: int, crop: str, row: pd.Series, hectares: float, land_text: str, lang: str) -> str:
    risky = row["profit_range_low"] < 0
    tag = f'<div class="kd-tag {"kd-risk" if risky else "kd-safe"}">{t("tag_risk" if risky else "tag_safe", lang)}</div>'
    notes = notes_for(row["advice"], lang)
    if not (row["yield_reliable"] and row["price_reliable"]):
        notes.append(t("less_certain", lang))
    notes_html = "".join(f'<div class="kd-note">• {note}</div>' for note in notes)
    return f"""
<div class="kd-card">
  <div><span class="kd-rank">{rank}</span><span class="kd-crop">{crop_name(crop, lang)}</span></div>
  <div class="kd-label">{t("profit", lang)} {land_text}</div>
  <div class="kd-profit">{rupees(row["profit_rs_per_ha"] * hectares)}</div>
  <div class="kd-range">
    <div>{t("bad_year", lang)}<span>{rupees(row["profit_range_low"] * hectares)}</span></div>
    <div>{t("good_year", lang)}<span>{rupees(row["profit_range_high"] * hectares)}</span></div>
  </div>
  {tag}
  {notes_html}
</div>"""


def all_crops_table(table: pd.DataFrame, hectares: float, lang: str) -> pd.DataFrame:
    rows = []
    for crop, row in table.iterrows():
        has_profit = pd.notna(row.get("profit_rs_per_ha"))
        if not row["suitable"]:
            remark = t("remark_no_water", lang)
        elif not has_profit:
            remark = t("remark_no_price", lang)
        else:
            remark = " ".join(notes_for(row["advice"], lang))
        rows.append({
            t("col_crop", lang): crop_name(crop, lang),
            t("profit", lang): rupees(row["profit_rs_per_ha"] * hectares) if has_profit else "-",
            t("bad_year", lang): rupees(row["profit_range_low"] * hectares) if has_profit else "-",
            t("good_year", lang): rupees(row["profit_range_high"] * hectares) if has_profit else "-",
            t("col_remark", lang): remark,
        })
    return pd.DataFrame(rows)


st.set_page_config(page_title="KrishiDrishti", page_icon="🌾", layout="centered")
st.markdown(STYLE, unsafe_allow_html=True)

space, language_box = st.columns([3, 1])
with language_box:
    asked = st.query_params.get("lang", "en")
    lang = st.selectbox("Language / भाषा", list(LANGUAGES), format_func=LANGUAGES.get,
                        index=list(LANGUAGES).index(asked) if asked in LANGUAGES else 0)
if lang in RIGHT_TO_LEFT:
    st.markdown("<style>.block-container { direction: rtl; text-align: right; }</style>", unsafe_allow_html=True)

st.markdown(f'<div class="kd-header"><h1>🌾 {t("title", lang)}</h1><p>{t("tagline", lang)}</p></div>', unsafe_allow_html=True)
st.markdown(f'<div class="kd-steps"><b>{t("how_title", lang)}</b><ol><li>{t("how_1", lang)}</li>'
            f'<li>{t("how_2", lang)}</li><li>{t("how_3", lang)}</li></ol></div>', unsafe_allow_html=True)

st.markdown(f"### {t('farm_title', lang)}")
left, right = st.columns(2)
with left:
    district = st.selectbox(t("district", lang), districts(), format_func=lambda d: district_name(d, lang))
with right:
    season_options = sorted(seasons(district), key=SEASON_ORDER.index)
    season = st.selectbox(t("season", lang), season_options, format_func=lambda s: season_name(s, lang))

left, middle, right = st.columns([2, 1, 3])
with left:
    land = st.number_input(t("land", lang), min_value=0.1, max_value=500.0, value=1.0, step=0.5)
with middle:
    unit = st.selectbox(t("unit", lang), ["acre", "hectare"], format_func=lambda u: t(u, lang))
with right:
    watered = st.radio(t("water", lang), ["yes", "no"], format_func=lambda v: t(v, lang), horizontal=True)

with st.expander(t("more", lang)):
    candidates = list(predict_yields(district, season).index)
    own_crop = st.selectbox(t("own_crop", lang), [None] + candidates,
                            format_func=lambda c: t("none", lang) if c is None else crop_name(c, lang))
    own_yield = st.number_input(t("own_yield", lang), min_value=0.0, max_value=500.0, value=0.0, step=1.0,
                                disabled=own_crop is None)
    st.write(t("soil_card", lang))
    saline = st.checkbox(t("saline", lang))
    alkaline = st.checkbox(t("alkaline", lang))

if st.button(t("button", lang), width="stretch"):
    st.session_state["shown"] = True

if st.session_state.get("shown"):
    hectares = land * HECTARES_PER_ACRE if unit == "acre" else land
    farmer_yields = None
    if own_crop is not None and own_yield > 0:
        tonnes_per_ha = own_yield * TONNES_PER_HA_PER_QUINTAL_PER_ACRE
        farmer_yields = {own_crop: tonnes_per_ha * RICE_PER_PADDY if own_crop == "Rice" else tonnes_per_ha}
    soil = {"saline": saline, "alkaline": alkaline} if (saline or alkaline) else None

    table = recommend_crops(district, season, farmer_yields=farmer_yields, irrigated=watered == "yes", soil=soil)
    ranked = table[table["suitable"] & table["profit_rs_per_ha"].notna()] if "profit_rs_per_ha" in table else table.iloc[0:0]
    land_text = t("on_land", lang, size=f"{land:g}", unit=t(unit, lang))

    st.markdown(f"### {t('result_title', lang)}")
    st.caption(f"{district_name(district, lang)} · {season_name(season, lang)}")
    if ranked.empty:
        st.info(t("no_result", lang))
    else:
        top = ranked.head(TOP_CROPS)
        for column, (rank, (crop, row)) in zip(st.columns(len(top)), enumerate(top.iterrows(), start=1)):
            column.markdown(card(rank, crop, row, hectares, land_text, lang), unsafe_allow_html=True)

    if "profit_rs_per_ha" in table:
        with st.expander(t("all_crops", lang)):
            st.dataframe(all_crops_table(table, hectares, lang), hide_index=True, width="stretch")

    st.markdown(f'<div class="kd-steps"><b>{t("read_title", lang)}</b><ol><li>{t("read_1", lang)}</li>'
                f'<li>{t("read_2", lang)}</li><li>{t("read_3", lang)}</li></ol></div>', unsafe_allow_html=True)

st.markdown(f'<div class="kd-foot">{t("footer", lang)}</div>', unsafe_allow_html=True)
