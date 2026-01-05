"""
Image service for handling file uploads and storage.
"""
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from fastapi import UploadFile
from app.config import UPLOAD_DIR
from app.utils import (
    validate_file_extension,
    validate_file_size,
    validate_file_content,
    ValidationError
)

class ImageService:
    """Service for managing image uploads and storage."""
    
    @staticmethod
    async def save_image(file: UploadFile) -> Dict[str, Any]:
        """
        Save uploaded image to local storage with validation.
        
        Args:
            file: Uploaded file object from FastAPI
            
        Returns:
            Dictionary containing image metadata
            
        Raises:
            ValidationError: If validation fails
        """
        validate_file_extension(file.filename)
        
        content = await file.read()
        file_size = len(content)
        
        # Validate file size
        validate_file_size(file_size)
        
        # Generate unique image ID
        image_id = str(uuid.uuid4()).replace('-', '')[:16]
        
        extension = Path(file.filename).suffix.lower()
        
        # Create file path
        filename = f"{image_id}{extension}"
        file_path = UPLOAD_DIR / filename
        
        try:
            with open(file_path, 'wb') as buffer:
                buffer.write(content)
            
            validate_file_content(file_path)
            
        except ValidationError:
            if file_path.exists():
                file_path.unlink()
            raise
        except Exception as e:
            if file_path.exists():
                file_path.unlink()
            raise ValidationError(f"Error saving file: {str(e)}")
        
        # Return metadata
        return {
            "image_id": image_id,
            "filename": file.filename,
            "size": file_size,
            "uploaded_at": datetime.utcnow().isoformat() + "Z"
        }
    
    @staticmethod
    def get_image_path(image_id: str) -> Path:
        """
        Get the file path for an image by ID.
        
        Args:
            image_id: Unique image identifier
            
        Returns:
            Path object to the image file
            
        Raises:
            FileNotFoundError: If image doesn't exist
        """
        # Find file with matching image_id (any extension)
        for ext in ['.jpg', '.jpeg', '.png']:
            file_path = UPLOAD_DIR / f"{image_id}{ext}"
            if file_path.exists():
                return file_path
        
        raise FileNotFoundError(f"Image with ID '{image_id}' not found")
    
    @staticmethod
    def image_exists(image_id: str) -> bool:
        """
        Check if an image exists by ID.
        
        Args:
            image_id: Unique image identifier
            
        Returns:
            True if image exists, False otherwise
        """
        try:
            ImageService.get_image_path(image_id)
            return True
        except FileNotFoundError:
            return False
