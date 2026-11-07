import os
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

import io
import subprocess
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import qrcode
import tif1

# =========================================================
# PAGE CONFIGURATION & F1 RACE CONTROL STYLING
# =========================================================

st.set_page_config(
    page_title="F1 Pitwall & Live Race Intelligence",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom Design System
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

:root {
    --f1-red: #E10600;
    --f1-dark: #07090E;
    --card-bg: #0E131F;
    --card-border: #1C2438;
    --text-primary: #F0F4FC;
    --text-muted: #8895AD;
    --accent-blue: #00D2BE;
}

html, body, [class*="css"] {
    font-family: 'Titillium Web', -apple-system, BlinkMacSystemFont, sans-serif;
}

code, pre, .mono {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Background */
.stApp {
    background: radial-gradient(circle at 10% 10%, #0d121e 0%, #06080d 90%);
    color: #F1F5F9 !important;
}

/* Global Text Clarity & Contrast */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    letter-spacing: -0.3px;
}

p, span, div {
    color: #F1F5F9;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0A0D15 !important;
    border-right: 1px solid #161D2E !important;
}

[data-testid="stSidebar"] * {
    color: #F1F5F9 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #161D2E !important;
}

/* Labels & Captions - Clear & High Contrast */
[data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] p, label {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px;
}

[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p, .stCaption {
    color: #94A3B8 !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
}

/* Selectbox and Dropdowns */
[data-baseweb="select"] {
    background-color: #0E1424 !important;
    border: 1px solid #222D42 !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] * {
    color: #FFFFFF !important;
    background-color: transparent !important;
}
div[data-baseweb="popover"], div[role="listbox"], ul[role="listbox"] {
    background-color: #0E1424 !important;
    border: 1px solid #25334D !important;
    border-radius: 8px !important;
}
li[role="option"] {
    color: #F1F5F9 !important;
    background-color: #0E1424 !important;
    font-weight: 600 !important;
}
li[role="option"]:hover, li[role="option"][aria-selected="true"] {
    background-color: #1A243D !important;
    color: #00D2BE !important;
}

/* Radio Buttons */
[data-testid="stRadio"] label {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
}
[data-testid="stRadio"] div[role="radiogroup"] p {
    color: #F1F5F9 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* Sliders */
[data-testid="stSlider"] label {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
}
[data-testid="stSlider"] [data-testid="stTickBarMin"], [data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: #94A3B8 !important;
    font-weight: 600 !important;
}
div[data-testid="stSlider"] div[data-baseweb="slider"] div {
    color: #FFFFFF !important;
}
div[data-testid="stSlider"] p {
    color: #F1F5F9 !important;
}

/* Checkboxes */
[data-testid="stCheckbox"] label span {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton > button {
    background: #111728 !important;
    color: #F8FAFC !important;
    border: 1px solid #25334D !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #1C2740 !important;
    border-color: #00D2BE !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 14px rgba(0, 210, 190, 0.25) !important;
}
.stButton > button:active {
    transform: scale(0.98) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #E10600 0%, #A80500 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    box-shadow: 0 4px 15px rgba(225, 6, 0, 0.3) !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #FF1A14 0%, #C40600 100%) !important;
    box-shadow: 0 6px 20px rgba(225, 6, 0, 0.5) !important;
    transform: translateY(-1px) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(14, 20, 36, 0.85) !important;
    border: 1px solid #1C253B !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35) !important;
}
[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 26px !important;
    font-weight: 850 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #202A40 !important;
    border-radius: 10px !important;
    background: #080B12 !important;
}
[data-testid="stDataFrame"] * {
    color: #F8FAFC !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    background-color: #0E1424 !important;
    border: 1px solid #202D45 !important;
    border-radius: 8px !important;
}
div[data-testid="stAlert"] * {
    color: #F8FAFC !important;
}

/* Audio Player Visibility */
audio {
    width: 100% !important;
    border-radius: 8px !important;
    filter: invert(0.9) hue-rotate(180deg) !important;
    margin-top: 6px !important;
}

/* Custom Header Badge */
.f1-badge {
    display: inline-block;
    padding: 3px 10px;
    background: linear-gradient(135deg, #E10600 0%, #900400 100%);
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    border-radius: 4px;
    text-transform: uppercase;
}

.live-pulse {
    display: inline-block;
    width: 8px;
    height: 8px;
    background-color: #00E676;
    border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 10px #00E676;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 230, 118, 0.7); }
    70% { transform: scale(1.15); box-shadow: 0 0 0 8px rgba(0, 230, 118, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 230, 118, 0); }
}

.hero-title {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin: 6px 0 0 0;
    color: #F8FAFC;
    line-height: 1.1;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 14px;
    margin-bottom: 16px;
}

/* Glassmorphism Metric Cards */
.f1-card {
    background: rgba(14, 19, 31, 0.85);
    border: 1px solid #1C2438;
    border-radius: 10px;
    padding: 14px 16px;
    backdrop-filter: blur(8px);
    transition: all 0.2s ease-in-out;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
}

.f1-card:hover {
    border-color: #2D3A56;
}

.f1-card-label {
    color: #CBD5E1;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.f1-card-value {
    color: #FFFFFF;
    font-size: 24px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.1;
}

.f1-card-sub {
    color: #00D2BE;
    font-size: 11px;
    font-weight: 600;
    margin-top: 4px;
}

/* Radio player card */
.radio-card {
    background: #0E1424;
    border: 1px solid #1A243D;
    border-left: 4px solid #00D2BE;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 12px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    border-bottom: 1px solid #1C2438;
    padding-bottom: 4px;
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    border-radius: 6px 6px 0 0;
    color: #94A3B8;
    font-weight: 700;
    font-size: 14px;
    border: none;
    padding: 0 16px;
    background: transparent;
}

.stTabs [aria-selected="true"] {
    color: #FFFFFF !important;
    background: #121828 !important;
    border-bottom: 2px solid #E10600 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #1C2438;
    border-radius: 8px;
    overflow: hidden;
}

.stDownloadButton button {
    background: linear-gradient(135deg, #E10600 0%, #A80500 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 18px !important;
}

/* F1 Cockpit Steering Wheel Display */
.f1-wheel-bezel {
    background: radial-gradient(circle at 50% 30%, #171E30 0%, #07090F 100%);
    border: 3px solid #25334D;
    border-radius: 20px;
    padding: 22px 24px;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.75), inset 0 1px 2px rgba(255, 255, 255, 0.12);
    max-width: 820px;
    margin: 10px auto 24px auto;
}

.led-bar {
    display: flex;
    justify-content: center;
    gap: 9px;
    margin-bottom: 16px;
    padding: 7px 18px;
    background: #05070C;
    border-radius: 24px;
    border: 1px solid #1C2438;
}

.led-dot {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #151D2D;
    transition: all 0.1s ease;
}

.wheel-screen {
    background: #04060A;
    border: 2px solid #1C2438;
    border-radius: 12px;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
}

.pedal-col {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 65px;
}

.pedal-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #CBD5E1;
    text-transform: uppercase;
}

.pedal-track {
    width: 26px;
    height: 140px;
    background: #0E1424;
    border: 1px solid #1C253B;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    overflow: hidden;
    margin: 8px 0;
}

.pedal-fill-brake {
    width: 100%;
    background: linear-gradient(180deg, #FF1744 0%, #B70024 100%);
    box-shadow: 0 0 12px #FF1744;
    transition: height 0.1s ease;
}

.pedal-fill-throttle {
    width: 100%;
    background: linear-gradient(180deg, #00E676 0%, #00964D 100%);
    box-shadow: 0 0 12px #00E676;
    transition: height 0.1s ease;
}

.wheel-center {
    flex-grow: 1;
    text-align: center;
}

.wheel-gear {
    font-size: 82px;
    font-weight: 900;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
    color: #F8FAFC;
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
}

.wheel-speed {
    font-size: 44px;
    font-weight: 850;
    font-family: 'JetBrains Mono', monospace;
    color: #FFFFFF;
    margin-top: 2px;
}

.wheel-rpm-bar {
    width: 100%;
    height: 8px;
    background: #141B2D;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 8px;
}

.wheel-rpm-fill {
    height: 100%;
    background: linear-gradient(90deg, #00E676 0%, #FFD700 70%, #FF1744 100%);
}

/* Mobile Responsive System */
@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-bottom: 2rem !important;
    }
    
    .hero-title {
        font-size: 20px !important;
        letter-spacing: -0.2px !important;
        line-height: 1.2 !important;
    }
    
    .hero-subtitle {
        font-size: 12px !important;
        margin-bottom: 10px !important;
    }
    
    .f1-card {
        padding: 10px 12px !important;
        margin-bottom: 6px !important;
    }
    
    .f1-card-value {
        font-size: 20px !important;
    }
    
    .f1-card-label {
        font-size: 10px !important;
    }

    /* Steering Wheel Mobile Scaling */
    .f1-wheel-bezel {
        padding: 12px 10px !important;
        border-radius: 14px !important;
        border-width: 2px !important;
        margin: 6px auto 14px auto !important;
        max-width: 100% !important;
    }
    
    .led-bar {
        gap: 4px !important;
        padding: 4px 8px !important;
        margin-bottom: 10px !important;
        border-radius: 16px !important;
    }
    
    .led-dot {
        width: 10px !important;
        height: 10px !important;
    }
    
    .wheel-screen {
        padding: 10px 8px !important;
        gap: 6px !important;
        border-radius: 8px !important;
    }
    
    .pedal-col {
        width: 44px !important;
    }
    
    .pedal-track {
        width: 18px !important;
        height: 95px !important;
        margin: 4px 0 !important;
    }
    
    .pedal-label {
        font-size: 9px !important;
    }
    
    .wheel-gear {
        font-size: 52px !important;
    }
    
    .wheel-speed {
        font-size: 28px !important;
    }
    
    .wheel-speed span {
        font-size: 11px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0 8px !important;
        font-size: 12px !important;
        height: 38px !important;
    }
    
    .stButton > button {
        padding: 7px 10px !important;
        font-size: 11px !important;
        min-height: 38px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Team Color Constants
TEAM_COLORS = {
    "Red Bull Racing": "#3671C6",
    "Ferrari": "#E80020",
    "Mercedes": "#27F4D2",
    "McLaren": "#FF8000",
    "Aston Martin": "#229971",
    "Alpine": "#0093CC",
    "Williams": "#64C4FF",
    "RB": "#6692FF",
    "Kick Sauber": "#52E252",
    "Haas F1 Team": "#B6BABD",
}

DRIVER_COLORS = {
    "VER": "#3671C6", "PER": "#1B3A6B",
    "HAM": "#27F4D2", "RUS": "#6CD3BF",
    "LEC": "#E80020", "SAI": "#AA0015",
    "NOR": "#FF8000", "PIA": "#FFB800",
    "ALO": "#229971", "STR": "#166349",
    "GAS": "#0093CC", "OCO": "#006699",
    "ALB": "#64C4FF", "SAR": "#3399FF", "COL": "#004CE5",
    "TSU": "#6692FF", "RIC": "#1E41FF", "LAW": "#4D79FF",
    "BOT": "#52E252", "ZHO": "#00A651",
    "HUL": "#B6BABD", "MAG": "#808285", "BEA": "#E80020",
    "ANT": "#27F4D2"
}

TYRE_COLORS = {
    "SOFT": "#E10600",
    "MEDIUM": "#FFD700",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#39B54A",
    "WET": "#00AEEF",
    "UNKNOWN": "#8895AD"
}

def get_driver_color(driver_code, team_name=None):
    if driver_code in DRIVER_COLORS:
        return DRIVER_COLORS[driver_code]
    if team_name and team_name in TEAM_COLORS:
        return TEAM_COLORS[team_name]
    return "#38BDF8"

def format_laptime(seconds):
    if pd.isna(seconds) or seconds is None or seconds <= 0:
        return "--:--.---"
    mins = int(seconds // 60)
    rem_sec = seconds % 60
    return f"{mins}:{rem_sec:06.3f}"

def get_compound_badge_html(compound, tyre_life=None):
    cmp = str(compound).upper() if compound else "UNKNOWN"
    bg = TYRE_COLORS.get(cmp, "#475569")
    fg = "#000000" if cmp in ["MEDIUM", "HARD"] else "#FFFFFF"
    life_txt = f" ({tyre_life}L)" if tyre_life else ""
    return f'<span style="background:{bg}; color:{fg}; font-weight:800; font-size:10px; padding:2px 7px; border-radius:4px; letter-spacing:0.5px; display:inline-block;">{cmp}{life_txt}</span>'

def get_local_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith("127."):
            return ip
    except Exception:
        pass
    for iface in ["en0", "en1"]:
        try:
            ip = subprocess.check_output(["ipconfig", "getifaddr", iface], timeout=1).decode().strip()
            if ip:
                return ip
        except Exception:
            pass
    return "192.168.1.8"

@st.cache_data(show_spinner=False)
def generate_mobile_qr(url):
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#F8FAFC", back_color="#0E1424")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def style_plotly_fig(fig):
    fig.update_layout(
        plot_bgcolor="#070A12",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F1F5F9", family="Titillium Web"),
        hoverlabel=dict(
            bgcolor="#0E1424",
            font_color="#FFFFFF",
            bordercolor="#2A3854",
            font_family="JetBrains Mono"
        ),
        legend=dict(
            font=dict(color="#FFFFFF", family="Titillium Web", size=11),
            bgcolor="rgba(14, 19, 31, 0.85)",
            bordercolor="#1C2438",
            borderwidth=1
        )
    )
    if hasattr(fig, "layout") and hasattr(fig.layout, "annotations") and fig.layout.annotations:
        for a in fig.layout.annotations:
            a.font.color = "#FFFFFF"
            a.font.size = 13
            a.font.family = "Titillium Web"
    fig.update_xaxes(
        gridcolor="#192233",
        zerolinecolor="#25314C",
        tickfont=dict(color="#CBD5E1", family="JetBrains Mono"),
        title_font=dict(color="#FFFFFF", family="Titillium Web")
    )
    fig.update_yaxes(
        gridcolor="#192233",
        zerolinecolor="#25314C",
        tickfont=dict(color="#CBD5E1", family="JetBrains Mono"),
        title_font=dict(color="#FFFFFF", family="Titillium Web")
    )
    return fig

# =========================================================
# OPENF1 REAL-TIME API CACHED CALLS
# =========================================================

OPENF1_BASE = "https://api.openf1.org/v1"

@st.cache_data(ttl=20, show_spinner=False)
def fetch_openf1_latest_session():
    try:
        r = requests.get(f"{OPENF1_BASE}/sessions?session_key=latest", timeout=6)
        if r.status_code == 200 and r.json():
            return r.json()[0]
    except Exception:
        pass
    return None

@st.cache_data(ttl=60, show_spinner=False)
def fetch_openf1_sessions_for_year(year):
    try:
        r = requests.get(f"{OPENF1_BASE}/sessions?year={year}", timeout=6)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []

@st.cache_data(ttl=20, show_spinner=False)
def fetch_openf1_live_weather(session_key):
    try:
        r = requests.get(f"{OPENF1_BASE}/weather?session_key={session_key}", timeout=5)
        if r.status_code == 200 and r.json():
            return r.json()[-1]
    except Exception:
        pass
    return {}

@st.cache_data(ttl=20, show_spinner=False)
def fetch_openf1_drivers(session_key):
    try:
        r = requests.get(f"{OPENF1_BASE}/drivers?session_key={session_key}", timeout=5)
        if r.status_code == 200 and r.json():
            return pd.DataFrame(r.json())
    except Exception:
        pass
    return pd.DataFrame()

@st.cache_data(ttl=20, show_spinner=False)
def fetch_openf1_laps(session_key):
    try:
        r = requests.get(f"{OPENF1_BASE}/laps?session_key={session_key}", timeout=7)
        if r.status_code == 200 and r.json():
            return pd.DataFrame(r.json())
    except Exception:
        pass
    return pd.DataFrame()

@st.cache_data(ttl=20, show_spinner=False)
def fetch_openf1_team_radio(session_key):
    try:
        r = requests.get(f"{OPENF1_BASE}/team_radio?session_key={session_key}", timeout=6)
        if r.status_code == 200 and r.json():
            return pd.DataFrame(r.json())
    except Exception:
        pass
    return pd.DataFrame()

@st.cache_data(ttl=20, show_spinner=False)
def fetch_openf1_race_control(session_key):
    try:
        r = requests.get(f"{OPENF1_BASE}/race_control?session_key={session_key}", timeout=6)
        if r.status_code == 200 and r.json():
            return pd.DataFrame(r.json())
    except Exception:
        pass
    return pd.DataFrame()

@st.cache_data(ttl=30, show_spinner=False)
def fetch_openf1_car_data(session_key, driver_number):
    try:
        r = requests.get(f"{OPENF1_BASE}/car_data?session_key={session_key}&driver_number={driver_number}", timeout=8)
        if r.status_code == 200 and r.json():
            return pd.DataFrame(r.json())
    except Exception:
        pass
    return pd.DataFrame()

# =========================================================
# TIF1 CACHED ARCHIVE CALLS
# =========================================================

@st.cache_data(show_spinner=False, ttl=3600)
def get_event_names(year):
    events = tif1.get_events(year)
    if "EventName" in events.columns:
        return events["EventName"].dropna().tolist()
    return []

@st.cache_data(show_spinner=False, ttl=3600)
def get_session_names(year, event_name):
    return tif1.get_sessions(year, event_name)

@st.cache_data(show_spinner=False, ttl=3600)
def get_session_and_drivers(year, event_name, session_name):
    session = tif1.get_session(year, event_name, session_name)
    laps = session.laps
    if laps is None or laps.empty or "Driver" not in laps.columns:
        return []
    return sorted(laps["Driver"].dropna().astype(str).unique().tolist())

@st.cache_data(show_spinner=False, ttl=3600)
def load_driver_data(year, event_name, session_name, driver_code):
    session = tif1.get_session(year, event_name, session_name)
    driver = session.get_driver(driver_code)
    telemetry = driver.get_fastest_lap_tel()
    df = pd.DataFrame(telemetry).copy()
    
    meta = {
        "driver": driver_code,
        "team": "Unknown Team",
        "lap_time": "N/A",
        "compound": "UNKNOWN",
        "tyre_life": None
    }
    
    try:
        fastest_lap = driver.get_fastest_lap()
        if fastest_lap is not None:
            if "Team" in fastest_lap:
                meta["team"] = str(fastest_lap["Team"].iloc[0] if isinstance(fastest_lap["Team"], pd.Series) else fastest_lap["Team"])
            if "LapTime" in fastest_lap:
                lt = fastest_lap["LapTime"].iloc[0] if isinstance(fastest_lap["LapTime"], pd.Series) else fastest_lap["LapTime"]
                if pd.notna(lt):
                    total_sec = lt.total_seconds()
                    meta["lap_time"] = format_laptime(total_sec)
            if "Compound" in fastest_lap:
                cmpnd = fastest_lap["Compound"].iloc[0] if isinstance(fastest_lap["Compound"], pd.Series) else fastest_lap["Compound"]
                if pd.notna(cmpnd):
                    meta["compound"] = str(cmpnd).upper()
            if "TyreLife" in fastest_lap:
                tl = fastest_lap["TyreLife"].iloc[0] if isinstance(fastest_lap["TyreLife"], pd.Series) else fastest_lap["TyreLife"]
                if pd.notna(tl):
                    meta["tyre_life"] = int(tl)
    except Exception:
        pass

    return df, meta

# =========================================================
# SOCIAL MEDIA DEBRIEF CARD GENERATOR
# =========================================================

def generate_f1_debrief_card(
    year, event_name, session_name,
    driver_1_code, meta1, tel1, color1,
    driver_2_code, meta2, tel2, color2,
    dist_grid, delta_time
):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(16, 9), dpi=140)
    fig.patch.set_facecolor('#07090E')

    # Grid: 3 rows, 2 columns
    gs = fig.add_gridspec(3, 2, height_ratios=[0.24, 0.46, 0.30], width_ratios=[0.48, 0.52], hspace=0.34, wspace=0.24)

    # 1. HEADER & DRIVER BATTLE CARD
    ax_head = fig.add_subplot(gs[0, :])
    ax_head.set_facecolor('#0E1424')
    ax_head.axis('off')

    ax_head.text(0.02, 0.82, 'FORMULA 1 // OFFICIAL TELEMETRY DEBRIEF', color='#E10600', fontsize=12, fontweight='bold')
    ax_head.text(0.02, 0.46, f'{year} {event_name.upper()}', color='#FFFFFF', fontsize=22, fontweight='bold')
    ax_head.text(0.02, 0.16, f'SESSION: {session_name.upper()} · CIRCUIT RACE INTELLIGENCE', color='#CBD5E1', fontsize=11, fontweight='bold')

    ax_head.text(0.55, 0.74, driver_1_code, color=color1, fontsize=28, fontweight='bold', ha='center')
    ax_head.text(0.55, 0.42, meta1.get('team', ''), color='#F0F4FC', fontsize=10, fontweight='bold', ha='center')
    ax_head.text(0.55, 0.15, f"{meta1.get('lap_time', 'N/A')} ({meta1.get('compound', '')})", color='#00D2BE', fontsize=11, fontweight='bold', ha='center')

    final_dt = delta_time[-1]
    ahead = driver_1_code if final_dt < 0 else driver_2_code
    lead_str = f"{ahead} -{abs(final_dt):.3f}s"
    ax_head.text(0.73, 0.55, 'VS', color='#CBD5E1', fontsize=14, fontweight='bold', ha='center')
    ax_head.text(0.73, 0.22, lead_str, color='#FFFFFF', fontsize=12, fontweight='bold', ha='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#E10600', edgecolor='none'))

    ax_head.text(0.91, 0.74, driver_2_code, color=color2, fontsize=28, fontweight='bold', ha='center')
    ax_head.text(0.91, 0.42, meta2.get('team', ''), color='#F0F4FC', fontsize=10, fontweight='bold', ha='center')
    ax_head.text(0.91, 0.15, f"{meta2.get('lap_time', 'N/A')} ({meta2.get('compound', '')})", color='#00D2BE', fontsize=11, fontweight='bold', ha='center')

    # 2. MIDDLE LEFT: PERFORMANCE METRICS TABLE
    ax_stats = fig.add_subplot(gs[1, 0])
    ax_stats.set_facecolor('#0E1424')
    ax_stats.axis('off')
    ax_stats.set_title('TELEMETRY PERFORMANCE BREAKDOWN', color='#CBD5E1', fontsize=11, fontweight='bold', pad=12, loc='left')

    wot1 = (tel1['Throttle'] >= 98).mean() * 100
    wot2 = (tel2['Throttle'] >= 98).mean() * 100
    brk1 = tel1['Brake'].astype(bool).mean() * 100
    brk2 = tel2['Brake'].astype(bool).mean() * 100

    metrics_list = [
        ("Lap Time", meta1.get("lap_time", "N/A"), meta2.get("lap_time", "N/A"), lead_str),
        ("Top Speed", f"{tel1['Speed'].max():.1f} km/h", f"{tel2['Speed'].max():.1f} km/h", f"{tel1['Speed'].max()-tel2['Speed'].max():+.1f} km/h"),
        ("Average Speed", f"{tel1['Speed'].mean():.1f} km/h", f"{tel2['Speed'].mean():.1f} km/h", f"{tel1['Speed'].mean()-tel2['Speed'].mean():+.1f} km/h"),
        ("Full Throttle %", f"{wot1:.1f}%", f"{wot2:.1f}%", f"{wot1-wot2:+.1f}%"),
        ("Braking Duty %", f"{brk1:.1f}%", f"{brk2:.1f}%", f"{brk1-brk2:+.1f}%"),
    ]

    y_pos = 0.85
    ax_stats.text(0.04, y_pos, "METRIC", color='#94A3B8', fontsize=10, fontweight='bold')
    ax_stats.text(0.40, y_pos, driver_1_code, color=color1, fontsize=11, fontweight='bold', ha='center')
    ax_stats.text(0.65, y_pos, driver_2_code, color=color2, fontsize=11, fontweight='bold', ha='center')
    ax_stats.text(0.88, y_pos, "DELTA", color='#F8FAFC', fontsize=10, fontweight='bold', ha='center')

    for label, val1, val2, delta in metrics_list:
        y_pos -= 0.15
        ax_stats.axhline(y_pos + 0.10, xmin=0.03, xmax=0.97, color='#1C2438', lw=0.8)
        ax_stats.text(0.04, y_pos, label, color='#F0F4FC', fontsize=11, fontweight='bold')
        ax_stats.text(0.40, y_pos, val1, color='#FFFFFF', fontsize=11, fontweight='bold', ha='center')
        ax_stats.text(0.65, y_pos, val2, color='#FFFFFF', fontsize=11, fontweight='bold', ha='center')
        ax_stats.text(0.88, y_pos, delta, color='#00D2BE', fontsize=10, fontweight='bold', ha='center')

    # 3. MIDDLE RIGHT: 2D CIRCUIT TRACK
    ax_map = fig.add_subplot(gs[1, 1])
    ax_map.set_facecolor('#0E1424')
    ax_map.set_title(f'CIRCUIT SPEED & TRAJECTORY // {event_name.upper()}', color='#CBD5E1', fontsize=11, fontweight='bold', pad=12, loc='left')

    if 'X' in tel1.columns and 'Y' in tel1.columns and not tel1['X'].dropna().empty:
        tdf = tel1.dropna(subset=['X', 'Y'])
        scatter = ax_map.scatter(tdf['X'], tdf['Y'], c=tdf['Speed'], cmap='turbo', s=12, alpha=0.9)
        ax_map.scatter(tdf['X'].iloc[0], tdf['Y'].iloc[0], color='#FFFFFF', s=80, marker='*', zorder=5, label='Start/Finish')
        ax_map.set_aspect('equal', adjustable='datalim')
        ax_map.axis('off')
        cbar = fig.colorbar(scatter, ax=ax_map, orientation='horizontal', pad=0.04, shrink=0.6, aspect=24)
        cbar.set_label('Speed (km/h)', color='#CBD5E1', fontsize=9)
        cbar.ax.tick_params(colors='#CBD5E1', labelsize=8)
    else:
        ax_map.text(0.5, 0.5, 'Circuit GPS Data Unavailable', color='#94A3B8', ha='center', va='center')
        ax_map.axis('off')

    # 4. BOTTOM PANEL: TIME DELTA (Δt) PROFILE
    ax_delta = fig.add_subplot(gs[2, :])
    ax_delta.set_facecolor('#0E1424')
    ax_delta.set_title(f'CUMULATIVE LAP TIME DELTA: Δt ({driver_1_code} vs {driver_2_code}) [SECONDS]', color='#CBD5E1', fontsize=11, fontweight='bold', loc='left')
    
    d1_lead_curve = -delta_time
    ax_delta.plot(dist_grid, d1_lead_curve, color='#00F0FF', lw=2.2, label=f'{driver_1_code} Advantage')
    ax_delta.axhline(0, color='#94A3B8', ls='--', alpha=0.6, lw=1)
    ax_delta.fill_between(dist_grid, d1_lead_curve, 0, where=(d1_lead_curve >= 0), color=color1, alpha=0.3)
    ax_delta.fill_between(dist_grid, d1_lead_curve, 0, where=(d1_lead_curve < 0), color=color2, alpha=0.3)
    
    ax_delta.set_xlabel('Track Distance (metres)', color='#CBD5E1', fontsize=10)
    ax_delta.set_ylabel('Δt (s)', color='#CBD5E1', fontsize=10)
    ax_delta.tick_params(colors='#CBD5E1', labelsize=9)
    ax_delta.grid(True, color='#1A2234', ls=':', alpha=0.6)
    for sp in ax_delta.spines.values():
        sp.set_color('#1C2438')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=140)
    plt.close(fig)
    buf.seek(0)
    return buf

# =========================================================
# SIDEBAR NAVIGATION & CONTROLS
# =========================================================

with st.sidebar:
    st.markdown('<div class="f1-badge">Pitwall Telemetry</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='margin:4px 0 14px 0; color:#FFF;'>F1 Race Intelligence</h2>", unsafe_allow_html=True)
    
    app_mode = st.radio(
        "SYSTEM VIEW",
        ["📡 Live Grand Prix Race Control", "🏎️ Deep Telemetry & Lap Archives"],
        index=0
    )
    
    st.markdown("---")
    
    # 📱 Mobile Access Panel
    with st.expander("📱 Open on Phone / Mobile", expanded=False):
        phone_ip = get_local_ip()
        phone_url = f"http://{phone_ip}:8501"
        st.markdown(f"""
        <div style="background:#0E1424; border:1px solid #1C2438; border-radius:8px; padding:10px; text-align:center;">
            <div style="font-size:11px; font-weight:700; color:#CBD5E1; margin-bottom:4px;">
                SCAN WITH PHONE CAMERA
            </div>
            <div style="font-family:'JetBrains Mono'; font-size:12px; color:#00D2BE; font-weight:700; word-break:break-all;">
                {phone_url}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        qr_buf = generate_mobile_qr(phone_url)
        st.image(qr_buf, width=175)
        st.caption("Ensure your phone is connected to the same Wi-Fi network.")
        st.markdown("---")

# =========================================================
# VIEW 1: LIVE GRAND PRIX RACE CONTROL (OPENF1)
# =========================================================

if app_mode == "📡 Live Grand Prix Race Control":
    with st.sidebar:
        st.markdown("### 📡 Live Feed Settings")
        latest_sess = fetch_openf1_latest_session()
        
        feed_option = st.selectbox(
            "Select Session Feed",
            ["🔥 Active / Most Recent Session", "Select Previous Session"]
        )
        
        selected_session_key = None
        current_sess_info = latest_sess or {}
        
        if feed_option == "🔥 Active / Most Recent Session" and latest_sess:
            selected_session_key = latest_sess.get("session_key")
        else:
            recent_sessions = fetch_openf1_sessions_for_year(2026) or fetch_openf1_sessions_for_year(2024)
            if recent_sessions:
                sess_df = pd.DataFrame(recent_sessions)
                sess_df = sess_df.sort_values("date_start", ascending=False).reset_index(drop=True)
                sess_df["label"] = sess_df["country_name"] + " · " + sess_df["session_name"] + " (" + sess_df["year"].astype(str) + ")"
                choice = st.selectbox("Choose Grand Prix Session", sess_df["label"].tolist(), index=0)
                sel_row = sess_df[sess_df["label"] == choice].iloc[0]
                selected_session_key = sel_row["session_key"]
                current_sess_info = sel_row.to_dict()
            elif latest_sess:
                selected_session_key = latest_sess.get("session_key")
                
        if st.button("🔄 Refresh Live Feed", width="stretch"):
            st.cache_data.clear()
            st.rerun()

        auto_refresh = st.toggle(
            "⚡ Live Auto-Poll",
            value=False,
            help="Automatically polls the track timing and car telemetry at regular intervals while you watch the Grand Prix."
        )
        refresh_sec = 15
        if auto_refresh:
            refresh_sec = st.selectbox(
                "Polling Frequency",
                [10, 15, 30, 60],
                index=1,
                format_func=lambda s: f"Every {s} seconds"
            )

        st.caption("Powered by OpenF1 Real-Time Streaming Telemetry")
    
    if not selected_session_key:
        st.error("No active session could be reached. Please verify connection or select an archive session.")
        st.stop()
        
    # Header Banner
    meeting_loc = current_sess_info.get("location", "Grand Prix")
    country_name = current_sess_info.get("country_name", "F1")
    sess_title = current_sess_info.get("session_name", "Live Session")
    sess_year = current_sess_info.get("year", 2026)
    circuit_name = current_sess_info.get("circuit_short_name", "Circuit")
    
    st.markdown(f'<span class="live-pulse"></span><span class="f1-badge">LIVE RACE CONTROL · {sess_year}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title">{country_name.upper()} GRAND PRIX // {sess_title.upper()}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-subtitle">📍 {circuit_name} ({meeting_loc}) · Official FIA Timing Tower, Live Cockpit Telemetry HUD & Team Radio.</div>', unsafe_allow_html=True)
    
    # Live Weather Station Bar
    weather = fetch_openf1_live_weather(selected_session_key)
    
    w1, w2, w3, w4, w5 = st.columns(5)
    with w1:
        track_temp = weather.get("track_temperature")
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Track Temperature</div>
            <div class="f1-card-value">{f"{track_temp:.1f}°C" if track_temp else "32.0°C"}</div>
            <div class="f1-card-sub">Asphalt Heat</div>
        </div>
        """)
        
    with w2:
        air_temp = weather.get("air_temperature")
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Air Temperature</div>
            <div class="f1-card-value">{f"{air_temp:.1f}°C" if air_temp else "21.5°C"}</div>
            <div class="f1-card-sub">Ambient</div>
        </div>
        """)
        
    with w3:
        humidity = weather.get("humidity")
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Humidity</div>
            <div class="f1-card-value">{f"{humidity:.0f}%" if humidity else "75%"}</div>
            <div class="f1-card-sub">Relative Humidity</div>
        </div>
        """)
        
    with w4:
        wind = weather.get("wind_speed")
        wind_dir = weather.get("wind_direction")
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Wind Speed</div>
            <div class="f1-card-value">{f"{wind:.1f} m/s" if wind else "2.4 m/s"}</div>
            <div class="f1-card-sub">{f"Direction: {wind_dir}°" if wind_dir else "Steady"}</div>
        </div>
        """)
        
    with w5:
        rain = weather.get("rainfall")
        is_wet = rain and rain > 0
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Track Condition</div>
            <div class="f1-card-value" style="color:{'#00D2BE' if is_wet else '#00E676'};">{'WET 🌧️' if is_wet else 'DRY ☀️'}</div>
            <div class="f1-card-sub">Rainfall: {f"{rain}mm" if rain else "0.0 mm"}</div>
        </div>
        """)
        
    st.write("")
    
    # LIVE TABS
    tab_timing, tab_cockpit, tab_radio, tab_rc = st.tabs([
        "⏱️ Live Timing Tower",
        "🏎️ Live Driver Cockpit HUD",
        "📻 Live Team Radio Audio",
        "🚨 FIA Race Control & Track Status"
    ])
    
    # -----------------------------------------------------
    # TAB 1: LIVE TIMING TOWER
    # -----------------------------------------------------
    with tab_timing:
        st.markdown("### Official Timing Tower Leaderboard")
        st.caption("Live lap durations, sector times, intervals, and car speed traps.")
        
        with st.expander("💡 New to F1? How to read this timing tower in 30 seconds"):
            c_g1, c_g2, c_g3, c_g4 = st.columns(4)
            c_g1.markdown("**⏱️ BEST LAP**<br><span style='color:#CBD5E1; font-size:12px;'>Fastest single lap completed by the driver so far in this session.</span>", unsafe_allow_html=True)
            c_g2.markdown("**🎯 GAP vs INT**<br><span style='color:#CBD5E1; font-size:12px;'><b>GAP</b> = Time behind the 1st place leader.<br><b>INT</b> = Gap to the car directly in front.</span>", unsafe_allow_html=True)
            c_g3.markdown("**⚡ SECTORS (S1, S2, S3)**<br><span style='color:#CBD5E1; font-size:12px;'>Track is split into 3 segments. Fast cars dominate S1 (straights) or S2/S3 (corners).</span>", unsafe_allow_html=True)
            c_g4.markdown("**🚀 SPEED TRAP**<br><span style='color:#CBD5E1; font-size:12px;'>Radar-measured top speed before the circuit's hardest braking zone.</span>", unsafe_allow_html=True)
        
        drivers_df = fetch_openf1_drivers(selected_session_key)
        laps_df = fetch_openf1_laps(selected_session_key)
        
        if not drivers_df.empty and not laps_df.empty and "lap_duration" in laps_df.columns:
            valid_laps = laps_df[laps_df["lap_duration"].notna()].copy()
            
            if not valid_laps.empty:
                best_laps = (
                    valid_laps.groupby("driver_number")
                    .agg(
                        best_lap=("lap_duration", "min"),
                        total_laps=("lap_number", "max"),
                        best_s1=("duration_sector_1", "min"),
                        best_s2=("duration_sector_2", "min"),
                        best_s3=("duration_sector_3", "min"),
                        top_st_speed=("st_speed", "max")
                    )
                    .reset_index()
                )
                
                leaderboard = pd.merge(drivers_df, best_laps, on="driver_number", how="inner")
                leaderboard = leaderboard.sort_values("best_lap").reset_index(drop=True)
                
                p1_time = leaderboard["best_lap"].iloc[0]
                leaderboard["Position"] = range(1, len(leaderboard) + 1)
                leaderboard["Gap_To_P1"] = leaderboard["best_lap"].apply(
                    lambda t: "LEADER" if t == p1_time else f"+{t - p1_time:.3f}s"
                )
                
                leaderboard["Interval"] = ["LEADER"] + [
                    f"+{leaderboard['best_lap'].iloc[i] - leaderboard['best_lap'].iloc[i-1]:.3f}s"
                    for i in range(1, len(leaderboard))
                ]
                
                leaderboard["Lap_Time_Str"] = leaderboard["best_lap"].apply(format_laptime)
                leaderboard["S1"] = leaderboard["best_s1"].apply(lambda s: f"{s:.3f}s" if pd.notna(s) else "--")
                leaderboard["S2"] = leaderboard["best_s2"].apply(lambda s: f"{s:.3f}s" if pd.notna(s) else "--")
                leaderboard["S3"] = leaderboard["best_s3"].apply(lambda s: f"{s:.3f}s" if pd.notna(s) else "--")
                leaderboard["Speed_Trap"] = leaderboard["top_st_speed"].apply(lambda sp: f"{sp:.0f} km/h" if pd.notna(sp) else "--")
                
                display_cols = [
                    "Position", "name_acronym", "full_name", "team_name",
                    "Lap_Time_Str", "Gap_To_P1", "Interval", "total_laps",
                    "S1", "S2", "S3", "Speed_Trap"
                ]
                
                renamed_cols = {
                    "Position": "POS",
                    "name_acronym": "CODE",
                    "full_name": "DRIVER",
                    "team_name": "TEAM",
                    "Lap_Time_Str": "BEST LAP",
                    "Gap_To_P1": "GAP",
                    "Interval": "INT",
                    "total_laps": "LAPS",
                    "Speed_Trap": "SPEED TRAP"
                }
                
                st.dataframe(
                    leaderboard[display_cols].rename(columns=renamed_cols),
                    width="stretch",
                    hide_index=True
                )
            else:
                st.info("Drivers are on out-laps; no timed laps recorded yet.")
        else:
            st.info("Waiting for live lap times from session telemetry...")

    # -----------------------------------------------------
    # TAB 2: LIVE DRIVER COCKPIT HUD
    # -----------------------------------------------------
    with tab_cockpit:
        st.markdown("### 🏎️ Live Digital Steering Wheel & Cockpit Telemetry")
        st.caption("Select any car to view high-frequency pedal inputs, F1 LED shift lights, RPM, and gear changes.")
        
        with st.expander("💡 Cockpit Guide: Steering Wheel & Shift Lights Explained"):
            s_col1, s_col2, s_col3 = st.columns(3)
            s_col1.markdown("**🚦 15 Shift LEDs**<br><span style='color:#CBD5E1; font-size:12px;'>Lights turn Green ➔ Red ➔ Purple as RPM approaches 12,500+. Flashing purple is the driver's cue to upshift!</span>", unsafe_allow_html=True)
            s_col2.markdown("**🟢 DRS (Drag Reduction System)**<br><span style='color:#CBD5E1; font-size:12px;'>Rear wing flap opens on straights. Drops aerodynamic drag and provides an instant +18 km/h speed boost.</span>", unsafe_allow_html=True)
            s_col3.markdown("**🦶 Pedal Gauges**<br><span style='color:#CBD5E1; font-size:12px;'>Left Red bar = Brake pedal force (0-100%). Right Green bar = Throttle application (0-100%).</span>", unsafe_allow_html=True)
        
        drivers_df = fetch_openf1_drivers(selected_session_key)
        
        if not drivers_df.empty:
            drivers_df["select_label"] = (
                drivers_df["name_acronym"] + " · " + drivers_df["full_name"] +
                " (#" + drivers_df["driver_number"].astype(str) + ") - " + drivers_df["team_name"]
            )
            
            sel_hud_driver_label = st.selectbox(
                "Select Driver Cockpit",
                drivers_df["select_label"].tolist(),
                index=0
            )
            
            sel_driver_row = drivers_df[drivers_df["select_label"] == sel_hud_driver_label].iloc[0]
            sel_driver_num = int(sel_driver_row["driver_number"])
            sel_driver_code = sel_driver_row["name_acronym"]
            sel_team_name = sel_driver_row["team_name"]
            
            with st.spinner(f"Loading {sel_driver_code} car telemetry..."):
                car_df = fetch_openf1_car_data(selected_session_key, sel_driver_num)
                
            if not car_df.empty:
                car_df = car_df.sort_values("date").reset_index(drop=True)
                
                # Driving Stats Bar for this car
                h_c1, h_c2, h_c3, h_c4 = st.columns(4)
                h_c1.metric("Session Top Speed", f"{car_df['speed'].max():.0f} km/h")
                h_c2.metric("Peak RPM", f"{car_df['rpm'].max():,}")
                h_c3.metric("Telemetry Data Points", f"{len(car_df):,}")
                gear_counts = car_df["n_gear"].diff().ne(0).sum()
                h_c4.metric("Gear Shifts Detected", f"{int(gear_counts):,}")
                
                st.markdown("---")
                
                # Quick jump timeline buttons & DRS Candidates
                drs_candidates = car_df[car_df["drs"].isin([10, 12, 14, 1, True])] if "drs" in car_df.columns else pd.DataFrame()
                if drs_candidates.empty:
                    drs_candidates = car_df[(car_df["speed"] >= 270) & (car_df["throttle"] >= 95) & (car_df["n_gear"] >= 7) & (car_df["brake"] <= 10)]

                q_col1, q_col2, q_col3, q_col4, q_col5 = st.columns(5)
                
                slider_key = f"scrub_slider_{sel_driver_num}"
                
                if q_col1.button("⚡ Top Speed", width="stretch"):
                    st.session_state[slider_key] = int(car_df["speed"].idxmax())
                if q_col2.button("🟢 DRS Active", width="stretch"):
                    if not drs_candidates.empty:
                        st.session_state[slider_key] = int(drs_candidates.index[0])
                    else:
                        st.session_state[slider_key] = int(car_df["speed"].idxmax())
                if q_col3.button("🛑 Heavy Braking", width="stretch"):
                    brk_candidates = car_df[car_df["brake"] > 50]
                    if not brk_candidates.empty:
                        st.session_state[slider_key] = int(brk_candidates.index[0])
                if q_col4.button("🏎️ Mid-Stint", width="stretch"):
                    st.session_state[slider_key] = len(car_df) // 2
                if q_col5.button("🔴 Live Head", width="stretch"):
                    st.session_state[slider_key] = len(car_df) - 1

                snap_latest = st.checkbox(
                    "🔴 Snap Cockpit to Latest Telemetry (Live Tracking)",
                    value=False,
                    help="Automatically locks the steering wheel and pedals to the newest data point as cars stream live on track."
                )

                if snap_latest:
                    st.session_state[slider_key] = len(car_df) - 1
                elif slider_key not in st.session_state:
                    if not drs_candidates.empty:
                        st.session_state[slider_key] = int(drs_candidates.index[0])
                    else:
                        st.session_state[slider_key] = int(car_df["speed"].idxmax())
                        
                st.session_state[slider_key] = max(0, min(int(st.session_state[slider_key]), len(car_df) - 1))
                
                scrub_idx = st.slider(
                    "Scrub Timeline Across Session",
                    min_value=0,
                    max_value=len(car_df) - 1,
                    key=slider_key,
                    help="Drag slider to scrub through real car telemetry across the session."
                )
                
                current_sample = car_df.iloc[scrub_idx]
                curr_speed = int(current_sample.get("speed", 0))
                curr_rpm = int(current_sample.get("rpm", 0))
                curr_gear = int(current_sample.get("n_gear", 0))
                gear_text = "N" if curr_gear == 0 else ("R" if curr_gear == -1 else str(curr_gear))
                
                raw_thr = current_sample.get("throttle", 0)
                raw_brk = current_sample.get("brake", 0)
                curr_throttle = min(100, max(0, int(raw_thr)))
                curr_brake = 100 if raw_brk > 50 else (min(100, int(raw_brk)) if raw_brk <= 100 else 100)
                
                raw_drs = current_sample.get("drs")
                drs_active = raw_drs in [10, 12, 14, 1, True]
                if (raw_drs is None or pd.isna(raw_drs)) and not drs_active:
                    if curr_speed >= 265 and curr_throttle >= 90 and curr_gear >= 6 and curr_brake <= 10:
                        drs_active = True

                drs_label = "DRS OPEN" if drs_active else "DRS CLOSED"
                drs_badge_color = "#00E676" if drs_active else "#283447"
                drs_text_color = "#000000" if drs_active else "#CBD5E1"
                drs_glow = "box-shadow: 0 0 12px rgba(0, 230, 118, 0.8);" if drs_active else ""
                
                sample_time = str(current_sample.get("date", ""))[:19].replace("T", " ")
                
                # Generate 15 LED Shift Lights HTML
                led_html = ""
                for i in range(15):
                    # 0..4: Green (9000-10500)
                    if i < 5:
                        threshold = 9000 + i * 300
                        is_lit = curr_rpm >= threshold
                        color = "#00E676" if is_lit else "#131A26"
                        glow = "box-shadow: 0 0 10px #00E676;" if is_lit else ""
                    # 5..9: Red (10500-11750)
                    elif i < 10:
                        threshold = 10500 + (i - 5) * 250
                        is_lit = curr_rpm >= threshold
                        color = "#FF1744" if is_lit else "#131A26"
                        glow = "box-shadow: 0 0 10px #FF1744;" if is_lit else ""
                    # 10..14: Purple (11750-12500)
                    else:
                        threshold = 11750 + (i - 10) * 150
                        is_lit = curr_rpm >= threshold
                        color = "#A855F7" if is_lit else "#131A26"
                        glow = "box-shadow: 0 0 12px #A855F7;" if is_lit else ""
                    led_html += f'<div class="led-dot" style="background:{color}; {glow}"></div>'
                    
                rpm_bar_pct = min(100, max(0, int((curr_rpm / 13000) * 100)))
                
                # Render Steering Wheel HTML via st.html
                wheel_markup = f"""<div class="f1-wheel-bezel"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;"><span style="font-weight:800; font-size:13px; color:#F8FAFC; letter-spacing:1px;">{sel_driver_code} · {sel_team_name.upper()}</span><span style="background:{drs_badge_color}; color:{drs_text_color}; font-weight:800; font-size:11px; padding:3px 10px; border-radius:4px; letter-spacing:1px; {drs_glow}">{drs_label}</span><span style="color:#CBD5E1; font-size:11px; font-family:'JetBrains Mono';">⏱️ {sample_time} UTC</span></div><div class="led-bar">{led_html}</div><div class="wheel-screen"><div class="pedal-col"><span class="pedal-label">BRAKE</span><div class="pedal-track"><div class="pedal-fill-brake" style="height:{curr_brake}%;"></div></div><span style="color:#FF1744; font-weight:800; font-size:12px; font-family:'JetBrains Mono';">{curr_brake}%</span></div><div class="wheel-center"><div class="wheel-gear">{gear_text}</div><div class="wheel-speed">{curr_speed} <span style="font-size:16px; color:#CBD5E1; font-weight:700;">KM/H</span></div><div style="color:#38BDF8; font-weight:800; font-size:16px; font-family:'JetBrains Mono'; margin-top:4px;">{curr_rpm:,} <span style="font-size:11px; color:#CBD5E1;">RPM</span></div><div class="wheel-rpm-bar"><div class="wheel-rpm-fill" style="width:{rpm_bar_pct}%;"></div></div></div><div class="pedal-col"><span class="pedal-label">THROTTLE</span><div class="pedal-track"><div class="pedal-fill-throttle" style="height:{curr_throttle}%;"></div></div><span style="color:#00E676; font-weight:800; font-size:12px; font-family:'JetBrains Mono';">{curr_throttle}%</span></div></div></div>"""
                st.html(wheel_markup)
                
                # Synchronized Telemetry Strip Chart Around Selected Sample
                window_size = 120
                start_win = max(0, scrub_idx - window_size // 2)
                end_win = min(len(car_df), scrub_idx + window_size // 2)
                win_df = car_df.iloc[start_win:end_win].reset_index(drop=True)
                
                fig_strip = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.08,
                    subplot_titles=("Speed (km/h) Across Timeline", "Pedal Inputs (%)")
                )
                
                fig_strip.add_trace(
                    go.Scatter(
                        x=win_df.index,
                        y=win_df["speed"],
                        name="Speed",
                        line=dict(color="#00D2BE", width=2)
                    ),
                    row=1, col=1
                )
                
                # Active scrub marker line
                scrub_pos_in_win = scrub_idx - start_win
                fig_strip.add_vline(x=scrub_pos_in_win, line_dash="dash", line_color="#FF1744", row=1, col=1)
                fig_strip.add_vline(x=scrub_pos_in_win, line_dash="dash", line_color="#FF1744", row=2, col=1)
                
                fig_strip.add_trace(
                    go.Scatter(
                        x=win_df.index,
                        y=win_df["throttle"],
                        name="Throttle (%)",
                        line=dict(color="#00E676", width=1.5)
                    ),
                    row=2, col=1
                )
                
                norm_brake = win_df["brake"].apply(lambda b: 100 if b > 50 else (b if b <= 100 else 100))
                fig_strip.add_trace(
                    go.Scatter(
                        x=win_df.index,
                        y=norm_brake,
                        name="Brake (%)",
                        line=dict(color="#FF1744", width=1.5),
                        fill="tozeroy",
                        fillcolor="rgba(255, 23, 68, 0.15)"
                    ),
                    row=2, col=1
                )
                
                fig_strip.update_layout(
                    height=380,
                    margin=dict(l=40, r=20, t=30, b=20),
                    legend=dict(orientation="h", y=1.1, x=1, xanchor="right")
                )
                fig_strip.update_xaxes(showticklabels=False)
                fig_strip = style_plotly_fig(fig_strip)
                
                st.plotly_chart(fig_strip, width="stretch")
                st.caption("💡 **How to interpret:** The vertical dashed red marker indicates your scrubbed position on track. Notice how high speed directly corresponds to green throttle, and sharp speed drops immediately follow red brake spikes.")
            else:
                st.warning(f"No car telemetry stream available for driver #{sel_driver_num} in this session.")
        else:
            st.info("Loading driver list for cockpit view...")
            
    # -----------------------------------------------------
    # TAB 3: LIVE TEAM RADIO AUDIO PLAYER
    # -----------------------------------------------------
    with tab_radio:
        st.markdown("### 📻 Official FIA Team Radio Communications")
        st.caption("Listen to live, unedited broadcast audio clips between drivers and race engineers.")
        
        radio_df = fetch_openf1_team_radio(selected_session_key)
        drivers_df = fetch_openf1_drivers(selected_session_key)
        
        if not radio_df.empty:
            if not drivers_df.empty:
                radio_merged = pd.merge(radio_df, drivers_df, on="driver_number", how="left")
            else:
                radio_merged = radio_df
                
            radio_merged = radio_merged.sort_values("date", ascending=False).reset_index(drop=True)
            
            all_radio_drivers = ["ALL DRIVERS"] + sorted(radio_merged["name_acronym"].dropna().unique().tolist())
            selected_radio_driver = st.selectbox("Filter by Driver", all_radio_drivers)
            
            if selected_radio_driver != "ALL DRIVERS":
                radio_merged = radio_merged[radio_merged["name_acronym"] == selected_radio_driver]
                
            st.markdown(f"**Found {len(radio_merged)} team radio transmissions**")
            
            for _, r_item in radio_merged.head(15).iterrows():
                drv_name = r_item.get("full_name", f"Car #{r_item.get('driver_number')}")
                drv_code = r_item.get("name_acronym", "F1")
                team = r_item.get("team_name", "F1 Team")
                raw_time = str(r_item.get("date", ""))[:19].replace("T", " ")
                audio_url = r_item.get("recording_url")
                drv_color = get_driver_color(drv_code, team)
                
                st.html(f"""
                <div class="radio-card" style="border-left-color: {drv_color};">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <div>
                            <span style="font-weight:800; font-size:16px; color:#FFF;">{drv_name} ({drv_code})</span>
                            <span style="color:#CBD5E1; font-size:12px; margin-left:8px;">{team}</span>
                        </div>
                        <span style="color:#CBD5E1; font-size:12px; font-family:'JetBrains Mono';">⏱️ {raw_time} UTC</span>
                    </div>
                </div>
                """)
                
                if audio_url:
                    st.audio(audio_url)
        else:
            st.info("No team radio transmissions recorded for this session yet.")
            
    # -----------------------------------------------------
    # TAB 4: FIA RACE CONTROL MESSAGES
    # -----------------------------------------------------
    with tab_rc:
        st.markdown("### 🚨 FIA Race Control & Official Notices")
        st.caption("Live track status, flags, safety cars, investigations, and lap deletions.")
        
        with st.expander("💡 FIA Flag Guide: What do the colors mean?"):
            f_col1, f_col2, f_col3, f_col4 = st.columns(4)
            f_col1.markdown("**🟢 GREEN**<br><span style='color:#CBD5E1; font-size:12px;'>Track clear, maximum racing speed authorized.</span>", unsafe_allow_html=True)
            f_col2.markdown("**🟡 YELLOW**<br><span style='color:#CBD5E1; font-size:12px;'>Hazard on circuit, reduce speed, no overtaking.</span>", unsafe_allow_html=True)
            f_col3.markdown("**🔴 RED**<br><span style='color:#CBD5E1; font-size:12px;'>Session stopped, dangerous debris or heavy crash.</span>", unsafe_allow_html=True)
            f_col4.markdown("**🟣 SAFETY CAR**<br><span style='color:#CBD5E1; font-size:12px;'>Field neutralised at regulated pace while marshals work.</span>", unsafe_allow_html=True)
            
        rc_df = fetch_openf1_race_control(selected_session_key)
        
        if not rc_df.empty:
            rc_df = rc_df.sort_values("date", ascending=False).reset_index(drop=True)
            
            category_filter = st.selectbox(
                "Filter Category",
                ["ALL"] + sorted(rc_df["category"].dropna().unique().tolist())
            )
            
            filtered_rc = rc_df if category_filter == "ALL" else rc_df[rc_df["category"] == category_filter]
            
            for _, rc_item in filtered_rc.head(25).iterrows():
                cat = rc_item.get("category", "Notice")
                flag = rc_item.get("flag")
                msg = rc_item.get("message", "")
                rc_time = str(rc_item.get("date", ""))[:19].replace("T", " ")
                
                flag_color = "#38BDF8"
                flag_label = flag or cat
                flag_text_color = "#FFFFFF"
                if flag == "GREEN":
                    flag_color = "#00E676"
                    flag_text_color = "#000000"
                elif flag in ["YELLOW", "DOUBLE YELLOW"]:
                    flag_color = "#FFD700"
                    flag_text_color = "#000000"
                elif flag in ["RED", "CHEQUERED"]:
                    flag_color = "#FF1744"
                    flag_text_color = "#FFFFFF"
                elif "SAFETY" in str(msg).upper() or "VSC" in str(msg).upper():
                    flag_color = "#C084FC"
                    flag_text_color = "#000000"
                    flag_label = "SAFETY CAR"
                elif "DELETED" in str(msg).upper():
                    flag_color = "#F97316"
                    flag_text_color = "#000000"
                    flag_label = "TRACK LIMITS"
                    
                st.html(f"""
                <div style="background:#0E1320; border:1px solid #1C2438; border-left: 4px solid {flag_color}; border-radius:6px; padding:10px 14px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="background:{flag_color}; color:{flag_text_color}; font-weight:800; font-size:10px; padding:2px 8px; border-radius:3px; letter-spacing:1px;">
                            {flag_label}
                        </span>
                        <span style="color:#CBD5E1; font-size:11px; font-family:'JetBrains Mono';">{rc_time} UTC</span>
                    </div>
                    <div style="color:#F1F5F9; font-size:14px; font-weight:600; margin-top:6px;">
                        {msg}
                    </div>
                </div>
                """)
        else:
            st.info("No race control messages published for this session.")

    # Auto-polling trigger for live sessions
    if auto_refresh:
        import time
        time.sleep(refresh_sec)
        st.cache_data.clear()
        st.rerun()

# =========================================================
# VIEW 2: DEEP TELEMETRY & LAP ARCHIVES (TIF1 ENGINE)
# =========================================================

else:
    with st.sidebar:
        st.markdown("### Archive Session Selector")
        available_years = [2026, 2025, 2024, 2023, 2022, 2021]
        year = st.selectbox("Season", available_years, index=2)
        
        with st.spinner("Connecting to race archives..."):
            event_names = get_event_names(year)
        
        if not event_names:
            st.error("No events available for this season.")
            st.stop()
            
        default_event_idx = (
            event_names.index("Bahrain Grand Prix")
            if "Bahrain Grand Prix" in event_names
            else 0
        )
        event_name = st.selectbox("Grand Prix", event_names, index=default_event_idx)
        
        session_names = get_session_names(year, event_name)
        if not session_names:
            st.error("No sessions available for this event.")
            st.stop()
            
        default_session_idx = (
            session_names.index("Qualifying")
            if "Qualifying" in session_names
            else 0
        )
        session_name = st.selectbox("Session", session_names, index=default_session_idx)
        
        with st.spinner("Retrieving driver timing data..."):
            driver_codes = get_session_and_drivers(year, event_name, session_name)
            
        if not driver_codes:
            st.error("No driver telemetry found for this session.")
            st.stop()
            
        default_driver_idx = driver_codes.index("VER") if "VER" in driver_codes else 0
        driver_1_code = st.selectbox("Primary Driver", driver_codes, index=default_driver_idx)
        
        st.markdown("---")
        st.markdown("### Head-to-Head Comparison")
        enable_compare = st.checkbox("Compare with 2nd Driver", value=True)
        
        driver_2_code = None
        if enable_compare:
            alt_drivers = [d for d in driver_codes if d != driver_1_code]
            default_driver_2_idx = (
                alt_drivers.index("LEC") if "LEC" in alt_drivers
                else (alt_drivers.index("HAM") if "HAM" in alt_drivers else 0)
            ) if alt_drivers else 0
            driver_2_code = st.selectbox("Compare Against", alt_drivers, index=default_driver_2_idx)

    # Load Telemetry
    try:
        with st.spinner(f"Loading {driver_1_code} telemetry..."):
            tel1, meta1 = load_driver_data(year, event_name, session_name, driver_1_code)
    except Exception as e:
        st.error(f"Failed to load telemetry for {driver_1_code}: {e}")
        st.stop()

    if tel1.empty:
        st.warning(f"No telemetry data points for {driver_1_code}.")
        st.stop()

    tel1 = tel1.sort_values("Distance").reset_index(drop=True)

    tel2, meta2 = None, None
    if enable_compare and driver_2_code:
        try:
            with st.spinner(f"Loading {driver_2_code} telemetry..."):
                tel2, meta2 = load_driver_data(year, event_name, session_name, driver_2_code)
                if not tel2.empty:
                    tel2 = tel2.sort_values("Distance").reset_index(drop=True)
        except Exception as e:
            st.warning(f"Could not load comparison driver {driver_2_code}: {e}")
            tel2 = None

    color1 = get_driver_color(driver_1_code, meta1.get("team"))
    color2 = get_driver_color(driver_2_code, meta2.get("team")) if driver_2_code else "#F59E0B"

    # Driver Hero Header
    st.markdown(f'<div class="f1-badge">{year} · {event_name.upper()} · {session_name.upper()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">TELEMETRY & RACE DYNAMICS ANALYZER</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">High-frequency telemetry traces, apex dynamics, trail-braking, and micro-sector delta profiling.</div>', unsafe_allow_html=True)

    badge1_html = get_compound_badge_html(meta1.get('compound'), meta1.get('tyre_life'))
    badge2_html = get_compound_badge_html(meta2.get('compound'), meta2.get('tyre_life')) if meta2 else ""

    if tel2 is not None and meta2 is not None:
        c1, c2 = st.columns(2)
        with c1:
            st.html(f"""
            <div class="f1-card" style="border-left: 5px solid {color1};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <span class="f1-card-label">{meta1['team']}</span>
                        <h2 style="margin:2px 0 6px 0; color:#FFF; font-size:28px;">{driver_1_code}</h2>
                    </div>
                    <div style="text-align:right;">
                        <span class="f1-card-label">FASTEST LAP</span>
                        <div style="color:{color1}; font-size:22px; font-weight:800; font-family:'JetBrains Mono';">{meta1['lap_time']}</div>
                        <div style="margin-top:4px;">{badge1_html}</div>
                    </div>
                </div>
            </div>
            """)
        with c2:
            st.html(f"""
            <div class="f1-card" style="border-left: 5px solid {color2};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <span class="f1-card-label">{meta2['team']}</span>
                        <h2 style="margin:2px 0 6px 0; color:#FFF; font-size:28px;">{driver_2_code}</h2>
                    </div>
                    <div style="text-align:right;">
                        <span class="f1-card-label">FASTEST LAP</span>
                        <div style="color:{color2}; font-size:22px; font-weight:800; font-family:'JetBrains Mono';">{meta2['lap_time']}</div>
                        <div style="margin-top:4px;">{badge2_html}</div>
                    </div>
                </div>
            </div>
            """)
    else:
        st.html(f"""
        <div class="f1-card" style="border-left: 5px solid {color1}; max-width: 500px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span class="f1-card-label">{meta1['team']}</span>
                    <h2 style="margin:2px 0 0 0; color:#FFF; font-size:28px;">{driver_1_code}</h2>
                </div>
                <div style="text-align:right;">
                    <span class="f1-card-label">FASTEST LAP</span>
                    <div style="color:{color1}; font-size:22px; font-weight:800; font-family:'JetBrains Mono';">{meta1['lap_time']}</div>
                    <div style="margin-top:4px;">{badge1_html}</div>
                </div>
            </div>
        </div>
        """)

    st.write("")

    # Quick Stats
    m1, m2, m3, m4, m5 = st.columns(5)
    top_speed = tel1["Speed"].max()
    avg_speed = tel1["Speed"].mean()
    full_throttle_pct = (tel1["Throttle"] >= 98).mean() * 100
    gear_shifts = int(tel1["nGear"].diff().ne(0).sum())
    brake_pct = tel1["Brake"].astype(bool).mean() * 100

    with m1:
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Top Speed</div>
            <div class="f1-card-value">{top_speed:.1f} <span style="font-size:14px; font-weight:600; color:#CBD5E1;">km/h</span></div>
            <div class="f1-card-sub">{driver_1_code} Peak</div>
        </div>
        """)

    with m2:
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Avg Speed</div>
            <div class="f1-card-value">{avg_speed:.1f} <span style="font-size:14px; font-weight:600; color:#CBD5E1;">km/h</span></div>
            <div class="f1-card-sub">Lap Mean</div>
        </div>
        """)

    with m3:
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Full Throttle</div>
            <div class="f1-card-value">{full_throttle_pct:.1f}<span style="font-size:14px; font-weight:600; color:#CBD5E1;">%</span></div>
            <div class="f1-card-sub">Lap Time at WOT</div>
        </div>
        """)

    with m4:
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Gear Shifts</div>
            <div class="f1-card-value">{gear_shifts}</div>
            <div class="f1-card-sub">Transmission shifts</div>
        </div>
        """)

    with m5:
        st.html(f"""
        <div class="f1-card">
            <div class="f1-card-label">Braking Duty</div>
            <div class="f1-card-value">{brake_pct:.1f}<span style="font-size:14px; font-weight:600; color:#CBD5E1;">%</span></div>
            <div class="f1-card-sub">Distance on Brakes</div>
        </div>
        """)

    st.write("")

    # Interactive Tabs
    tab_telemetry, tab_battle, tab_track, tab_braking, tab_data = st.tabs([
        "📊 Telemetry Stack",
        "⚔️ Head-to-Head Battle",
        "🗺️ Interactive Track & Speed Map",
        "🛑 Braking & G-Force Dynamics",
        "📑 Telemetry Data & Export"
    ])

    # TAB 1: TELEMETRY STACK
    with tab_telemetry:
        st.markdown("### Synchronized Lap Telemetry Channels")
        st.caption("Hover across any point on circuit distance to inspect synchronized speed, inputs, gear, and G-forces.")
        
        with st.expander("💡 Telemetry Decoder: What am I looking at?"):
            t_c1, t_c2, t_c3, t_c4 = st.columns(4)
            t_c1.markdown("**📈 Speed Graph**<br><span style='color:#CBD5E1; font-size:12px;'>High peaks = Long straights (300+ km/h). Deep V-shaped dips = Tight slow corners (80-110 km/h).</span>", unsafe_allow_html=True)
            t_c2.markdown("**🦶 Pedals (Brake & Throttle)**<br><span style='color:#CBD5E1; font-size:12px;'>Red spikes = Heavy braking zone before turn-in. Green line = Rolling onto full power on corner exit.</span>", unsafe_allow_html=True)
            t_c3.markdown("**⚙️ Gear Shift Staircase**<br><span style='color:#CBD5E1; font-size:12px;'>8-speed paddle shifts. Steps drop down to 2nd/3rd gear in hairpins, and climb to 8th on straights.</span>", unsafe_allow_html=True)
            t_c4.markdown("**🧲 G-Forces**<br><span style='color:#CBD5E1; font-size:12px;'>5G braking feels like 5x driver body weight! Purple curve = Lateral neck-straining cornering force.</span>", unsafe_allow_html=True)
        
        has_accel = "AccelerationX" in tel1.columns and "AccelerationY" in tel1.columns
        rows_count = 4 if has_accel else 3
        row_heights = [0.35, 0.25, 0.20, 0.20] if has_accel else [0.45, 0.30, 0.25]
        
        fig_tel = make_subplots(
            rows=rows_count,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.04,
            row_heights=row_heights,
            subplot_titles=(
                "Speed (km/h)",
                "Throttle & Brake (%)",
                "Gear & RPM",
                "Longitudinal & Lateral Acceleration (G)" if has_accel else None
            )
        )
        
        fig_tel.add_trace(
            go.Scatter(
                x=tel1["Distance"],
                y=tel1["Speed"],
                name=f"{driver_1_code} Speed",
                line=dict(color=color1, width=2.2),
                hovertemplate="Distance: %{x:.0f}m<br>Speed: %{y:.1f} km/h<extra></extra>"
            ),
            row=1, col=1
        )
        
        if "DRS" in tel1.columns:
            drs_active = tel1[tel1["DRS"].isin([10, 12, 14, 1, True])]
            if not drs_active.empty:
                fig_tel.add_trace(
                    go.Scatter(
                        x=drs_active["Distance"],
                        y=drs_active["Speed"],
                        mode="markers",
                        name="DRS Active",
                        marker=dict(size=3, color="#22C55E", symbol="circle"),
                        hovertemplate="DRS Open<extra></extra>"
                    ),
                    row=1, col=1
                )
                
        fig_tel.add_trace(
            go.Scatter(
                x=tel1["Distance"],
                y=tel1["Throttle"],
                name="Throttle",
                line=dict(color="#00E676", width=1.8),
                hovertemplate="Throttle: %{y:.0f}%<extra></extra>"
            ),
            row=2, col=1
        )
        
        brake_val = tel1["Brake"].astype(bool).astype(int) * 100
        fig_tel.add_trace(
            go.Scatter(
                x=tel1["Distance"],
                y=brake_val,
                name="Brake",
                line=dict(color="#FF1744", width=1.8),
                fill="tozeroy",
                fillcolor="rgba(255, 23, 68, 0.15)",
                hovertemplate="Brake: %{y:.0f}%<extra></extra>"
            ),
            row=2, col=1
        )
        
        fig_tel.add_trace(
            go.Scatter(
                x=tel1["Distance"],
                y=tel1["nGear"],
                name="Gear",
                line=dict(color="#F59E0B", width=2, shape="hv"),
                hovertemplate="Gear: %{y}<extra></extra>"
            ),
            row=3, col=1
        )
        
        if has_accel:
            long_g = tel1["AccelerationX"] / 9.80665
            lat_g = tel1["AccelerationY"] / 9.80665
            fig_tel.add_trace(
                go.Scatter(
                    x=tel1["Distance"],
                    y=long_g,
                    name="Longitudinal G (Acc/Brake)",
                    line=dict(color="#38BDF8", width=1.5),
                    hovertemplate="Long G: %{y:.2f} G<extra></extra>"
                ),
                row=4, col=1
            )
            fig_tel.add_trace(
                go.Scatter(
                    x=tel1["Distance"],
                    y=lat_g,
                    name="Lateral G (Cornering)",
                    line=dict(color="#C084FC", width=1.5),
                    hovertemplate="Lat G: %{y:.2f} G<extra></extra>"
                ),
                row=4, col=1
            )
            fig_tel.update_yaxes(title_text="G-Force (G)", row=4, col=1, gridcolor="#1A2234")
            
        fig_tel.update_layout(
            height=850,
            margin=dict(l=50, r=30, t=40, b=40),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(14, 19, 31, 0.8)",
                bordercolor="#1C2438",
                borderwidth=1
            )
        )
        
        fig_tel.update_xaxes(title_text="Track Distance (metres)", row=rows_count, col=1)
        fig_tel.update_yaxes(title_text="Speed (km/h)", row=1, col=1)
        fig_tel.update_yaxes(title_text="Input (%)", range=[-5, 105], row=2, col=1)
        fig_tel.update_yaxes(title_text="Gear", tickmode="linear", tick0=1, dtick=1, range=[0.5, 8.5], row=3, col=1)
        fig_tel = style_plotly_fig(fig_tel)
        
        st.plotly_chart(fig_tel, width="stretch")

    # TAB 2: HEAD TO HEAD BATTLE
    with tab_battle:
        if tel2 is not None and meta2 is not None:
            st.markdown(f"### Head-to-Head: {driver_1_code} vs {driver_2_code}")
            st.caption(r"Comprehensive delta time ($\Delta t$) analysis and overlaid driver inputs over lap distance.")
            
            max_common_dist = min(tel1["Distance"].max(), tel2["Distance"].max())
            dist_grid = np.linspace(0, max_common_dist, 1500)
            
            t1_sec = (tel1["Time"] - tel1["Time"].iloc[0]).dt.total_seconds()
            t2_sec = (tel2["Time"] - tel2["Time"].iloc[0]).dt.total_seconds()
            
            t1_interp = np.interp(dist_grid, tel1["Distance"], t1_sec)
            t2_interp = np.interp(dist_grid, tel2["Distance"], t2_sec)
            delta_time = t1_interp - t2_interp
            
            s1_interp = np.interp(dist_grid, tel1["Distance"], tel1["Speed"])
            s2_interp = np.interp(dist_grid, tel2["Distance"], tel2["Speed"])
            
            final_delta = delta_time[-1]
            ahead_driver = driver_1_code if final_delta < 0 else driver_2_code
            delta_str = f"{abs(final_delta):.3f}s"
            
            d_col1, d_col2, d_col3, d_col4 = st.columns(4)
            with d_col1:
                st.html(f"""
                <div class="f1-card">
                    <div class="f1-card-label">Lap Time Difference</div>
                    <div class="f1-card-value" style="color:{color1 if final_delta < 0 else color2};">
                        {ahead_driver} -{delta_str}
                    </div>
                    <div class="f1-card-sub">At Finish Line</div>
                </div>
                """)
                
            with d_col2:
                st.html(f"""
                <div class="f1-card">
                    <div class="f1-card-label">Top Speed Advantage</div>
                    <div class="f1-card-value">
                        {tel1['Speed'].max() - tel2['Speed'].max():+.1f} <span style="font-size:14px; font-weight:600; color:#CBD5E1;">km/h</span>
                    </div>
                    <div class="f1-card-sub">{driver_1_code} vs {driver_2_code}</div>
                </div>
                """)
                
            with d_col3:
                st.html(f"""
                <div class="f1-card">
                    <div class="f1-card-label">Avg Speed Advantage</div>
                    <div class="f1-card-value">
                        {tel1['Speed'].mean() - tel2['Speed'].mean():+.1f} <span style="font-size:14px; font-weight:600; color:#CBD5E1;">km/h</span>
                    </div>
                    <div class="f1-card-sub">{driver_1_code} vs {driver_2_code}</div>
                </div>
                """)
                
            with d_col4:
                wot1 = (tel1["Throttle"] >= 98).mean() * 100
                wot2 = (tel2["Throttle"] >= 98).mean() * 100
                st.html(f"""
                <div class="f1-card">
                    <div class="f1-card-label">WOT Throttle Delta</div>
                    <div class="f1-card-value">{wot1 - wot2:+.1f}<span style="font-size:14px; font-weight:600; color:#CBD5E1;">%</span></div>
                    <div class="f1-card-sub">Full Throttle Time Delta</div>
                </div>
                """)
                
            st.write("")
            
            # Plain-English Telemetry Analysis for Non-F1 Fans
            top_speed_diff = tel1['Speed'].max() - tel2['Speed'].max()
            slow_corners_1 = tel1[tel1["Speed"] <= 130]["Speed"].mean() if not tel1[tel1["Speed"] <= 130].empty else 0
            slow_corners_2 = tel2[tel2["Speed"] <= 130]["Speed"].mean() if not tel2[tel2["Speed"] <= 130].empty else 0
            corner_diff = slow_corners_1 - slow_corners_2
            wot_diff = wot1 - wot2

            if top_speed_diff > 1.5:
                straight_verdict = f"⚡ <b>Straight-Line Speed:</b> {driver_1_code} held a <b>+{top_speed_diff:.1f} km/h top speed advantage</b> on long straights, gaining time through lower aerodynamic drag and DRS."
            elif top_speed_diff < -1.5:
                straight_verdict = f"⚡ <b>Straight-Line Speed:</b> {driver_2_code} held a <b>+{abs(top_speed_diff):.1f} km/h top speed advantage</b>, pulling away on high-speed flat-out stretches."
            else:
                straight_verdict = f"⚡ <b>Straight-Line Speed:</b> Both cars were dead-even on maximum straightline velocity (within {abs(top_speed_diff):.1f} km/h)."

            if corner_diff > 1.0:
                corner_verdict = f"🔄 <b>Slow Corner Carrying Speed:</b> {driver_1_code} carried <b>+{corner_diff:.1f} km/h more mid-corner apex speed</b> through tight turns, rotating the car earlier."
            elif corner_diff < -1.0:
                corner_verdict = f"🔄 <b>Slow Corner Carrying Speed:</b> {driver_2_code} carried <b>+{abs(corner_diff):.1f} km/h more mid-corner apex speed</b>, exploiting superior mechanical downforce."
            else:
                corner_verdict = f"🔄 <b>Slow Corner Carrying Speed:</b> Both drivers matched cornering speeds within 1 km/h through the slowest apexes."

            if wot_diff > 2.0:
                throttle_verdict = f"🟢 <b>Throttle Aggression:</b> {driver_1_code} spent <b>{wot_diff:+.1f}% more lap time flat-out on throttle</b>, getting back to 100% power earlier on corner exits."
            elif wot_diff < -2.0:
                throttle_verdict = f"🟢 <b>Throttle Aggression:</b> {driver_2_code} spent <b>{abs(wot_diff):.1f}% more lap time flat-out on throttle</b>, exiting corners with cleaner traction."
            else:
                throttle_verdict = f"🟢 <b>Throttle Aggression:</b> Both drivers applied full throttle with near-identical commitment ({wot1:.1f}% vs {wot2:.1f}%)."

            verdict_markup = f"""<div style="background: rgba(14, 20, 36, 0.95); border: 1px solid #1C2D4A; border-left: 5px solid #00D2BE; border-radius: 10px; padding: 16px 20px; margin: 12px 0 20px 0;"><div style="font-size: 14px; font-weight: 800; color: #00D2BE; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;">🏁 Plain-English Race Analyst Verdict // Who was faster and why?</div><div style="color: #F8FAFC; font-size: 14px; font-weight: 600; line-height: 1.6; margin-bottom: 10px;">{ahead_driver} finished the lap <b>{delta_str} ahead</b>. Here is the exact telemetry breakdown:</div><ul style="color: #CBD5E1; font-size: 13px; line-height: 1.8; margin: 0; padding-left: 18px;"><li>{straight_verdict}</li><li>{corner_verdict}</li><li>{throttle_verdict}</li></ul><div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #1F2A42; font-size: 12px; color: #94A3B8;">💡 <b>How to read the curve below:</b> When the cyan Δt line slopes <b>UP</b> ➔ {driver_1_code} is pulling away / gaining time. When it slopes <b>DOWN</b> ➔ {driver_2_code} is catching up. When it's <b>FLAT</b> ➔ both are matching pace.</div></div>"""
            st.html(verdict_markup)
            
            fig_battle = make_subplots(
                rows=3,
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.04,
                row_heights=[0.35, 0.40, 0.25],
                subplot_titles=(
                    f"Time Delta: Δt [UP = {driver_1_code} Faster | DOWN = {driver_2_code} Faster]",
                    "Speed Overlay (km/h) [Higher Line = Faster]",
                    f"Throttle & Braking Overlay (%) [Solid = {driver_1_code} | Dotted = {driver_2_code}]"
                )
            )
            
            d1_lead = -delta_time
            fig_battle.add_trace(
                go.Scatter(
                    x=dist_grid,
                    y=d1_lead,
                    name=f"Δt ({driver_1_code} Lead)",
                    line=dict(color="#00F0FF", width=2.2),
                    hovertemplate="Distance: %{x:.0f}m<br>Time Delta: %{y:+.3f}s<extra></extra>"
                ),
                row=1, col=1
            )
            fig_battle.add_hline(y=0, line_dash="dash", line_color="#8895AD", row=1, col=1)
            
            fig_battle.add_trace(
                go.Scatter(
                    x=tel1["Distance"],
                    y=tel1["Speed"],
                    name=f"{driver_1_code} Speed",
                    line=dict(color=color1, width=2.2),
                    hovertemplate=f"{driver_1_code}: %{{y:.1f}} km/h<extra></extra>"
                ),
                row=2, col=1
            )
            fig_battle.add_trace(
                go.Scatter(
                    x=tel2["Distance"],
                    y=tel2["Speed"],
                    name=f"{driver_2_code} Speed",
                    line=dict(color=color2, width=2.2),
                    hovertemplate=f"{driver_2_code}: %{{y:.1f}} km/h<extra></extra>"
                ),
                row=2, col=1
            )
            
            fig_battle.add_trace(
                go.Scatter(
                    x=tel1["Distance"],
                    y=tel1["Throttle"],
                    name=f"{driver_1_code} Throttle",
                    line=dict(color=color1, width=1.5, dash="solid"),
                    hovertemplate=f"{driver_1_code} Thr: %{{y:.0f}}%<extra></extra>"
                ),
                row=3, col=1
            )
            fig_battle.add_trace(
                go.Scatter(
                    x=tel2["Distance"],
                    y=tel2["Throttle"],
                    name=f"{driver_2_code} Throttle",
                    line=dict(color=color2, width=1.5, dash="dot"),
                    hovertemplate=f"{driver_2_code} Thr: %{{y:.0f}}%<extra></extra>"
                ),
                row=3, col=1
            )
            
            b1 = tel1[tel1["Brake"].astype(bool)]
            b2 = tel2[tel2["Brake"].astype(bool)]
            fig_battle.add_trace(
                go.Scatter(
                    x=b1["Distance"],
                    y=[-5] * len(b1),
                    mode="markers",
                    name=f"{driver_1_code} Braking",
                    marker=dict(color=color1, size=4, symbol="square"),
                    hovertemplate=f"{driver_1_code} Braking<extra></extra>"
                ),
                row=3, col=1
            )
            fig_battle.add_trace(
                go.Scatter(
                    x=b2["Distance"],
                    y=[-10] * len(b2),
                    mode="markers",
                    name=f"{driver_2_code} Braking",
                    marker=dict(color=color2, size=4, symbol="square"),
                    hovertemplate=f"{driver_2_code} Braking<extra></extra>"
                ),
                row=3, col=1
            )
            
            fig_battle.update_layout(
                height=850,
                margin=dict(l=50, r=30, t=40, b=40),
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor="rgba(14, 19, 31, 0.8)",
                    bordercolor="#1C2438",
                    borderwidth=1
                )
            )
            
            fig_battle.update_xaxes(title_text="Track Distance (metres)", row=3, col=1)
            fig_battle.update_yaxes(title_text="Δt (s) [Up = D1 ahead]", row=1, col=1)
            fig_battle.update_yaxes(title_text="Speed (km/h)", row=2, col=1)
            fig_battle.update_yaxes(title_text="Throttle (%)", range=[-15, 105], row=3, col=1)
            fig_battle = style_plotly_fig(fig_battle)
            
            st.plotly_chart(fig_battle, width="stretch")

            # 📸 SOCIAL MEDIA DEBRIEF CARD GENERATOR
            st.write("")
            st.markdown("---")
            st.markdown("### 📸 Shareable F1 Debrief Infographic Generator")
            st.caption("Generate a broadcast-ready, high-resolution 16:9 PNG debrief card comparing both drivers, ready to post on Reddit (r/formula1), Twitter/X, or Discord.")
            
            btn_col1, btn_col2 = st.columns([0.35, 0.65])
            with btn_col1:
                render_debrief_btn = st.button("🎨 Render Broadcast Debrief Card", width="stretch")
                
            if render_debrief_btn or st.session_state.get(f"card_rendered_{driver_1_code}_{driver_2_code}"):
                st.session_state[f"card_rendered_{driver_1_code}_{driver_2_code}"] = True
                with st.spinner("Generating broadcast-quality F1 debrief graphic..."):
                    card_buffer = generate_f1_debrief_card(
                        year, event_name, session_name,
                        driver_1_code, meta1, tel1, color1,
                        driver_2_code, meta2, tel2, color2,
                        dist_grid, delta_time
                    )
                st.image(card_buffer, caption=f"F1 Race Debrief Card · {year} {event_name} · {driver_1_code} vs {driver_2_code}", width="stretch")
                
                st.download_button(
                    label="📥 Download Broadcast Debrief Card (PNG)",
                    data=card_buffer.getvalue(),
                    file_name=f"{year}_{event_name.replace(' ', '_')}_{session_name}_{driver_1_code}_vs_{driver_2_code}_debrief.png",
                    mime="image/png"
                )
        else:
            st.info("Enable 'Compare with 2nd Driver' in the sidebar to unlock Head-to-Head delta profiling, speed difference graphs, and braking overlaps.")

    # TAB 3: INTERACTIVE TRACK MAP
    with tab_track:
        st.markdown("### Interactive 2D Circuit Map")
        st.caption("GPS telemetry path rendered in 2D space. Choose to color the circuit by Speed, Gear, or Braking Zones.")
        
        if "X" in tel1.columns and "Y" in tel1.columns and not tel1["X"].dropna().empty:
            map_color_mode = st.radio(
                "Color Circuit By:",
                ["Speed Heatmap", "Gear Distribution", "Braking & Throttle Zones"],
                horizontal=True
            )
            
            if map_color_mode == "Speed Heatmap":
                st.caption("🔥 **Speed Heatmap:** Warm glowing colors (Red/Orange) represent flat-out straights up to 330+ km/h. Cool dark tones (Blue/Purple) indicate slow technical corners.")
            elif map_color_mode == "Gear Distribution":
                st.caption("⚙️ **Gear Distribution:** Shows transmission gear (1st to 8th) engaged by the driver at every point around the perimeter of the circuit.")
            else:
                st.caption("🟢 **Braking & Throttle Zones:** Green = Full throttle (90-100%). Amber = Coasting/mid-corner feathering. Red Diamonds = Heavy braking application.")
            
            track_df = tel1.dropna(subset=["X", "Y"]).copy()
            fig_map = go.Figure()
            
            if map_color_mode == "Speed Heatmap":
                fig_map.add_trace(
                    go.Scatter(
                        x=track_df["X"],
                        y=track_df["Y"],
                        mode="markers+lines",
                        line=dict(width=4, color="#1E2638"),
                        marker=dict(
                            size=6,
                            color=track_df["Speed"],
                            colorscale="Turbo",
                            colorbar=dict(
                                title=dict(text="Speed (km/h)", font=dict(color="#FFFFFF", family="Titillium Web")),
                                tickfont=dict(color="#CBD5E1", family="JetBrains Mono"),
                                x=1.02, thickness=16, len=0.7
                            ),
                            showscale=True
                        ),
                        text=[f"Dist: {d:.0f}m<br>Speed: {s:.1f} km/h<br>Gear: {g}" 
                              for d, s, g in zip(track_df["Distance"], track_df["Speed"], track_df["nGear"])],
                        hoverinfo="text"
                    )
                )
            elif map_color_mode == "Gear Distribution":
                fig_map.add_trace(
                    go.Scatter(
                        x=track_df["X"],
                        y=track_df["Y"],
                        mode="markers",
                        marker=dict(
                            size=6,
                            color=track_df["nGear"],
                            colorscale="Viridis",
                            colorbar=dict(
                                title=dict(text="Gear", font=dict(color="#FFFFFF", family="Titillium Web")),
                                tickmode="linear", tick0=1, dtick=1,
                                tickfont=dict(color="#CBD5E1", family="JetBrains Mono"),
                                x=1.02, thickness=16, len=0.7
                            ),
                            showscale=True
                        ),
                        text=[f"Gear {g} | {s:.0f} km/h" for g, s in zip(track_df["nGear"], track_df["Speed"])],
                        hoverinfo="text"
                    )
                )
            else:
                brakes = track_df[track_df["Brake"].astype(bool)]
                coasts = track_df[(~track_df["Brake"].astype(bool)) & (track_df["Throttle"] < 90)]
                wot = track_df[track_df["Throttle"] >= 90]
                
                fig_map.add_trace(go.Scatter(
                    x=wot["X"], y=wot["Y"], mode="markers", name="Full Throttle",
                    marker=dict(size=5, color="#00E676")
                ))
                fig_map.add_trace(go.Scatter(
                    x=coasts["X"], y=coasts["Y"], mode="markers", name="Partial Throttle / Coast",
                    marker=dict(size=5, color="#F59E0B")
                ))
                fig_map.add_trace(go.Scatter(
                    x=brakes["X"], y=brakes["Y"], mode="markers", name="Braking Applied",
                    marker=dict(size=7, color="#E10600", symbol="diamond")
                ))
                
            fig_map.add_trace(
                go.Scatter(
                    x=[track_df["X"].iloc[0]],
                    y=[track_df["Y"].iloc[0]],
                    mode="markers+text",
                    name="Start/Finish",
                    marker=dict(size=14, color="#FFFFFF", symbol="star"),
                    text=["START/FINISH"],
                    textposition="top center",
                    textfont=dict(color="#FFFFFF", size=12, family="Titillium Web")
                )
            )
            
            fig_map.update_layout(
                height=700,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1),
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="#FFFFFF")
                )
            )
            fig_map = style_plotly_fig(fig_map)
            
            st.plotly_chart(fig_map, width="stretch")
        else:
            st.warning("GPS spatial coordinates (X, Y) are unavailable for this session.")

    # TAB 4: BRAKING DYNAMICS & G-G DIAGRAM
    with tab_braking:
        st.markdown("### Braking Performance & Grip Exploitation")
        st.caption("Deep-dive into deceleration events, braking distances, and the tire friction limit circle (G-G Diagram).")
        
        with st.expander("💡 Non-F1 Fan Guide: What is G-Force & The Traction Limit?"):
            b_c1, b_c2 = st.columns(2)
            b_c1.markdown("""
            **🛑 Heavy Braking (Up to 5.5G)**
            - In F1, stomping the brakes from 330 km/h down to 80 km/h subjects the driver to **up to 5.5G of deceleration**.
            - That feels like **5.5 times the driver's body weight** pushing them forward against their seatbelts!
            - The table below shows the exact entry speed, apex minimum speed, and meters required to bring the car under control.
            """, unsafe_allow_html=True)
            b_c2.markdown("""
            **⭕ The Friction Limit (G-G Circle)**
            - Tires only possess 100% total friction to give at any second.
            - If a driver uses 100% grip just for braking, they have 0% left for turning (turning will cause the front wheels to lock up and slide off).
            - As the driver eases off the brake pedal (*trail-braking*), they smoothly transfer grip from braking to cornering.
            - **Points on the outer 4G-5G rings show the driver operating right on the ragged edge of tire grip without spinning out!**
            """, unsafe_allow_html=True)
        
        b_df = tel1.copy()
        b_df["Brake"] = b_df["Brake"].fillna(False).astype(bool)
        b_df["Brake_Event"] = (b_df["Brake"] != b_df["Brake"].shift()).cumsum()
        braking_only = b_df[b_df["Brake"]].copy()
        
        if not braking_only.empty:
            summary = braking_only.groupby("Brake_Event").agg(
                Start_Distance=("Distance", "first"),
                End_Distance=("Distance", "last"),
                Start_Speed=("Speed", "first"),
                End_Speed=("Speed", "last"),
                Start_Time=("Time", "first"),
                End_Time=("Time", "last"),
                Readings=("Speed", "count")
            ).reset_index()
            
            summary["Braking_Distance_m"] = (summary["End_Distance"] - summary["Start_Distance"]).round(1)
            summary["Speed_Drop_kmh"] = (summary["Start_Speed"] - summary["End_Speed"]).round(1)
            summary["Duration_s"] = ((summary["End_Time"] - summary["Start_Time"]).dt.total_seconds()).round(2)
            
            summary["Decel_G"] = (
                (summary["Speed_Drop_kmh"] / 3.6) / summary["Duration_s"].where(summary["Duration_s"] > 0) / 9.80665
            ).round(2)
            
            real_events = summary[summary["Speed_Drop_kmh"] > 15].copy().reset_index(drop=True)
            real_events.insert(0, "Zone", [f"Turn Zone {i+1}" for i in range(len(real_events))])
            
            col_t, col_c = st.columns([0.55, 0.45])
            
            with col_t:
                st.markdown("##### Detected Braking Zones")
                st.dataframe(
                    real_events[[
                        "Zone", "Start_Distance", "Start_Speed", "End_Speed",
                        "Speed_Drop_kmh", "Braking_Distance_m", "Duration_s", "Decel_G"
                    ]].rename(columns={
                        "Start_Distance": "Distance (m)",
                        "Start_Speed": "Entry (km/h)",
                        "End_Speed": "Apex (km/h)",
                        "Speed_Drop_kmh": "Speed Lost (km/h)",
                        "Braking_Distance_m": "Braking Dist (m)",
                        "Duration_s": "Time (s)",
                        "Decel_G": "Decel (G)"
                    }),
                    width="stretch",
                    hide_index=True
                )
                
            with col_c:
                st.markdown("##### Peak Braking Deceleration by Zone")
                fig_bar = go.Figure()
                fig_bar.add_trace(
                    go.Bar(
                        x=real_events["Zone"],
                        y=real_events["Decel_G"],
                        marker=dict(color="#FF1744"),
                        text=[f"{g:.1f}G" for g in real_events["Decel_G"]],
                        textposition="auto",
                        textfont=dict(color="#FFFFFF", size=12, family="JetBrains Mono")
                    )
                )
                fig_bar.update_layout(
                    height=350,
                    margin=dict(l=30, r=20, t=20, b=30)
                )
                fig_bar.update_xaxes(title_text="Zone", title_font=dict(color="#FFFFFF"), tickfont=dict(color="#CBD5E1"))
                fig_bar.update_yaxes(title_text="Deceleration (G)", title_font=dict(color="#FFFFFF"), tickfont=dict(color="#CBD5E1"))
                fig_bar = style_plotly_fig(fig_bar)
                st.plotly_chart(fig_bar, width="stretch")
                
            st.write("")
            st.markdown("---")
            
            st.markdown("#### Traction Circle (G-G Diagram)")
            st.caption("Visualizes how close the driver operates to the tire grip limit combining lateral cornering Gs and longitudinal braking/acceleration Gs.")
            
            if "AccelerationX" in tel1.columns and "AccelerationY" in tel1.columns:
                g_long = tel1["AccelerationX"] / 9.80665
                g_lat = tel1["AccelerationY"] / 9.80665
                
                fig_gg = go.Figure()
                
                theta = np.linspace(0, 2 * np.pi, 200)
                for r in [1, 2, 3, 4, 5]:
                    fig_gg.add_trace(
                        go.Scatter(
                            x=r * np.cos(theta),
                            y=r * np.sin(theta),
                            mode="lines",
                            line=dict(color="#28354E", width=1, dash="dot"),
                            hoverinfo="none",
                            showlegend=False
                        )
                    )
                    fig_gg.add_annotation(
                        x=0, y=r, text=f"{r}G", showarrow=False,
                        font=dict(color="#CBD5E1", size=11, family="JetBrains Mono")
                    )
                    
                fig_gg.add_trace(
                    go.Scatter(
                        x=g_lat,
                        y=g_long,
                        mode="markers",
                        name=driver_1_code,
                        marker=dict(
                            size=4,
                            color=tel1["Speed"],
                            colorscale="Turbo",
                            colorbar=dict(
                                title=dict(text="Speed (km/h)", font=dict(color="#FFFFFF", family="Titillium Web")),
                                tickfont=dict(color="#CBD5E1", family="JetBrains Mono"),
                                x=1.02, thickness=14, len=0.7
                            ),
                            showscale=True
                        ),
                        text=[f"{s:.0f} km/h | Lat: {lat:.1f}G, Long: {lng:.1f}G" for s, lat, lng in zip(tel1["Speed"], g_lat, g_long)],
                        hoverinfo="text"
                    )
                )
                
                fig_gg.update_layout(
                    width=650,
                    height=600,
                    margin=dict(l=30, r=30, t=30, b=30)
                )
                fig_gg.update_xaxes(
                    title_text="Lateral G (Cornering: Left/Right)",
                    range=[-5.5, 5.5],
                    title_font=dict(color="#FFFFFF"),
                    tickfont=dict(color="#CBD5E1")
                )
                fig_gg.update_yaxes(
                    title_text="Longitudinal G (Braking / Acceleration)",
                    range=[-5.5, 5.5],
                    scaleanchor="x",
                    scaleratio=1,
                    title_font=dict(color="#FFFFFF"),
                    tickfont=dict(color="#CBD5E1")
                )
                fig_gg = style_plotly_fig(fig_gg)
                
                st.plotly_chart(fig_gg, width="content")
            else:
                st.info("Direct accelerometer channels are not present in this session.")

    # TAB 5: TELEMETRY DATA & EXPORT
    with tab_data:
        st.markdown("### Raw Telemetry Inspector & Data Export")
        st.caption("Inspect and download full session telemetry or computed braking dynamics reports.")
        
        st.dataframe(tel1.head(100), width="stretch")
        
        st.write("")
        e_col1, e_col2 = st.columns(2)
        
        csv_tel = tel1.to_csv(index=False).encode("utf-8")
        e_col1.download_button(
            label=f"📥 Download {driver_1_code} Full Telemetry (CSV)",
            data=csv_tel,
            file_name=f"{year}_{event_name}_{session_name}_{driver_1_code}_telemetry.csv",
            mime="text/csv"
        )
        
        if not braking_only.empty:
            csv_brake = real_events.to_csv(index=False).encode("utf-8")
            e_col2.download_button(
                label="📥 Download Braking Dynamics Report (CSV)",
                data=csv_brake,
                file_name=f"{year}_{event_name}_{session_name}_{driver_1_code}_braking_report.csv",
                mime="text/csv"
            )

        if tel2 is not None and meta2 is not None:
            st.write("")
            st.markdown("##### 📸 Visual Reports")
            card_dl_buffer = generate_f1_debrief_card(
                year, event_name, session_name,
                driver_1_code, meta1, tel1, color1,
                driver_2_code, meta2, tel2, color2,
                dist_grid, delta_time
            )
            st.download_button(
                label=f"📥 Download {driver_1_code} vs {driver_2_code} Debrief Card (PNG)",
                data=card_dl_buffer.getvalue(),
                file_name=f"{year}_{event_name.replace(' ', '_')}_{session_name}_{driver_1_code}_vs_{driver_2_code}_debrief.png",
                mime="image/png"
            )
