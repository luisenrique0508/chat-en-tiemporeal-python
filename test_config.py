#!/usr/bin/env python3
"""
Script para verificar la configuración antes del deploy
"""

import os
from dotenv import load_dotenv

def verificar_configuracion():
    print("🔍 Verificando configuración...\n")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar variables
    errores = []
    
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    print("📋 Variables de entorno:")
    print("-" * 50)
    
    if telegram_token:
        # Ocultar parte del token por seguridad
        token_oculto = telegram_token[:10] + "..." + telegram_token[-10:]
        print(f"✅ TELEGRAM_TOKEN: {token_oculto}")
    else:
        print("❌ TELEGRAM_TOKEN: NO CONFIGURADO")
        errores.append("TELEGRAM_TOKEN no está configurado")
    
    if chat_id:
        print(f"✅ TELEGRAM_CHAT_ID: {chat_id}")
    else:
        print("❌ TELEGRAM_CHAT_ID: NO CONFIGURADO")
        errores.append("TELEGRAM_CHAT_ID no está configurado")
    
    port = os.getenv("PORT", "5000")
    print(f"✅ PORT: {port}")
    
    host = os.getenv("HOST", "0.0.0.0")
    print(f"✅ HOST: {host}")
    
    print("-" * 50)
    
    # Verificar dependencias
    print("\n📦 Verificando dependencias...")
    print("-" * 50)
    
    dependencias = [
        "flask",
        "flask_socketio",
        "telegram",
        "requests",
        "eventlet",
        "dotenv"
    ]
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NO INSTALADO")
            errores.append(f"Dependencia {dep} no instalada")
    
    print("-" * 50)
    
    # Resultado final
    print("\n" + "=" * 50)
    if errores:
        print("❌ CONFIGURACIÓN INCOMPLETA")
        print("\nErrores encontrados:")
        for error in errores:
            print(f"  • {error}")
        print("\n💡 Solución:")
        print("  1. Verifica que el archivo .env existe")
        print("  2. Configura las variables faltantes")
        print("  3. Instala dependencias: pip install -r requirements.txt")
        return False
    else:
        print("✅ CONFIGURACIÓN CORRECTA")
        print("\n🚀 Todo listo para ejecutar:")
        print("   python chattelegram.py")
        return True
    print("=" * 50)

if __name__ == "__main__":
    verificar_configuracion()
