import random
from typing import Tuple
from fastapi import UploadFile

class ImageAnalyzer:
    """Dummy image analyzer that returns random predictions."""
    
    # Valid predictions for our dummy system
    VALID_PREDICTIONS = [
        "unripe_banana", "ripe_banana", "rotten_banana",
        "unripe_avocado", "ripe_avocado", "rotten_avocado",
        "unripe_tomato", "ripe_tomato", "rotten_tomato",
        "unripe_mango", "ripe_mango", "rotten_mango",
        "unripe_strawberry", "ripe_strawberry", "rotten_strawberry"
    ]

    async def analyze_image(self, file: UploadFile) -> Tuple[str, float]:
        """
        Analyze an image and return prediction and confidence.
        Currently returns random values for testing.
        
        Args:
            file: The uploaded image file
            
        Returns:
            Tuple of (prediction, confidence)
        """
        # In a real implementation, this would:
        # 1. Read the image file
        # 2. Process it through a ML model
        # 3. Return actual predictions
        
        # For now, return random values
        prediction = random.choice(self.VALID_PREDICTIONS)
        confidence = round(random.uniform(85.0, 99.9), 2)
        
        return prediction, confidence

# Create a singleton instance
image_analyzer = ImageAnalyzer() 