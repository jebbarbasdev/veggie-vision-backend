from pydantic import BaseModel, Field
from typing import Literal

class AmbientData(BaseModel):
    """Model for ambient data with temperature and humidity readings."""
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Humidity percentage")

    @classmethod
    def from_spanish(cls, data: dict) -> "AmbientData":
        """
        Create AmbientData from Spanish field names.
        
        Args:
            data: Dictionary with 'temperatura' and 'humedad' fields
            
        Returns:
            AmbientData instance with English field names
        """
        return cls(
            temperature=float(data["temperatura"]),
            humidity=float(data["humedad"])
        )

class AnalysisResponse(BaseModel):
    """Model for the analysis endpoint response."""
    prediction: str = Field(..., description="Predicted produce and ripeness state (e.g., 'unripe_banana')")
    confidence: float = Field(..., ge=0, le=100, description="Confidence score of the prediction (0-100)")
    temperature: float = Field(..., description="Current temperature in Celsius")
    humidity: float = Field(..., description="Current humidity percentage")
    category: Literal["fruit", "vegetable"] = Field(..., description="Category of the produce")
    ripes_in_days: int = Field(..., ge=0, description="Estimated days until ripe")
    spoils_in_days: int = Field(..., ge=0, description="Estimated days until spoiled") 