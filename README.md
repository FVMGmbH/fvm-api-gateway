# FVM GmbH API Gateway 🚀

**Sichere FastAPI für Google Gemini & Sheets Integration**

## ⚡ Schnellstart (Lokal)

### 1. Repository klonen
```bash
git clone https://github.com/FVMGmbH/fvm-api-gateway.git
cd fvm-api-gateway
```

### 2. Python-Umgebung erstellen
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 4. API-Keys konfigurieren

**a) `.env`-Datei erstellen:**
```bash
cp .env.example .env
```

**b) `.env` bearbeiten und Keys eintragen:**
```env
API_TOKEN=dein-eigener-sicherer-token
GOOGLE_API_KEY=AIzaSy...
```

💡 **Google Gemini API Key holen:**
- Gehe zu https://makersuite.google.com/app/apikey
- Erstelle neuen API Key
- Kopiere in `.env`

### 5. Server starten
```bash
python app.py
```

✅ **Server läuft auf:** http://localhost:8000

---

## 📖 API-Dokumentation

### Interaktive Docs
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpunkte

#### `GET /` - Status
Prüft ob die API online ist.

#### `GET /health` - Gesundheitscheck
Zeigt Konfigurationsstatus.

#### `POST /api/gemini` - KI-Textgenerierung

**Header:**
```
Authorization: Bearer DEIN_API_TOKEN
```

**Body:**
```json
{
  "prompt": "Erkläre Haftpflichtversicherung in 3 Sätzen",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Beispiel mit cURL:**
```bash
curl -X POST "http://localhost:8000/api/gemini" \
  -H "Authorization: Bearer dein-token" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Was ist eine PHV?"}'
```

---

## 🌐 Deployment (Render.com)

### Schritt 1: Repository verbinden
1. Gehe zu https://render.com
2. Erstelle **New Web Service**
3. Verbinde GitHub → **FVMGmbH/fvm-api-gateway**

### Schritt 2: Konfiguration

| Einstellung | Wert |
|------------|------|
| **Name** | `fvm-api-gateway` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |

### Schritt 3: Environment Variables

Füge hinzu:
```
API_TOKEN=dein-production-token
GOOGLE_API_KEY=dein-gemini-key
```

### Schritt 4: Deployen
Klick **Create Web Service** → Fertig! 🎉

Deine API ist online unter: `https://fvm-api-gateway.onrender.com`

---

## 🔒 Sicherheit

- ✅ Token-basierte Authentifizierung
- ✅ `.gitignore` schützt Secrets
- ✅ HTTPS bei Render.com
- ✅ Environment Variables für Keys

---

## 🛠️ Entwicklung

### Tests lokal ausführen
```bash
# Server starten
python app.py

# In anderem Terminal:
curl http://localhost:8000/health
```

### Code-Struktur
```
fvm-api-gateway/
├── app.py              # Haupt-API
├── requirements.txt    # Python-Pakete
├── .env               # Lokale Secrets (nicht in Git!)
├── .env.example       # Template für .env
├── .gitignore         # Schützt sensible Dateien
└── README.md          # Diese Datei
```

---

## 📞 Support

**Entwickelt für:** FVM GmbH Versicherungsmakler
**Tech-Stack:** FastAPI + Google Gemini + Render.com