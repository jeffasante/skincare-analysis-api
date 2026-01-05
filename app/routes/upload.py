"""
Upload route for image uploads.
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from typing import Dict, Any
import logging

from app.services import ImageService
from app.utils import ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def upload_image(
    file: UploadFile = File(..., description="Image file (JPEG or PNG, max 5MB)")
) -> Dict[str, Any]:
    """
    Upload an image for analysis.
    
    This endpoint accepts image uploads with the following validations:
    - File type: JPEG or PNG only
    - File size: Maximum 5MB
    - Content validation: Checks actual file content (not just extension)
    
    Args:
        file: Uploaded image file
        
    Returns:
        Dictionary containing:
        - image_id: Unique identifier for the uploaded image
        - filename: Original filename
        - size: File size in bytes
        - uploaded_at: ISO 8601 timestamp
        
    Raises:
        HTTPException 400: Invalid file type or size
        HTTPException 500: Server error during upload
    """
    try:
        logger.info(f"Received upload request for file: {file.filename}")
        
        # Save and validate image
        result = await ImageService.save_image(file)
        
        logger.info(f"Successfully uploaded image with ID: {result['image_id']}")
        return result
        
    except ValidationError as e:
        logger.warning(f"Validation error for {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error uploading {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while uploading the image"
        )
