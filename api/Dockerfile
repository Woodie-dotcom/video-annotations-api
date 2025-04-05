# Fase 1: Scegliere un'immagine Python di base ufficiale e leggera
FROM python:3.11-slim

# Impostare variabili d'ambiente utili
# PYTHONDONTWRITEBYTECODE: Evita che Python scriva file .pyc (non servono nel container)
# PYTHONUNBUFFERED: Assicura che l'output di Python (print, log) appaia immediatamente nei log Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Impostare la directory di lavoro all'interno del container
WORKDIR /app

# Copiare *solo* il file delle dipendenze per sfruttare la cache Docker
COPY requirements.txt .

# Installare le dipendenze Python
# --no-cache-dir: Non salvare la cache di pip (riduce dimensione immagine)
# -r requirements.txt: Installa le librerie elencate nel file
RUN pip install --no-cache-dir -r requirements.txt

# Copiare il resto del codice dell'applicazione nella directory di lavoro (/app)
# Copiamo la cartella 'app' locale nella cartella '/app/app' del container
COPY ./app /app/app

# Esponi la porta su cui Uvicorn/FastAPI sarà in ascolto all'interno del container
# Nota: La mappatura alla porta host avviene nel docker-compose.yml
EXPOSE 8000

# Comando per avviare l'applicazione quando il container parte
# Esegue uvicorn, puntando all'oggetto 'app' nel file 'app/main.py'
# --host 0.0.0.0: Rende il server accessibile dall'esterno del container (necessario per Docker)
# --port 8000: Specifica la porta interna (corrisponde a EXPOSE)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
