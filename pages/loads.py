import streamlit as st
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


def show_loads():

    # ==================================
    # HEADER
    # ==================================

    st.markdown("""<div class="topbar">
<h2 style="margin-bottom:4px;color:white;">🚂 Load Monitoring Center</h2>
<div style="font-size:13px;opacity:0.9;">Real-Time Load Tracking &amp; Monitoring</div>
</div>""", unsafe_allow_html=True)

    # ==================================
    # DATE SELECTION
    # ==================================

    selected_tab = st.selectbox(
        "📅 Select Control Sheet",
        get_tabs()
    )

    raw = get_sheet_data(selected_tab)

    df = extract_dataframe(raw)

    # ==================================
    # FILTERS
    # ==================================

    st.subheader("🔍 Search & Filters")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        search = st.text_input(
            "Search Load / Destination"
        )

    with col2:

        priority = st.selectbox(
            "Priority",
            [
                "ALL",
                "HIGH"
            ]
        )

    with col3:

        status = st.text_input(
            "Load Status"
        )

    with col4:

        lobby = st.text_input(
            "Lobby"
        )

    filtered = df.copy()

    # ==================================
    # GLOBAL SEARCH
    # ==================================

    if search:

        filtered = filtered[
            filtered.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    # ==================================
    # PRIORITY FILTER
    # ==================================

    if (
        priority == "HIGH"
        and
        "Priority to improve mobility"
        in filtered.columns
    ):

        filtered = filtered[
            filtered[
                "Priority to improve mobility"
            ]
            .astype(str)
            .str.contains(
                "HIGH",
                case=False,
                na=False
            )
        ]

    # ==================================
    # STATUS FILTER
    # ==================================

    if (
        status
        and
        "Status of load"
        in filtered.columns
    ):

        filtered = filtered[
            filtered[
                "Status of load"
            ]
            .astype(str)
            .str.contains(
                status,
                case=False,
                na=False
            )
        ]

    # ==================================
    # LOBBY FILTER
    # ==================================

    if lobby:

        lobby_cols = [
            col
            for col in filtered.columns
            if "Lobby" in col
        ]

        if lobby_cols:

            mask = False

            for col in lobby_cols:

                current_mask = (
                    filtered[col]
                    .astype(str)
                    .str.contains(
                        lobby,
                        case=False,
                        na=False
                    )
                )

                mask = (
                    current_mask
                    if isinstance(mask, bool)
                    else mask | current_mask
                )

            filtered = filtered[mask]

    # ==================================
    # KPI SECTION
    # ==================================

    total_loads = len(filtered)

    high_priority = 0

    on_run = 0

    if (
        "Priority to improve mobility"
        in filtered.columns
    ):

        high_priority = len(
            filtered[
                filtered[
                    "Priority to improve mobility"
                ]
                .astype(str)
                .str.contains(
                    "HIGH",
                    case=False,
                    na=False
                )
            ]
        )

    if (
        "Status of load"
        in filtered.columns
    ):

        on_run = len(
            filtered[
                filtered[
                    "Status of load"
                ]
                .astype(str)
                .str.contains(
                    "ON RUN",
                    case=False,
                    na=False
                )
            ]
        )

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
            "#EF6C00"
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
    # ALERTS
    # ==================================

    st.subheader(
        "🚨 Operational Status"
    )

    if high_priority > 0:

        st.warning(
            f"{high_priority} High Priority Loads Found"
        )

    if len(filtered) == 0:

        st.error(
            "No Matching Loads Found"
        )

    else:

        st.success(
            f"{len(filtered)} Loads Available"
        )

    st.divider()

    # ==================================
    # HIGH PRIORITY TABLE
    # ==================================

    if (
        "Priority to improve mobility"
        in filtered.columns
    ):

        high_df = filtered[
            filtered[
                "Priority to improve mobility"
            ]
            .astype(str)
            .str.contains(
                "HIGH",
                case=False,
                na=False
            )
        ]

        if len(high_df):

            st.subheader(
                "⭐ High Priority Loads"
            )

            st.dataframe(
                high_df,
                width="stretch",
                height=250
            )

            st.divider()

    # ==================================
    # EXPORT
    # ==================================

    csv = (
        filtered
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "📥 Export Filtered Data",
        csv,
        file_name=f"{selected_tab}_loads.csv",
        mime="text/csv"
    )

    st.divider()

    # ==================================
    # LOAD REGISTER
    # ==================================

    st.subheader(
        "📋 Live Load Register"
    )

    st.dataframe(
        filtered,
        width="stretch",
        height=700
    )