import unittest
from unittest.mock import MagicMock, patch
import json
import random
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.perception import perception_service
from app.services.cognitive import cognitive_service, CognitiveService
from app.models.schemas import LLMInput

class TestPerformance(unittest.TestCase):
    def test_perception_determinism(self):
        """
        Verify that PerceptionService is deterministic.
        """
        image_data = b"fake_image_data_12345"
        cancer_type = "brain"

        # Call 1
        result1 = perception_service.predict(image_data, cancer_type)

        # Call 2
        result2 = perception_service.predict(image_data, cancer_type)

        print(f"\n[Perception] Run 1: {result1.confidence}, Run 2: {result2.confidence}")

        self.assertEqual(result1.confidence, result2.confidence, "Perception confidence should be deterministic")
        self.assertEqual(result1.prediction, result2.prediction, "Perception prediction should be deterministic")

    @patch('app.services.cognitive.genai.GenerativeModel')
    def test_cognitive_caching(self, mock_model_cls):
        """
        Verify that CognitiveService caches results.
        """
        # Setup mock
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = json.dumps({
            "triage_level": "Moderate",
            "risk_adjustment": 0,
            "explanation": "Mock explanation",
            "recommendation": "Mock recommendation"
        })

        # Create a fresh instance to avoid side effects from other tests
        # We need to inject the mock model
        service = CognitiveService()
        service.model = mock_model

        input_data = LLMInput(
            cancer_type="brain",
            ml_confidence=0.85,
            preliminary_cri=60,
            symptoms=["headache"],
            age=45,
            risk_factors=["smoking"]
        )

        # Call 1
        service.analyze(input_data)

        # Call 2
        service.analyze(input_data)

        print(f"\n[Cognitive] API Calls: {mock_model.generate_content.call_count}")

        self.assertEqual(mock_model.generate_content.call_count, 1, "Should hit cache on second call")

if __name__ == '__main__':
    unittest.main()
