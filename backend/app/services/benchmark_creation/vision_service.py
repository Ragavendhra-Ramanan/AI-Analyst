"""Google Vision API service for PDF text extraction."""

import os
import json
from google.cloud import vision_v1 as vision
from .gcp_service import gcp_service


class VisionService:
    """Google Vision API service for text extraction."""
    
    def __init__(self):
        try:
            self.client = vision.ImageAnnotatorClient()
            self.available = True
        except Exception as e:
            print(f"Warning: Vision API initialization failed: {e}")
            self.client = None
            self.available = False
    
    def extract_text_from_pdf(self, pdf_path, bucket_name=None):
        """Extract text from PDF using Vision API."""
        if not self.available:
            raise RuntimeError("Vision API service not available")
        
        # Upload to GCS if needed
        if bucket_name:
            blob_name = f"pdfs/{os.path.basename(pdf_path)}"
            if gcp_service.upload_file(pdf_path, blob_name):
                gcs_uri = f"gs://{gcp_service.bucket_name}/{blob_name}"
            else:
                raise RuntimeError("Failed to upload PDF to GCS")
        else:
            # Assume pdf_path is already a GCS URI
            gcs_uri = pdf_path
        
        return self._extract_from_gcs_uri(gcs_uri)
    
    def _extract_from_gcs_uri(self, gcs_uri):
        """Extract text from PDF stored in GCS."""
        feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
        
        gcs_source = vision.GcsSource(uri=gcs_uri)
        input_config = vision.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')
        
        gcs_destination = vision.GcsDestination(
            uri=gcs_uri.replace('.pdf', '_vision_output/')
        )
        output_config = vision.OutputConfig(
            gcs_destination=gcs_destination, 
            batch_size=1
        )
        
        async_request = vision.AsyncAnnotateFileRequest(
            features=[feature],
            input_config=input_config,
            output_config=output_config
        )
        
        operation = self.client.async_batch_annotate_files(
            requests=[async_request]
        )
        
        print('Waiting for Vision API operation to complete...')
        result = operation.result(timeout=420)
        
        # Process the results
        storage_client = gcp_service.client
        if not storage_client:
            raise RuntimeError("GCS client not available for processing results")
        
        gcs_destination_uri = gcs_destination.uri
        bucket_name = gcs_destination_uri.split('/')[2]
        prefix = '/'.join(gcs_destination_uri.split('/')[3:])
        
        bucket = storage_client.bucket(bucket_name)
        blob_list = list(bucket.list_blobs(prefix=prefix))
        
        extracted_text = ""
        for blob in blob_list:
            json_string = blob.download_as_text()
            response = json.loads(json_string)
            
            for page in response['responses']:
                if 'fullTextAnnotation' in page:
                    extracted_text += page['fullTextAnnotation']['text'] + "\n"
        
        return extracted_text.strip()
    
    def is_available(self):
        """Check if Vision API service is available."""
        return self.available


# Global instance
vision_service = VisionService()
