import unittest
from unittest.mock import MagicMock, patch
from app.services.cognitive import CognitiveService
from app.models.schemas import LLMInput

class TestCognitiveCache(unittest.IsolatedAsyncioTestCase):
    @patch('app.services.cognitive.genai.GenerativeModel')
    async def test_analyze_caching(self, mock_model_class):
        # Setup mock
        mock_model_instance = MagicMock()
        async def mock_generate(*args, **kwargs):
            mock_response = MagicMock()
            mock_response.text = '{"triage_level": "Low", "risk_adjustment": 0, "explanation": "test", "recommendation": "test"}'
            return mock_response

        mock_model_instance.generate_content_async = MagicMock(side_effect=mock_generate)

        # Inject mock
        service = CognitiveService()
        service.model = mock_model_instance
        # Clear any existing cache if implemented later (though for this test, it's a fresh instance)
        if hasattr(service, '_cache'):
            service._cache.clear()

        # Create dummy input
        llm_input = LLMInput(
            cancer_type="Lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["cough"],
            age=60,
            risk_factors=["smoking"]
        )

        # First call
        await service.analyze(llm_input)

        # Second call (same input)
        await service.analyze(llm_input)

        # Verify call count. Should be 1 if cached, but currently expecting failure (will be 2)
        mock_model_instance.generate_content_async.assert_called_once()

if __name__ == "__main__":
    unittest.main()
