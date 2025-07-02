from pydantic import BaseModel
from datetime import datetime
class LibroCreate(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: str = "disponible"  # Valor opcional (si no se envía, usa "disponible")

class LibroResponse(LibroCreate):
    id: int
    fecha_creacion: datetime  # Se convertirá automáticamente desde datetime
    

