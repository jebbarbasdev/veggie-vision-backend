from typing import Tuple, Literal
import random
from models import AmbientData

class RipeningAnalyzer:
    """Dummy ripening analyzer that returns random predictions based on ambient conditions."""
    
    def analyze_ripening_with_ambient_data(
        self, 
        prediction: str, 
        ambient_data: AmbientData
    ) -> Tuple[Literal["fruit", "vegetable"], int, int]:
        """
        Analyze ripening status based on prediction and ambient data.
        Currently returns random values for testing.
        
        Args:
            prediction: The produce prediction (e.g., 'unripe_banana')
            ambient_data: Current temperature and humidity readings
            
        Returns:
            Tuple of (category, days_until_ripe, days_until_spoil)
        """
        # Extract produce type and ripeness from prediction
        ripeness, produce = prediction.split('_')
        
        # Determine category
        category: Literal["fruit", "vegetable"] = "fruit" if produce in [
            "banana", "avocado", "mango", "strawberry"
        ] else "vegetable"
        
        # Generate random days based on ripeness state
        if ripeness == "rotten":
            ripes_in_days = 0
            spoils_in_days = random.randint(1, 2)
        elif ripeness == "ripe":
            ripes_in_days = 0
            spoils_in_days = random.randint(3, 7)
        else:  # unripe
            ripes_in_days = random.randint(2, 5)
            spoils_in_days = ripes_in_days + random.randint(3, 7)
            
        return category, ripes_in_days, spoils_in_days

# Create a singleton instance
ripening_analyzer = RipeningAnalyzer() 