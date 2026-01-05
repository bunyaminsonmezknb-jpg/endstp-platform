# app/api/v1/endpoints/segmentation.py (YENİ DOSYA)
"""
Segmentation Engine API Endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
from app.core.segmentation_engine import get_segmentation_engine

router = APIRouter()

@router.get("/segment/{user_id}")
async def get_user_segment(
    user_id: str,
    window_days: Optional[int] = 14
):
    """
    Get student segment level
    
    Example:
        GET /api/v1/segmentation/segment/user-123?window_days=14
    """
    try:
        engine = get_segmentation_engine()
        segment = engine.get_segment(user_id, window_days)
        
        return {
            "status": "success",
            "user_id": user_id,
            "segment": segment
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test-segments")
async def test_segment_scenarios():
    """
    Test different segment scenarios with mock data
    """
    # Mock test scenarios
    scenarios = [
        {
            "name": "Cold Start",
            "user_id": "test-cold-start",
            "expected": "L1"
        },
        {
            "name": "Struggling",
            "user_id": "test-struggling",
            "expected": "L2"
        },
        {
            "name": "Average",
            "user_id": "test-average",
            "expected": "L4"
        },
        {
            "name": "Elite",
            "user_id": "test-elite",
            "expected": "L7"
        }
    ]
    
    engine = get_segmentation_engine()
    results = []
    
    for scenario in scenarios:
        segment = engine.get_segment(scenario["user_id"])
        results.append({
            "scenario": scenario["name"],
            "user_id": scenario["user_id"],
            "expected_level": scenario["expected"],
            "actual_level": segment["level"],
            "score": segment["score"],
            "confidence": segment["confidence"]
        })
    
    return {
        "status": "success",
        "test_count": len(scenarios),
        "results": results
    }