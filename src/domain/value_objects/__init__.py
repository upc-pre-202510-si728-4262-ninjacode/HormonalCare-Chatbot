from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

class RiskLevel(Enum):
    """Nivel de riesgo médico"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class RecommendationType(Enum):
    """Tipo de recomendación"""
    DIETARY = "dietary"
    EXERCISE = "exercise"
    MEDICATION = "medication"
    MEDICAL_CONSULTATION = "medical_consultation"
    LIFESTYLE = "lifestyle"

@dataclass(frozen=True)
class BloodTestAnalysis:
    """Análisis de examen de sangre - Value Object"""
    overall_risk: RiskLevel
    glucose_status: str
    cholesterol_status: str
    kidney_function_status: str
    blood_count_status: str
    recommendations: list
    needs_doctor_consultation: bool
    risk_factors: list
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'overall_risk': self.overall_risk.value,
            'glucose_status': self.glucose_status,
            'cholesterol_status': self.cholesterol_status,
            'kidney_function_status': self.kidney_function_status,
            'blood_count_status': self.blood_count_status,
            'recommendations': self.recommendations,
            'needs_doctor_consultation': self.needs_doctor_consultation,
            'risk_factors': self.risk_factors
        }

@dataclass(frozen=True)
class Recommendation:
    """Recomendación médica - Value Object"""
    type: RecommendationType
    title: str
    description: str
    priority: int  # 1-5, siendo 5 la máxima prioridad
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type.value,
            'title': self.title,
            'description': self.description,
            'priority': self.priority
        }

@dataclass(frozen=True)
class BloodTestRanges:
    """Rangos normales para exámenes de sangre - Value Object"""
    glucose_min: float = 70.0
    glucose_max: float = 100.0
    cholesterol_max: float = 200.0
    hdl_cholesterol_min: float = 40.0  # hombres
    hdl_cholesterol_min_women: float = 50.0  # mujeres
    ldl_cholesterol_max: float = 100.0
    triglycerides_max: float = 150.0
    hemoglobin_min_men: float = 13.5
    hemoglobin_max_men: float = 17.5
    hemoglobin_min_women: float = 12.0
    hemoglobin_max_women: float = 15.5
    creatinine_min_men: float = 0.74
    creatinine_max_men: float = 1.35
    creatinine_min_women: float = 0.59
    creatinine_max_women: float = 1.04
