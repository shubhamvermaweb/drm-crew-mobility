import streamlit as st

from modules.auth import login_page
from modules.styles import load_styles
from pages.alerts import show_alerts
from pages.analytics import show_analytics
from pages.crew import show_crew
from pages.home import show_home
from pages.loads import show_loads
from pages.users import show_users

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Crew Arrangement & Mobility",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================
# LOAD THEME
# ==================================

load_styles()

# ==================================
# SESSION STATE
# ==================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "home"

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# ==================================
# LOGIN
# ==================================

if not st.session_state.logged_in:
    login_page()
    st.stop()

# ==================================
# FIXED TOP & BOTTOM BAR CSS (DESKTOP + MOBILE)
# ==================================

st.markdown("""<style>
header[data-testid="stHeader"] {
    display: none !important;
}
.block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 98px !important;
    padding-bottom: 96px !important;
}

/* 1. FIXED TOP HEADER BAR (ALWAYS SINGLE ROW) */
div[data-testid="stHorizontalBlock"]:has(.top-title-box) {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100vw !important;
    height: 76px !important;
    min-height: 76px !important;
    max-height: 76px !important;
    background: linear-gradient(90deg, #061b4e 0%, #082567 100%) !important;
    color: white !important;
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 8px 20px !important;
    margin: 0 !important;
    gap: 8px !important;
    z-index: 99999 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.22) !important;
}

/* Prevent Streamlit column wrappers from stacking vertically on mobile */
div[data-testid="stHorizontalBlock"]:has(.top-title-box) > div[data-testid="stColumn"] {
    width: auto !important;
    min-width: 0 !important;
    flex-shrink: 1 !important;
}
div[data-testid="stHorizontalBlock"]:has(.top-title-box) > div[data-testid="stColumn"]:first-child {
    flex: 1 1 auto !important;
    overflow: hidden !important;
}
div[data-testid="stHorizontalBlock"]:has(.top-title-box) > div[data-testid="stColumn"]:nth-child(2),
div[data-testid="stHorizontalBlock"]:has(.top-title-box) > div[data-testid="stColumn"]:nth-child(3) {
    flex: 0 0 auto !important;
}

.top-title-box {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    background: transparent !important;
    overflow: hidden !important;
}
.top-title-box h2 {
    margin: 0 0 2px 0 !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    line-height: 1.2 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
.top-title-box span {
    display: block !important;
    font-size: 14px !important;
    color: rgba(255, 255, 255, 0.88) !important;
    line-height: 1.2 !important;
    background: transparent !important;
    white-space: nowrap !important;
}

.top-user-wrap {
    display: flex !important;
    justify-content: flex-end !important;
    align-items: center !important;
    background: transparent !important;
}
.user-badge {
    background: rgba(255, 255, 255, 0.16) !important;
    padding: 6px 14px !important;
    border-radius: 18px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #ffffff !important;
    white-space: nowrap !important;
}

/* Red Logout Button Inside Top Header Bar */
div[data-testid="stHorizontalBlock"]:has(.top-title-box) button {
    background: #E53935 !important;
    color: #ffffff !important;
    border-radius: 18px !important;
    height: 38px !important;
    min-height: 38px !important;
    padding: 0 14px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
    margin: 0 !important;
    white-space: nowrap !important;
}
div[data-testid="stHorizontalBlock"]:has(.top-title-box) button:hover {
    background: #C62828 !important;
    color: #ffffff !important;
}

/* 2. FIXED BOTTOM NAVIGATION BAR (ALWAYS SINGLE ROW) */
div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100vw !important;
    background: #ffffff !important;
    border-top: 1px solid #cbd5e1 !important;
    padding: 8px 14px !important;
    margin: 0 !important;
    z-index: 99999 !important;
    box-shadow: 0 -4px 14px rgba(0, 0, 0, 0.12) !important;
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 8px !important;
}

div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) > div[data-testid="stColumn"] {
    flex: 1 1 0 !important;
    width: auto !important;
    min-width: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) button {
    width: 100% !important;
    height: 48px !important;
    min-height: 48px !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    padding: 0 6px !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) button p {
    font-size: 16px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    margin: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) button:hover {
    background: #e2e8f0 !important;
    color: #082567 !important;
}

div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) button[kind="primary"] {
    background: #082567 !important;
    color: #ffffff !important;
    border-color: #082567 !important;
    box-shadow: 0 3px 10px rgba(8, 37, 103, 0.28) !important;
}

/* MOBILE COMPACT ADJUSTMENTS (<= 768px) */
@media (max-width: 768px) {
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-top: 74px !important;
        padding-bottom: 84px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.top-title-box) {
        height: 60px !important;
        min-height: 60px !important;
        max-height: 60px !important;
        padding: 6px 10px !important;
        gap: 6px !important;
    }
    .top-title-box h2 {
        font-size: 14px !important;
        margin: 0 0 1px 0 !important;
    }
    .top-title-box span {
        font-size: 11px !important;
    }
    .user-badge {
        padding: 4px 8px !important;
        font-size: 12px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.top-title-box) button {
        height: 32px !important;
        min-height: 32px !important;
        padding: 0 10px !important;
        font-size: 12px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.top-title-box) button p {
        font-size: 12px !important;
    }
    div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) {
        padding: 6px 4px !important;
        gap: 4px !important;
    }
    div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) button {
        height: 46px !important;
        min-height: 46px !important;
        padding: 0 2px !important;
        border-radius: 10px !important;
    }
    div[data-testid="stHorizontalBlock"]:has([class*="st-key-nav_"]) button p {
        font-size: 11px !important;
        line-height: 1.15 !important;
        white-space: normal !important;
    }
}
</style>""", unsafe_allow_html=True)

# ==================================
# FIXED TOP HEADER (TITLE | USER | LOGOUT)
# ==================================

t_col1, t_col2, t_col3 = st.columns([7.8, 1.1, 1.1])

with t_col1:
    st.markdown("""<div class="top-title-box">
<h2>🚆 Crew Arrangement &amp; Mobility</h2>
<span>DRM Control Dashboard</span>
</div>""", unsafe_allow_html=True)

with t_col2:
    st.markdown(f"""<div class="top-user-wrap">
<span class="user-badge">👤 {st.session_state.username}</span>
</div>""", unsafe_allow_html=True)

with t_col3:
    if st.button("🚪 Logout", key="top_logout_btn", width="stretch"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.page = "home"
        st.rerun()

# ==================================
# PAGE ROUTING
# ==================================

page = st.session_state.page

if page == "home":
    show_home()
elif page == "loads":
    show_loads()
elif page == "crew":
    show_crew()
elif page == "analytics":
    show_analytics()
elif page == "alerts":
    show_alerts()
elif page == "users":
    show_users()

# ==================================
# BOTTOM SPACER + FIXED NAVIGATION
# ==================================

st.markdown('<div style="height: 24px; background: transparent;"></div>', unsafe_allow_html=True)

nav_items = [
    ("home", "🏠 Home"),
    ("loads", "🚂 Loads"),
    ("crew", "👨‍✈️ Crew"),
    ("analytics", "📊 Analytics"),
    ("alerts", "🚨 Alerts"),
]

if st.session_state.role == "admin":
    nav_items.append(("users", "⚙️ Users"))

cols = st.columns(len(nav_items))
for col, (key, label) in zip(cols, nav_items):
    with col:
        btn_type = "primary" if page == key else "secondary"
        if st.button(label, key=f"nav_{key}", type=btn_type, width="stretch"):
            st.session_state.page = key
            st.rerun()