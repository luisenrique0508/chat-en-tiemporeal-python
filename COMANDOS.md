# 🎯 Comandos para Ejecutar Ahora

## 📦 PASO 1: Instalar Dependencias

```bash
# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

## ✅ PASO 2: Verificar Configuración

```bash
# Ejecutar script de verificación
python test_config.py
```

Si todo está bien, verás ✅ en todas las líneas.

## 🚀 PASO 3: Probar Localmente

```bash
# Ejecutar la aplicación
python chattelegram.py
```

Abre tu navegador en: http://localhost:5000

## 📤 PASO 4: Subir a GitHub

```bash
# Ver archivos preparados
git status

# Hacer el primer commit
git commit -m "Initial commit: Chat en tiempo real con Telegram"

# Crear repositorio en GitHub (hazlo desde github.com)
# Luego ejecuta estos comandos (reemplaza con tu URL):

git remote add origin https://github.com/TU_USUARIO/chat-realtime.git
git branch -M main
git push -u origin main
```

## 🌐 PASO 5: Deploy en Render

### Desde la Web de Render:

1. Ve a https://render.com
2. Haz clic en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Environment:** Docker
   - **Plan:** Free
5. Agrega estas variables de entorno:
   ```
   TELEGRAM_TOKEN = 8671619795:AAEM_vQBPMgxKLhvDIcQrFp-yeQ3Ign5w9o
   TELEGRAM_CHAT_ID = 1477558390
   ```
6. Haz clic en "Create Web Service"

## 🐳 ALTERNATIVA: Probar con Docker Localmente

```bash
# Construir la imagen
docker build -t chat-realtime .

# Ejecutar el contenedor
docker run -p 5000:5000 \
  -e TELEGRAM_TOKEN="8671619795:AAEM_vQBPMgxKLhvDIcQrFp-yeQ3Ign5w9o" \
  -e TELEGRAM_CHAT_ID="1477558390" \
  chat-realtime
```

## 🔍 Comandos Útiles

```bash
# Ver logs en tiempo real (si usas Docker)
docker logs -f <container_id>

# Detener la aplicación
Ctrl + C

# Desactivar entorno virtual
deactivate

# Ver puertos en uso
lsof -i :5000

# Matar proceso en puerto 5000 (si está ocupado)
kill -9 $(lsof -t -i:5000)
```

## 📋 Checklist Final

- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Archivo .env configurado
- [ ] test_config.py ejecutado sin errores
- [ ] Aplicación probada localmente
- [ ] Commit realizado en Git
- [ ] Repositorio creado en GitHub
- [ ] Código subido a GitHub
- [ ] Web Service creado en Render
- [ ] Variables de entorno configuradas en Render
- [ ] Deploy exitoso en Render
- [ ] Aplicación funcionando en producción

## 🎉 ¡Listo!

Una vez completados todos los pasos, tu chat estará funcionando en:
- **Local:** http://localhost:5000
- **Producción:** https://tu-app.onrender.com
