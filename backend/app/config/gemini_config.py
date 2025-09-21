"""Gemini AI configuration and initialization."""

import google.generativeai as genai
from .settings import get_gemini_api_key

class GeminiConfig:
    """Gemini AI configuration manager."""
    
    def __init__(self):
        self.is_configured = False
        self.api_key = None
    
    def configure(self):
        """Configure Gemini AI with API key."""
        self.api_key = get_gemini_api_key()
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.is_configured = True
            print("Gemini API configured successfully")
            return True
        else:
            print("Warning: GEMINI_API_KEY environment variable not set. Structured extraction will be skipped.")
            return False
    
    def is_available(self):
        """Check if Gemini is configured and available."""
        return self.is_configured and self.api_key is not None

# Global instance
gemini_config = GeminiConfig()
