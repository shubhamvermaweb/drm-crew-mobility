import streamlit as st
import plotly.express as px
import pandas as pd

from modules.sheets import (
    get_tabs,
    get_sheet_data
)

from modules.dashboard_parser import (
    extract_dataframe
)

from modules.ui import (
    kpi_card
)


def show_analytics():

    st.markdown("""<div class="topbar">
<h2 style="margin-bottom:4px;color:white;">📊 Analytics Center</h2>
<div style="font-size:13px;opacity:0.9;">DRM Performance Analytics Dashboard</div>
</div>""", unsafe_allow_html=True)

    # ==================================
    # DATE SELECTION
    # ==================================

    tab = st.selectbox(
        "📅 Select Control Sheet",
        get_tabs()
    )

    raw = get_sheet_data(tab)

    df = extract_dataframe(raw)

    # ==================================
    # KPI COUNTS
    # ==================================

    total_loads = len(df)

    high_priority = 0

    on_run = 0

    if "Priority to improve mobility" in df.columns:

        high_priority = len(
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

    # ==================================
    # KPI CARDS
    # ==================================

    c1, c2, c3 = st.columns(3)

    with c1:

        kpi_card(
            "Total Loads",
            total_loads,
            "🚂",
            "#082567"
        )

    with c2:

        kpi_card(
            "High Priority",
            high_priority,
            "⭐",
            "#FB8C00"
        )

    with c3:

        kpi_card(
            "On Run",
            on_run,
            "✅",
            "#2E7D32"
        )

    st.divider()

    # ==================================
    # CHARTS
    # ==================================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "📊 Load Status Distribution"
        )

        if "Status of load" in df.columns:

            status_df = (
                df["Status of load"]
                .value_counts()
                .reset_index()
            )

            status_df.columns = [
                "Status",
                "Count"
            ]

            fig = px.pie(
                status_df,
                names="Status",
                values="Count",
                hole=0.65,
                color_discrete_sequence=px.colors.sequential.Blues
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    with right:

        st.subheader(
            "📈 Lobby Performance"
        )

        lobby_cols = [
            c
            for c in df.columns
            if "Lobby" in c
        ]

        if lobby_cols:

            lobby_col = lobby_cols[0]

            lobby_df = (
                df[lobby_col]
                .value_counts()
                .reset_index()
            )

            lobby_df.columns = [
                "Lobby",
                "Count"
            ]

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

    # ==================================
    # HIGH PRIORITY LOADS
    # ==================================

    st.subheader(
        "⭐ High Priority Analysis"
    )

    if (
        "Priority to improve mobility"
        in df.columns
    ):

        high_df = df[
            df[
                "Priority to improve mobility"
            ]
            .astype(str)
            .str.contains(
                "HIGH",
                case=False,
                na=False
            )
        ]

        st.dataframe(
            high_df,
            width="stretch",
            height=300
        )

    st.divider()

    # ==================================
    # DESTINATION ANALYSIS
    # ==================================

    destination_cols = [
        c
        for c in df.columns
        if "Destination" in c
    ]

    if destination_cols:

        st.subheader(
            "🚂 Destination Analysis"
        )

        destination_df = (
            df[destination_cols[0]]
            .value_counts()
            .head(10)
            .reset_index()
        )

        destination_df.columns = [
            "Destination",
            "Count"
        ]

        fig3 = px.bar(
            destination_df,
            x="Destination",
            y="Count",
            color="Count",
            color_continuous_scale="Blues"
        )

        st.plotly_chart(
            fig3,
            width="stretch"
        )

    st.divider()

    # ==================================
    # STATUS SUMMARY
    # ==================================

    st.subheader(
        "📋 Status Summary"
    )

    if "Status of load" in df.columns:

        summary = (
            df["Status of load"]
            .value_counts()
            .reset_index()
        )

        summary.columns = [
            "Status",
            "Count"
        ]

        st.dataframe(
            summary,
            width="stretch"
        )

    st.divider()

    # ==================================
    # ALERT INDICATORS
    # ==================================

    st.subheader(
        "🚨 Analytics Alerts"
    )

    if high_priority > 5:

        st.error(
            f"{high_priority} High Priority Loads Pending"
        )

    if on_run < 10:

        st.warning(
            "Low Running Load Count"
        )

    if total_loads > 0:

        st.success(
            f"{total_loads} Total Loads Processed"
        )