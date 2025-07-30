# RALT Agent - Agente Multimodal

RALT Agent es un agente multimodal avanzado inspirado en Manus AI, con capacidades de visión, navegación web, asistencia de código, investigación y creatividad.

## 🚀 Características

- **Agente General**: Conversación y asistencia general
- **Agente de Visión**: Análisis y procesamiento de imágenes
- **Navegador Web**: Capacidades de navegación y extracción de información web
- **Asistente de Código**: Generación y análisis de código
- **Agente de Investigación**: Búsqueda y análisis de información
- **Agente Creativo**: Generación de contenido creativo

## 📁 Estructura del Proyecto

```
ralt-agent/
├── frontend/          # Aplicación React
│   ├── src/
│   │   ├── App.jsx
│   │   ├── config.js
│   │   └── services/
│   └── package.json
├── backend/           # API Flask
│   ├── src/
│   │   ├── main.py
│   │   ├── routes/
│   │   └── services/
│   └── requirements.txt
└── README.md
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Node.js (v16 o superior)
- Python 3.8 o superior
- pip

### Backend

1. Navega al directorio del backend:
```bash
cd backend
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
```

4. Edita el archivo `.env` con tus claves API:
```
OPENROUTER_API_KEY=tu_clave_openrouter
FIREBASE_PROJECT_ID=tu_proyecto_firebase
FIREBASE_API_KEY=tu_clave_firebase
FIREBASE_AUTH_DOMAIN=tu_dominio_firebase
FIREBASE_DATABASE_URL=tu_url_database
FIREBASE_STORAGE_BUCKET=tu_bucket_storage
```

5. Ejecuta el backend:
```bash
python src/main.py
```

### Frontend

1. Navega al directorio del frontend:
```bash
cd frontend
```

2. Instala las dependencias:
```bash
npm install
```

3. Ejecuta el frontend:
```bash
npm run dev
```

## 🔧 Uso

1. Asegúrate de que el backend esté ejecutándose en `http://localhost:5000`
2. Asegúrate de que el frontend esté ejecutándose en `http://localhost:5173`
3. Abre tu navegador y ve a `http://localhost:5173`
4. Selecciona el tipo de agente que deseas usar
5. Comienza a chatear con el agente

## 🤖 Tipos de Agentes

- **General**: Para conversaciones generales y tareas básicas
- **Vision**: Para análisis de imágenes y contenido visual
- **Web Navigator**: Para navegación web y extracción de información
- **Code Assistant**: Para programación y desarrollo
- **Research**: Para investigación y análisis de datos
- **Creative**: Para tareas creativas y generación de contenido

## 🔑 Configuración de APIs

### OpenRouter API
1. Ve a [OpenRouter](https://openrouter.ai/)
2. Crea una cuenta y obtén tu API key
3. Agrega la key al archivo `.env`

### Firebase
1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuevo proyecto
3. Obtén la configuración del proyecto
4. Agrega los valores al archivo `.env`

## 🚀 Despliegue

Para desplegar en producción, puedes usar servicios como:
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Backend**: Heroku, Railway, DigitalOcean

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🆘 Soporte

Si tienes problemas o preguntas, por favor abre un issue en GitHub.

