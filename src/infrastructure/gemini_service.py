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
Eres un asistente médico virtual especializado en análisis de exámenes de sangre. 
Analiza los siguientes resultados y proporciona una explicación clara y comprensible para el paciente.

DATOS DEL PACIENTE:
- Nombre: {user_data.get('name', 'Paciente')}
- Edad: {user_data.get('age')} años
- Género: {user_data.get('gender')}

RESULTADOS DEL EXAMEN:
- Glucosa: {blood_test_data.get('glucose')} mg/dL
- Colesterol total: {blood_test_data.get('cholesterol')} mg/dL
- HDL (colesterol bueno): {blood_test_data.get('hdl_cholesterol')} mg/dL
- LDL (colesterol malo): {blood_test_data.get('ldl_cholesterol')} mg/dL
- Triglicéridos: {blood_test_data.get('triglycerides')} mg/dL
- Hemoglobina: {blood_test_data.get('hemoglobin')} g/dL
- Hematocrito: {blood_test_data.get('hematocrit')}%
- Glóbulos blancos: {blood_test_data.get('white_blood_cells')}/μL
- Glóbulos rojos: {blood_test_data.get('red_blood_cells')} millones/μL
- Plaquetas: {blood_test_data.get('platelets')}/μL
- Creatinina: {blood_test_data.get('creatinine')} mg/dL
- Urea: {blood_test_data.get('urea')} mg/dL

ANÁLISIS AUTOMATIZADO:
- Riesgo general: {analysis.get('overall_risk')}
- Estado de glucosa: {analysis.get('glucose_status')}
- Estado del colesterol: {analysis.get('cholesterol_status')}
- Función renal: {analysis.get('kidney_function_status')}
- Hemograma: {analysis.get('blood_count_status')}
- Necesita consulta médica: {'Sí' if analysis.get('needs_doctor_consultation') else 'No'}

INSTRUCCIONES:
1. Explica los resultados de manera clara y sin usar jerga médica excesiva
2. Enfócate en los valores que están fuera del rango normal
3. Proporciona contexto sobre qué significan estos valores para la salud
4. Mantén un tono tranquilizador pero honesto
5. Siempre recuerda que esto no reemplaza una consulta médica
6. Responde en español
7. Estructura tu respuesta de manera organizada y fácil de leer

Por favor, proporciona un análisis detallado y comprensible de estos resultados.
"""

    def _create_chat_prompt(self, user_message: str, blood_test_data: Dict[str, Any], 
                           user_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Crea el prompt para conversación del chatbot"""
        
        return f"""
Eres un asistente médico virtual amigable y empático que ayuda a pacientes a entender sus exámenes de sangre.

CONTEXTO DEL PACIENTE:
- Edad: {user_data.get('age')} años
- Género: {user_data.get('gender')}

ÚLTIMOS RESULTADOS DE EXAMEN:
- Glucosa: {blood_test_data.get('glucose')} mg/dL
- Colesterol total: {blood_test_data.get('cholesterol')} mg/dL
- Riesgo general: {analysis.get('overall_risk')}
- Necesita consulta médica: {'Sí' if analysis.get('needs_doctor_consultation') else 'No'}

PREGUNTA/MENSAJE DEL PACIENTE:
"{user_message}"

INSTRUCCIONES:
1. Responde de manera empática y comprensible
2. Usa los datos del examen para contextualizar tu respuesta
3. Si el usuario pregunta sobre valores específicos, explícalos claramente
4. Si detectas preocupación o ansiedad, tranquiliza apropiadamente
5. Siempre recuerda que no reemplazas una consulta médica profesional
6. Si los resultados sugieren riesgo alto, recomienda consultar un médico
7. Responde en español
8. Mantén respuestas concisas pero informativas
9. Si el usuario pregunta sobre síntomas o tratamientos específicos, recomienda consultar un profesional

Proporciona una respuesta útil y empática.
"""
