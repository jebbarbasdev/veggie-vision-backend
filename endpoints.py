from fastapi import APIRouter, HTTPException
from mqtt_client import mqtt_client_instance
from ripening_analyzer import ripening_analyzer
from models import AmbientData, PredictionRequest, RipeningAnalysis

router = APIRouter()

def get_ambient() -> AmbientData:
    """
    Returns the latest ambient data from the MQTT topic.
    Converts the Spanish field names (temperatura, humedad) to English (temperature, humidity).
    """
    latest_data = mqtt_client_instance.get_latest_data()
    if latest_data is None:
        raise HTTPException(
            status_code=404,
            detail="No ambient data available yet. Please wait for MQTT messages."
        )
    
    try:
        return AmbientData.from_spanish(latest_data)
    except (ValueError, TypeError, KeyError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing ambient data: {str(e)}"
        )

@router.get(
    "/ambient",
    response_model=AmbientData,
    summary="Get latest ambient readings",
    description="Retrieve the most recent ambient data from the MQTT topic."
)
async def ambient_endpoint() -> AmbientData:
    """
    Get the latest ambient data from the MQTT topic.
    Returns temperature and humidity values in English, regardless of the input language.
    """
    return get_ambient()

@router.post(
    "/analyze-ripening",
    response_model=RipeningAnalysis,
    summary="Analyze produce ripening",
    description="""
    Analyze the ripening status of produce based on current conditions.
    Uses GPT to predict days until ripe and spoiled.
    """
)
async def analyze_ripening(request: PredictionRequest) -> RipeningAnalysis:
    """
    Analyze ripening status of produce using current conditions.
    
    Args:
        request: Prediction and current environmental conditions
        
    Returns:
        Analysis of days until ripe and spoiled
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        return ripening_analyzer.analyze_ripening(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze ripening: {str(e)}"
        ) 