# Cometa - Sistema de Gestión de Bar

Este proyecto consiste en una API de gestión de pedidos de bar (backend) y una interfaz de usuario web (frontend).

## Estructura del Proyecto

```
cometa/
├── api/         # Backend (FastAPI)
└── web/         # Frontend (Next.js)
```

## Requisitos Previos

- Python 3.8+
- Node.js 14+
- npm o yarn

## Instalación y Ejecución

### Backend (API)

1. Navega al directorio de la API:
   ```
   cd api
   ```

2. Crea un entorno virtual:
   ```
   python -m venv venv
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS y Linux:
     ```
     source venv/bin/activate
     ```

4. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

5. Ejecuta la API:
   ```
   python run.py
   ```

La API estará disponible en `http://0.0.0.0:8000`.

### Frontend (Web)

1. Navega al directorio web:
   ```
   cd web
   ```

2. Instala las dependencias:
   ```
   npm install
   # o
   yarn install
   ```

3. Ejecuta el servidor de desarrollo:
   ```
   npm run dev
   # o
   yarn dev
   ```

El frontend estará disponible en `http://localhost:3000`.

## Uso

- La documentación de la API estará disponible en `http://localhost:8000/rdocs`
- Accede a la interfaz web a través de `http://localhost:3000`

## Desarrollo

- Para el backend, los principales archivos de configuración y rutas se encuentran en `api/app/`.
- Para el frontend, los componentes y páginas se encuentran en `web/`.

## Pruebas

### Backend
```
cd api
pytest
```
