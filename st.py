import streamlit as st
from poc_theragraph import get_information
from PIL import Image
import os

image = Image.open('damco_.png')
st.image(image)

st.title("Theragraph - POC")

uploaded_file = st.file_uploader("Choose a document", type=["pdf"])

if uploaded_file is not None:

    filename = 'document.pdf'
    # Save the PDF to the desired directory
    save_path = "data"  # Change this to your desired directory
    os.makedirs(save_path, exist_ok=True)
    pdf_save_location = os.path.join(save_path, filename)
    with open(pdf_save_location, "wb") as f:
        f.write(uploaded_file.getbuffer())
    #st.success(f"PDF saved successfully at: {pdf_save_location}")

    with st.spinner('Please wait...'):
        response=get_information('data/document.pdf')
        #print(response)
        #st.success(response)
        st.json(response)
# else:
#     st.error("Please upload a PDF file.")
