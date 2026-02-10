import unittest
from unittest.mock import MagicMock
from app.services.cognitive import CognitiveService
from app.models.schemas import LLMInput

class TestCognitiveCachingOrder(unittest.IsolatedAsyncioTestCase):
    async def test_analyze_caching_order_independence(self):
        # Setup service and mock model
        service = CognitiveService()
        service.model = MagicMock()

        # Mock the async generation method
        async def mock_generate(*args, **kwargs):
            mock_response = MagicMock()
            mock_response.text = '{"triage_level": "Low", "risk_adjustment": 0, "explanation": "Cached result", "recommendation": "None"}'
            return mock_response

        service.model.generate_content_async = MagicMock(side_effect=mock_generate)

        # Create inputs with DIFFERENT order of list fields
        llm_input1 = LLMInput(
            cancer_type="Lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["cough", "fatigue"],
            age=60,
            risk_factors=["smoking", "hypertension"]
        )

        llm_input2 = LLMInput(
            cancer_type="Lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["fatigue", "cough"], # Swapped order
            age=60,
            risk_factors=["hypertension", "smoking"] # Swapped order
        )

        # First call
        await service.analyze(llm_input1)

        # Second call with SEMANTICALLY SAME input
        await service.analyze(llm_input2)

        # Verify that the underlying API was called ONLY ONCE
        # If caching is working correctly regardless of order, this should be 1.
        # Currently, it will be 2 (failure).
        service.model.generate_content_async.assert_called_once()

if __name__ == "__main__":
    unittest.main()
