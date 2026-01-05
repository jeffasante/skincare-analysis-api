"""
Analysis service for mock skincare analysis logic.
"""
import random
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from PIL import Image


class AnalysisService:
    """Service for performing mock skincare analysis."""
    
    # Mock data for realistic responses
    SKIN_TYPES = ["Normal", "Oily", "Dry", "Combination", "Sensitive"]
    
    ISSUES = [
        "Hyperpigmentation",
        "Fine Lines",
        "Acne",
        "Dark Circles",
        "Redness",
        "Uneven Texture",
        "Large Pores",
        "Dryness"
    ]
    
    RECOMMENDATIONS = {
        "Hyperpigmentation": "Use vitamin C serum for hyperpigmentation",
        "Fine Lines": "Apply retinol for fine lines",
        "Acne": "Consider salicylic acid for acne treatment",
        "Dark Circles": "Use caffeine-based eye cream for dark circles",
        "Redness": "Apply soothing niacinamide for redness",
        "Uneven Texture": "Use AHA/BHA exfoliant for texture improvement",
        "Large Pores": "Try niacinamide to minimize pore appearance",
        "Dryness": "Apply hyaluronic acid serum for hydration"
    }
    
    @staticmethod
    def analyze_image(image_path: Path) -> Dict[str, Any]:
        """
        Perform mock analysis on an image.
        
        This simulates AI analysis using deterministic logic based on
        image properties. In production, this would integrate with a
        real ML model.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing analysis results
        """
        # Open image to get properties for deterministic mock logic
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Use image dimensions as seed for deterministic results
                seed = width + height
                random.seed(seed)
                
                rng = random.Random(seed)
                
                # Determine skin type based on image properties
                skin_type = rng.choice(AnalysisService.SKIN_TYPES)
                
                # Determine number of issues (1-3)
                num_issues = 1 + (seed % 3)
                
                # Select issues deterministically using sampling
                # This fixes the infinite loop caused by short cycles in the previous LCG implementation
                issues = rng.sample(AnalysisService.ISSUES, num_issues)
                issues.sort() # Keep consistent order based on string value
                
                confidence = 0.75 + (seed % 20) / 100
                
                recommendations = [
                    AnalysisService.RECOMMENDATIONS[issue] 
                    for issue in issues
                ]
                
        except Exception as e:
            # Fallback to basic mock data if image can't be opened
            skin_type = "Combination"
            issues = ["Hyperpigmentation"]
            confidence = 0.85
            recommendations = [AnalysisService.RECOMMENDATIONS["Hyperpigmentation"]]
        
        # Extract image_id from filename
        image_id = image_path.stem
        
        return {
            "image_id": image_id,
            "skin_type": skin_type,
            "issues": issues,
            "confidence": round(confidence, 2),
            "recommendations": recommendations,
            "analyzed_at": datetime.utcnow().isoformat() + "Z"
        }
