import streamlit as st
import requests
# from dashboard import main as dashboard_main
st.set_page_config(page_title="CryptoSim Auth", layout="centered", page_icon="🔐")



# --- CONFIG ---
BASE_URL = "http://127.0.0.1:7000"  # Update if deployed

st.set_page_config(page_title="Crypto Vault Auth", page_icon="🪙", layout="centered")
st.markdown("<h1 style='text-align: center;'>CryptoSim</h1>", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2 = st.tabs(["Register", "Login"])

# --- LOGIN TAB ---
with tab2:
    st.subheader("Login to Your Account")
    identifier = st.text_input("Username or Email", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    st.write('')

    if st.button("Login", type='primary', use_container_width=True):
        if not identifier or not password:
            st.error("Please fill in all fields.")
        else:
            res = requests.post(f"{BASE_URL}/login", params={
                "identifier": identifier,
                "password": password
            })
            if res.status_code == 200 and res.json().get("success"):
                data = res.json()
                st.success(f"✅ Login successful!  Welcome, {data['user']['name']}")
                # st.write(f"**Welcome, {data['user']['name']}!**")
                st.code(f"Token: {data['token']}")
            else:
                st.error(res.json().get("message", "Login failed."))

# --- REGISTER TAB ---
with tab1:
    st.subheader("Create a New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=18, max_value=100)
    phone = st.text_input("Phone Number")
    st.write('')

    if st.button("Register", type='primary', use_container_width=True):
        if not all([name, email, username, password, gender, age, phone]):
            st.warning("Please fill out all fields.")
        else:
            res = requests.post(f"{BASE_URL}/register", params={
                "email": email,
                "name": name,
                "username": username,
                "password": password,
                "gender": gender,
                "age": age,
                "phone": phone
            })
            if res.status_code == 200 and res.json().get("success"):
                st.success("🎉 Registered successfully! You can now log in.")
            else:
                st.error(res.json().get("message", "Registration failed."))
