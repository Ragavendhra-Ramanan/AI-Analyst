import requests
import streamlit as st
from streamlit_option_menu import option_menu
import os

# Get the base URL for API calls - works both locally and in container
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_UPLOAD_URL = f"{API_BASE_URL}/api/upload/"
API_GENERATE_MEMO_URL = f"{API_BASE_URL}/api/generate_memo/"
API_BENCHMARK_URL = f"{API_BASE_URL}/api/benchmark/"


selected_option = option_menu(
    None,
    ["Investment Memo", "Benchmark Report"],
    default_index=0,
    orientation="horizontal",
)

if selected_option == "Investment Memo":
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
else:
    st.title("AI Benchmark Report Generator")
    st.write("Upload the Company's Investment Memo (PDF)")
    # File uploader for benchmark
    benchmark_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if benchmark_file is not None:
        st.write(f"File selected: {benchmark_file.name}")

        # Step 1: Upload & start benchmark processing
        if st.button("Upload & Generate Benchmark Report"):
            files = {"file": (benchmark_file.name, benchmark_file, benchmark_file.type)}
            with st.spinner("Uploading and generating benchmark report..."):
                response = requests.post(API_BENCHMARK_URL, files=files)

            if response.status_code == 200:
                report_bytes = response.content
                st.success("✅ Benchmark report generated!")
                st.download_button(
                    "Download Benchmark Report",
                    data=report_bytes,
                    file_name="benchmark_report.pdf",
                    mime="application/pdf",
                )
            else:
                st.error("❌ Failed to generate Benchmark Report.")
