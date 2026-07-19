# Chat en Tiempo Real con Telegram Proyecto UDABOL-PRG-Avanzada-2026

Chat en tiempo real que integra Flask-SocketIO con Telegram Bot, permitiendo comunicación bidireccional entre usuarios web y Telegram.

##  Características

- Chat web en tiempo real usando WebSockets
- Integración con Telegram Bot
- Mensajes bidireccionales (Web ↔ Telegram)
- Interfaz responsive y moderna

##  Requisitos

- Python 3.11+
- Token de Bot de Telegram
- Chat ID de Telegram

##  Instalación Local

1. **Clonar el repositorio Duu **

```sh
git clone <tu-repositorio>
cd chatrealtime
```

2. **Crear entorno virtual en tu entorno**

```sh
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias de .pyy**

```sh
pip install -r requirements.txt
```

4. **Configurar variables de entorno los Enviromentssss**

```sh
cp .env.example .env
# Editar .env con tus credenciales
```

5. **Ejecutar la aplicación**

```sh
python chattelegram.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🐳 Docker tambien lo puedes levantar con Docker

**Construir la imagen:**

```sh
docker build -t chat-realtime .
```

**Ejecutar el contenedor:**

```sh
docker run -p 5000:5000 \
  -e TELEGRAM_TOKEN=tu_token \
  -e TELEGRAM_CHAT_ID=tu_chat_id \
  chat-realtime
```

##  Deploy en Render

1. Crear cuenta en [Render](https://render.com)
2. Conectar tu repositorio de GitHub
3. Crear un nuevo **Web Service**
4. Configurar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python chattelegram.py`
5. Agregar variables de entorno:
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `PORT` (Render lo asigna automáticamente)

##  Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| `TELEGRAM_TOKEN` | Token del Bot de Telegram |
| `TELEGRAM_CHAT_ID` | ID del chat de Telegram |
| `PORT` | Puerto del servidor (default: 5000) |
| `HOST` | Host del servidor (default: 0.0.0.0) |

##  Configurar Bot de Telegram

1. Hablar con [@BotFather](https://t.me/botfather) en Telegram
2. Crear un nuevo bot con `/newbot`
3. Copiar el token proporcionado
4. Para obtener tu Chat ID, envía un mensaje a tu bot y visita:
   ```
   https://api.telegram.org/bot<TU_TOKEN>/getUpdates
   ```

##  Licencia

MIT
