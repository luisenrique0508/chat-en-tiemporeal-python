# 🚀 INICIO RÁPIDO - 5 Minutos

## 1️⃣ Instalar (2 min)

```sh
source venv/bin/activate
pip install -r requirements.txt
```

## 2️⃣ Probar (1 min)

```sh
python chattelegram.py
```

Abre: http://localhost:5000

## 3️⃣ Subir a GitHub (1 min)

```sh
git commit -m "Initial commit: Chat en tiempo real"
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

## 4️⃣ Deploy en Render (1 min)

1. Ve a https://render.com
2. New + → Web Service
3. Conecta tu repo de GitHub
4. Environment: **Docker**
5. Variables de entorno:
   ```
   TELEGRAM_TOKEN = 8671619795:AAEM_vQBPMgxKLhvDIcQrFp-yeQ3Ign5w9o
   TELEGRAM_CHAT_ID = 1477558390
   ```
6. Create Web Service

##  ¡Listo!

Tu chat estará en: `https://tu-app.onrender.com`