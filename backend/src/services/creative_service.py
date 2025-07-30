import json
from typing import Dict, Any, Optional

class CreativeService:
    def __init__(self):
        pass

    def is_available(self) -> bool:
        """Verifica si el servicio creativo está disponible"""
        return True

    async def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Procesa una solicitud creativa"""
        # Detectar tipo de contenido creativo
        content_types = {
            "story": ["historia", "cuento", "narrativa"],
            "poem": ["poema", "poesía", "verso"],
            "script": ["guion", "escena", "diálogo"],
            "design_concept": ["diseño", "concepto visual", "idea gráfica"],
            "song_lyrics": ["letra de canción", "canción"]
        }
        
        detected_type = "general_creative"
        for c_type, keywords in content_types.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                detected_type = c_type
                break
        
        # Extraer tema creativo
        topic = user_input.replace("crear", "").replace("generar", "").strip()
        
        return {
            "type": "creative",
            "creative_type": detected_type,
            "topic": topic,
            "result": f"Generando contenido creativo de tipo \'{detected_type}\' sobre: \'{topic}\'. Preparando la inspiración."
        }

