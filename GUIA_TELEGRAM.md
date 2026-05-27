# 🤖 Guía del Bot de Telegram y Comandos Personalizados

Esta guía explica el funcionamiento del puente entre Flask y Telegram, y cómo puedes expandir el bot agregando comandos interactivos.

---

## 1. Arquitectura de Funcionamiento

El servidor local realiza dos tareas simultáneas mediante hilos (`threading`):
1. **Servidor Flask + Socket.IO**: Escucha y transmite mensajes en tiempo real en la web (`http://localhost:8080`).
2. **Poller de Telegram**: Escucha mensajes en el chat de Telegram usando el token configurado en tu archivo `.env`.

---

## 2. Cómo Crear Comandos de Telegram

Para crear comandos como `/ayuda` o `/info` en Telegram y hacer que respondan al usuario o se reflejen en la web, debes modificar el archivo `chattelegram.py`.

### Paso 1: Importar el CommandHandler
Asegúrate de importar `CommandHandler` de `telegram.ext` en la parte superior de `chattelegram.py`:
```python
from telegram.ext import CommandHandler
```

### Paso 2: Definir las funciones del comando
Crea las funciones asíncronas para manejar cada comando. Por ejemplo, agrega estas funciones antes de `iniciarBot()`:

```python
# Comando /start
async def comandoStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy el Bot de sincronización del chat. "
        "Usa /ayuda para ver los comandos disponibles."
    )

# Comando /ayuda
async def comandoAyuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - Iniciar interacción\n"
        "/ayuda - Ver esta ayuda\n"
        "/anunciar [mensaje] - Enviar un anuncio importante a la Web"
    )

# Comando /anunciar (envía un mensaje especial de sistema a la web)
async def comandoAnunciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtener el texto después de /anunciar
    mensaje = " ".join(context.args)
    if not mensaje:
        await update.message.reply_text("Uso correcto: /anunciar [tu mensaje]")
        return
        
    texto_anuncio = f"📢 ANUNCIO: {mensaje}"
    # Emitir a la interfaz web mediante socket
    socket.emit("telegram_message", f"Sistema: {texto_anuncio}")
    await update.message.reply_text("¡Anuncio enviado a la interfaz web!")
```

### Paso 3: Registrar los comandos en el bot
Busca la función `iniciarBot()` en `chattelegram.py` y registra tus nuevos controladores de comandos **antes** del controlador de texto general (`MessageHandler`):

```python
        # Registrar comandos
        botTelegram.add_handler(CommandHandler("start", comandoStart))
        botTelegram.add_handler(CommandHandler("ayuda", comandoAyuda))
        botTelegram.add_handler(CommandHandler("anunciar", comandoAnunciar))
        
        # Filtro de texto normal (ignora comandos)
        botTelegram.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                recibirTelegram
            )
        )
```

---

## 3. Resolviendo Conflictos de Bot

Si ves este error en consola:
> `telegram.error.Conflict: Conflict: terminated by other getUpdates request`

Significa que el bot está activo en dos lados a la vez con el mismo `TELEGRAM_TOKEN`.
- **Solución**: Asegúrate de apagar cualquier otra terminal en local que esté corriendo `chattelegram.py` o apaga temporalmente el servicio web en Render si estás haciendo pruebas locales de desarrollo.
