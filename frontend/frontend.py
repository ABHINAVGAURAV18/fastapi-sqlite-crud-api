import streamlit as st
import requests

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="User Management",
    page_icon="👤",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #A9A9A9;
    }

    /* Main title */
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    /* Card */
    .card {
        background-color: #333;
        text-align: center;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-weight: bold;
    }

    /* User information */
    .user-info {
        background-color: #333;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Title
# -----------------------------
st.markdown(
    '<div class="title">👤 User Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">FastAPI + SQLite + Streamlit</div>',
    unsafe_allow_html=True
)


# -----------------------------
# API URL
# -----------------------------
API_URL = "http://127.0.0.1:8000"


# -----------------------------
# Create User
# -----------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Create User")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=150)

    if st.button("Create User"):

        response = requests.post(
            f"{API_URL}/users/",
            json={
                "name": name,
                "age": age
            }
        )

        if response.status_code == 201:
            st.success("User created successfully!")
        else:
            st.error(response.text)

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Get All Users
# -----------------------------
st.subheader("All Users")

if st.button("Load Users"):

    response = requests.get(f"{API_URL}/users/")

    if response.status_code == 200:

        users = response.json()

        if users:
            for user in users:
                st.markdown(
                    f"""
                    <div class="user-info">
                        <b>ID:</b> {user['user_id']}<br>
                        <b>Name:</b> {user['name']}<br>
                        <b>Age:</b> {user['age']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No users found.")

    else:
        st.error("Failed to fetch users.")