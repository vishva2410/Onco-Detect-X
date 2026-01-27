import json
import os
from typing import List, Optional

class HospitalService:
    def __init__(self, data_path: str = "backend/data/hospitals.json"):
        self.data_path = data_path
        self.hospitals = self._load_data()

    def _load_data(self):
        try:
            with open(self.data_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading hospital data: {e}")
            return []

    def recommend(self, cancer_type: str) -> Optional[str]:
        # Filter by specialty
        candidates = [h for h in self.hospitals if cancer_type in h.get("specialties", []) or "general" in h.get("specialties", [])]
        
        if not candidates:
            return "No specific hospital recommendation found nearby."
            
        # Sort by distance (mock logic)
        candidates.sort(key=lambda x: x.get("distance_km", 999))
        
        best = candidates[0]
        return f"Recommended: {best['name']} ({best['distance_km']} km away) - Specialized in {cancer_type}."

hospital_service = HospitalService()
