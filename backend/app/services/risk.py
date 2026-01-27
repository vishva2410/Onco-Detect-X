from app.models.schemas import PatientInput, PerceptionOutput

class RiskService:
    def calculate_preliminary_cri(self, input_data: PatientInput, perception: PerceptionOutput) -> int:
        """
        Calculates the preliminary Cancer Risk Index (CRI) based on deterministic logic.
        Formula:
        - ML Confidence: 60%
        - Symptom Severity: 30%
        - Risk Factors: 10%
        """
        
        # 1. ML Contribution (0-60)
        # Only count if prediction is "suspected" or "inconclusive"
        ml_score = 0
        if perception.prediction in ["suspected", "inconclusive"]:
             ml_score = perception.confidence * 60
        
        # 2. Symptom Score (0-30)
        # Simple heyristic: 5 points per symptom, max 30
        symptom_score = min(len(input_data.symptoms) * 5, 30)
        
        # 3. Risk Factor Score (0-10)
        # 5 points per risk factor, max 10
        risk_score = min(len(input_data.risk_factors) * 5, 10)
        
        total_cri = round(ml_score + symptom_score + risk_score)
        return min(total_cri, 100) # Cap at 100

risk_service = RiskService()
