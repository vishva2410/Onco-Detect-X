import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
import json
from app.services.cognitive import CognitiveService
from app.models.schemas import LLMInput

class TestCognitiveAsync(unittest.TestCase):
    def setUp(self):
        # Patch the environment variable to avoid real API configuration during init
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'dummy_key'}):
            with patch('google.generativeai.configure'):
                with patch('google.generativeai.GenerativeModel'):
                    self.service = CognitiveService()

        # Mock the model and its async method
        self.service.model = MagicMock()
        self.service.model.generate_content_async = AsyncMock()

    def test_analyze_async_and_caching(self):
        # Create a sample input
        llm_input = LLMInput(
            cancer_type="lung",
            ml_confidence=0.9,
            preliminary_cri=80,
            symptoms=["cough", "shortness of breath"],
            age=65,
            risk_factors=["smoker"]
        )

        # Mock return value
        mock_response = MagicMock()
        mock_response.text = '{"triage_level": "High", "risk_adjustment": 5, "explanation": "Test explanation", "recommendation": "Test recommendation"}'
        self.service.model.generate_content_async.return_value = mock_response

        # Run async test
        async def run_test():
            # First call - should hit mock
            print("First call...")
            result1 = await self.service.analyze(llm_input)

            # Second call with same input - should use cache
            print("Second call...")
            result2 = await self.service.analyze(llm_input)

            # Third call with DIFFERENT input order in lists (should be same key)
            llm_input_reordered = LLMInput(
                cancer_type="lung",
                ml_confidence=0.9,
                preliminary_cri=80,
                symptoms=["shortness of breath", "cough"], # Reordered
                age=65,
                risk_factors=["smoker"]
            )
            print("Third call (reordered)...")
            result3 = await self.service.analyze(llm_input_reordered)

            return result1, result2, result3

        # Execute the async function
        try:
            result1, result2, result3 = asyncio.run(run_test())
        except AttributeError as e:
            self.fail(f"Method 'analyze' is likely not async yet: {e}")
        except TypeError as e:
            self.fail(f"Method 'analyze' signature mismatch or not awaitable: {e}")

        self.assertEqual(result1.triage_level, "High")
        self.assertEqual(result2.triage_level, "High")
        self.assertEqual(result3.triage_level, "High")

        # Verify generate_content_async was called ONLY ONCE
        # This confirms both caching works and key generation is stable (sorted lists)
        self.service.model.generate_content_async.assert_called_once()

if __name__ == '__main__':
    unittest.main()
