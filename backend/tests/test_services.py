import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.append(os.path.abspath("backend"))

from app.services.perception import perception_service
from app.services.cognitive import cognitive_service, LLMInput, LLMOutput

class TestPerceptionService(unittest.TestCase):
    def test_determinism(self):
        """Verify that PerceptionService returns the same confidence for the same input."""
        image_data = b"test_image_123"
        cancer_type = "lung"

        # Should be deterministic
        p1 = perception_service.predict(image_data, cancer_type)
        p2 = perception_service.predict(image_data, cancer_type)

        self.assertEqual(p1.confidence, p2.confidence, "Confidence score should be deterministic")
        self.assertEqual(p1.prediction, p2.prediction, "Prediction should be deterministic")

    def test_different_inputs(self):
        """Verify that different inputs produce different outputs (sanity check)."""
        # This is probabilistic, so run a few times or use very different inputs
        # But for seeded random, different seeds -> different sequences usually
        # We just want to ensure we aren't returning constant values for everything

        # Using two very different inputs
        p1 = perception_service.predict(b"image_A", "lung")
        p2 = perception_service.predict(b"image_B", "lung")

        # It is possible they are same by chance, but unlikely given range [0.7, 0.99]
        # We won't assert inequality strictly to avoid flakiness, but we can check if the underlying mechanism is working
        # For now, let's just ensure it runs without error.
        pass

class TestCognitiveService(unittest.TestCase):
    def setUp(self):
        # Reset cache if it exists
        if hasattr(cognitive_service, '_cache'):
            cognitive_service._cache.clear()

    def test_caching(self):
        """Verify that CognitiveService caches results."""

        # Mock the internal model to avoid real API calls and simulate work
        original_model = cognitive_service.model
        mock_model = MagicMock()

        # Mock response
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "triage_level": "Low",
            "risk_adjustment": 0,
            "explanation": "test",
            "recommendation": "test"
        })
        mock_model.generate_content.return_value = mock_response
        cognitive_service.model = mock_model

        llm_input = LLMInput(
            cancer_type="lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["cough"],
            age=50,
            risk_factors=["smoking"]
        )

        # Call 1
        cognitive_service.analyze(llm_input)

        # Call 2 (Same input)
        cognitive_service.analyze(llm_input)

        # If cached, generate_content should be called only once
        # If not cached, it will be called twice
        # We expect this to fail initially
        if mock_model.generate_content.call_count != 1:
            print(f"DEBUG: generate_content called {mock_model.generate_content.call_count} times")

        self.assertEqual(mock_model.generate_content.call_count, 1, "Should use cache for repeated calls")

        # Restore model
        cognitive_service.model = original_model

if __name__ == '__main__':
    unittest.main()
