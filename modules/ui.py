import streamlit as st


def kpi_card(title, value, icon, color="#082567"):

    st.markdown(f"""<div style="background:{color};color:white;border-radius:20px;padding:22px;min-height:146px;box-shadow:0 6px 15px rgba(0,0,0,.15);">
<div style="font-size:38px;margin-bottom:8px;">{icon}</div>
<div style="font-size:18px;opacity:.94;font-weight:500;">{title}</div>
<div style="font-size:42px;font-weight:700;line-height:1.15;margin-top:4px;">{value}</div>
</div>""", unsafe_allow_html=True)


def alert_card(message):

    st.markdown(f"""<div style="background:#FFEBEE;border-left:6px solid #E53935;padding:16px;border-radius:15px;margin-bottom:12px;font-size:18px;font-weight:500;box-shadow:0px 2px 6px rgba(0,0,0,.08);">
🚨 {message}
</div>""", unsafe_allow_html=True)


def warning_card(message):

    st.markdown(f"""<div style="background:#FFF8E1;border-left:6px solid #FB8C00;padding:16px;border-radius:15px;margin-bottom:12px;font-size:18px;font-weight:500;box-shadow:0px 2px 6px rgba(0,0,0,.08);">
⚠️ {message}
</div>""", unsafe_allow_html=True)


def success_card(message):

    st.markdown(f"""<div style="background:#E8F5E9;border-left:6px solid #43A047;padding:16px;border-radius:15px;margin-bottom:12px;font-size:18px;font-weight:500;box-shadow:0px 2px 6px rgba(0,0,0,.08);">
✅ {message}
</div>""", unsafe_allow_html=True)


def info_card(message):

    st.markdown(f"""<div style="background:#E3F2FD;border-left:6px solid #1565C0;padding:16px;border-radius:15px;margin-bottom:12px;font-size:18px;font-weight:500;box-shadow:0px 2px 6px rgba(0,0,0,.08);">
ℹ️ {message}
</div>""", unsafe_allow_html=True)


def priority_card(load_name, destination, status):

    st.markdown(f"""<div style="background:white;padding:18px;border-radius:15px;box-shadow:0 3px 10px rgba(0,0,0,.08);margin-bottom:12px;font-size:18px;">
<h4 style="color:#082567;margin-bottom:6px;font-size:21px;">⭐ {load_name}</h4>
<b>Destination:</b> {destination}
<br>
<b>Status:</b> {status}
</div>""", unsafe_allow_html=True)


def section_title(title):

    st.markdown(f"""<div style="background:white;padding:14px;border-radius:12px;margin-top:12px;margin-bottom:12px;border-left:6px solid #082567;">
<h4 style="color:#082567;margin:0;font-size:21px;">{title}</h4>
</div>""", unsafe_allow_html=True)


def deadline_card(load_name, remaining_minutes):

    color = "#43A047"

    if remaining_minutes <= 30:
        color = "#E53935"

    elif remaining_minutes <= 60:
        color = "#FB8C00"

    st.markdown(f"""<div style="background:white;padding:16px;border-left:6px solid {color};border-radius:15px;margin-bottom:12px;font-size:18px;">
⏰ <b>{load_name}</b>
<br>
Remaining: {remaining_minutes} Min
</div>""", unsafe_allow_html=True)