from flask import Flask, render_template
from flask_socketio import SocketIO, send
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes
)

import threading
import requests
import os
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


# PAGINA PRINCIPAL


@app.route("/")
def index():
    return render_template('index.html')

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


# ENVIAR A TELEGRAM


def enviarTelegram(mensaje):

    url = (
        f"https://api.telegram.org/bot"
        f"{tokenTelegram}/sendMessage"
    )

    data = {
        "chat_id": chatID,
        "text": f"{mensaje}"
    }

    try:

        requests.post(url, data=data)

    except Exception as e:

        print("Error Telegram:", e)


# RECIBIR DESDE TELEGRAM


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
    
    # Crear un nuevo event loop para este thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
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
    loop.run_until_complete(botTelegram.updater.start_polling())
    
    # Mantener el loop corriendo
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(botTelegram.updater.stop())
        loop.run_until_complete(botTelegram.stop())
        loop.run_until_complete(botTelegram.shutdown())
        loop.close()


# MAIN


if __name__ == "__main__":

    hiloBot = threading.Thread(
        target=iniciarBot
    )

    hiloBot.start()

    print("Servidor iniciado")

    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")

    socket.run(
        app,
        host=host,
        port=port
    )