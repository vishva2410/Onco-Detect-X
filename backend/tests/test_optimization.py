import unittest
import asyncio
from unittest.mock import MagicMock, patch
from app.services.perception import PerceptionService
from app.services.cognitive import CognitiveService
from app.models.schemas import LLMInput

class TestOptimization(unittest.IsolatedAsyncioTestCase):
    def test_perception_determinism(self):
        service = PerceptionService()
        img_data = b"fake_image_content"

        r1 = service.predict(img_data, "lung")
        r2 = service.predict(img_data, "lung")

        # This is expected to fail before optimization
        self.assertEqual(r1.confidence, r2.confidence, "Perception service should be deterministic")
        self.assertEqual(r1.prediction, r2.prediction, "Perception service should be deterministic")

    async def test_cognitive_caching(self):
        service = CognitiveService()
        # Mock the model to track calls
        service.model = MagicMock()

        async def mock_generate(*args, **kwargs):
            await asyncio.sleep(0.01) # Simulate delay
            mock_response = MagicMock()
            mock_response.text = '{"triage_level": "Low", "risk_adjustment": 0, "explanation": "test", "recommendation": "test"}'
            return mock_response

        service.model.generate_content_async = MagicMock(side_effect=mock_generate)

        input_data = LLMInput(
            cancer_type="Lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["cough"],
            age=60,
            risk_factors=["smoking"]
        )

        # First call
        await service.analyze(input_data)

        # Second call (same input)
        await service.analyze(input_data)

        # Should be called only once if cached
        # This is expected to fail (called twice) before optimization
        self.assertEqual(service.model.generate_content_async.call_count, 1, "Cognitive service should use caching")

if __name__ == "__main__":
    unittest.main()
