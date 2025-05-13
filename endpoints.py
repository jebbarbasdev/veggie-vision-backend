from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from mqtt_client import mqtt_client_instance
from image_analyzer import image_analyzer
from ripening_analyzer import ripening_analyzer
from models import AmbientData, AnalysisResponse

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
    "/analysis",
    response_model=AnalysisResponse,
    summary="Analyze produce image",
    description="Analyze a produce image and return prediction, confidence, and ripening analysis. Combines image analysis with current ambient conditions."
)
async def analyze_produce(
    file: UploadFile = File(...),
    user_id: str = Form(...)
) -> AnalysisResponse:
    """
    Analyze a produce image and return comprehensive analysis.
    
    Args:
        file: The image file to analyze
        user_id: Firebase user ID (not used in current implementation)
        
    Returns:
        AnalysisResponse with prediction, confidence, and ripening analysis
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # 1. Analyze image
        prediction, confidence = await image_analyzer.analyze_image(file)
        
        # 2. Get ambient data
        ambient_data = get_ambient()
        
        # 3. Analyze ripening
        category, ripes_in_days, spoils_in_days = ripening_analyzer.analyze_ripening_with_ambient_data(
            prediction, ambient_data
        )
        
        # 4. Combine all data
        return AnalysisResponse(
            prediction=prediction,
            confidence=confidence,
            temperature=ambient_data.temperature,
            humidity=ambient_data.humidity,
            category=category,
            ripes_in_days=ripes_in_days,
            spoils_in_days=spoils_in_days
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze produce: {str(e)}"
        ) 