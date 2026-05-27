# 📋 Guía Completa de Deploy

## ✅ PASO 1: Verificar Entorno Virtual

```sh
# Si no existe el entorno virtual, créalo:
python3 -m venv venv

# Activar entorno virtual:
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

# Instalar dependencias:
pip install -r requirements.txt
```

## ✅ PASO 2: Probar Localmente

```sh
# Asegúrate de que el archivo .env tiene tus credenciales correctas
python chattelegram.py
```

```text
/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python: can't open file '/private/var/folders/pm/6l_47zk12nz8565n0y1jctcw0000gn/T/mdlab/chattelegram.py': [Errno 2] No such file or directory
```

Abre tu navegador en `http://localhost:5000` y verifica que funciona.

## ✅ PASO 3: Subir a GitHub

```sh
# Ver archivos preparados
git status

# Hacer commit
git commit -m "Initial commit: Chat en tiempo real con Telegram"

# Crear repositorio en GitHub (ve a github.com y crea un nuevo repo)
# Luego conecta tu repo local:
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git

# Subir a GitHub
git push -u origin main
```

## ✅ PASO 4: Deploy en Render

### Opción A: Deploy con Docker (Recomendado)

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name:** chat-realtime (o el que prefieras)
   - **Environment:** Docker
   - **Plan:** Free
5. **Variables de Entorno** (Add Environment Variables):
   ```
   TELEGRAM_TOKEN = tu_token_aqui
   TELEGRAM_CHAT_ID = tu_chat_id_aqui
   ```
6. Click en **"Create Web Service"**

### Opción B: Deploy sin Docker

1. Ve a [render.com](https://render.com)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name:** chat-realtime
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python chattelegram.py`
   - **Plan:** Free
5. **Variables de Entorno:**
   ```
   TELEGRAM_TOKEN = tu_token_aqui
   TELEGRAM_CHAT_ID = tu_chat_id_aqui
   ```
6. Click en **"Create Web Service"**

## 🔍 Verificar Deploy

Una vez desplegado, Render te dará una URL como:
```
https://chat-realtime-xxxx.onrender.com
```

Abre esa URL en tu navegador y prueba el chat.

## 🐛 Troubleshooting

### Error: "Application failed to respond"
- Verifica que las variables de entorno estén configuradas correctamente
- Revisa los logs en Render Dashboard

### Error: "Telegram bot not responding"
- Verifica que el token de Telegram sea correcto
- Asegúrate de que el bot esté activo en Telegram

### El chat web funciona pero Telegram no
- Verifica el TELEGRAM_CHAT_ID
- Envía un mensaje a tu bot y obtén el chat_id desde:
  ```
  https://api.telegram.org/bot<TU_TOKEN>/getUpdates
  ```

## 📱 Probar la Integración

1. Abre la URL de Render en tu navegador
2. Ingresa tu nombre y envía un mensaje
3. El mensaje debe aparecer en tu chat de Telegram
4. Responde desde Telegram
5. La respuesta debe aparecer en el chat web

## 🎉 ¡Listo!

Tu chat en tiempo real está funcionando en producción.

## 📝 Notas Importantes

- **Plan Free de Render:** El servicio se "duerme" después de 15 minutos de inactividad
- **Primera carga:** Puede tardar 30-60 segundos en despertar
- **WebSockets:** Render soporta WebSockets en todos los planes
- **Logs:** Puedes ver los logs en tiempo real desde el dashboard de Render