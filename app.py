from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import google.generativeai as genai
import os
from typing import Optional

# =====================================
# KONFIGURATION
# =====================================

app = FastAPI(
    title="FVM GmbH API Gateway",
    description="Sichere API für Google Gemini, Sheets & Drive Integration",
    version="1.0.0"
)

# API-Token aus Environment Variable laden
API_TOKEN = os.getenv("API_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini konfigurieren
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# =====================================
# SICHERHEIT: TOKEN-PRÜFUNG
# =====================================

def verify_token(authorization: str = Header(None)):
    """Prüft ob der API-Token gültig ist"""
    if not authorization:
        raise HTTPException(
            status_code=401, 
            detail="Kein Token bereitgestellt. Header: 'Authorization: Bearer DEIN_TOKEN'"
        )
    
    # Token aus "Bearer XXXXX" extrahieren
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Ungültiges Token-Format. Nutze 'Bearer TOKEN'")
    except ValueError:
        raise HTTPException(status_code=401, detail="Token-Format ungültig")
    
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Ungültiger Token")
    
    return True

# =====================================
# DATENMODELLE
# =====================================

class GeminiRequest(BaseModel):
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class GeminiResponse(BaseModel):
    response: str
    model: str = "gemini-pro"

# =====================================
# ENDPUNKTE
# =====================================

@app.get("/")
def root():
    """Willkommens-Endpunkt"""
    return {
        "message": "FVM GmbH API Gateway ist online! \ud83d\ude80",
        "version": "1.0.0",
        "endpoints": [
            "/api/gemini - KI-Textgenerierung",
            "/health - Status-Check"
        ]
    }

@app.get("/health")
def health_check():
    """Status der API prüfen"""
    return {
        "status": "healthy",
        "api_token_configured": bool(API_TOKEN),
        "google_api_configured": bool(GOOGLE_API_KEY)
    }

@app.post("/api/gemini", response_model=GeminiResponse)
async def generate_text(
    request: GeminiRequest,
    token_valid: bool = Depends(verify_token)
):
    """
    Google Gemini KI-Textgenerierung
    
    Benötigt:
    - Authorization Header mit Bearer Token
    - JSON Body mit 'prompt'
    """
    try:
        # Gemini-Modell initialisieren
        model = genai.GenerativeModel('gemini-pro')
        
        # Text generieren
        response = model.generate_content(
            request.prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens,
            )
        )
        
        return GeminiResponse(
            response=response.text,
            model="gemini-pro"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei Gemini-Anfrage: {str(e)}"
        )

# =====================================
# GOOGLE SHEETS INTEGRATION (Optional)
# =====================================

@app.get("/api/sheets/test")
async def test_sheets_connection(token_valid: bool = Depends(verify_token)):
    """
    Testet die Google Sheets Verbindung
    (Benötigt Service Account Credentials)
    """
    try:
        return {
            "status": "Sheets-Integration noch nicht konfiguriert",
            "info": "Service Account JSON wird benötigt"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =====================================
# FEHLERBEHANDLUNG
# =====================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpunkt nicht gefunden",
        "verfügbare_endpunkte": ["/", "/health", "/api/gemini"]
    }

# =====================================
# SERVER STARTEN (nur lokal)
# =====================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)