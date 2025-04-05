# api/app/models.py

from pydantic import BaseModel
from typing import List, Dict

# Definiamo un modello Pydantic per la struttura della risposta JSON.
# Questo aiuta FastAPI a validare l'output e a generare una documentazione precisa.
# Ci aspettiamo un dizionario dove le chiavi sono stringhe (nomi persona)
# e i valori sono liste di liste di stringhe (ogni sotto-lista è [start_time, end_time])
AnnotationsResponse = Dict[str, List[List[str]]]

# Potremmo anche definire modelli più dettagliati se necessario, ad esempio:
# class TimeInterval(BaseModel):
#     start_time: str
#     end_time: str
#
# class PersonAnnotation(BaseModel):
#     intervals: List[TimeInterval]
#
# AnnotationsResponse = Dict[str, PersonAnnotation]
# Ma per ora, il tipo Dict[...] è sufficiente per rappresentare il JSON richiesto.
