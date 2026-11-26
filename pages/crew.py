import streamlit as st
import plotly.express as px

from modules.sheets import (
    get_tabs,
    get_sheet_data
)

from modules.dashboard_parser import (
    extract_dataframe
)

from modules.ui import (
    kpi_card,
    alert_card,
    success_card
)


def show_crew():

    st.markdown("""<div class="topbar">
<h2 style="margin-bottom:4px;color:white;">👨‍✈️ Crew Management Dashboard</h2>
<div style="font-size:13px;opacity:0.9;">Crew Monitoring &amp; Utilization</div>
</div>""", unsafe_allow_html=True)

    # =========================
    # DATE SELECTION
    # =========================

    tab = st.selectbox(
        "📅 Control Sheet",
        get_tabs()
    )

    raw = get_sheet_data(tab)

    df = extract_dataframe(raw)

    # =========================
    # COLUMN DETECTION
    # =========================

    alp_cols = [
        c for c in df.columns
        if "ALP" in c.upper()
    ]

    lpg_cols = [
        c for c in df.columns
        if "LPG" in c.upper()
    ]

    tm_cols = [
        c for c in df.columns
        if "TM" in c.upper()
    ]

    def is_assigned(series):
        return series.notna() & ~series.astype(str).str.strip().isin(["", "nan", "None", "NaT"])

    # =========================
    # COUNTS
    # =========================

    alp_count = 0
    lpg_count = 0
    tm_count = 0

    if alp_cols:
        alp_count = int(is_assigned(df[alp_cols[0]]).sum())

    if lpg_cols:
        lpg_count = int(is_assigned(df[lpg_cols[0]]).sum())

    if tm_cols:
        tm_count = int(is_assigned(df[tm_cols[0]]).sum())

    total_crew = (
        alp_count +
        lpg_count +
        tm_count
    )

    # =========================
    # KPI CARDS
    # =========================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        kpi_card(
            "Total Crew",
            total_crew,
            "👨‍✈️",
            "#082567"
        )

    with c2:

        kpi_card(
            "ALP",
            alp_count,
            "🚆",
            "#1565C0"
        )

    with c3:

        kpi_card(
            "LPG",
            lpg_count,
            "🚂",
            "#2E7D32"
        )

    with c4:

        kpi_card(
            "TM",
            tm_count,
            "📋",
            "#EF6C00"
        )

    st.divider()

    # =========================
    # CREW ALERTS
    # =========================

    st.subheader(
        "🚨 Crew Alerts"
    )

    empty_tm = 0

    if tm_cols:
        empty_tm = int((~is_assigned(df[tm_cols[0]])).sum())

    if empty_tm > 0:

        alert_card(
            f"{empty_tm} Loads Without TM"
        )

    else:

        success_card(
            "All Loads Have TM Assigned"
        )

    st.divider()

    # =========================
    # CREW DISTRIBUTION
    # =========================

    st.subheader(
        "📊 Crew Distribution"
    )

    crew_chart = px.pie(
        names=[
            "ALP",
            "LPG",
            "TM"
        ],

        values=[
            alp_count,
            lpg_count,
            tm_count
        ],

        hole=0.65,

        color_discrete_sequence=[
            "#082567",
            "#1565C0",
            "#2E7D32"
        ]
    )

    st.plotly_chart(
        crew_chart,
        width="stretch"
    )

    st.divider()

    # =========================
    # LOBBY ANALYSIS
    # =========================

    lobby_cols = [
        c
        for c in df.columns
        if "Lobby" in c
    ]

    if lobby_cols:

        st.subheader(
            "📈 Lobby Crew Distribution"
        )

        lobby_df = (
            df[lobby_cols[0]]
            .value_counts()
            .reset_index()
        )

        lobby_df.columns = [
            "Lobby",
            "Count"
        ]

        lobby_chart = px.bar(
            lobby_df,
            x="Lobby",
            y="Count",
            color="Count",
            color_continuous_scale="Blues"
        )

        st.plotly_chart(
            lobby_chart,
            width="stretch"
        )

    st.divider()

    # =========================
    # CREW REGISTER
    # =========================

    st.subheader(
        "📋 Crew Register"
    )

    crew_columns = []

    for col in df.columns:

        if (
            "ALP" in col.upper()
            or
            "LPG" in col.upper()
            or
            "TM" in col.upper()
            or
            "Lobby" in col
        ):

            crew_columns.append(col)

    if crew_columns:

        st.dataframe(
            df[crew_columns],
            width="stretch",
            height=600
        )

    else:

        st.warning(
            "Crew related columns not found"
        )