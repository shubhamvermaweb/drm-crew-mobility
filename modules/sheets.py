import os

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1D_4S15j3nxHyrjdPeeTqVglVRGSvJxtZYdTY3xaTNj4"


@st.cache_resource(ttl=3600)
def get_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    if "gcp_service_account" in st.secrets:
        creds_dict = dict(st.secrets["gcp_service_account"])
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=scope,
        )
    elif os.path.exists("service_account.json"):
        creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=scope,
        )
    else:
        st.error("Google Service Account credentials missing. Configure [gcp_service_account] in Streamlit Secrets.")
        st.stop()

    return gspread.authorize(creds)


def get_sheet():
    client = get_client()
    return client.open_by_key(SPREADSHEET_ID)


@st.cache_data(ttl=60)
def get_tabs():
    sheet = get_sheet()
    return [
        ws.title
        for ws in sheet.worksheets()
        if ws.title.strip().lower() != "users"
    ]


@st.cache_data(ttl=60)
def get_sheet_data(tab):
    ws = get_sheet().worksheet(tab)
    return ws.get_all_values()


@st.cache_data(ttl=60)
def get_df(tab):
    data = get_sheet_data(tab)

    if len(data) < 5:
        return pd.DataFrame(data)

    headers = data[3]

    # Handle Duplicate Headers
    new_headers = []
    counter = {}

    for h in headers:
        h = str(h).strip()

        if h == "":
            h = "Column"

        if h in counter:
            counter[h] += 1
            h = f"{h}_{counter[h]}"
        else:
            counter[h] = 0

        new_headers.append(h)

    rows = data[4:]

    df = pd.DataFrame(
        rows,
        columns=new_headers,
    )

    return df.fillna("")