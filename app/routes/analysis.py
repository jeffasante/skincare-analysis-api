"""
Analysis route for image analysis.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import logging

from app.services import ImageService, AnalysisService
from app.utils import validate_image_id, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)


class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint."""
    image_id: str = Field(..., description="Unique image identifier from upload")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "abc123def456"
            }
        }


class AnalysisResponse(BaseModel):
    """Response model for analysis endpoint."""
    image_id: str
    skin_type: str
    issues: List[str]
    confidence: float
    recommendations: List[str]
    analyzed_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "abc123def456",
                "skin_type": "Combination",
                "issues": ["Hyperpigmentation", "Fine Lines"],
                "confidence": 0.87,
                "recommendations": [
                    "Use vitamin C serum for hyperpigmentation",
                    "Apply retinol for fine lines"
                ],
                "analyzed_at": "2026-01-05T10:31:00Z"
            }
        }


@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_image(request: AnalysisRequest) -> Dict[str, Any]:
    """
    Analyze an uploaded image.
    
    This endpoint performs mock skincare analysis on a previously uploaded image.
    The analysis includes:
    - Skin type classification
    - Detected skin issues
    - Confidence score
    - Personalized recommendations
    
    Args:
        request: Analysis request containing image_id
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        HTTPException 400: Invalid image_id format
        HTTPException 404: Image not found
        HTTPException 500: Server error during analysis
    """
    try:
        logger.info(f"Received analysis request for image_id: {request.image_id}")
        
        # Validate image_id format
        validate_image_id(request.image_id)
        
        # Get image path
        try:
            image_path = ImageService.get_image_path(request.image_id)
        except FileNotFoundError:
            logger.warning(f"Image not found: {request.image_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image with ID '{request.image_id}' not found"
            )
        
        # Perform analysis
        result = AnalysisService.analyze_image(image_path)
        
        logger.info(f"Successfully analyzed image: {request.image_id}")
        return result
        
    except ValidationError as e:
        logger.warning(f"Validation error for {request.image_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error analyzing {request.image_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while analyzing the image"
        )
