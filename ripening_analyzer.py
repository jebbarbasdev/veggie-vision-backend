from typing import Tuple, Literal
from models import AmbientData
from openai import OpenAI
from config import OPENAI_API_KEY
import json

class RipeningAnalyzer:
    """Ripening analyzer that uses ChatGPT to predict ripening times based on ambient conditions."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def _get_chatgpt_prediction(self, prediction: str, ambient_data: AmbientData) -> dict:
        """
        Get ripening prediction from ChatGPT.
        
        Args:
            prediction: The produce prediction (e.g., 'unripe_banana')
            ambient_data: Current temperature and humidity readings
            
        Returns:
            Dictionary with ripening prediction data
        """
        prompt = f"""You are an expert in produce ripening analysis. Given the following information:
        - Produce: {prediction}
        - Current temperature: {ambient_data.temperature}°C
        - Current humidity: {ambient_data.humidity}%
        
        Please analyze and return ONLY a JSON object with the following structure:
        {{
            "category": "fruit" or "vegetable",
            "ripes_in_days": number of days until ripe (0 if already ripe/rotten),
            "spoils_in_days": number of days until spoiled (0 if already spoiled),
            "explanation": "brief explanation of the prediction"
        }}
        
        Consider that:
        - Temperature affects ripening speed (higher = faster)
        - Humidity affects spoilage (higher = faster spoilage)
        - Different fruits/vegetables have different ripening patterns
        - Return only the JSON, no other text
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You are a produce ripening expert that returns only JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={ "type": "json_object" }
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Error getting ChatGPT prediction: {e}")
            # Fallback to safe default values
            return {
                "category": "fruit",
                "ripes_in_days": 3,
                "spoils_in_days": 7,
                "explanation": "Using fallback values due to API error"
            }
    
    def analyze_ripening_with_ambient_data(
        self, 
        prediction: str, 
        ambient_data: AmbientData
    ) -> Tuple[Literal["fruit", "vegetable"], int, int]:
        """
        Analyze ripening status based on prediction and ambient data using ChatGPT.
        
        Args:
            prediction: The produce prediction (e.g., 'unripe_banana')
            ambient_data: Current temperature and humidity readings
            
        Returns:
            Tuple of (category, days_until_ripe, days_until_spoil)
        """
        # Get prediction from ChatGPT
        result = self._get_chatgpt_prediction(prediction, ambient_data)
        
        # Extract values from result
        category: Literal["fruit", "vegetable"] = result["category"]
        ripes_in_days = result["ripes_in_days"]
        spoils_in_days = result["spoils_in_days"]
        
        # Log the explanation for debugging
        print(f"ChatGPT prediction explanation: {result['explanation']}")
            
        return category, ripes_in_days, spoils_in_days

# Create a singleton instance
ripening_analyzer = RipeningAnalyzer() 