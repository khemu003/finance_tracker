import streamlit as st
from data_handler import authenticate_user, register_user

# Page Configuration
st.set_page_config(page_title="Login Form", layout="centered")

# Custom CSS
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #a8c0ff, #3f2b96);
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .login-container {
        width: 400px;
        background: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    .stRadio div label {
        padding: 8px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 16px;
        background: #f1f1f1;
    }
    .stRadio div label[data-selected="true"] {
        background: linear-gradient(to right, #0052d4, #4364f7);
        color: white;
    }
    .input-box {
        width: 100%;
        padding: 12px;
        margin-bottom: 15px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .login-btn {
        width: 100%;
        background: linear-gradient(to right, #0052d4, #4364f7);
        color: white;
        border: none;
        padding: 12px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }
    .switch-text {
        margin-top: 10px;
        font-size: 14px;
    }
    .switch-text a {
        color: #0052d4;
        font-weight: bold;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session state for user authentication
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

# Toggle between Login and Signup using st.radio
option = st.radio("Select Option:", ["Login", "Signup"], horizontal=True, key="login_signup")

st.markdown(f"<h2>{option}</h2>", unsafe_allow_html=True)

# Input Fields
username = st.text_input("Email Address", placeholder="Enter your email")
password = st.text_input("Password", type="password", placeholder="Enter your password")

if option == "Login":
    st.markdown('<a href="#" style="color: #0052d4; font-size: 14px;">Forgot password?</a>', unsafe_allow_html=True)
    if st.button("Login", use_container_width=True):
        user_id = authenticate_user(username, password)
        if user_id:
            st.session_state["user_id"] = user_id
            st.success("Login successful! Redirecting...")
            st.switch_page("pages/finance_tracker.py")
        else:
            st.error("Invalid credentials. Please try again.")
else:
    if st.button("Create Account", use_container_width=True):
        if register_user(username, password):
            st.success("Account created successfully! Please login.")
        else:
            st.error("Username already taken. Try a different one.")

st.markdown("</div>", unsafe_allow_html=True)