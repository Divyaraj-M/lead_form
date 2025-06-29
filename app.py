import streamlit as st
from PIL import Image
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Custom CSS for better UI ---
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fa;
    }
    .stApp {
        background-color: #f7f9fa;
    }
    .form-card {
        background: white;
        padding: 2.5rem 2rem 2rem 2rem;
        border-radius: 18px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.07);
        max-width: 520px;
        margin: 2rem auto;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 2.2rem;
        font-size: 1.1rem;
        border: none;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2a5298 0%, #1e3c72 100%);
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page setup
logo = Image.open("logo.png")
st.set_page_config(page_title="TnBcS Inquiry", page_icon=logo, layout="centered")

# Google Sheets connection using modern google-auth
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SERVICE_ACCOUNT_FILE = "tnbcs-credentials.json"

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open("TnBcS Prospects").sheet1

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Show confirmation if submitted
if st.session_state.form_submitted:
    st.success("✅ Thank you! Our team will connect with you shortly.")
    st.markdown("You can close this tab or go back to the [TnBcS Home Page](https://tnbcs.framer.website).")
else:
    st.image("logo.png", width=120)
    st.markdown("<h2 style='text-align:center; margin-bottom:0.5rem;'>🤝 Connect with <span style='color:#1e3c72;'>TnBcS</span></h2>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#555; margin-bottom:1.5rem;'>We act as tunnels and bridges to overcome your business obstacles. Let's build together!</div>", unsafe_allow_html=True)
    st.markdown("<div class='form-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Inquiry Form")
    st.markdown("<div style='color:#888; margin-bottom:1.2rem;'>Please fill out the form below. Our team will reach out to assist you.</div>", unsafe_allow_html=True)

    with st.form("contact_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name *")
            email = st.text_input("Email Address")
        with col2:
            company = st.text_input("Company Name")
            phone = st.text_input("Phone Number *")
        service = st.selectbox("Service Interested In", [
            "CRM", "Outsourcing Vendor Cycle", "Recruitment Tracker",
            "Approval Request System", "Performance Management", "Attendance Tracker",
            "Project Management", "Sales-Design-Tooling-Production", "Financial Module",
            "Inventory Management", "Shipping Management", "Machine Planning",
            "Downtime Tracking", "One-click MIS", "Hotel Booking System", "Quotation", "Invoicing", "Other"
        ])
        message = st.text_area("Additional Message", height=90)

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Please fill all required fields marked with *.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.append_row([timestamp, name, company, email, phone, service, message])
                st.session_state.form_submitted = True
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
