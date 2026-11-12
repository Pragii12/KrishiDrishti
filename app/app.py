"""KrishiDrishti web application (prototype).

Run from the project folder:

    streamlit run app/app.py

Pages: Home, Find Best Crop, Farmer Schemes. The page and the language are kept in the address
(?page=crops&lang=hi). The application only calls src/predict.py; every word it shows is in
app/texts.py and the schemes are in app/schemes.py.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "app"))

from src.predict import districts, predict_yields, recommend_crops, seasons  # noqa: E402
from schemes import SCHEMES  # noqa: E402
from texts import CROPS, LANGUAGES, RIGHT_TO_LEFT, crop_name, district_name, pick, season_name, t  # noqa: E402

HECTARES_PER_ACRE = 0.4047
TONNES_PER_HA_PER_QUINTAL_PER_ACRE = 0.1 / HECTARES_PER_ACRE
RICE_PER_PADDY = 2 / 3
SEASON_ORDER = ["Kharif", "Rabi", "Summer", "Whole Year"]
TOP_CROPS = 3
PAGES = ["home", "crops", "schemes"]
YEARS_OF_RECORDS = 27

GREEN, DARK_GREEN, PALE_GREEN = "#15803d", "#14532d", "#ecfdf3"
AMBER, PALE_AMBER, NAVY, SAFFRON = "#b45309", "#fff7ed", "#1e3a5f", "#ff9933"

STYLE = f"""
<style>
:root {{ color-scheme: light; }}
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
.stApp {{ background: #f8fafc; color: #1f2937; }}
.block-container {{ max-width: 1080px; padding-top: 0.6rem; padding-bottom: 2rem; }}
a, a:hover, .kd-nav a, .kd-btn, .kd-scheme, .kd-scheme * {{ text-decoration: none !important; }}
.kd-strip {{ background: {NAVY}; color: #e5e7eb; font-size: 0.85rem; padding: 6px 16px; border-radius: 6px 6px 0 0;
            display: flex; justify-content: space-between; flex-wrap: wrap; gap: 6px; }}
.kd-tricolour {{ height: 5px; background: linear-gradient(to right, {SAFFRON} 33.3%, #ffffff 33.3% 66.6%, #138808 66.6%); }}
.kd-brand {{ display: flex; align-items: center; gap: 14px; padding: 12px 4px 6px 4px; }}
.kd-logo {{ width: 62px; height: 62px; border-radius: 50%; background: {PALE_GREEN}; border: 3px solid {GREEN};
           display: flex; align-items: center; justify-content: center; font-size: 2rem; flex-shrink: 0; }}
.kd-brand-name {{ font-size: 1.9rem; font-weight: 800; color: {DARK_GREEN}; line-height: 1.15; }}
.kd-brand-tag {{ color: #4b5563; font-size: 1rem; }}
.kd-nav {{ background: {GREEN}; border-radius: 6px; display: flex; flex-wrap: wrap; margin: 4px 0 18px 0; overflow: hidden; }}
.kd-nav a {{ color: #ffffff !important; font-weight: 700; font-size: 1.05rem; padding: 13px 22px; display: block; }}
.kd-nav a:hover {{ background: {DARK_GREEN}; }}
.kd-nav a.kd-active {{ background: {DARK_GREEN}; box-shadow: inset 0 -4px 0 {SAFFRON}; }}
.kd-hero {{ background: linear-gradient(120deg, {DARK_GREEN}, {GREEN}); color: #ffffff; border-radius: 12px; padding: 34px 30px; }}
.kd-hero h1 {{ color: #ffffff; font-size: 2.1rem; margin: 0 0 10px 0; padding: 0; }}
.kd-hero p {{ color: #dcfce7; font-size: 1.15rem; margin: 0 0 20px 0; max-width: 720px; }}
.kd-btn {{ display: inline-block; padding: 12px 22px; border-radius: 8px; font-weight: 700; font-size: 1.05rem; margin: 4px 8px 4px 0; }}
.kd-btn-light {{ background: #ffffff; color: {DARK_GREEN} !important; }}
.kd-btn-line {{ border: 2px solid #ffffff; color: #ffffff !important; }}
.kd-btn-green {{ background: {GREEN}; color: #ffffff !important; }}
.kd-btn:hover {{ opacity: 0.9; }}
.kd-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; margin: 18px 0; }}
.kd-stat {{ background: {PALE_GREEN}; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; text-align: center; }}
.kd-stat b {{ display: block; font-size: 2rem; color: {DARK_GREEN}; }}
.kd-stat span {{ color: #374151; font-size: 0.95rem; }}
.kd-section {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 18px 22px; margin: 14px 0; }}
.kd-section h2 {{ color: {DARK_GREEN}; font-size: 1.4rem; border-bottom: 3px solid {GREEN}; padding: 0 0 6px 0; margin: 0 0 10px 0; }}
.kd-section p {{ font-size: 1.05rem; margin: 0; }}
.kd-works {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }}
.kd-work {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; }}
.kd-work .kd-rank {{ margin-bottom: 8px; }}
.kd-work b {{ display: block; font-size: 1.08rem; color: #111827; margin-bottom: 4px; }}
.kd-steps {{ background: {PALE_GREEN}; border: 1px solid #bbf7d0; border-radius: 10px; padding: 14px 20px; font-size: 1.05rem; margin: 10px 0; }}
.kd-steps b {{ color: {DARK_GREEN}; }}
.kd-steps ol {{ margin: 6px 0 0 0; padding-inline-start: 22px; }}
.kd-warning {{ background: {PALE_AMBER}; border: 1px solid #fdba74; border-inline-start: 8px solid {AMBER}; border-radius: 10px;
              padding: 14px 18px; margin: 14px 0; display: flex; gap: 14px; align-items: flex-start; }}
.kd-warning .kd-sign {{ font-size: 2.2rem; line-height: 1; }}
.kd-warning b {{ color: {AMBER}; font-size: 1.1rem; display: block; margin-bottom: 4px; }}
.kd-years {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-top: 8px; }}
.kd-year {{ border-radius: 10px; padding: 12px 14px; font-size: 1rem; }}
.kd-year b {{ display: block; font-size: 1.1rem; margin-bottom: 4px; }}
.kd-year-bad {{ background: {PALE_AMBER}; border: 1px solid #fdba74; }}
.kd-year-bad b {{ color: {AMBER}; }}
.kd-year-good {{ background: {PALE_GREEN}; border: 1px solid #bbf7d0; }}
.kd-year-good b {{ color: {DARK_GREEN}; }}
h3 {{ color: {DARK_GREEN}; border-bottom: 3px solid {GREEN}; padding-bottom: 4px; }}
.kd-card {{ border: 1px solid #d1d5db; border-top: 6px solid {GREEN}; border-radius: 10px; padding: 16px; background: #ffffff;
            margin-bottom: 14px; }}
.kd-rank {{ display: inline-block; background: {GREEN}; color: #ffffff; border-radius: 50%; width: 32px; height: 32px;
            line-height: 32px; text-align: center; font-weight: 700; margin-inline-end: 8px; }}
.kd-crop {{ font-size: 1.35rem; font-weight: 700; color: #111827; }}
.kd-label {{ color: #4b5563; font-size: 0.95rem; margin-top: 12px; }}
.kd-profit {{ font-size: 1.9rem; font-weight: 700; color: {DARK_GREEN}; line-height: 1.2; }}
.kd-range {{ display: flex; gap: 8px; margin-top: 12px; }}
.kd-range div {{ flex: 1; background: #f3f4f6; border-radius: 8px; padding: 8px 10px; font-size: 0.9rem; color: #4b5563; }}
.kd-range span {{ display: block; font-size: 1.1rem; font-weight: 700; color: #111827; }}
.kd-tag {{ border-radius: 8px; padding: 8px 10px; margin-top: 12px; font-weight: 600; font-size: 0.95rem; }}
.kd-safe {{ background: {PALE_GREEN}; color: {DARK_GREEN}; }}
.kd-risk {{ background: {PALE_AMBER}; color: {AMBER}; }}
.kd-note {{ color: #4b5563; font-size: 0.92rem; margin-top: 8px; }}
.kd-schemes {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 16px; margin: 14px 0; }}
.kd-scheme {{ position: relative; overflow: hidden; display: block; height: 200px; background: #ffffff; border: 1px solid #d1d5db;
              border-top: 6px solid {GREEN}; border-radius: 10px; padding: 18px 16px; color: #111827 !important;
              transition: box-shadow 0.2s, transform 0.2s; }}
.kd-scheme:hover {{ box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15); transform: translateY(-3px); }}
.kd-scheme-icon {{ width: 64px; height: 64px; border-radius: 50%; background: {PALE_GREEN}; border: 2px solid #bbf7d0;
                   display: flex; align-items: center; justify-content: center; font-size: 2rem; margin-bottom: 14px; }}
.kd-scheme-name {{ font-size: 1.15rem; font-weight: 700; line-height: 1.3; }}
.kd-slide {{ position: absolute; left: 0; right: 0; bottom: 0; height: 100%; background: {DARK_GREEN}; color: #ffffff;
             padding: 18px 16px; transform: translateY(101%); transition: transform 0.3s ease; display: flex;
             flex-direction: column; justify-content: space-between; }}
.kd-scheme:hover .kd-slide, .kd-scheme:focus .kd-slide {{ transform: translateY(0); }}
.kd-slide b {{ font-size: 1.05rem; }}
.kd-slide p {{ font-size: 0.98rem; margin: 6px 0 0 0; color: #dcfce7; }}
.kd-slide span {{ color: {SAFFRON}; font-weight: 700; font-size: 0.95rem; }}
.kd-detail-head {{ display: flex; align-items: center; gap: 14px; margin-bottom: 8px; }}
.kd-detail-head .kd-scheme-icon {{ margin: 0; flex-shrink: 0; }}
.kd-detail-head h2 {{ border: 0; margin: 0; padding: 0; }}
.kd-detail b {{ color: {DARK_GREEN}; font-size: 1.08rem; display: block; margin-top: 12px; }}
.kd-foot {{ background: {NAVY}; color: #e5e7eb; font-size: 0.9rem; border-radius: 0 0 6px 6px; margin-top: 28px; padding: 14px 18px; }}
.kd-foot b {{ color: #ffffff; }}
div.stButton > button {{ background: {GREEN}; color: #ffffff; border: 0; padding: 0.7rem 1rem; }}
div.stButton > button p {{ font-size: 1.15rem; font-weight: 700; }}
div.stButton > button:hover, div.stButton > button:focus {{ background: {DARK_GREEN}; color: #ffffff; }}
label, .stRadio p, .stCheckbox p {{ font-size: 1.02rem !important; }}
</style>
"""


def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def link(page: str, lang: str, **extra) -> str:
    query = "&".join([f"page={page}", f"lang={lang}", *[f"{key}={value}" for key, value in extra.items()]])
    return f"?{query}"


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


def warning_box(lang: str) -> str:
    return (f'<div class="kd-warning"><div class="kd-sign">⚠️</div><div><b>{t("warn_title", lang)}</b>'
            f'{t("warn_text", lang)}</div></div>')


def header(page: str, lang: str) -> None:
    """The top of every page: language box, brand and navigation bar."""
    html(f'<div class="kd-strip"><span>{t("strip", lang)}</span><span>{t("not_official", lang)}</span></div>'
         '<div class="kd-tricolour"></div>')
    brand, language_box = st.columns([4, 1])
    with language_box:
        chosen = st.selectbox("Language / भाषा", list(LANGUAGES), format_func=LANGUAGES.get,
                              index=list(LANGUAGES).index(lang))
    if chosen != lang:
        st.query_params["lang"] = chosen
        st.rerun()
    with brand:
        html(f'<div class="kd-brand"><div class="kd-logo">🌾</div><div><div class="kd-brand-name">{t("title", lang)}</div>'
             f'<div class="kd-brand-tag">{t("tagline", lang)}</div></div></div>')
    items = "".join(f'<a href="{link(name, lang)}" target="_self" class="{"kd-active" if name == page else ""}">'
                    f'{t("nav_" + name, lang)}</a>' for name in PAGES)
    html(f'<div class="kd-nav">{items}</div>')


def footer(lang: str) -> None:
    html(f'<div class="kd-foot"><b>{t("title", lang)}</b> · {t("not_official", lang)}<br>{t("footer", lang)}</div>')


def home_page(lang: str) -> None:
    html(f'<div class="kd-hero"><h1>{t("hero_title", lang)}</h1><p>{t("hero_text", lang)}</p>'
         f'<a class="kd-btn kd-btn-light" href="{link("crops", lang)}" target="_self">{t("btn_crops", lang)}</a>'
         f'<a class="kd-btn kd-btn-line" href="{link("schemes", lang)}" target="_self">{t("btn_schemes", lang)}</a></div>')
    stats = [(len(districts()), "stat_districts"), (len(CROPS), "stat_crops"),
             (YEARS_OF_RECORDS, "stat_years"), (len(LANGUAGES), "stat_languages")]
    html('<div class="kd-stats">' + "".join(f'<div class="kd-stat"><b>{number}</b><span>{t(key, lang)}</span></div>'
                                            for number, key in stats) + "</div>")
    html(f'<div class="kd-section"><h2>{t("about_title", lang)}</h2><p>{t("about_text", lang)}</p></div>')
    works = "".join(f'<div class="kd-work"><span class="kd-rank">{step}</span><b>{t(f"works_{step}_title", lang)}</b>'
                    f'{t(f"works_{step}_text", lang)}</div>' for step in (1, 2, 3))
    html(f'<div class="kd-section"><h2>{t("works_title", lang)}</h2><div class="kd-works">{works}</div></div>')
    html(warning_box(lang))


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
    return (f'<div class="kd-card"><div><span class="kd-rank">{rank}</span><span class="kd-crop">{crop_name(crop, lang)}</span></div>'
            f'<div class="kd-label">{t("profit", lang)} {land_text}</div>'
            f'<div class="kd-profit">{rupees(row["profit_rs_per_ha"] * hectares)}</div>'
            f'<div class="kd-range"><div>{t("bad_year", lang)}<span>{rupees(row["profit_range_low"] * hectares)}</span></div>'
            f'<div>{t("good_year", lang)}<span>{rupees(row["profit_range_high"] * hectares)}</span></div></div>'
            f'{tag}{notes_html}</div>')


def years_box(lang: str) -> str:
    return (f'<div class="kd-section"><h2>{t("year_title", lang)}</h2><div class="kd-years">'
            f'<div class="kd-year kd-year-bad"><b>🌧️ {t("bad_year", lang)}</b>{t("year_bad", lang)}</div>'
            f'<div class="kd-year kd-year-good"><b>☀️ {t("good_year", lang)}</b>{t("year_good", lang)}</div></div>'
            f'<p style="margin-top:10px">{t("year_between", lang)}</p></div>')


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


def crops_page(lang: str) -> None:
    html(f'<div class="kd-steps"><b>{t("how_title", lang)}</b><ol><li>{t("how_1", lang)}</li>'
         f'<li>{t("how_2", lang)}</li><li>{t("how_3", lang)}</li></ol></div>')

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
    if not st.session_state.get("shown"):
        html(warning_box(lang))
        return

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
    html(warning_box(lang))
    if ranked.empty:
        st.info(t("no_result", lang))
    else:
        top = ranked.head(TOP_CROPS)
        for column, (rank, (crop, row)) in zip(st.columns(len(top)), enumerate(top.iterrows(), start=1)):
            column.markdown(card(rank, crop, row, hectares, land_text, lang), unsafe_allow_html=True)
        html(years_box(lang))

    if "profit_rs_per_ha" in table:
        with st.expander(t("all_crops", lang)):
            st.dataframe(all_crops_table(table, hectares, lang), hide_index=True, width="stretch")

    html(f'<div class="kd-steps"><b>{t("read_title", lang)}</b><ol><li>{t("read_1", lang)}</li>'
         f'<li>{t("read_3", lang)}</li></ol></div>')


def schemes_page(lang: str, chosen: str | None) -> None:
    scheme = next((item for item in SCHEMES if item["id"] == chosen), None)
    if scheme is not None:
        html(f'<a class="kd-btn kd-btn-green" href="{link("schemes", lang)}" target="_self">{t("scheme_back", lang)}</a>')
        parts = "".join(f'<b>{t(key, lang)}</b>{pick(scheme[field], lang)}'
                        for key, field in [("scheme_benefit", "benefit"), ("scheme_who", "who"), ("scheme_how", "how")])
        html(f'<div class="kd-section kd-detail"><div class="kd-detail-head"><div class="kd-scheme-icon">{scheme["icon"]}</div>'
             f'<h2>{pick(scheme["name"], lang)}</h2></div><p>{pick(scheme["short"], lang)}</p>{parts}</div>')
        st.link_button(f'{t("scheme_visit", lang)}: {scheme["url"]}', scheme["url"], type="primary", width="stretch")
        html(f'<div class="kd-warning"><div class="kd-sign">⚠️</div><div>{t("schemes_note", lang)}</div></div>')
        return

    html(f'<div class="kd-section"><h2>{t("schemes_title", lang)}</h2><p>{t("schemes_intro", lang)}</p></div>')
    cards = "".join(
        f'<a class="kd-scheme" href="{link("schemes", lang, scheme=item["id"])}" target="_self">'
        f'<div class="kd-scheme-icon">{item["icon"]}</div><div class="kd-scheme-name">{pick(item["name"], lang)}</div>'
        f'<div class="kd-slide"><div><b>{pick(item["name"], lang)}</b><p>{pick(item["short"], lang)}</p></div>'
        f'<span>{t("scheme_more", lang)}</span></div></a>' for item in SCHEMES)
    html(f'<div class="kd-schemes">{cards}</div>')
    html(f'<div class="kd-warning"><div class="kd-sign">⚠️</div><div>{t("schemes_note", lang)}</div></div>')


st.set_page_config(page_title="KrishiDrishti", page_icon="🌾", layout="centered")
html(STYLE)

asked_lang, asked_page = st.query_params.get("lang", "en"), st.query_params.get("page", "home")
lang = asked_lang if asked_lang in LANGUAGES else "en"
page = asked_page if asked_page in PAGES else "home"
if lang in RIGHT_TO_LEFT:
    html("<style>.block-container { direction: rtl; text-align: right; }</style>")

header(page, lang)
if page == "crops":
    crops_page(lang)
elif page == "schemes":
    schemes_page(lang, st.query_params.get("scheme"))
else:
    home_page(lang)
footer(lang)
