import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import base64


# Streamlit application for Wedding RSVP
st.set_page_config(page_title="Wedding RSVP", page_icon="💒")

# Page title and introduction
st.title("You're Invited!")
st.header("Join us for the wedding of [Name] & [Name]")
st.write("**Date:** [Date]")
st.write("**Venue:** [Venue]")
st.write(
    "We are excited to celebrate this special day with you. Please let us know if you can join by filling out the form below.")

# Google Sheets integration setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
gsheet = gc.open("Wedding RSVP").sheet1


# Function to get base64-encoded image from a local file
def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as file:
        bin_file = file.read()
    return base64.b64encode(bin_file).decode()

# Specify the path to your local image
image_path = 'background.jpg'  # Replace with your image path
base64_image = get_base64_of_bin_file(image_path)

# Add custom CSS for background image
background_image = f"""
<style>
body {{
    background-image: url("data:image/jpg;base64,{base64_image}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

# Display the CSS
st.markdown(background_image, unsafe_allow_html=True)

# RSVP form
with st.form("rsvp_form"):
    name = st.text_input("Name:", placeholder="Enter your full name", max_chars=100)
    guests = st.number_input("Number of Guests:", min_value=1, max_value=10, step=1)
    message = st.text_area("Special Requests / Dietary Restrictions:",
                           placeholder="Any special requests or dietary needs")
    
    # Submit button
    submitted = st.form_submit_button("Submit RSVP")
    
    if submitted:
        if name:
            # Append the data to Google Sheets
            gsheet.append_row([name, guests, message])
            st.success("Thank you for your RSVP, " + name + "! We look forward to seeing you at the wedding.")
        else:
            st.error("Please fill out all required fields.")
