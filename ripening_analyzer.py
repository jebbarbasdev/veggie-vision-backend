from typing import Optional, Dict, Any
import openai
from config import OPENAI_API_KEY
from models import RipeningAnalysis, PredictionRequest

class RipeningAnalyzer:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self._setup_prompt_template()

    def _setup_prompt_template(self):
        """Setup the prompt template for GPT analysis."""
        self.prompt_template = """
        Analyze the ripening status of {prediction} under the following conditions:
        - Temperature: {temperature}°C
        - Humidity: {humidity}%

        Return a JSON object with:
        1. days_to_ripe: number of days until ripe (null if already ripe)
        2. days_to_spoil: number of days until spoiled (null if already spoiled)

        Consider:
        - Optimal ripening conditions
        - Current environmental conditions
        - Typical ripening and spoilage times
        - Impact of temperature and humidity on ripening

        Return ONLY the JSON object, no additional text.
        """

    def _create_prompt(self, request: PredictionRequest) -> str:
        """Create the prompt for GPT analysis."""
        return self.prompt_template.format(
            prediction=request.prediction,
            temperature=request.temperature,
            humidity=request.humidity
        )

    def analyze_ripening(self, request: PredictionRequest) -> RipeningAnalysis:
        """
        Analyze ripening status using GPT.
        
        Args:
            request: PredictionRequest with prediction and environmental data
            
        Returns:
            RipeningAnalysis with days to ripe and spoil
            
        Raises:
            Exception: If GPT analysis fails
        """
        try:
            prompt = self._create_prompt(request)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in produce ripening analysis. Provide only JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            # Extract and parse the JSON response
            analysis_text = response.choices[0].message.content.strip()
            analysis_dict = eval(analysis_text)  # Convert string to dict
            
            return RipeningAnalysis(**analysis_dict)
            
        except Exception as e:
            raise Exception(f"Failed to analyze ripening: {str(e)}")

# Create a singleton instance
ripening_analyzer = RipeningAnalyzer() 