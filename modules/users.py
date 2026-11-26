import gspread
import streamlit as st
from modules.sheets import get_sheet


def _get_or_create_users_ws():
    sheet = get_sheet()
    try:
        ws = sheet.worksheet("Users")
    except gspread.WorksheetNotFound:
        ws = sheet.add_worksheet(title="Users", rows=100, cols=10)
        ws.append_row(["username", "password", "role", "status"])
        ws.append_row(["admin", "admin123", "admin", "Active"])
        ws.append_row(["user", "user123", "user", "Active"])
    return ws


def _normalize_records(ws):
    """
    Safely reads all rows as string-normalized dictionaries even if usernames
    or passwords are pure numbers in Google Sheets.
    """
    rows = ws.get_all_values()
    if not rows:
        return []

    headers = [h.strip().lower() for h in rows[0]]
    records = []

    for row_idx, row in enumerate(rows[1:], start=2):
        padded = row + [""] * (len(headers) - len(row))
        item = {headers[i]: str(padded[i]).strip() for i in range(len(headers))}
        item["_row_idx"] = row_idx
        records.append(item)

    return records


# ==========================================
# GET USERS
# ==========================================

def get_users():
    ws = _get_or_create_users_ws()
    return _normalize_records(ws)


# ==========================================
# CREATE USER
# ==========================================

def create_user(username, password, role):
    ws = _get_or_create_users_ws()
    users = _normalize_records(ws)

    clean_user = str(username).strip()
    clean_pass = str(password).strip()
    clean_role = str(role).strip().lower()

    if not clean_user or not clean_pass:
        return False

    for user in users:
        if user.get("username", "").lower() == clean_user.lower():
            return False

    ws.append_row(
        [clean_user, clean_pass, clean_role, "Active"],
        value_input_option="RAW"
    )
    st.cache_data.clear()
    return True


# ==========================================
# DELETE USER
# ==========================================

def delete_user(username):
    clean_user = str(username).strip()
    if clean_user.lower() == "drm":
        return False

    ws = _get_or_create_users_ws()
    records = _normalize_records(ws)

    for row in records:
        if row.get("username", "").lower() == clean_user.lower():
            ws.delete_rows(row["_row_idx"])
            st.cache_data.clear()
            return True

    return False


# ==========================================
# UPDATE STATUS
# ==========================================

def update_status(username, status):
    clean_user = str(username).strip()
    clean_status = str(status).strip()

    ws = _get_or_create_users_ws()
    headers = [h.strip().lower() for h in ws.row_values(1)]
    status_col = headers.index("status") + 1 if "status" in headers else 4

    records = _normalize_records(ws)

    for row in records:
        if row.get("username", "").lower() == clean_user.lower():
            ws.update_cell(row["_row_idx"], status_col, clean_status)
            st.cache_data.clear()
            return True

    return False


# ==========================================
# RESET PASSWORD
# ==========================================

def reset_password(username, new_password):
    clean_user = str(username).strip()
    clean_pass = str(new_password).strip()

    if not clean_pass:
        return False

    ws = _get_or_create_users_ws()
    headers = [h.strip().lower() for h in ws.row_values(1)]
    pass_col = headers.index("password") + 1 if "password" in headers else 2

    records = _normalize_records(ws)

    for row in records:
        if row.get("username", "").lower() == clean_user.lower():
            ws.update_cell(row["_row_idx"], pass_col, clean_pass)
            st.cache_data.clear()
            return True

    return False