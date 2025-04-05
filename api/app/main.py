# api/app/main.py

import os
from fastapi import FastAPI, Depends, HTTPException # Aggiungi Depends e HTTPException
from urllib.parse import urlparse, urlunparse

# Import per SQLAlchemy (interazione DB)
from sqlalchemy import create_engine, text # Aggiungi create_engine, text
from sqlalchemy.orm import sessionmaker, Session # Aggiungi sessionmaker, Session

# Importa funzioni/modelli da altri file dell'app
from . import crud # Importa il modulo crud (che creeremo tra poco)
from . import models # Importa il modulo models

# --- Configurazione Database ---
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ATTENZIONE: Variabile d'ambiente DATABASE_URL non trovata! Impossibile connettersi al DB.")
    # Potresti voler far fallire l'avvio qui in un'app reale
    # exit(1) # Rimuovi il commento per uscire se manca DATABASE_URL
    # Per ora, impostiamo un valore dummy per permettere l'avvio, ma le chiamate al DB falliranno
    DATABASE_URL = "postgresql://user:password@host:port/db" # Valore fittizio

# Crea l'engine SQLAlchemy
# - connect_args: Opzioni specifiche per il driver (psycopg2)
# - pool_pre_ping: Verifica la connessione prima di usarla dal pool (aiuta con connessioni interrotte)
engine = create_engine(DATABASE_URL, connect_args={}, pool_pre_ping=True)

# Crea una SessionLocal class configurata
# - autocommit=False: Le modifiche non vengono committate automaticamente
# - autoflush=False: Non invia automaticamente le modifiche pendenti al DB
# - bind=engine: Associa questa session factory all'engine creato
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Funzione Dependency per ottenere la sessione DB ---
def get_db():
    """
    Dependency di FastAPI che crea e fornisce una sessione di database per richiesta.
    Assicura che la sessione venga chiusa correttamente dopo l'uso.
    """
    db = SessionLocal()
    try:
        yield db # Fornisce la sessione alla funzione dell'endpoint
    finally:
        db.close() # Chiude la sessione quando la richiesta è finita

# --- Crea Istanza FastAPI ---
app = FastAPI(title="Video Annotations API", version="0.1.0") # Aggiunta versione

# (Stampa di verifica DATABASE_URL - come prima)
if DATABASE_URL and "user:password@host" not in DATABASE_URL: # Non stampare il valore fittizio
    try:
        parsed_url = urlparse(DATABASE_URL)
        safe_url = urlunparse(parsed_url._replace(netloc=f"{parsed_url.username}:***@{parsed_url.hostname}:{parsed_url.port}"))
        print(f"INFO:     DATABASE_URL letto correttamente: {safe_url}")
    except Exception as e:
        print(f"WARNING:  Errore nel parsing di DATABASE_URL: {e}")
        print(f"INFO:     DATABASE_URL trovato ma non stampato per sicurezza.")
else:
     if "user:password@host" in DATABASE_URL:
         print("ATTENZIONE: DATABASE_URL non configurato, usando valore fittizio.")

# === Endpoint Esistenti ===

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Benvenuto/a nella Video Annotations API. Visita /docs per la documentazione interattiva."}


# === NUOVO Endpoint per le Annotazioni ===

# Definiamo il percorso, il metodo GET, e il modello di risposta atteso
@app.get("/api/v1/annotations",
         response_model=models.AnnotationsResponse, # Usa il modello definito in models.py
         tags=["Annotations"]) # Raggruppa nella documentazione
async def get_video_annotations(
    filename: str, # Accetta 'filename' come query parameter obbligatorio (es. ?filename=video.mp4)
    db: Session = Depends(get_db) # Inietta la sessione DB usando la dependency 'get_db'
    ):
    """
    Recupera le annotazioni (nomi persona e intervalli di tempo) per un dato video.

    Richiede il parametro `filename` nella query string.
    """
    # Chiama la funzione nel modulo 'crud' per ottenere i dati dal DB
    annotations = crud.get_annotations_by_filename(db=db, filename=filename)

    # Se la funzione crud restituisce None (o un dizionario vuoto),
    # significa che il video non è stato trovato o non ha annotazioni.
    # In questo caso, solleviamo un'eccezione HTTP 404.
    if not annotations: # Verifica se il dizionario è vuoto o None
        raise HTTPException(status_code=404, detail=f"Annotations not found for filename: {filename}")

    # Se tutto va bene, restituisce i dati. FastAPI li convertirà in JSON
    # e verificherà che corrispondano al modello 'AnnotationsResponse'.
    return annotations
