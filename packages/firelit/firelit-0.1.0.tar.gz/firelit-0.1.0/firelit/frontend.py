import streamlit as st

from firelit.admin import FirebaseAdmin


def firelit_login_form(
    firelit_config: str | dict | None = None, sidebar: bool = False
) -> FirebaseAdmin:
    if sidebar:
        with st.sidebar:
            return firelit_login_form(firelit_config=firelit_config, sidebar=False)

    if "firelit_admin" not in st.session_state:
        admin = FirebaseAdmin(config=firelit_config)
        st.session_state["firelit_admin"] = admin
    else:
        admin = st.session_state["firelit_admin"]

    if not admin.authentication_status:
        with st.form("**Login**"):
            st.subheader("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.form_submit_button(
                "🔐 Login", type="primary", use_container_width=True
            ):
                admin.login(email, password)

                if admin.authentication_status:
                    st.success(
                        "Login successful 🎉 Welcome %s" % admin.user_info["name"]
                    )
                    st.rerun()

                else:
                    st.error("Invalid credentials")
                    st.stop()

    else:
        with st.expander("Logged", expanded=False):
            st.subheader(f"Welcome {admin.user_info['name']}")

            st.info("Licence expiration date: %s" % admin.licence["expiration_date"])

            if st.button("🔒 Logout", type="primary", use_container_width=True):
                admin.reset_connection()
                st.rerun()

    return admin
