import unittest
from unittest.mock import AsyncMock, MagicMock
from app.services.cognitive import CognitiveService
from app.models.schemas import LLMInput, LLMOutput

class TestCognitiveOrdering(unittest.IsolatedAsyncioTestCase):
    async def test_cache_order_independence(self):
        # Setup service and mock model
        service = CognitiveService()
        service.model = MagicMock()

        # Mock the async generation method using AsyncMock for awaitable
        service.model.generate_content_async = AsyncMock()
        mock_response = MagicMock()
        mock_response.text = '{"triage_level": "Low", "risk_adjustment": 0, "explanation": "Cached result", "recommendation": "None"}'
        service.model.generate_content_async.return_value = mock_response

        # Create input 1
        llm_input1 = LLMInput(
            cancer_type="Lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["cough", "fever"],
            age=60,
            risk_factors=["smoking", "obesity"]
        )

        # Create input 2 (same data, different order in lists)
        llm_input2 = LLMInput(
            cancer_type="Lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["fever", "cough"],
            age=60,
            risk_factors=["obesity", "smoking"]
        )

        # First call
        await service.analyze(llm_input1)

        # Second call
        await service.analyze(llm_input2)

        # Verify that the underlying API was called ONLY ONCE
        # Without optimization, this assertion will FAIL (called twice)
        service.model.generate_content_async.assert_called_once()

if __name__ == "__main__":
    unittest.main()
