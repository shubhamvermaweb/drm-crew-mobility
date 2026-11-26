import streamlit as st
import pandas as pd
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
    warning_card,
    success_card
)

from modules.alerts import (
    generate_alerts
)


def show_alerts():

    # =================================
    # HEADER
    # =================================

    st.markdown("""<div class="topbar">
<h2 style="margin-bottom:4px;color:white;">🚨 Alert Control Center</h2>
<div style="font-size:13px;opacity:0.9;">High Priority Loads • Crew Alerts • Duty Monitoring</div>
</div>""", unsafe_allow_html=True)

    # =================================
    # DATE SELECTION
    # =================================

    tab = st.selectbox(
        "📅 Select Date Sheet",
        get_tabs()
    )

    raw = get_sheet_data(tab)

    df = extract_dataframe(raw)

    alerts = generate_alerts(df)

    # =================================
    # DATA PREPARATION
    # =================================

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

    else:

        high_df = pd.DataFrame()

    if "Status of load" in df.columns:

        attention_df = df[
            ~df["Status of load"]
            .astype(str)
            .str.contains(
                "ON RUN|MADE OVER",
                case=False,
                na=False
            )
        ]

    else:

        attention_df = pd.DataFrame()

    # =================================
    # KPI CARDS
    # =================================

    critical_count = len(
        [
            x for x in alerts
            if x["type"] == "critical"
        ]
    )

    warning_count = len(
        [
            x for x in alerts
            if x["type"] == "warning"
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        kpi_card(
            "Critical",
            critical_count,
            "🚨",
            "#D32F2F"
        )

    with c2:

        kpi_card(
            "Warnings",
            warning_count,
            "⚠️",
            "#FB8C00"
        )

    with c3:

        kpi_card(
            "High Priority",
            len(high_df),
            "⭐",
            "#FF9800"
        )

    with c4:

        kpi_card(
            "Total Loads",
            len(df),
            "🚂",
            "#082567"
        )

    st.divider()

    # =================================
    # ALERT SUMMARY
    # =================================

    st.subheader("🚨 Active Alerts")

    for item in alerts:

        if item["type"] == "critical":

            alert_card(
                item["message"]
            )

        elif item["type"] == "warning":

            warning_card(
                item["message"]
            )

        elif item["type"] == "success":

            success_card(
                item["message"]
            )

        elif item["type"] == "high":

            st.info(
                f"⭐ {item['message']}"
            )

    st.divider()

    # =================================
    # CHARTS
    # =================================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "📊 Alert Distribution"
        )

        chart_df = pd.DataFrame({

            "Type": [
                "Critical",
                "Warning",
                "High Priority"
            ],

            "Count": [
                critical_count,
                warning_count,
                len(high_df)
            ]
        })

        fig = px.pie(
            chart_df,
            names="Type",
            values="Count",
            hole=0.6,
            color="Type",
            color_discrete_map={
                "Critical": "#D32F2F",
                "Warning": "#FF9800",
                "High Priority": "#FFD600"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with right:

        st.subheader(
            "📈 Load Status"
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

            fig2 = px.bar(
                status_df,
                x="Status",
                y="Count",
                color="Count",
                color_continuous_scale="Reds"
            )

            st.plotly_chart(
                fig2,
                width="stretch"
            )

    st.divider()

    # =================================
    # HIGH PRIORITY TABLE
    # =================================

    st.subheader(
        "⭐ High Priority Loads"
    )

    if len(high_df):

        st.dataframe(
            high_df,
            width="stretch",
            height=300
        )

    else:

        st.success(
            "No High Priority Loads"
        )

    st.divider()

    # =================================
    # LOADS NEEDING ATTENTION
    # =================================

    st.subheader(
        "🚨 Loads Requiring Attention"
    )

    if len(attention_df):

        st.dataframe(
            attention_df,
            width="stretch",
            height=350
        )

    else:

        st.success(
            "No Load Requires Attention"
        )

    st.divider()

    # =================================
    # DUTY HOURS
    # =================================

    st.subheader(
        "⏰ Duty Hours Tracker"
    )

    duty_cols = [
        c
        for c in df.columns
        if "Duty" in c
    ]

    if duty_cols:

        display_cols = []

        if "Load stabled" in df.columns:

            display_cols.append(
                "Load stabled"
            )

        display_cols.extend(
            duty_cols
        )

        duty_df = df[
            display_cols
        ]

        st.dataframe(
            duty_df,
            width="stretch",
            height=300
        )

        try:

            duty_col = duty_cols[0]

            over_limit = (
                duty_df[duty_col]
                .astype(str)
                .str.extract(r"(\d+)")[0]
                .fillna(0)
                .astype(int)
            )

            over_limit = over_limit[
                over_limit > 10
            ]

            if len(over_limit):

                st.error(
                    f"🚨 {len(over_limit)} Crew Above 10 Duty Hours"
                )

        except Exception:

            pass

    st.divider()

    # =================================
    # STATUS TABLE
    # =================================

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

    # =================================
    # RAW DATA
    # =================================

    with st.expander(
        "📄 View Complete Dataset"
    ):

        st.dataframe(
            df,
            width="stretch",
            height=600
        )