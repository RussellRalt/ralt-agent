from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
from src.services.openrouter_service import OpenRouterService
from src.services.vision_service import VisionService
from src.services.web_service import WebService
from src.services.code_service import CodeService
from src.services.research_service import ResearchService
from src.services.creative_service import CreativeService

chat_bp = Blueprint("chat", __name__)
openrouter_service = OpenRouterService()
vision_service = VisionService()
web_service = WebService()
code_service = CodeService()
research_service = ResearchService()
creative_service = CreativeService()
AGENT_TYPES = {
    'general': {
        'name': 'General Chat',
        'description': 'Conversación general y asistencia',
        'capabilities': ['chat', 'qa', 'general_assistance'],
        'model': 'gpt-4o'
    },
    'vision': {
        'name': 'Vision Agent',
        'description': 'Análisis de imágenes y contenido visual',
        'capabilities': ['image_analysis', 'ocr', 'visual_qa'],
        'model': 'gpt-4o-vision'
    },
    'web': {
        'name': 'Web Navigator',
        'description': 'Navegación y automatización web',
        'capabilities': ['web_scraping', 'automation', 'research'],
        'model': 'gpt-4o'
    },
    'code': {
        'name': 'Code Assistant',
        'description': 'Programación y desarrollo',
        'capabilities': ['code_generation', 'debugging', 'review'],
        'model': 'deepseek-coder'
    },
    'research': {
        'name': 'Research Agent',
        'description': 'Investigación profunda y análisis',
        'capabilities': ['deep_research', 'data_analysis', 'synthesis'],
        'model': 'claude-3.5-sonnet'
    },
    'creative': {
        'name': 'Creative Agent',
        'description': 'Contenido creativo y multimedia',
        'capabilities': ['content_creation', 'design', 'storytelling'],
        'model': 'gpt-4o'
    }
}

@chat_bp.route("/chat", methods=["POST"])
async def chat():
    """Endpoint principal para el chat con agentes"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('message', '')
        agent_type = data.get('agent_type', 'general')
        context = data.get('context', [])
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if agent_type not in AGENT_TYPES:
            return jsonify({'error': f'Invalid agent type: {agent_type}'}), 400
        
        # Procesar el mensaje según el tipo de agente
        response = await process_agent_message(message, agent_type, context)        
        return jsonify({
            'success': True,
            'response': response['content'],
            'agent_type': agent_type,
            'model_used': AGENT_TYPES[agent_type]['model'],
            'capabilities_used': response['capabilities_used'],
            'metadata': response['metadata'],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/agents', methods=['GET'])
def get_agents():
    """Obtener lista de agentes disponibles"""
    return jsonify({
        'success': True,
        'agents': AGENT_TYPES
    })

@chat_bp.route('/agent/<agent_type>/capabilities', methods=['GET'])
def get_agent_capabilities(agent_type):
    """Obtener capacidades específicas de un agente"""
    if agent_type not in AGENT_TYPES:
        return jsonify({'error': f'Invalid agent type: {agent_type}'}), 400
    
    return jsonify({
        'success': True,
        'agent': AGENT_TYPES[agent_type]
    })

async def process_agent_message(message, agent_type, context):
    """Procesa un mensaje según el tipo de agente, integrando servicios multimodales."""
    agent_config = AGENT_TYPES[agent_type]
    service_results = {}
    agent_response_content = ""

    # 1. Intentar usar servicios específicos si el tipo de agente lo requiere
    if agent_type == 'vision' and vision_service.is_available():
        # Aquí se debería añadir lógica para detectar si el mensaje contiene una imagen
        # Por ahora, simulamos que el servicio de visión procesa la entrada de texto
        service_results['vision'] = await vision_service.process(message, context)
        agent_response_content = service_results['vision'].get('result', 'Análisis de visión completado.')
    elif agent_type == 'web' and web_service.is_available():
        service_results['web'] = await web_service.process(message, context)
        agent_response_content = service_results['web'].get('result', 'Navegación web completada.')
    elif agent_type == 'code' and code_service.is_available():
        service_results['code'] = await code_service.process(message, context)
        agent_response_content = service_results['code'].get('result', 'Asistencia de código completada.')
    elif agent_type == 'research' and research_service.is_available():
        service_results['research'] = await research_service.process(message, context)
        agent_response_content = service_results['research'].get('result', 'Investigación completada.')
    elif agent_type == 'creative' and creative_service.is_available():
        service_results['creative'] = await creative_service.process(message, context)
        agent_response_content = service_results['creative'].get('result', 'Contenido creativo generado.')
    
    # 2. Si no se usó un servicio específico o se necesita una respuesta más elaborada, usar OpenRouter
    if not agent_response_content or agent_type == 'general' or (agent_type != 'general' and 'error' in agent_response_content.lower()):
        agent_context_prompt = f"""
Eres un {agent_config["name"]} especializado en {agent_config["description"]}.

Tus capacidades principales incluyen:
{', '.join(agent_config["capabilities"])}

Responde a la siguiente consulta del usuario, utilizando tus capacidades especializadas. Si la consulta requiere una capacidad multimodal que no puedes simular, indica al usuario qué tipo de entrada necesitas (ej. "Por favor, sube una imagen para que pueda analizarla").
"""

        chat_history_formatted = []
        for msg in context:
            if msg["type"] == "user":
                chat_history_formatted.append({"role": "user", "content": msg["content"]})
            elif msg["type"] == "agent":
                chat_history_formatted.append({"role": "assistant", "content": msg["content"]})

        try:
            response_content = await openrouter_service.generate_response(
                user_input=message,
                model=agent_config["model"],
                agent_context=agent_context_prompt,
                service_results=service_results, # Pasar resultados de servicios al LLM
                chat_history=chat_history_formatted
            )
            agent_response_content = response_content
        except Exception as e:
            agent_response_content = "Ocurrió un error al procesar la solicitud."
            service_results["error"] = str(e)
    return {
        'content': agent_response_content,
        'capabilities_used': agent_config["capabilities"],
        'metadata': {
            'response_source': 'openrouter' if not service_results else 'multimodal_orchestration',
            'model_name': agent_config["model"],
            'service_results': service_results
        }
    }

