"""
Validation utilities for file uploads and processing.
"""
import magic
from pathlib import Path
from typing import Tuple
from app.config import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, MAX_FILE_SIZE


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_file_extension(filename: str) -> bool:
    """
    Validate file extension against allowed types.
    
    Args:
        filename: Name of the file to validate
        
    Returns:
        True if extension is valid
        
    Raises:
        ValidationError: If extension is not allowed
    """
    extension = Path(filename).suffix.lower().lstrip('.')
    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return True


def validate_file_size(file_size: int) -> bool:
    """
    Validate file size against maximum allowed size.
    
    Args:
        file_size: Size of file in bytes
        
    Returns:
        True if size is valid
        
    Raises:
        ValidationError: If file is too large
    """
    if file_size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        raise ValidationError(f"File too large. Maximum size: {max_mb}MB")
    return True


def validate_file_content(file_path: Path) -> Tuple[bool, str]:
    """
    Validate file content using magic numbers (MIME type detection).
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        Tuple of (is_valid, mime_type)
        
    Raises:
        ValidationError: If MIME type is not allowed
    """
    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(str(file_path))
        
        if mime_type not in ALLOWED_MIME_TYPES:
            raise ValidationError(
                f"Invalid file content. File must be a valid image (JPEG or PNG)"
            )
        
        return True, mime_type
    except Exception as e:
        raise ValidationError(f"Error validating file content: {str(e)}")


def validate_image_id(image_id: str) -> bool:
    """
    Validate image ID format.
    
    Args:
        image_id: Image ID to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If image ID is invalid
    """
    if not image_id or not isinstance(image_id, str):
        raise ValidationError("Invalid image_id format")
    
    if len(image_id) < 8:
        raise ValidationError("Invalid image_id format")
    
    return True
