import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from typing import Tuple, Dict
from fastapi import UploadFile
import io

class ImageAnalyzer:
    """Image analyzer that uses a trained model to classify produce images."""
    
    # Class names mapping from model
    CLASS_NAMES: Dict[int, str] = {
        0: 'avocado_ripe', 1: 'avocado_rotten', 2: 'avocado_unripe',
        3: 'banana_ripe', 4: 'banana_rotten', 5: 'banana_unripe',
        6: 'mango_ripe', 7: 'mango_rotten', 8: 'mango_unripe',
        9: 'strawberry_ripe', 10: 'strawberry_rotten', 11: 'strawberry_unripe',
        12: 'tomato_ripe', 13: 'tomato_rotten', 14: 'tomato_unripe'
    }

    def __init__(self):
        """Initialize the analyzer by loading the trained model."""
        try:
            self.model = load_model('veggie-vision-model.h5')
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess the image for model input.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image as numpy array
        """
        # Resize image to match model's expected input size
        target_size = (224, 224)  # Ajusta esto al tamaño que espera tu modelo
        image = image.resize(target_size)
        
        # Convert to numpy array and normalize
        img_array = np.array(image) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array

    async def analyze_image(self, file: UploadFile) -> Tuple[str, float]:
        """
        Analyze an image using the trained model and return prediction and confidence.
        
        Args:
            file: The uploaded image file
            
        Returns:
            Tuple of (prediction, confidence)
        """
        try:
            # Read and decode the image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Preprocess the image
            processed_image = self._preprocess_image(image)
            
            # Get model prediction
            predictions = self.model.predict(processed_image)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class] * 100)
            
            # Get the class name from our mapping
            prediction = self.CLASS_NAMES[predicted_class]
            
            return prediction, round(confidence, 2)
            
        except Exception as e:
            print(f"Error analyzing image: {e}")
            raise

# Create a singleton instance
image_analyzer = ImageAnalyzer() 