import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

# Streamlit application for Wedding RSVP
st.set_page_config(page_title="Wedding RSVP", page_icon="❤️")

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add custom CSS to style the submit button
def style_submit_button():
    custom_button_css = '''
    <style>
    div.stButton > button:first-child {
        background-color: #F2E6F9;
        color: #800080;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #e4befa;
    }
    </style>
    '''
    st.markdown(custom_button_css, unsafe_allow_html=True)

    
# Cache the base64 encoding of the binary file
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()


# Set the background of the Streamlit app
def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    

# Page title and introduction
st.markdown("<h1 style='text-align: center;'>Wedding RSVP</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>James Playground</h3>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'><i>We are excited to celebrate this special day with you!</i></h6>", unsafe_allow_html=True)

# st.write("*We are excited to celebrate this special day with you!*")

# Google Sheets integration setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
gc = gspread.authorize(credentials)

try:
    gsheet = gc.open("Streamlit Playground").sheet1
except Exception as e:
    st.error(f"Error opening Google Sheet: {e}")
# Open the Google Sheet
#gsheet = gc.open("Streamlit Playground").sheet1

# Set background image
set_background('background.png')

# Apply button styling
style_submit_button()

# RSVP form
#with st.form("rsvp_form"):
st.write("Please let us know if you can join us by filling the form")
name = st.text_input("**Name**", placeholder="Please enter you name", max_chars=100)
guests = st.number_input("**Number of Guests**", min_value=1, max_value=10, step=1)
st.write("**Reception** *14-December | 6:30PM onwards*")
attend_both = st.checkbox("**Reception and Wedding**")
attend_reception = st.checkbox("**Reception** *[14-December-2024]*")
st.write("**Wedding** *15-December | 12:01PM Muhurthum*")
attend_wedding = st.checkbox("**Wedding**&nbsp;&nbsp;*[15-December-2024]*")
    

# Submit button
submitted = st.form_submit_button("Submit RSVP")

# if submitted:
if name.strip():
    # Append the data to Google Sheets
    st.balloons()
    gsheet.append_row([name, guests, attend_both, attend_reception, attend_wedding])
    st.success("Thank you for your RSVP! We'll see you soon!")
# else:
  st.error("Please fill out all required fields.")


st.write("**Venue:** Somewhere Awesome, U.S.A")
