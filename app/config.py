"""
Configuration settings for the Skincare Analysis API.
"""
import os
from pathlib import Path

# API Configuration
API_KEY = os.getenv("API_KEY", "dev-api-key-12345")

# File Upload Configuration
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 5 * 1024 * 1024))  # 5MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
