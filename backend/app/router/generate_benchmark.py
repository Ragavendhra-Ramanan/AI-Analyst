import argparse
import sys
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import io
from ..services.benchmark_creation.vision_service import (
                        vision_service,
                    )
from ..services.benchmark_creation.gcp_service import gcp_service

router = APIRouter()


def _import_benchmarking_flow():
    """Lazy import of benchmarking flow to handle missing dependencies."""
    try:
        from ..flows.orchestrators import benchmarking_flow
        return benchmarking_flow
    except ImportError as e:
        print(f"ImportError: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Benchmarking services not available: {str(e)}. Please ensure Google Cloud dependencies are installed."
        )


@router.post("/benchmark/")
async def benchmark_mode(file: UploadFile = File(...), output_dir: str = "output"):
    """Execute benchmarking mode with uploaded file and return PDF content."""
    temp_file_path = None
    pdf_path = None
    try:
        print("=== Benchmark Analysis Mode ===")
        print(f"Processing uploaded file: {file.filename}")
        print(f"Output directory: {output_dir}")
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=422, detail="Only PDF files are allowed for benchmark analysis.")
        
        # Save uploaded file temporarily
        temp_file_path = file.filename
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        memo_file = temp_file_path
        
        # Read memo content - handle PDF files
        try:
            if memo_file.lower().endswith('.pdf'):
                # PDF file - extract text using Vision API
                print("PDF memo detected, extracting text...")
                
                if not vision_service.is_available():
                    # Clean up temp file
                    if temp_file_path and os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    error_msg = "Error: Vision API not available for PDF extraction"
                    print(error_msg)
                    raise HTTPException(
                        status_code=500,
                        detail=error_msg
                    )
                
                if not gcp_service.is_available():
                    # Clean up temp file
                    if temp_file_path and os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    error_msg = "Error: Google Cloud Storage not available for PDF upload"
                    print(error_msg)
                    raise HTTPException(
                        status_code=500,
                        detail=error_msg
                    )
                
                # Upload PDF to GCS first
                blob_name = f"memo_inputs/{os.path.basename(memo_file)}"
                if not gcp_service.upload_file(memo_file, blob_name):
                    # Clean up temp file
                    if temp_file_path and os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    error_msg = "Error: Failed to upload PDF to GCS"
                    print(error_msg)
                    raise HTTPException(
                        status_code=500,
                        detail=error_msg
                    )
                
                # Extract text from GCS URI
                gcs_uri = f"gs://{gcp_service.bucket_name}/{blob_name}"
                memo_text = vision_service.extract_text_from_pdf(gcs_uri)
                if not memo_text:
                    # Clean up temp file
                    if temp_file_path and os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    error_msg = "Error: Failed to extract text from PDF"
                    print(error_msg)
                    raise HTTPException(
                        status_code=500,
                        detail=error_msg
                    )
            else:
                # This shouldn't happen since we validate for PDF only
                # Clean up temp file
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                error_msg = "Error: Only PDF files are supported"
                print(error_msg)
                raise HTTPException(
                    status_code=422,
                    detail=error_msg
                )
        except Exception as e:
            # Clean up temp file
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            error_msg = f"Error reading memo file: {e}"
            print(error_msg)
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )
        
        if not memo_text:
            # Clean up temp file
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            error_msg = "Error: Memo file is empty"
            print(error_msg)
            raise HTTPException(
                status_code=422,
                detail=error_msg
            )
        
        # Execute benchmarking flow
        benchmarking_flow = _import_benchmarking_flow()
        pdf_path = benchmarking_flow.create_benchmark_analysis(memo_text, output_dir)
        
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"✅ Benchmark analysis completed successfully!")
            print(f"📄 PDF report generated: {pdf_path}")
            
            # Read PDF content and return as streaming response
            def iter_pdf_content():
                with open(pdf_path, 'rb') as pdf_file:
                    yield from pdf_file
            
            return StreamingResponse(
                iter_pdf_content(),
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=benchmark_report.pdf"
                },
            )
        else:
            print("❌ Benchmark analysis failed")
            raise HTTPException(status_code=500, detail="Benchmark analysis failed to generate PDF")
        
    except Exception as e:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        print(f"❌ Error in benchmark mode: {e}")
        raise HTTPException(status_code=500, detail=f"Error in benchmark mode: {str(e)}")
        

