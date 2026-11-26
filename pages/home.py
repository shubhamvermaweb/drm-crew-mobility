import streamlit as st
import plotly.express as px

from modules.sheets import (
    get_tabs,
    get_sheet_data
)

from modules.dashboard_parser import (
    extract_kpis,
    extract_dataframe
)

from modules.ui import (
    kpi_card,
    alert_card,
    success_card
)


def show_home():

    # ===================================
    # HEADER
    # ===================================

    st.markdown("""<div class="topbar">
<h2 style="margin-bottom:4px;color:white;">🚆 DRM CONTROL DASHBOARD</h2>
<div style="font-size:15px;opacity:0.9;">Crew Arrangement &amp; Mobility System</div>
</div>""", unsafe_allow_html=True)

    # ===================================
    # DATE SHEET
    # ===================================

    selected_tab = st.selectbox(
        "📅 Select Control Sheet",
        get_tabs()
    )

    raw = get_sheet_data(selected_tab)

    kpi = extract_kpis(raw)

    df = extract_dataframe(raw)

    # ===================================
    # KPI ROW 1
    # ===================================

    c1, c2, c3 = st.columns(3)

    with c1:
        kpi_card(
            "Crew Required",
            kpi["crew_required"],
            "🚆",
            "#082567"
        )

    with c2:
        kpi_card(
            "ALP / LPG",
            kpi["alp_lpg"],
            "👨‍✈️",
            "#1565C0"
        )

    with c3:
        kpi_card(
            "TM Nominated",
            kpi["tm"],
            "📋",
            "#00897B"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ===================================
    # KPI ROW 2
    # ===================================

    c4, c5, c6 = st.columns(3)

    with c4:
        kpi_card(
            "Made Over",
            kpi["made_over"],
            "✅",
            "#2E7D32"
        )

    with c5:
        kpi_card(
            "On Run",
            kpi["on_run"],
            "🚂",
            "#0D47A1"
        )

    with c6:
        kpi_card(
            "Not Moved",
            kpi["not_moved"],
            "⚠️",
            "#E53935"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ===================================
    # ALERTS
    # ===================================

    left, right = st.columns([6, 4])

    with left:
        st.subheader("🚨 Control Alerts")

        if "Status of load" in df.columns:
            pending = df[
                ~df["Status of load"]
                .astype(str)
                .str.contains(
                    "ON RUN|MADE OVER",
                    case=False,
                    na=False
                )
            ]

            if len(pending) > 0:
                alert_card(
                    f"{len(pending)} Loads Need Immediate Attention"
                )
            else:
                success_card(
                    "No Active Alerts"
                )

    with right:
        st.subheader("⭐ High Priority Loads")

        if "Priority to improve mobility" in df.columns:
            high = df[
                df["Priority to improve mobility"]
                .astype(str)
                .str.contains(
                    "HIGH",
                    case=False,
                    na=False
                )
            ]

            st.metric(
                "High Priority Loads",
                len(high)
            )

    st.divider()

    # ===================================
    # DEADLINE TRACKER
    # ===================================

    st.subheader("⏰ Duty Hours Tracker")

    duty_columns = [
        col
        for col in df.columns
        if "Duty" in col
    ]

    if duty_columns:
        show_cols = []

        if "Load stabled" in df.columns:
            show_cols.append("Load stabled")

        show_cols.extend(duty_columns)

        st.dataframe(
            df[show_cols].head(10),
            width="stretch",
            height=250
        )

    st.divider()

    # ===================================
    # ANALYTICS CHARTS
    # ===================================

    ch1, ch2 = st.columns(2)

    with ch1:
        st.subheader("📊 Status Distribution")

        if "Status of load" in df.columns:
            status = (
                df["Status of load"]
                .value_counts()
                .reset_index()
            )
            status.columns = ["Status", "Count"]

            fig = px.pie(
                status,
                names="Status",
                values="Count",
                hole=0.65,
                color_discrete_sequence=px.colors.sequential.Blues
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    with ch2:
        st.subheader("📈 Lobby Performance")

        lobby_cols = [
            c
            for c in df.columns
            if c.startswith("Lobby")
        ]

        if lobby_cols:
            lobby_col = lobby_cols[0]

            lobby_df = (
                df[lobby_col]
                .value_counts()
                .reset_index()
            )
            lobby_df.columns = ["Lobby", "Count"]

            fig2 = px.bar(
                lobby_df,
                x="Lobby",
                y="Count",
                color="Count",
                color_continuous_scale="Blues"
            )

            st.plotly_chart(
                fig2,
                width="stretch"
            )

    st.divider()

    # ===================================
    # HIGH PRIORITY REGISTER
    # ===================================

    st.subheader("⭐ High Priority Load Register")

    if "Priority to improve mobility" in df.columns:
        high_df = df[
            df["Priority to improve mobility"]
            .astype(str)
            .str.contains(
                "HIGH",
                case=False,
                na=False
            )
        ]

        if len(high_df):
            st.dataframe(
                high_df,
                width="stretch",
                height=300
            )
        else:
            st.success("No High Priority Loads Found")

    st.divider()

    # ===================================
    # RECENT LOAD REGISTER
    # ===================================

    st.subheader("📋 Latest Load Register")

    st.dataframe(
        df.head(20),
        width="stretch",
        height=400
    )

    # ===================================
    # QUICK SUMMARY
    # ===================================

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Loads", len(df))

    with c2:
        if "Priority to improve mobility" in df.columns:
            high_count = len(
                df[
                    df["Priority to improve mobility"]
                    .astype(str)
                    .str.contains(
                        "HIGH",
                        case=False,
                        na=False
                    )
                ]
            )
        else:
            high_count = 0

        st.metric("High Priority", high_count)

    with c3:
        if "Status of load" in df.columns:
            on_run = len(
                df[
                    df["Status of load"]
                    .astype(str)
                    .str.contains(
                        "ON RUN",
                        case=False,
                        na=False
                    )
                ]
            )
        else:
            on_run = 0

        st.metric("Running Loads", on_run)