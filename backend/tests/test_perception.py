import unittest
from app.services.perception import perception_service

class TestPerceptionService(unittest.TestCase):
    def test_predict_determinism(self):
        """
        Verify that PerceptionService.predict returns the same result for the same input image.
        This is crucial for CognitiveService caching to work effectively.
        """
        # Create dummy image data
        image_data = b"fake_image_bytes_for_testing_determinism" * 10
        cancer_type = "lung"

        # First call
        result1 = perception_service.predict(image_data, cancer_type)

        # Second call with SAME data
        result2 = perception_service.predict(image_data, cancer_type)

        # Verify results are identical
        self.assertEqual(result1.prediction, result2.prediction,
                         f"Prediction mismatch: {result1.prediction} vs {result2.prediction}")
        self.assertEqual(result1.confidence, result2.confidence,
                         f"Confidence mismatch: {result1.confidence} vs {result2.confidence}")

if __name__ == "__main__":
    unittest.main()
