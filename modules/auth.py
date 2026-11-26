import streamlit as st
from modules.users import get_users


def login_page():

    st.markdown("""<div style="background:linear-gradient(135deg,#082567,#0A2A66);padding:30px;border-radius:20px;color:white;text-align:center;margin-top:30px;margin-bottom:25px;box-shadow:0 8px 24px rgba(0,0,0,.20);">
<h1 style="margin-bottom:8px;color:white;">🚆 Crew Arrangement &amp; Mobility</h1>
<h4 style="margin:0;color:rgba(255,255,255,0.9);font-weight:500;">DRM Control Dashboard</h4>
</div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("### 🔐 Login")

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button(
            "Login",
            width="stretch"
        ):

            users = get_users()

            login_ok = False

            for user in users:

                if (
                    str(user.get("username", "")).strip() == username.strip()
                    and
                    str(user.get("password", "")).strip() == password.strip()
                    and
                    str(user.get("status", "")).strip().lower() == "active"
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username.strip()
                    st.session_state.role = str(user.get("role", "")).strip().lower()

                    login_ok = True

                    st.rerun()

            if not login_ok:

                st.error(
                    "❌ Invalid Username or Password"
                )

    st.markdown("<br>", unsafe_allow_html=True)