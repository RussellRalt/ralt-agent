"""
Vision Service - Maneja el procesamiento y análisis de imágenes
"""
import base64
import io
from PIL import Image
import requests
from typing import Dict, Any, Optional, List

class VisionService:
    def __init__(self):
        self.supported_formats = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]
        self.max_image_size = 10 * 1024 * 1024  # 10MB
        
    def is_available(self) -> bool:
        """Verifica si el servicio está disponible"""
        return True
    
    async def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Procesa una solicitud relacionada con visión"""
        try:
            result = {
                "type": "vision",
                "processed": False,
                "images_analyzed": [],
                "text_extracted": "",
                "objects_detected": [],
                "analysis": ""
            }
            
            # Buscar imágenes en el contexto
            images = self._extract_images_from_context(context)
            
            if images:
                for image_data in images:
                    analysis = await self._analyze_image(image_data, user_input)
                    result["images_analyzed"].append(analysis)
                    result["processed"] = True
            
            return result
            
        except Exception as e:
            return {
                "type": "vision",
                "error": str(e),
                "processed": False
            }
    
    def _extract_images_from_context(self, context: Optional[Dict]) -> List[Dict]:
        """Extrae imágenes del contexto proporcionado"""
        images = []
        
        if not context:
            return images
        
        # Buscar imágenes en diferentes formatos del contexto
        if "images" in context:
            images.extend(context["images"])
        
        if "files" in context:
            for file_info in context["files"]:
                if self._is_image_file(file_info.get("name", "")):
                    images.append(file_info)
        
        return images
    
    def _is_image_file(self, filename: str) -> bool:
        """Verifica si un archivo es una imagen soportada"""
        if not filename:
            return False
        
        extension = filename.lower().split(".")[-1]
        return extension in self.supported_formats
    
    async def _analyze_image(self, image_data: Dict, user_query: str) -> Dict[str, Any]:
        """Analiza una imagen específica"""
        try:
            analysis = {
                "filename": image_data.get("name", "unknown"),
                "size": image_data.get("size", 0),
                "format": image_data.get("format", "unknown"),
                "dimensions": None,
                "description": "",
                "objects": [],
                "text": "",
                "colors": [],
                "metadata": {}
            }
            
            # Cargar la imagen
            image = self._load_image(image_data)
            if image:
                analysis["dimensions"] = image.size
                analysis["format"] = image.format
                
                # Análisis básico de la imagen
                analysis["description"] = self._generate_description(image, user_query)
                analysis["colors"] = self._extract_dominant_colors(image)
                analysis["text"] = self._extract_text_ocr(image)
                analysis["objects"] = self._detect_objects(image)
            
            return analysis
            
        except Exception as e:
            return {
                "filename": image_data.get("name", "unknown"),
                "error": str(e)
            }
    
    def _load_image(self, image_data: Dict) -> Optional[Image.Image]:
        """Carga una imagen desde los datos proporcionados"""
        try:
            if "base64" in image_data:
                # Imagen en base64
                image_bytes = base64.b64decode(image_data["base64"])
                return Image.open(io.BytesIO(image_bytes))
            
            elif "url" in image_data:
                # Imagen desde URL
                response = requests.get(image_data["url"], timeout=10)
                response.raise_for_status()
                return Image.open(io.BytesIO(response.content))
            
            elif "path" in image_data:
                # Imagen desde archivo local
                return Image.open(image_data["path"])
            
            return None
            
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def _generate_description(self, image: Image.Image, user_query: str) -> str:
        """Genera una descripción de la imagen"""
        # Análisis básico de la imagen
        width, height = image.size
        mode = image.mode
        
        description = f"Imagen de {width}x{height} píxeles en modo {mode}."
        
        # Análisis de contenido básico (esto se mejoraría con un modelo de visión real)
        if image.mode == "RGB":
            # Análisis de colores dominantes
            colors = image.getcolors(maxcolors=256*256*256)
            if colors:
                dominant_color = max(colors, key=lambda x: x[0])
                description += f" Color dominante detectado."
        
        # Aquí se integraría con un modelo de visión real como GPT-4V o Claude Vision
        description += " Para un análisis más detallado, se requiere integración con modelo de visión."
        
        return description
    
    def _extract_dominant_colors(self, image: Image.Image) -> List[str]:
        """Extrae los colores dominantes de la imagen"""
        try:
            # Convertir a RGB si es necesario
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Reducir el tamaño para análisis más rápido
            image = image.resize((150, 150))
            
            # Obtener colores
            colors = image.getcolors(maxcolors=256*256*256)
            if not colors:
                return []
            
            # Ordenar por frecuencia y tomar los top 5
            colors.sort(key=lambda x: x[0], reverse=True)
            dominant_colors = []
            
            for count, color in colors[:5]:
                hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                dominant_colors.append(hex_color)
            
            return dominant_colors
            
        except Exception as e:
            print(f"Error extracting colors: {e}")
            return []
    
    def _extract_text_ocr(self, image: Image.Image) -> str:
        """Extrae texto de la imagen usando OCR"""
        try:
            # Aquí se integraría con una biblioteca OCR como Tesseract
            # Por ahora, retornamos un placeholder
            return "OCR no implementado - se requiere integración con Tesseract o servicio OCR"
            
        except Exception as e:
            print(f"Error in OCR: {e}")
            return ""
    
    def _detect_objects(self, image: Image.Image) -> List[Dict]:
        """Detecta objetos en la imagen"""
        try:
            # Aquí se integraría con un modelo de detección de objetos
            # Por ahora, retornamos un placeholder
            return [
                {
                    "name": "objeto_detectado",
                    "confidence": 0.85,
                    "bbox": [0, 0, 100, 100],
                    "note": "Detección de objetos no implementada - se requiere modelo especializado"
                }
            ]
            
        except Exception as e:
            print(f"Error in object detection: {e}")
            return []
    
    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Codifica una imagen a base64 para envío a APIs"""
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                return encoded_string
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None
    
    def resize_image(self, image: Image.Image, max_size: tuple = (1024, 1024)) -> Image.Image:
        """Redimensiona una imagen manteniendo la proporción"""
        try:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            return image
        except Exception as e:
            print(f"Error resizing image: {e}")
            return image

