"""Firestore service for data storage and retrieval."""

from google.cloud import firestore
from config.settings import FIRESTORE_COLLECTION


class FirestoreService:
    """Firestore service for storing and retrieving investor memo data."""
    
    def __init__(self):
        try:
            self.client = firestore.Client()
            self.collection = self.client.collection(FIRESTORE_COLLECTION)
            self.available = True
        except Exception as e:
            print(f"Warning: Firestore initialization failed: {e}")
            self.client = None
            self.collection = None
            self.available = False
    
    def store_memo(self, structured_data, source_filename):
        """Store structured memo data in Firestore."""
        if not self.available:
            print("Firestore not available, skipping storage")
            return None
        
        try:
            # Create document data
            doc_data = {
                'data': structured_data,
                'source_file': source_filename,
                'created_at': firestore.SERVER_TIMESTAMP,
                'last_updated': firestore.SERVER_TIMESTAMP
            }
            
            # Use company name as document ID if available, otherwise use filename
            company_name = structured_data.get('company_overview', {}).get('name')
            if company_name:
                # Clean company name for use as document ID
                doc_id = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
            else:
                # Use filename without extension
                import os
                doc_id = os.path.splitext(source_filename)[0]
            
            # Store in Firestore
            self.collection.document(doc_id).set(doc_data)
            print(f"    Stored in Firestore with ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"    Warning: Failed to store in Firestore: {e}")
            return None
    
    def get_sector_competitors(self, target_company_data):
        """Retrieve companies from the same sector."""
        if not self.available:
            print("Firestore not available for competitor retrieval")
            return []
        
        try:
            sector_hierarchy = target_company_data.get('company_overview', {}).get('sector_hierarchy', [])
            
            if not sector_hierarchy:
                print("No sector information found for competitor matching")
                return []
            
            print(f"Searching for companies in sectors: {sector_hierarchy}")
            
            # Get all documents from Firestore
            docs = self.collection.stream()
            matching_companies = []
            
            for doc in docs:
                doc_data = doc.to_dict().get('data', {})
                doc_sector = doc_data.get('company_overview', {}).get('sector_hierarchy', [])
                
                # Check if there's any overlap in sector hierarchy
                if any(sector in doc_sector for sector in sector_hierarchy):
                    matching_companies.append({
                        'id': doc.id,
                        'data': doc_data
                    })
            
            print(f"Found {len(matching_companies)} companies in similar sectors")
            return matching_companies
            
        except Exception as e:
            print(f"Error retrieving sector competitors: {e}")
            return []
    
    def get_all_memos(self):
        """Retrieve all memos from Firestore."""
        if not self.available:
            return []
        
        try:
            docs = self.collection.stream()
            return [{'id': doc.id, 'data': doc.to_dict().get('data', {})} for doc in docs]
        except Exception as e:
            print(f"Error retrieving memos: {e}")
            return []
    
    def is_available(self):
        """Check if Firestore service is available."""
        return self.available


# Global instance
firestore_service = FirestoreService()
