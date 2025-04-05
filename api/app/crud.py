# api/app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import text # Per eseguire query SQL testuali in modo sicuro
from collections import defaultdict # Utile per raggruppare facilmente i risultati

def get_annotations_by_filename(db: Session, filename: str) -> dict:
    """
    Interroga il database per recuperare le annotazioni per un nome file video specifico.

    Args:
        db: L'oggetto Sessione SQLAlchemy (fornito da FastAPI/Depends).
        filename: Il nome del file video da cercare.

    Returns:
        Un dizionario dove le chiavi sono i nomi delle persone e i valori sono liste
        contenenti liste [start_time_str, end_time_str].
        Restituisce un dizionario vuoto se il video non viene trovato o non ha annotazioni.
    """
    # Definiamo la query SQL. Usiamo :filename come placeholder (named parameter)
    # per sicurezza (previene SQL Injection). SQLAlchemy lo sostituirà.
    # Usiamo CAST(... AS TEXT) per assicurarci che gli intervalli siano stringhe HH:MM:SS.
    sql_query = text("""
        SELECT
            p.name,
            CAST(a.start_time AS TEXT) AS start_time_str,
            CAST(a.end_time AS TEXT) AS end_time_str
        FROM annotations a
        JOIN people p ON a.person_id = p.id
        JOIN videos v ON a.video_id = v.id
        WHERE v.filename = :filename
        ORDER BY
            p.name,         -- Ordina per nome per raggruppare correttamente
            a.start_time;   -- Ordina gli intervalli di una stessa persona
    """)

    # Eseguiamo la query passando il parametro 'filename'
    try:
        result = db.execute(sql_query, {"filename": filename})
        rows = result.fetchall() # Otteniamo tutte le righe restituite
    except Exception as e:
        # In caso di errore DB, lo stampiamo nei log e restituiamo dizionario vuoto
        # In un'app reale, potresti voler loggare meglio o sollevare un'eccezione specifica
        print(f"Errore durante l'esecuzione della query per filename '{filename}': {e}")
        return {}

    # Se la query non ha restituito righe (video non trovato o senza annotazioni)
    if not rows:
        return {} # Restituiamo un dizionario vuoto

    # Elaboriamo le righe per creare il dizionario nel formato desiderato
    # Usiamo defaultdict(list) per creare automaticamente una lista vuota per ogni nuova persona
    annotations_dict = defaultdict(list)
    for row in rows:
        # Le righe restituite da fetchall() sono simili a tuple. Possiamo accedere
        # per indice (0, 1, 2) o, se l'engine lo supporta, per nome di colonna.
        # Usiamo gli indici per sicurezza.
        person_name = row[0] # p.name
        start_time_str = row[1] # start_time_str
        end_time_str = row[2] # end_time_str

        # Aggiungiamo l'intervallo alla lista della persona corrispondente
        annotations_dict[person_name].append([start_time_str, end_time_str])

    # Convertiamo il defaultdict in un dizionario normale prima di restituirlo
    # (è una buona pratica, anche se FastAPI probabilmente lo gestirebbe comunque)
    return dict(annotations_dict)
