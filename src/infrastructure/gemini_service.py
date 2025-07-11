import google.generativeai as genai
from typing import Dict, Any
import json
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    """Servicio para interactuar con Google Gemini AI"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
        
        genai.configure(api_key=self.api_key)
        
        # Usar el modelo más avanzado disponible
        # Opciones: 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro'
        model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')
        self.model = genai.GenerativeModel(model_name)
        
        print(f"🤖 Usando modelo Gemini: {model_name}")
    
    def analyze_blood_test_with_ai(self, blood_test_data: Dict[str, Any], 
                                  user_data: Dict[str, Any], 
                                  analysis: Dict[str, Any]) -> str:
        """
        Usa Gemini para generar una explicación detallada del análisis de sangre
        """
        prompt = self._create_analysis_prompt(blood_test_data, user_data, analysis)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error al generar análisis con IA: {str(e)}"
    
    def chat_with_user(self, user_message: str, blood_test_data: Dict[str, Any], 
                      user_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        Maneja la conversación del chatbot con el usuario
        """
        prompt = self._create_chat_prompt(user_message, blood_test_data, user_data, analysis)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Lo siento, hubo un error al procesar tu consulta. Por favor intenta de nuevo."
    
    def _create_analysis_prompt(self, blood_test_data: Dict[str, Any], 
                               user_data: Dict[str, Any], 
                               analysis: Dict[str, Any]) -> str:
        """Crea el prompt para análisis de examen de sangre"""
        
        return f"""
Eres un asistente médico virtual especializado en análisis de sangre para pacientes con diabetes.

PACIENTE:
- Nombre: {user_data.get('name', 'Paciente')}
- Edad: {user_data.get('age')} años
- Género: {user_data.get('gender')}

RESULTADOS CLAVE:
- Glucosa: {blood_test_data.get('glucose')} mg/dL
- Colesterol total: {blood_test_data.get('cholesterol')} mg/dL
- LDL: {blood_test_data.get('ldl_cholesterol')} mg/dL
- HDL: {blood_test_data.get('hdl_cholesterol')} mg/dL
- Triglicéridos: {blood_test_data.get('triglycerides')} mg/dL
- Creatinina: {blood_test_data.get('creatinine')} mg/dL

ANÁLISIS:
- Riesgo general: {analysis.get('overall_risk')}
- Glucosa: {analysis.get('glucose_status')}
- Colesterol: {analysis.get('cholesterol_status')}
- Función renal: {analysis.get('kidney_function_status')}

INSTRUCCIONES:
1. Respuesta máximo 4 párrafos cortos
2. Enfócate solo en valores alterados
3. Menciona implicaciones para diabetes
4. Usa lenguaje simple y directo
5. Incluye 2-3 recomendaciones específicas
6. Responde en español

Proporciona un análisis breve y directo.
"""

    def _create_chat_prompt(self, user_message: str, blood_test_data: Dict[str, Any], 
                           user_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Crea el prompt para conversación del chatbot"""
        
        return f"""
Eres un asistente médico virtual para pacientes con diabetes.

PACIENTE:
- Edad: {user_data.get('age')} años
- Género: {user_data.get('gender')}

ÚLTIMO ANÁLISIS:
- Glucosa: {blood_test_data.get('glucose')} mg/dL
- Colesterol total: {blood_test_data.get('cholesterol')} mg/dL
- Riesgo: {analysis.get('overall_risk')}

PREGUNTA:
"{user_message}"

INSTRUCCIONES:
1. Respuesta máximo 2 párrafos
2. Responde solo lo que preguntan
3. Relaciona con diabetes cuando sea relevante
4. Usa lenguaje simple
5. Sé directo y conciso
6. Responde en español

Respuesta breve y útil.
"""
