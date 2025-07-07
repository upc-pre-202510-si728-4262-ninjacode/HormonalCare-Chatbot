from typing import List
from ..entities import BloodTest, User
from ..value_objects import BloodTestAnalysis, RiskLevel, Recommendation, RecommendationType, BloodTestRanges

class BloodTestAnalysisService:
    """Servicio de dominio para analizar exámenes de sangre"""
    
    def __init__(self):
        self.ranges = BloodTestRanges()
    
    def analyze_blood_test(self, blood_test: BloodTest, user: User) -> BloodTestAnalysis:
        """Analiza un examen de sangre y retorna el análisis"""
        
        # Análisis de glucosa
        glucose_status = self._analyze_glucose(blood_test.glucose)
        
        # Análisis de colesterol
        cholesterol_status = self._analyze_cholesterol(blood_test)
        
        # Análisis de función renal
        kidney_status = self._analyze_kidney_function(blood_test, user)
        
        # Análisis de hemograma
        blood_count_status = self._analyze_blood_count(blood_test, user)
        
        # Evaluar riesgo general
        overall_risk = self._calculate_overall_risk(
            glucose_status, cholesterol_status, kidney_status, blood_count_status
        )
        
        # Generar recomendaciones
        recommendations = self._generate_recommendations(
            blood_test, user, glucose_status, cholesterol_status, kidney_status, blood_count_status
        )
        
        # Determinar si necesita consulta médica
        needs_doctor = self._needs_doctor_consultation(overall_risk, recommendations)
        
        # Identificar factores de riesgo
        risk_factors = self._identify_risk_factors(blood_test, user)
        
        return BloodTestAnalysis(
            overall_risk=overall_risk,
            glucose_status=glucose_status,
            cholesterol_status=cholesterol_status,
            kidney_function_status=kidney_status,
            blood_count_status=blood_count_status,
            recommendations=[rec.to_dict() for rec in recommendations],
            needs_doctor_consultation=needs_doctor,
            risk_factors=risk_factors
        )
    
    def _analyze_glucose(self, glucose: float) -> str:
        """Analiza los niveles de glucosa"""
        if glucose < 70:
            return "Hipoglucemia - Nivel bajo de glucosa"
        elif glucose <= 100:
            return "Normal - Nivel de glucosa en ayunas normal"
        elif glucose <= 125:
            return "Prediabetes - Glucosa alterada en ayunas"
        else:
            return "Diabetes - Nivel elevado de glucosa"
    
    def _analyze_cholesterol(self, blood_test: BloodTest) -> str:
        """Analiza los niveles de colesterol"""
        issues = []
        
        if blood_test.cholesterol > self.ranges.cholesterol_max:
            issues.append("colesterol total elevado")
        
        if blood_test.ldl_cholesterol > self.ranges.ldl_cholesterol_max:
            issues.append("LDL (colesterol malo) elevado")
        
        if blood_test.triglycerides > self.ranges.triglycerides_max:
            issues.append("triglicéridos elevados")
        
        if not issues:
            return "Normal - Perfil lipídico dentro de rangos normales"
        else:
            return f"Alterado - {', '.join(issues)}"
    
    def _analyze_kidney_function(self, blood_test: BloodTest, user: User) -> str:
        """Analiza la función renal"""
        creatinine_max = (self.ranges.creatinine_max_men if user.gender.lower() == 'male' 
                         else self.ranges.creatinine_max_women)
        
        if blood_test.creatinine > creatinine_max:
            return "Alterada - Creatinina elevada, posible disfunción renal"
        elif blood_test.urea > 50:  # Valor de referencia típico
            return "Alterada - Urea elevada"
        else:
            return "Normal - Función renal dentro de parámetros normales"
    
    def _analyze_blood_count(self, blood_test: BloodTest, user: User) -> str:
        """Analiza el hemograma"""
        issues = []
        
        # Analizar hemoglobina según género
        if user.gender.lower() == 'male':
            if blood_test.hemoglobin < self.ranges.hemoglobin_min_men:
                issues.append("hemoglobina baja (anemia)")
        else:
            if blood_test.hemoglobin < self.ranges.hemoglobin_min_women:
                issues.append("hemoglobina baja (anemia)")
        
        # Analizar otros parámetros
        if blood_test.white_blood_cells > 11000:
            issues.append("glóbulos blancos elevados")
        elif blood_test.white_blood_cells < 4000:
            issues.append("glóbulos blancos bajos")
        
        if blood_test.platelets > 450000:
            issues.append("plaquetas elevadas")
        elif blood_test.platelets < 150000:
            issues.append("plaquetas bajas")
        
        if not issues:
            return "Normal - Hemograma completo dentro de rangos normales"
        else:
            return f"Alterado - {', '.join(issues)}"
    
    def _calculate_overall_risk(self, glucose_status: str, cholesterol_status: str, 
                              kidney_status: str, blood_count_status: str) -> RiskLevel:
        """Calcula el riesgo general basado en todos los análisis"""
        risk_score = 0
        
        # Evaluar glucosa
        if "Diabetes" in glucose_status:
            risk_score += 3
        elif "Prediabetes" in glucose_status:
            risk_score += 2
        elif "Hipoglucemia" in glucose_status:
            risk_score += 2
        
        # Evaluar colesterol
        if "Alterado" in cholesterol_status:
            risk_score += 2
        
        # Evaluar función renal
        if "Alterada" in kidney_status:
            risk_score += 3
        
        # Evaluar hemograma
        if "Alterado" in blood_count_status:
            risk_score += 1
        
        # Determinar nivel de riesgo
        if risk_score >= 6:
            return RiskLevel.CRITICAL
        elif risk_score >= 4:
            return RiskLevel.HIGH
        elif risk_score >= 2:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW
    
    def _generate_recommendations(self, blood_test: BloodTest, user: User, 
                                glucose_status: str, cholesterol_status: str,
                                kidney_status: str, blood_count_status: str) -> List[Recommendation]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Recomendaciones para glucosa
        if "Diabetes" in glucose_status or "Prediabetes" in glucose_status:
            recommendations.extend([
                Recommendation(
                    type=RecommendationType.DIETARY,
                    title="Dieta baja en carbohidratos",
                    description="Reducir el consumo de azúcares y carbohidratos refinados. Incluir más vegetales y proteínas magras.",
                    priority=5
                ),
                Recommendation(
                    type=RecommendationType.EXERCISE,
                    title="Ejercicio regular",
                    description="Realizar al menos 150 minutos de actividad física moderada por semana.",
                    priority=4
                )
            ])
        
        # Recomendaciones para colesterol
        if "Alterado" in cholesterol_status:
            recommendations.extend([
                Recommendation(
                    type=RecommendationType.DIETARY,
                    title="Dieta baja en grasas saturadas",
                    description="Reducir carnes rojas, productos lácteos enteros y frituras. Incluir más pescado y nueces.",
                    priority=4
                ),
                Recommendation(
                    type=RecommendationType.LIFESTYLE,
                    title="Control de peso",
                    description="Mantener un peso saludable mediante dieta equilibrada y ejercicio.",
                    priority=3
                )
            ])
        
        # Recomendaciones para función renal
        if "Alterada" in kidney_status:
            recommendations.extend([
                Recommendation(
                    type=RecommendationType.DIETARY,
                    title="Reducir sal y proteínas",
                    description="Limitar el consumo de sal y moderar la ingesta de proteínas.",
                    priority=5
                ),
                Recommendation(
                    type=RecommendationType.LIFESTYLE,
                    title="Hidratación adecuada",
                    description="Mantener una hidratación adecuada, aproximadamente 2 litros de agua al día.",
                    priority=4
                )
            ])
        
        return recommendations
    
    def _needs_doctor_consultation(self, overall_risk: RiskLevel, recommendations: List[Recommendation]) -> bool:
        """Determina si se necesita consulta médica"""
        return overall_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL] or len(recommendations) >= 4
    
    def _identify_risk_factors(self, blood_test: BloodTest, user: User) -> List[str]:
        """Identifica factores de riesgo específicos"""
        risk_factors = []
        
        if blood_test.glucose > 125:
            risk_factors.append("Diabetes mellitus")
        elif blood_test.glucose > 100:
            risk_factors.append("Prediabetes")
        
        if blood_test.cholesterol > 240:
            risk_factors.append("Colesterol alto")
        
        if blood_test.ldl_cholesterol > 130:
            risk_factors.append("LDL elevado")
        
        if user.age > 45:
            risk_factors.append("Edad de riesgo cardiovascular")
        
        return risk_factors
