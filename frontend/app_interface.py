import requests
import streamlit as st

API_UPLOAD_URL = "http://localhost:8000/api/upload/"
API_GENERATE_MEMO_URL = "http://localhost:8000/api/generate_memo/"

st.title("AI Investment Analyser")
st.write("Upload a PPT, PDF, Video, or Audio file to process.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a file", type=["ppt", "pptx", "pdf", "mp4", "avi", "mp3", "wav"]
)

if uploaded_file is not None:
    st.write(f"File selected: {uploaded_file.name}")

    # Step 1: Upload & start processing
    if st.button("Upload & Start Processing"):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        with st.spinner("Uploading and starting processing..."):
            response = requests.post(API_UPLOAD_URL, files=files)

        if response.status_code == 200:
            st.success("✅ Upload and processing started!")
            st.session_state["processing_done"] = True
        else:
            st.error("Failed to start processing.")

    # Step 2: Generate PDF
    if st.session_state.get("processing_done", False):
        if st.button("Generate Memo"):
            with st.spinner("Generating Memo..."):
                memo_response = requests.post(API_GENERATE_MEMO_URL)
            if memo_response.status_code == 200:
                memo_bytes = memo_response.content
                st.download_button(
                    "Download Generated Memo",
                    data=memo_bytes,
                    file_name="deal_note.pdf",
                    mime="application/pdf",
                )
            else:
                st.error("❌ Failed to generate Memo.")
