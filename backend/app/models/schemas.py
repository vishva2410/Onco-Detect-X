from pydantic import BaseModel, Field
from typing import List, Optional

class PatientInput(BaseModel):
    cancer_type: str = Field(..., description="Type of cancer suspected (e.g., brain, lung, breast)")
    age: int = Field(..., ge=0, le=120, description="Patient age")
    symptoms: List[str] = Field(..., description="List of reported symptoms")
    risk_factors: List[str] = Field(..., description="List of patient risk factors")

class PerceptionOutput(BaseModel):
    prediction: str = Field(..., description="Predicted class from ML model")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the prediction")

class LLMInput(BaseModel):
    cancer_type: str
    ml_confidence: float
    preliminary_cri: int
    symptoms: List[str]
    age: int
    risk_factors: List[str]

class LLMOutput(BaseModel):
    triage_level: str = Field(..., description="Low, Moderate, High, or Critical")
    risk_adjustment: int = Field(..., ge=-10, le=10, description="Adjustment score from -10 to +10")
    explanation: str = Field(..., description="Reasoning for the triage level")
    recommendation: str = Field(..., description="Suggested next steps")

class FinalResult(BaseModel):
    cancer_type: str
    ml_confidence: float
    preliminary_cri: int
    final_cri: int
    triage_level: str
    explanation: str
    recommendation: str
    hospital_recommendation: Optional[str] = None
