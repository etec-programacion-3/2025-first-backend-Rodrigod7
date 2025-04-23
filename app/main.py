from fastapi import FastAPI, HTTPException  
from app.models import Libro
from app.schemas import LibroCreate, LibroResponse
from app.database import init_db

app = FastAPI(title="API Biblioteca", version="1.0")

# Inicializar la base de datos al iniciar la app
@app.on_event("startup")
async def startup():
    await init_db()

# Endpoint para crear un libro
@app.post("/libros", response_model=LibroResponse)
async def crear_libro(libro: LibroCreate):
    nuevo_libro = await Libro.create(**libro.dict())
    return nuevo_libro

# Endpoint para listar todos los libros
@app.get("/libros", response_model=list[LibroResponse])
async def listar_libros():
    return await Libro.all()

# Endpoint para obtener un libro por ID
@app.get("/libros/{id}", response_model=LibroResponse)
async def obtener_libro(id: int):
    libro = await Libro.get_or_none(id=id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

# Endpoint para actualizar un libro
@app.put("/libros/{id}", response_model=LibroResponse)
async def actualizar_libro(id: int, libro: LibroCreate):
    existe = await Libro.filter(id=id).exists()
    if not existe:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    await Libro.filter(id=id).update(**libro.dict())
    return await Libro.get(id=id)

# Endpoint para eliminar un libro
@app.delete("/libros/{id}")
async def eliminar_libro(id: int):
    eliminado = await Libro.filter(id=id).delete()
    if not eliminado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"mensaje": "Libro eliminado"}
from fastapi import Query

@app.get("/libros/buscar", response_model=list[LibroResponse])
async def buscar_libros(
    titulo: str = Query(None),
    autor: str = Query(None),
    categoria: str = Query(None)
):
    query = Libro.all()
    if titulo:
        query = query.filter(titulo__icontains=titulo)  # Búsqueda parcial insensible a mayúsculas
    if autor:
        query = query.filter(autor__icontains=autor)
    if categoria:
        query = query.filter(categoria=categoria)
    return await query