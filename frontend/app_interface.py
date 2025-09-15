import requests
import streamlit as st

API_URL = "http://localhost:8000/api/upload/"

st.title("📂 File Upload Demo")
st.write("Upload a PPT, Video, or Audio file to process.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a file", type=["ppt", "pptx", "pdf", "mp4", "avi", "mp3", "wav"]
)

if uploaded_file is not None:
    st.write(f"✅ File selected: {uploaded_file.name}")

    if st.button("Upload & Process"):
        # Send file to FastAPI backend
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        with st.spinner("Processing..."):
            response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            result = response.json()
            st.success("Processing complete ✅")
            st.json(result)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
