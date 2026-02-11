import asyncio
import inspect
import sys
import unittest
from unittest.mock import MagicMock, patch
from app.services.cognitive import CognitiveService, cognitive_service
from app.models.schemas import LLMInput

class TestCognitiveAsync(unittest.IsolatedAsyncioTestCase):
    async def test_analyze_is_async(self):
        # Check if the method is defined as async
        is_async = inspect.iscoroutinefunction(cognitive_service.analyze)
        self.assertTrue(is_async, "analyze method should be async")

    @patch('app.services.cognitive.genai.GenerativeModel')
    async def test_analyze_calls_async_generate(self, mock_model_class):
        # Setup mock
        mock_model_instance = MagicMock()
        # Mock generate_content_async to return a future/coroutine
        async def mock_generate(*args, **kwargs):
            mock_response = MagicMock()
            mock_response.text = '{"triage_level": "Low", "risk_adjustment": 0, "explanation": "test", "recommendation": "test"}'
            return mock_response

        mock_model_instance.generate_content_async = MagicMock(side_effect=mock_generate)

        # Inject mock
        service = CognitiveService()
        service.model = mock_model_instance

        # Create dummy input
        llm_input = LLMInput(
            cancer_type="Lung",
            ml_confidence=0.8,
            preliminary_cri=50,
            symptoms=["cough"],
            age=60,
            risk_factors=["smoking"]
        )

        # Run analyze
        result = await service.analyze(llm_input)

        # Verify call
        mock_model_instance.generate_content_async.assert_called_once()
        self.assertEqual(result.triage_level, "Low")

if __name__ == "__main__":
    unittest.main()
