import streamlit as st

from modules.users import (
    get_users,
    create_user,
    delete_user,
    update_status,
    reset_password
)

from modules.ui import (
    kpi_card
)


def show_users():

    if st.session_state.role != "admin":

        st.error("Access Denied")

        return

    # ==================================
    # HEADER
    # ==================================

    st.markdown("""<div class="topbar">
<h2 style="margin-bottom:4px;color:white;">👤 User Management</h2>
<div style="font-size:13px;opacity:0.9;">DRM Administrator Panel</div>
</div>""", unsafe_allow_html=True)

    users = get_users()

    # ==================================
    # USER COUNTS
    # ==================================

    total_users = len(users)

    admins = len([
        u for u in users
        if str(u["role"]).lower() == "admin"
    ])

    normal_users = len([
        u for u in users
        if str(u["role"]).lower() == "user"
    ])

    c1, c2, c3 = st.columns(3)

    with c1:

        kpi_card(
            "Total Users",
            total_users,
            "👥",
            "#082567"
        )

    with c2:

        kpi_card(
            "Admins",
            admins,
            "⚙️",
            "#1565C0"
        )

    with c3:

        kpi_card(
            "Users",
            normal_users,
            "👤",
            "#2E7D32"
        )

    st.divider()

    # ==================================
    # CREATE USER
    # ==================================

    st.subheader("➕ Create User")

    col1, col2, col3 = st.columns(3)

    with col1:

        username = st.text_input(
            "Username"
        )

    with col2:

        password = st.text_input(
            "Password",
            type="password"
        )

    with col3:

        role = st.selectbox(
            "Role",
            [
                "user",
                "admin"
            ]
        )

    if st.button(
        "➕ Create User",
        width="stretch"
    ):

        if not username or not password:

            st.warning(
                "Username and Password required"
            )

        else:

            created = create_user(
                username,
                password,
                role
            )

            if created:

                st.success(
                    "✅ User Created Successfully"
                )

                st.rerun()

            else:

                st.error(
                    "Username already exists"
                )

    st.divider()

    # ==================================
    # DELETE USER
    # ==================================

    st.subheader("🗑 Delete User")

    delete_users = [
        u["username"]
        for u in users
        if str(u["username"]).lower() != "drm"
    ]

    if delete_users:

        selected_user = st.selectbox(
            "Select User",
            delete_users
        )

        if st.button(
            "Delete User",
            width="stretch"
        ):

            if delete_user(
                selected_user
            ):

                st.success(
                    f"{selected_user} deleted"
                )

                st.rerun()

    st.divider()

    # ==================================
    # ACTIVATE / DEACTIVATE USER
    # ==================================

    st.subheader(
        "🔄 Update User Status"
    )

    status_user = st.selectbox(
        "User",
        [
            u["username"]
            for u in users
        ],
        key="status_user"
    )

    status = st.selectbox(
        "Status",
        [
            "Active",
            "Inactive"
        ]
    )

    if st.button(
        "Update Status",
        width="stretch"
    ):

        update_status(
            status_user,
            status
        )

        st.success(
            "Status Updated"
        )

        st.rerun()

    st.divider()

    # ==================================
    # RESET PASSWORD
    # ==================================

    st.subheader(
        "🔒 Reset Password"
    )

    user_for_reset = st.selectbox(
        "Select User",
        [
            u["username"]
            for u in users
        ],
        key="reset_user"
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    if st.button(
        "Reset Password",
        width="stretch"
    ):

        if new_password:

            reset_password(
                user_for_reset,
                new_password
            )

            st.success(
                "Password Updated"
            )

    st.divider()

    # ==================================
    # USER TABLE
    # ==================================

    st.subheader(
        "📋 Existing Users"
    )

    user_df = []

    for user in users:

        user_df.append({
            "Username": user["username"],
            "Role": user["role"],
            "Status": user["status"]
        })

    st.dataframe(
        user_df,
        width="stretch",
        height=350
    )

    st.divider()

    # ==================================
    # SECURITY INFO
    # ==================================

    st.info("""
🔒 DRM Admin Permissions

✅ Create Users

✅ Delete Users

✅ Activate/Deactivate Users

✅ Reset Passwords

✅ Manage Roles

✅ View User List

❌ DRM Account Cannot Be Deleted
""")