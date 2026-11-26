import streamlit as st


def load_styles():

    st.markdown("""<style>

/* Hide Streamlit UI */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="stSidebarNav"] {
    display: none;
}

/* App Background (Only on main container, never on inner div/span!) */

html,
body,
[data-testid="stAppViewContainer"] {
    background-color: #F3F7FC !important;
}

/* Global Larger Text Scaling Everywhere */

html,
body,
[data-testid="stAppViewContainer"],
.stMarkdown,
p,
span,
div,
label,
input,
select,
textarea {
    font-size: 18px !important;
}

h1 { font-size: 38px !important; }
h2 { font-size: 30px !important; }
h3 { font-size: 25px !important; }
h4 { font-size: 22px !important; }

/* Selectboxes & Inputs */
[data-baseweb="select"] * {
    font-size: 18px !important;
}

[data-testid="stWidgetLabel"] p {
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* Metrics */
[data-testid="stMetricLabel"] p {
    font-size: 18px !important;
}

[data-testid="stMetricValue"] {
    font-size: 38px !important;
}

/* Dataframes & Tables */
[data-testid="stDataFrame"] * {
    font-size: 17px !important;
}

/* Main Container */

.block-container {
    max-width: 100% !important;
    padding-top: 108px !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    padding-bottom: 135px !important;
}

/* Top Header Banner */

.topbar {
    background: linear-gradient(135deg, #082567, #0A2A66) !important;
    color: white !important;
    padding: 22px;
    border-radius: 20px;
    margin-bottom: 22px;
    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.15);
}

.topbar h2 {
    font-size: 30px !important;
    color: white !important;
    background: transparent !important;
}

.topbar small,
.topbar div {
    font-size: 17px !important;
    color: rgba(255, 255, 255, 0.92) !important;
    background: transparent !important;
}

/* KPI Cards */

.kpi-card {
    background: white;
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

/* Alerts */

.alert-red {
    background: #FFE5E5;
    padding: 16px;
    border-left: 6px solid #E53935;
    border-radius: 15px;
    font-size: 18px !important;
}

.alert-yellow {
    background: #FFF5CC;
    padding: 16px;
    border-left: 6px solid #FB8C00;
    border-radius: 15px;
    font-size: 18px !important;
}

.alert-green {
    background: #E8F5E9;
    padding: 16px;
    border-left: 6px solid #43A047;
    border-radius: 15px;
    font-size: 18px !important;
}

/* Metrics Box */

[data-testid="metric-container"] {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

/* Dataframes */

.stDataFrame {
    border-radius: 15px;
    overflow: hidden;
}

/* Buttons */

.stButton > button {
    width: 100%;
    height: 56px;
    border-radius: 16px;
    border: none;
    background: #082567;
    color: white !important;
    font-size: 18px !important;
    font-weight: 600;
}

.stButton > button p,
.stButton > button span {
    background: transparent !important;
    color: inherit !important;
}

.stButton > button:hover {
    background: #123B8A;
    color: white !important;
}

/* Mobile */

@media only screen and (max-width: 768px) {
    html,
    body,
    [data-testid="stAppViewContainer"],
    .stMarkdown,
    p,
    label,
    input,
    select,
    textarea {
        font-size: 16px !important;
    }

    h1 { font-size: 30px !important; }
    h2 { font-size: 24px !important; }
    h3 { font-size: 21px !important; }

    .block-container {
        padding-top: 96px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        padding-bottom: 120px !important;
    }

    .topbar {
        padding: 16px;
        border-radius: 15px;
    }
}

</style>""", unsafe_allow_html=True)