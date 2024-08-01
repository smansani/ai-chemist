import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Directly setting the API key
api_key = "AIzaSyAX9HyVAEBqZgXH7IQ2GKmm1WQaUYPPIpI"
if api_key is None:
    st.error("GOOGLE_API_KEY not found")
else:
    genai.configure(api_key=api_key)

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to setup input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="AI Chemist App")
st.header("AI Chemist App")

input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me")

# If submit button is clicked
if submit:
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload an image to proceed.")
