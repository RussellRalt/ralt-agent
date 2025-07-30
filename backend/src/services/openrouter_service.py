import os
import requests
import json
from typing import Dict, Any, Optional, List

class OpenRouterService:
    def __init__(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def is_available(self) -> bool:
        """Verifica si el servicio de OpenRouter está configurado y disponible"""
        return self.api_key is not None and self.api_key != "your-openrouter-api-key"

    async def generate_response(self, 
                                user_input: str, 
                                model: str = "openai/gpt-4o", 
                                agent_context: Optional[str] = None, 
                                service_results: Optional[Dict] = None,
                                chat_history: Optional[List[Dict]] = None) -> str:
        """Genera una respuesta utilizando un modelo de OpenRouter"""
        if not self.is_available():
            return "Error: OPENROUTER_API_KEY no configurada. Por favor, configura tu clave API."

        messages = []
        if agent_context:
            messages.append({"role": "system", "content": agent_context})
        
        if chat_history:
            for msg in chat_history:
                if msg["type"] == "user":
                    messages.append({"role": "user", "content": msg["content"]})
                elif msg["type"] == "agent":
                    messages.append({"role": "assistant", "content": msg["content"]})

        messages.append({"role": "user", "content": user_input})

        # Añadir resultados de servicios al contexto si existen
        if service_results:
            service_info = "\n\nResultados de servicios adicionales:\n"
            for service_name, result in service_results.items():
                service_info += f"- {service_name.capitalize()} Service: {json.dumps(result, indent=2)}\n"
            messages.append({"role": "system", "content": service_info})

        payload = {
            "model": model,
            "messages": messages
        }

        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
            response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP erróneos
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Error al llamar a OpenRouter API: {e}")
            return f"Error al conectar con el modelo de IA: {e}"
        except KeyError:
            print(f"Respuesta inesperada de OpenRouter API: {response.json()}")
            return "Error: Respuesta inesperada del modelo de IA."

    async def get_models(self) -> List[Dict]:
        """Obtiene la lista de modelos disponibles en OpenRouter"""
        if not self.is_available():
            return []
        try:
            response = requests.get(f"{self.base_url}/models", headers=self.headers)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener modelos de OpenRouter: {e}")
            return []



