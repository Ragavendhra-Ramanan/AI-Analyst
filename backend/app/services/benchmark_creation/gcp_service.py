"""Google Cloud Storage service operations."""

from google.cloud import storage
from config.settings import BUCKET_NAME


class GCSService:
    """Google Cloud Storage service for file operations."""
    
    def __init__(self):
        try:
            self.client = storage.Client()
            self.bucket_name = BUCKET_NAME
            self.available = True
            # Try to create bucket if it doesn't exist
            self.create_bucket_if_not_exists(self.bucket_name)
        except Exception as e:
            print(f"Warning: GCS initialization failed: {e}")
            self.client = None
            self.bucket_name = None
            self.available = False
    
    def upload_file(self, local_file_path, destination_blob_name):
        """Upload a file to GCS."""
        if not self.available:
            print("GCS service not available")
            return False
        
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(local_file_path)
            print(f"Uploaded {local_file_path} to gs://{self.bucket_name}/{destination_blob_name}")
            return True
        except Exception as e:
            print(f"Failed to upload file: {e}")
            return False
    
    def create_bucket_if_not_exists(self, bucket_name):
        """Create a GCS bucket if it doesn't exist."""
        if not self.available:
            print("GCS not available, skipping bucket creation")
            return False
        
        try:
            bucket = self.client.bucket(bucket_name)
            bucket.reload()
            print(f"Bucket {bucket_name} already exists")
            return True
        except:
            try:
                bucket = self.client.create_bucket(bucket_name)
                print(f"Created bucket {bucket_name}")
                return True
            except Exception as e:
                print(f"Failed to create bucket {bucket_name}: {e}")
                return False
    
    def is_available(self):
        """Check if GCS service is available."""
        return self.available


# Global instance
gcp_service = GCSService()
