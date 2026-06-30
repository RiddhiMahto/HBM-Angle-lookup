import streamlit as st
import pandas as pd
import os
import textwrap
from icons_data import ICONS_B64

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="JUARISTI Milling Head Angle Lookup",
    page_icon="⚙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def _find_data_path():
    here = os.path.dirname(__file__)
    candidates = [
        os.path.join(here, "data", "angles.csv"),  # nested layout
        os.path.join(here, "angles.csv"),           # flat layout (e.g. GitHub web upload)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]  # fall back to nested path; will raise a clear error if missing

DATA_PATH = _find_data_path()

ORIENTATION_INFO = {
    "RIGHT-DOWN": {"icon": "↘", "label": "Right-Down"},
    "LEFT-DOWN":  {"icon": "↙", "label": "Left-Down"},
    "LEFT-UP":    {"icon": "↖", "label": "Left-Up"},
    "RIGHT-UP":   {"icon": "↗", "label": "Right-Up"},
}

# plane code used in icon keys (xz_LEFT-DOWN, yz_RIGHT-UP, etc.)
PLANE_CODE = {"X-Z": "xz", "Y-Z": "yz"}

def icon_b64(plane, orientation):
    code = PLANE_CODE.get(plane, "xz")
    return ICONS_B64.get(f"{code}_{orientation}")

ACCENT = "#c4161c"
ACCENT_DARK = "#931217"
TEXT_DARK = "#1a1f29"
TEXT_MUTED = "#667085"
BORDER = "#e3e6ec"
SURFACE = "#ffffff"
BG = "#f7f8fa"

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"]  {{ font-family: 'Inter', sans-serif; }}

    .stApp {{ background: {BG}; }}

    .block-container {{ padding-top: 1.6rem; padding-bottom: 2.5rem; max-width: 760px; }}

    .juaristi-header {{
        background: {TEXT_DARK};
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 24px;
    }}
    .juaristi-header h1 {{
        color: #fff;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.2px;
    }}
    .juaristi-header p {{
        color: rgba(255,255,255,0.72);
        margin: 6px 0 0 0;
        font-size: 0.88rem;
        font-weight: 400;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 12px !important;
        border: 1px solid {BORDER} !important;
        background: {SURFACE};
    }}

    .section-title {{
        color: {TEXT_MUTED};
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        margin-bottom: 4px;
    }}

    .result-panel {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 24px;
        margin: 4px 0 18px 0;
    }}
    .result-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-top: 12px;
    }}
    .value-box {{
        background: {BG};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }}
    .value-label {{
        color: {TEXT_MUTED};
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}
    .value-number {{
        font-family: 'JetBrains Mono', monospace;
        color: {TEXT_DARK};
        font-size: 1.9rem;
        font-weight: 700;
        line-height: 1.1;
    }}
    .value-unit {{ color: {TEXT_MUTED}; font-size: 0.9rem; font-weight: 500; }}

    .meta-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 16px;
        padding-top: 14px;
        border-top: 1px solid {BORDER};
    }}
    .meta-chip {{
        background: {BG};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 5px 11px;
        font-size: 0.8rem;
        color: {TEXT_MUTED};
        font-weight: 500;
    }}
    .meta-chip b {{ color: {TEXT_DARK}; }}

    .footnote {{
        color: {TEXT_MUTED};
        font-size: 0.76rem;
        margin-top: 6px;
        text-align: center;
    }}

    .warn-note {{
        color: #9a6700;
        background: #fff8e6;
        border: 1px solid #f2dca0;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 0.8rem;
        margin-top: 14px;
    }}

    .orient-thumb-wrap {{
        border: 1px solid {BORDER};
        border-radius: 8px;
        background: {BG};
        padding: 6px;
        margin-bottom: 6px;
        text-align: center;
    }}
    .orient-thumb-wrap.selected {{
        border-color: {ACCENT};
        background: #fdeceb;
    }}
    .orient-thumb-wrap img {{
        width: 100%;
        height: auto;
        display: block;
    }}

    .confirm-panel {{
        display: flex;
        align-items: center;
        gap: 18px;
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 14px 18px;
        margin: 4px 0 18px 0;
    }}
    .confirm-panel img {{
        width: 92px;
        height: auto;
        flex-shrink: 0;
    }}
    .confirm-panel .confirm-text {{
        font-size: 0.95rem;
        color: {TEXT_DARK};
        font-weight: 600;
    }}
    .confirm-panel .confirm-sub {{
        font-size: 0.8rem;
        color: {TEXT_MUTED};
        font-weight: 400;
        margin-top: 2px;
    }}

    div[role="radiogroup"] label p {{ font-size: 0.95rem !important; color: {TEXT_DARK} !important; }}

    div[data-testid="stButton"] button {{
        border-radius: 8px;
        border: 1px solid {BORDER};
        font-weight: 600;
        color: {TEXT_DARK};
        background: {SURFACE};
        white-space: pre-line;
        padding: 10px 6px;
    }}
    div[data-testid="stButton"] button:hover {{
        border-color: {ACCENT};
        color: {ACCENT};
    }}
    div[data-testid="stButton"] button[kind="primary"] {{
        background: {ACCENT};
        border-color: {ACCENT};
        color: #fff;
    }}
    div[data-testid="stButton"] button[kind="primary"]:hover {{
        background: {ACCENT_DARK};
        border-color: {ACCENT_DARK};
        color: #fff;
    }}

    div[data-testid="stExpander"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
        background: {SURFACE};
    }}

    div[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{
        background-color: {ACCENT};
    }}

    /* Force red accent on focus states (overrides browser-default blue) */
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"]:focus-within,
    div[data-baseweb="base-input"]:focus-within {{
        border-color: {ACCENT} !important;
        box-shadow: 0 0 0 1px {ACCENT} !important;
    }}
    input:focus, select:focus, textarea:focus {{
        outline-color: {ACCENT} !important;
        border-color: {ACCENT} !important;
    }}
    div[data-testid="stNumberInput"] button:hover {{
        color: {ACCENT} !important;
        border-color: {ACCENT} !important;
    }}
    /* Streamlit theme variable overrides, in case a config.toml sets a blue primaryColor */
    :root {{
        --primary-color: {ACCENT} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(
            f"Could not find angles.csv (looked for it at: {DATA_PATH}). "
            "Make sure angles.csv is uploaded to the repo, either alongside app.py "
            "or inside a 'data' folder."
        )
        st.stop()
    return pd.read_csv(DATA_PATH)

df = load_data()

def img_tag(plane, orientation, css_class=""):
    b64 = icon_b64(plane, orientation)
    if b64 is None:
        return ""
    return f'<img class="{css_class}" src="data:image/png;base64,{b64}" />'

# Streamlit < 1.31 doesn't support st.container(border=True).
# Detect support once and fall back gracefully if unavailable.
def bordered_container():
    try:
        return st.container(border=True)
    except TypeError:
        return st.container()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="juaristi-header">
        <h1>⚙️ JUARISTI Milling Head Angle Lookup</h1>
        <p>Digital A-axis / C-axis reference for the 45° manual milling head — X–Z and Y–Z planes</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 1 · Machining plane
# ---------------------------------------------------------------------------
with bordered_container():
    st.markdown('<div class="section-title">1 · Machining Plane</div>', unsafe_allow_html=True)
    plane = st.radio(
        "Machining plane", options=["X-Z", "Y-Z"],
        horizontal=True, label_visibility="collapsed",
    )

# ---------------------------------------------------------------------------
# 2 · Orientation
# ---------------------------------------------------------------------------
with bordered_container():
    st.markdown('<div class="section-title">2 · Milling Head Orientation</div>', unsafe_allow_html=True)
    orient_cols = st.columns(4)
    orientations = ["RIGHT-DOWN", "LEFT-DOWN", "LEFT-UP", "RIGHT-UP"]
    if "orientation" not in st.session_state:
        st.session_state.orientation = "RIGHT-DOWN"

    for col, orient in zip(orient_cols, orientations):
        info = ORIENTATION_INFO[orient]
        selected = st.session_state.orientation == orient
        thumb_class = "orient-thumb-wrap selected" if selected else "orient-thumb-wrap"
        thumb_html = img_tag(plane, orient)
        col.markdown(f'<div class="{thumb_class}">{thumb_html}</div>', unsafe_allow_html=True)
        btn_label = f"{info['icon']}\n{info['label']}"
        if col.button(btn_label, key=f"btn_{orient}", use_container_width=True,
                      type="primary" if selected else "secondary"):
            st.session_state.orientation = orient

    orientation = st.session_state.orientation

    confirm_thumb = img_tag(plane, orientation)
    confirm_html = (
        '<div class="confirm-panel">'
        + confirm_thumb
        + '<div>'
        + f'<div class="confirm-text">Selected: {ORIENTATION_INFO[orientation]["label"]} — {plane} plane</div>'
        + '<div class="confirm-sub">Match this head orientation against the physical machine before entering an angle.</div>'
        + '</div></div>'
    )
    st.markdown(confirm_html, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 3 · Angle
# ---------------------------------------------------------------------------
with bordered_container():
    st.markdown('<div class="section-title">3 · Required Tool Angle (0° – 90°)</div>', unsafe_allow_html=True)

    input_mode = st.radio(
        "Angle entry mode", ["Slider", "Type degrees + minutes"],
        horizontal=True, label_visibility="collapsed",
    )

    if input_mode == "Slider":
        angle_value = st.slider(
            "Tool angle (degrees)", min_value=0.0, max_value=90.0, value=45.0, step=0.5,
            label_visibility="collapsed",
        )
    else:
        c1, c2 = st.columns(2)
        with c1:
            deg = st.number_input("Degrees", min_value=0, max_value=90, value=45, step=1)
        with c2:
            minute = st.selectbox("Minutes", [0, 30], index=0)
        angle_value = min(deg + minute / 60.0, 90.0)

# ---------------------------------------------------------------------------
# Lookup logic — snap to nearest tabulated 0.5° increment
# ---------------------------------------------------------------------------
def nearest_tabulated_angle(value):
    return round(value * 2) / 2.0

lookup_angle = nearest_tabulated_angle(angle_value)

subset = df[(df["plane"] == plane) & (df["orientation"] == orientation)]
row = subset.iloc[(subset["angle"] - lookup_angle).abs().argsort()[:1]]

if row.empty:
    st.error("No matching entry found in the angle table. Please check your inputs.")
else:
    neck_c = float(row["neck_C"].values[0])
    head_a = float(row["head_A"].values[0])
    matched_angle = float(row["angle"].values[0])

    deg_part = int(matched_angle)
    min_part = int(round((matched_angle - deg_part) * 60))

    exact_note = ""
    if abs(matched_angle - angle_value) > 1e-6:
        exact_note = (
            f'<div class="warn-note">⚠️ Table is tabulated in 30\' steps — '
            f'showing nearest value: {deg_part}° {min_part}\'</div>'
        )

    st.markdown(
        textwrap.dedent(f"""\
        <div class="result-panel">
            <div class="section-title">Lookup Result</div>
            <div class="result-grid">
                <div class="value-box">
                    <div class="value-label">Neck (C-axis)</div>
                    <div class="value-number">{neck_c:.4f}<span class="value-unit">°</span></div>
                </div>
                <div class="value-box">
                    <div class="value-label">Head (A-axis)</div>
                    <div class="value-number">{head_a:.4f}<span class="value-unit">°</span></div>
                </div>
            </div>
            <div class="meta-row">
                <div class="meta-chip">Plane: <b>{plane}</b></div>
                <div class="meta-chip">Orientation: <b>{ORIENTATION_INFO[orientation]['label']}</b></div>
                <div class="meta-chip">Angle: <b>{deg_part}° {min_part}'</b></div>
            </div>
            {exact_note}
        </div>
        """),
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Reference table
# ---------------------------------------------------------------------------
with st.expander("📋 View full reference table for this plane & orientation"):
    table_df = subset[["angle", "neck_C", "head_A"]].sort_values("angle").reset_index(drop=True)
    table_df.columns = ["Angle (°)", "Neck C-axis (°)", "Head A-axis (°)"]
    st.dataframe(table_df, use_container_width=True, height=400)

st.markdown(
    textwrap.dedent("""\
    <div class="footnote">
        Data digitized from JUARISTI "Table of Angles for Manual Heads" reference charts (X–Z and Y–Z horizontal planes).<br>
        Always verify against the machine's physical setup before production runs.
    </div>
    """),
    unsafe_allow_html=True,
)
