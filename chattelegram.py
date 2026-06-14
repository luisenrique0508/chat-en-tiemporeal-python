from flask import Flask, render_template
from flask_socketio import SocketIO, send
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes
)

import threading
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# CONFIGURACION TELEGRAM

tokenTelegram = os.getenv("TELEGRAM_TOKEN")
chatID = os.getenv("TELEGRAM_CHAT_ID")


# CREAR APP


app = Flask(__name__)


# CONFIGURAR SOCKETIO


socket = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading'
)


# CREAR BOT TELEGRAM


botTelegram = ApplicationBuilder().token(
    tokenTelegram
).build()


# Contador de usuarios web conectados
usuarios_web = 0


# PAGINA PRINCIPAL


@app.route("/")
def index():
    return render_template('index.html')


# Rastrear conexiones web
@socket.on("connect")
def handle_connect():
    global usuarios_web
    usuarios_web += 1
    print(f"Usuario web conectado. Total: {usuarios_web}")


@socket.on("disconnect")
def handle_disconnect():
    global usuarios_web
    usuarios_web = max(0, usuarios_web - 1)
    print(f"Usuario web desconectado. Total: {usuarios_web}")


# MENSAJES DESDE WEB


@socket.on("message")
def recibirMensaje(mensaje):

    print("Mensaje WEB:", mensaje)

    # Mostrar a todos los clientes WEB
    send(mensaje, broadcast=True)

    # Enviar a Telegram
    threading.Thread(
        target=enviarTelegram,
        args=(mensaje,)
    ).start()

    # Procesar comandos del bot si vienen de la web
    partes = mensaje.split(": ", 1)
    if len(partes) == 2 and partes[1].startswith("/"):
        comando = partes[1].split()[0]
        respuesta_bot = None
        
        if comando == "/start":
            respuesta_bot = (
                "🤖 ¡Hola! Soy el Bot del Chat en Tiempo Real.\n\n"
                "Estoy conectado y sincronizando mensajes entre Telegram y la Web.\n\n"
                "Escribe /ayuda para ver los comandos."
            )
        elif comando == "/ayuda":
            respuesta_bot = (
                "📋 *Comandos Disponibles:*\n\n"
                "🟢 /start - Iniciar el bot\n"
                "❓ /ayuda - Ver esta ayuda\n"
                "📡 /estado - Ver estado del servidor\n"
                "📢 /anunciar [mensaje] - Enviar anuncio a la Web\n"
                "👥 /usuarios - Ver usuarios web conectados\n"
                "🏓 /ping - Verificar que el bot responde"
            )
        elif comando == "/estado":
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            host = os.getenv("RENDER_EXTERNAL_URL", "localhost")
            respuesta_bot = (
                f"📡 *Estado del Servidor*\n\n"
                f"🟢 Bot: Activo\n"
                f"🟢 Servidor Web: Activo\n"
                f"🌐 URL: {host}\n"
                f"👥 Usuarios web: {usuarios_web}\n"
                f"🕐 Hora servidor: {ahora}"
            )
        elif comando == "/ping":
            respuesta_bot = "🏓 ¡Pong! El bot está vivo y funcionando."
        elif comando == "/usuarios":
            respuesta_bot = f"👥 Usuarios conectados en la web: {usuarios_web}"
        elif comando == "/anunciar":
            anuncio = partes[1].replace("/anunciar", "").strip()
            if not anuncio:
                respuesta_bot = "⚠️ Uso correcto: /anunciar [tu mensaje]\nEjemplo: /anunciar ¡Reunión a las 8pm!"
            else:
                texto_anuncio = f"📢 ANUNCIO: {anuncio}"
                # Emitir a la interfaz web (esto ya se hace como Sistema)
                socket.emit("telegram_message", f"Sistema: {texto_anuncio}")
                respuesta_bot = f"✅ Anuncio enviado a la web:\n{texto_anuncio}"

        if respuesta_bot:
            texto_sistema = f"Sistema: {respuesta_bot}"
            # Emitir a la web
            socket.emit("telegram_message", texto_sistema)
            # Enviar a Telegram para que también se vea la respuesta del bot ahí
            threading.Thread(
                target=enviarTelegram,
                args=(texto_sistema,)
            ).start()



# ENVIAR A TELEGRAM


def enviarTelegram(mensaje):

    url = (
        f"https://api.telegram.org/bot"
        f"{tokenTelegram}/sendMessage"
    )

    data = {
        "chat_id": chatID,
        "text": f"💬 {mensaje}"
    }

    try:

        requests.post(url, data=data)

    except Exception as e:

        print("Error Telegram:", e)


