#!/bin/bash

echo "🚀 Configurando Chat en Tiempo Real..."

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "✅ Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar archivo .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "⚙️  Por favor, edita el archivo .env con tus credenciales de Telegram"
else
    echo "✅ Archivo .env encontrado"
fi

echo ""
echo "✨ Configuración completada!"
echo ""
echo "Para ejecutar la aplicación:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Ejecuta: python chattelegram.py"
echo ""
