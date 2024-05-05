from dotenv import load_dotenv
import os
import mysql.connector
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from PIL import Image



# Load environment variables
load_dotenv()

# Configure Google Gemini Pro Vision API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Database connection
db_connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="expiry"
    )
db_cursor=db_connection.cursor()

# Function to save to database
def save_to_db(email, product_names, expire_dates):
    query = "INSERT INTO invoice (email, product_names, expire_dates) VALUES (%s, %s, %s)"
    db_cursor.execute(query, (email, ', '.join(product_names), ', '.join(expire_dates)))
    db_connection.commit()
    db_connection.close()

# Function to get response from Google Gemini Pro Vision API
def get_gemini_response(input_prompt, image_parts):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_parts[0]])
    return response.text

# Function to setup input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Invoice Items App")

# User inputs
email = st.text_input("Email:", key="email")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

submit = st.button("Tell me the items in the image")

input_prompt = """
You are an expert in identifying different items from the image of an invoice.
               Format:
               1. Item 1
               2. Item 2
               ----
"""

if submit and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    items = response.split('\n')  # Assuming each item is on a new line
    if items:
        st.session_state['items'] = items
        st.session_state['expiry_dates'] = {item: datetime.now().date() for item in items}

# Display inputs for expiry dates if items are loaded
if 'items' in st.session_state:
    for item in st.session_state['items']:
        st.session_state['expiry_dates'][item] = st.date_input(f"Expiry Date for {item}:", value=st.session_state['expiry_dates'][item], key=item,min_value=datetime.now().date())

save_data = st.button("Save Data to Database")
if save_data and 'items' in st.session_state and 'expiry_dates' in st.session_state:
    expiry_dates_str = [f"{item}: {st.session_state['expiry_dates'][item].strftime('%Y-%m-%d')}" for item in st.session_state['items']]
    save_to_db(email, st.session_state['items'], expiry_dates_str)
    st.success("Data saved to database successfully we will alert you 10 days before your product expires!")
