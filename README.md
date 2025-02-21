# Python Flask Token System

## Project Overview
A Flask-based token management system with relationship tracking and search capabilities.

## Project Structure
```
.
├── src/           # Source code directory
│   ├── app.py         # Main Flask application
│   └── token_system.py # Token management system
├── tests/         # Test directory
├── Procfile       # Railway deployment configuration
├── runtime.txt    # Python runtime specification
└── requirements.txt # Project dependencies
```

## Local Development
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/app.py
   ```

## Deployment on Railway

1. Fork this repository to your GitHub account

2. Visit [Railway](https://railway.app/) and sign in with your GitHub account

3. Click on "New Project" and select "Deploy from GitHub repo"

4. Choose this repository from the list

5. Railway will automatically:
   - Detect the Python runtime from runtime.txt
   - Install dependencies from requirements.txt
   - Start the application using the Procfile

6. Once deployed, you can access your API at the provided Railway URL

## Environment Variables
No environment variables are required for basic functionality.

## API Documentation

### Add Token
```http
POST /tokens
Content-Type: application/json

{
  "token": "string",
  "category": "string",
  "metadata": {}
}
```

### Add Relationship
```http
POST /tokens/relationship
Content-Type: application/json

{
  "token1": "string",
  "token2": "string",
  "type": "string"
}
```

### Search Tokens
```http
GET /tokens/search?q=query&n=5
```

### Get Token Info
```http
GET /tokens/{token}
```

## Herramientas Incluidas

- **pytest**: Para testing
- **python-dotenv**: Para manejar variables de entorno
- **flake8**: Para linting de código
- **black**: Para formateo de código
- **ipython**: Shell interactiva mejorada

## Uso

1. Activa el entorno virtual:
   ```bash
   source venv/bin/activate
   ```

2. Ejecuta tu código:
   ```bash
   python src/tu_programa.py
   ```

3. Para ejecutar tests:
   ```bash
   pytest
   ```

4. Para formatear código:
   ```bash
   black src/
   ```

5. Para verificar el estilo del código:
   ```bash
   flake8 src/
   ```