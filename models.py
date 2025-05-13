from pydantic import BaseModel, Field
from typing import Optional

class AmbientData(BaseModel):
    """Model for ambient data with temperature and humidity readings."""
    temperature: int = Field(..., description="Temperature value")
    humidity: int = Field(..., description="Humidity value")

    @classmethod
    def from_spanish(cls, data: dict) -> "AmbientData":
        """Convert Spanish field names to English."""
        return cls(
            temperature=data["temperatura"],
            humidity=data["humedad"]
        )

class RipeningAnalysis(BaseModel):
    """Model for ripening analysis response."""
    days_to_ripe: Optional[int] = Field(
        None,
        description="Number of days until the produce is ripe. Null if already ripe.",
        ge=0
    )
    days_to_spoil: Optional[int] = Field(
        None,
        description="Number of days until the produce spoils. Null if already spoiled.",
        ge=0
    )

class PredictionRequest(BaseModel):
    """Model for ripening prediction request."""
    prediction: str = Field(..., description="Model prediction (e.g., 'ripe_banana')")
    temperature: int = Field(..., description="Current temperature in Celsius")
    humidity: int = Field(..., description="Current humidity percentage")

    class Config:
        populate_by_name = True 