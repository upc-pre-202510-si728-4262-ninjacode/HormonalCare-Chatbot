# Medical Chatbot Backend

Backend Flask con arquitectura DDD para un chatbot médico que analiza exámenes de sangre usando Gemini AI.

## Características

- Arquitectura Domain Driven Design (DDD)
- Análisis de exámenes de sangre con IA
- API REST para aplicaciones móviles
- Integración con Google Gemini AI
- Evaluación de riesgos y recomendaciones médicas
- **Documentación interactiva con Swagger/OpenAPI**
- **Base de datos MySQL para producción**

## Instalación

### 1. Requisitos previos
- Python 3.8+
- MySQL Server 8.0+
- Git

### 2. Configurar MySQL
```sql
-- Conectar a MySQL como root
mysql -u root -p

-- Crear base de datos
CREATE DATABASE chatbot;

-- Crear usuario (opcional)
CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON chatbot.* TO 'chatbot_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Instalar el proyecto
```bash
# Clonar el repositorio
git clone <repo-url>
cd chatBot

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

**Archivo .env requerido:**
```env
# API Key de Google Gemini
GEMINI_API_KEY=tu_api_key_aqui
GEMINI_MODEL=gemini-1.5-pro

# Configuración de MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=chatbot
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/chatbot

# Configuración de Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_secret_key_super_segura_aqui
PORT=5000
```

### 5. Configurar base de datos
```bash
# Configurar MySQL y crear tablas
python setup_mysql.py

# O ejecutar directamente la aplicación (crea tablas automáticamente)
python app.py
```

## 📖 Documentación API

Una vez iniciado el servidor, la documentación interactiva estará disponible en:

**🚀 Swagger UI: http://localhost:5000/docs/**

Desde la interfaz de Swagger puedes:
- Ver todos los endpoints disponibles
- Probar las APIs directamente desde el navegador
- Ver ejemplos de request/response
- Entender la estructura de datos

## Estructura del Proyecto

```
src/
├── domain/          # Dominio (entidades, value objects, reglas de negocio)
├── infrastructure/  # Infraestructura (BD, APIs externas)
├── application/     # Casos de uso y servicios de aplicación
└── presentation/    # Controladores y API REST con Swagger
```

## API Endpoints

- `POST /api/users` - Crear usuario
- `GET /api/users/{user_id}/history` - Historial de conversaciones
- `POST /api/chat/analyze` - Analizar examen de sangre
- `POST /api/chat/{conversation_id}/message` - Enviar mensaje al chat
- `GET /api/health` - Estado de la API

## 🛠️ Herramientas de Base de Datos

### Configurar MySQL
```bash
python setup_mysql.py
```
Verifica conexión, crea la base de datos y configura las tablas.

### Limpiar Base de Datos
```bash
python clean_database.py
```
Script interactivo para:
- Ver estadísticas de la BD
- Limpiar todos los datos
- Resetear completamente la BD

### Backup de Base de Datos
```bash
python backup_database.py
```
Crea backup automático en formato JSON (compatible con MySQL).

### Migrar de SQLite a MySQL
```bash
python migrate_to_mysql.py
```
Migra datos existentes de SQLite a MySQL automáticamente.

## Modelos de IA Disponibles

Configura el modelo en `.env`:

```env
# Máxima calidad para análisis médicos (recomendado)
GEMINI_MODEL=gemini-1.5-pro

# Velocidad optimizada
GEMINI_MODEL=gemini-1.5-flash

# Modelo base
GEMINI_MODEL=gemini-pro
```
