import json
from typing import Dict, Any, Optional

class CodeService:
    def __init__(self):
        pass

    def is_available(self) -> bool:
        """Verifica si el servicio de código está disponible"""
        return True

    async def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Procesa una solicitud relacionada con código"""
        # Detectar lenguaje de programación
        languages = {
            "python": ["python", "py", "django", "flask"],
            "javascript": ["javascript", "js", "node", "react", "vue"],
            "java": ["java", "spring"],
            "cpp": ["c++", "cpp"],
            "go": ["go", "golang"],
            "rust": ["rust"]
        }
        
        detected_language = "general"
        for lang, keywords in languages.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                detected_language = lang
                break
        
        # Detectar tipo de solicitud
        if "generar" in user_input.lower() or "crear" in user_input.lower():
            action = "generate"
        elif "revisar" in user_input.lower() or "debug" in user_input.lower():
            action = "review"
        elif "explicar" in user_input.lower():
            action = "explain"
        else:
            action = "general"
        
        return {
            "type": "code",
            "action": action,
            "language": detected_language,
            "result": f"Solicitud de código detectada: {action} en {detected_language}. Procesando con modelo especializado en código."
        }