# =============================================
# COMANDOS DE TELEGRAM
# =============================================


# /start - Saludo inicial del bot
async def comandoStart(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        " ¡Hola! Soy el Bot del Chat en Tiempo Real.\n\n"
        "Estoy conectado y sincronizando mensajes "
        "entre Telegram y la Web.\n\n"
        "Escribe /ayuda para ver los comandos."
    )


# /ayuda - Lista de comandos disponibles
async def comandoAyuda(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📋 *Comandos Disponibles:*\n\n"
        "🟢 /start - Iniciar el bot\n"
        "❓ /ayuda - Ver esta ayuda\n"
        "📡 /estado - Ver estado del servidor\n"
        "📢 /anunciar [mensaje] - Enviar anuncio a la Web\n"
        "👥 /usuarios - Ver usuarios web conectados\n"
        "🏓 /ping - Verificar que el bot responde",
        parse_mode="Markdown"
    )


# /estado - Estado del servidor y bot
async def comandoEstado(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    host = os.getenv("RENDER_EXTERNAL_URL", "localhost")

    await update.message.reply_text(
        f"📡 *Estado del Servidor*\n\n"
        f"🟢 Bot: Activo\n"
        f"🟢 Servidor Web: Activo\n"
        f"🌐 URL: {host}\n"
        f"👥 Usuarios web: {usuarios_web}\n"
        f"🕐 Hora servidor: {ahora}",
        parse_mode="Markdown"
    )


# /ping - Respuesta rápida para verificar conexión
async def comandoPing(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🏓 ¡Pong! El bot está vivo y funcionando."
    )


# /usuarios - Cuántos hay conectados en la web
async def comandoUsuarios(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        f"👥 Usuarios conectados en la web: {usuarios_web}"
    )


# /anunciar - Enviar anuncio a la interfaz web
async def comandoAnunciar(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    mensaje = " ".join(context.args)

    if not mensaje:
        await update.message.reply_text(
            "⚠️ Uso correcto: /anunciar [tu mensaje]\n"
            "Ejemplo: /anunciar ¡Reunión a las 8pm!"
        )
        return

    texto_anuncio = f"📢 ANUNCIO: {mensaje}"

    # Emitir a la interfaz web
    socket.emit(
        "telegram_message",
        f"Sistema: {texto_anuncio}"
    )

    await update.message.reply_text(
        f"✅ Anuncio enviado a la web:\n{texto_anuncio}"
    )


# =============================================
# RECIBIR MENSAJES NORMALES DESDE TELEGRAM
# =============================================


async def recibirTelegram(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    usuario = update.message.from_user.first_name

    mensaje = update.message.text

    texto = f"{usuario}: {mensaje}"

    print("Telegram:", texto)

    # SOLO enviar a WEB
    socket.emit(
        "telegram_message",
        texto
    )


# INICIAR BOT


def iniciarBot():
    import asyncio

    try:
        # Crear un nuevo event loop para este thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Registrar comandos PRIMERO
        botTelegram.add_handler(
            CommandHandler("start", comandoStart)
        )
        botTelegram.add_handler(
            CommandHandler("ayuda", comandoAyuda)
        )
        botTelegram.add_handler(
            CommandHandler("estado", comandoEstado)
        )
        botTelegram.add_handler(
            CommandHandler("ping", comandoPing)
        )
        botTelegram.add_handler(
            CommandHandler("usuarios", comandoUsuarios)
        )
        botTelegram.add_handler(
            CommandHandler("anunciar", comandoAnunciar)
        )

        # Mensajes de texto normales (después de comandos)
        botTelegram.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                recibirTelegram
            )
        )

        print("BOT TELEGRAM ACTIVO")

        # Ejecutar el bot en el event loop
        loop.run_until_complete(botTelegram.initialize())
        loop.run_until_complete(botTelegram.start())
        loop.run_until_complete(
            botTelegram.updater.start_polling()
        )

        # Mantener el loop corriendo
        loop.run_forever()
    except Exception as e:
        print(f"Error en bot de Telegram: {e}")
    finally:
        try:
            if loop and not loop.is_closed():
                loop.run_until_complete(
                    botTelegram.updater.stop()
                )
                loop.run_until_complete(botTelegram.stop())
                loop.run_until_complete(
                    botTelegram.shutdown()
                )
                loop.close()
        except:
            pass


# MAIN


if __name__ == "__main__":

    hiloBot = threading.Thread(
        target=iniciarBot,
        daemon=True
    )

    hiloBot.start()

    print("Servidor iniciado")

    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")

    socket.run(
        app,
        host=host,
        port=port,
        allow_unsafe_werkzeug=True
    )