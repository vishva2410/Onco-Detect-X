import unittest
from unittest.mock import MagicMock, patch
from app.services.cognitive import CognitiveService
from app.models.schemas import LLMInput, LLMOutput

class TestCognitiveCaching(unittest.IsolatedAsyncioTestCase):
    async def test_analyze_caching_behavior(self):
        # Setup service and mock model
        service = CognitiveService()
        service.model = MagicMock()

        # Mock the async generation method
        async def mock_generate(*args, **kwargs):
            mock_response = MagicMock()
            mock_response.text = '{"triage_level": "Low", "risk_adjustment": 0, "explanation": "Cached result", "recommendation": "None"}'
            return mock_response

        service.model.generate_content_async = MagicMock(side_effect=mock_generate)

        # Create input
        llm_input = LLMInput(
            cancer_type="Lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["cough"],
            age=60,
            risk_factors=["smoking"]
        )

        # First call
        result1 = await service.analyze(llm_input)

        # Second call with SAME input
        result2 = await service.analyze(llm_input)

        # Verify results are same
        self.assertEqual(result1.explanation, "Cached result")
        self.assertEqual(result2.explanation, "Cached result")

        # Verify that the underlying API was called ONLY ONCE
        service.model.generate_content_async.assert_called_once()

if __name__ == "__main__":
    unittest.main()
