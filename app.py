import os
import json
import streamlit as st
from PIL import Image
import gspread
from datetime import datetime
from google.oauth2 import service_account

# --- Credential Setup from Render ENV ---
creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
creds_dict = json.loads(creds_json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# --- Connect to Google Sheet ---
gc = gspread.authorize(credentials)
sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1ipcHhEb_qhlHRXXZfqBEf3anrmeAHm-kEehV_kAXyc0").sheet1

# --- Page Setup ---
logo = Image.open("logo.png")
st.set_page_config(page_title="TnBcS Inquiry", page_icon=logo, layout="centered")

# --- Session State ---
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# --- After Submission ---
if st.session_state.form_submitted:
    st.success("✅ Thank you! Our team will connect with you shortly.")
    st.markdown("You will be redirected to the [TnBcS Home Page](https://tnbcs.framer.website) shortly...")
    st.markdown("""<meta http-equiv="refresh" content="5;url=https://tnbcs.framer.website">""", unsafe_allow_html=True)

# --- Show Form ---
else:
    st.image("logo.png", width=120)
    st.title("Connect with TnBcS")
    st.write("We act as tunnels and bridges to overcome your business obstacles. Let’s build together!")
    st.markdown("Please fill out the form below. Our team will reach out to assist you.")

    with st.form("contact_form", clear_on_submit=False):
        name = st.text_input("Your Name *")
        company = st.text_input("Company Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number *")
        service = st.multiselect("Service Interested In", [
            "CRM", "Outsourcing Vendor Cycle", "Recruitment Tracker",
            "Approval Request System", "Performance Management", "Attendance Tracker",
            "Project Management", "Sales-Design-Tooling-Production", "Financial Module",
            "Inventory Management", "Shipping Management", "Machine Planning",
            "Downtime Tracking", "One-click MIS", "Hotel Booking System",
            "Quotation", "Invoicing", "Other"
        ])
        message = st.text_area("Additional Message")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Please fill all required fields marked with *.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                service_str = ", ".join(service)
                sheet.append_row([timestamp, name, company, email, phone, service_str, message])
                st.session_state.form_submitted = True
                st.rerun()
