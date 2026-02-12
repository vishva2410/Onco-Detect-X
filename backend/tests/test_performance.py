import unittest
import sys
import os
import json
import time
from unittest.mock import MagicMock, patch

# Add backend to path if running from root
if os.path.abspath("backend") not in sys.path:
    sys.path.append(os.path.abspath("backend"))

from app.services.perception import perception_service
from app.services.cognitive import cognitive_service, LLMInput, LLMOutput

class TestPerformance(unittest.TestCase):

    def test_perception_service_determinism(self):
        """Test that PerceptionService returns the same output for the same input."""
        image_data = b"deterministic_test_image_123"
        cancer_type = "lung"

        p1 = perception_service.predict(image_data, cancer_type)
        p2 = perception_service.predict(image_data, cancer_type)

        self.assertEqual(p1.confidence, p2.confidence, "PerceptionService confidence should be deterministic")
        self.assertEqual(p1.prediction, p2.prediction, "PerceptionService prediction should be deterministic")

    def test_cognitive_service_caching(self):
        """Test that CognitiveService caches responses for identical inputs."""

        # Prepare input
        input_data = LLMInput(
            cancer_type="lung",
            ml_confidence=0.85,
            preliminary_cri=75,
            symptoms=["cough", "fatigue"],
            age=45,
            risk_factors=["smoker"]
        )

        # Mock the model to track calls
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "triage_level": "High",
            "risk_adjustment": 5,
            "explanation": "Test explanation",
            "recommendation": "Test recommendation"
        })
        mock_model.generate_content.return_value = mock_response

        # Backup original model
        original_model = cognitive_service.model
        cognitive_service.model = mock_model

        try:
            # Clear cache if implemented
            if hasattr(cognitive_service, 'cache'):
                cognitive_service.cache.clear()

            # First call
            cognitive_service.analyze(input_data)

            # Second call with same input
            cognitive_service.analyze(input_data)

            # Third call with different input (different symptom order)
            input_data_reordered = LLMInput(
                cancer_type="lung",
                ml_confidence=0.85,
                preliminary_cri=75,
                symptoms=["fatigue", "cough"], # Reordered
                age=45,
                risk_factors=["smoker"]
            )
            cognitive_service.analyze(input_data_reordered)

            # Assertions
            # With caching: generate_content should be called ONCE.
            self.assertEqual(mock_model.generate_content.call_count, 1, "LLM should be called only once for identical/equivalent inputs")

        finally:
            cognitive_service.model = original_model

if __name__ == '__main__':
    unittest.main()
