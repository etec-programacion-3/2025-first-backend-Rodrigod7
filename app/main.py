from fastapi import FastAPI, HTTPException  
from app.models import Libro
from app.schemas import LibroCreate, LibroResponse
from app.database import init_db
from fastapi import Query
from fastapi import Query, HTTPException
from tortoise.expressions import Q
app = FastAPI(title="API Biblioteca", version="1.0")

# Inicializar la base de datos al iniciar la app
@app.on_event("startup")
async def startup():
    await init_db()

# Endpoint para crear un libro
@app.post("/libros", response_model=LibroResponse, status_code=201)
async def crear_libro(libro: LibroCreate):
    existente = await Libro.filter(isbn=libro.isbn).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un libro con ese ISBN.")
    nuevo_libro = await Libro.create(**libro.dict())
    return nuevo_libro

# Endpoint para listar todos los libros
@app.get("/libros", response_model=list[LibroResponse])
async def listar_libros():
    return await Libro.all()

@app.get("/libros/buscar", response_model=list[LibroResponse])
async def buscar_libros(
    titulo: str = Query(None),
    autor: str = Query(None),
    categoria: str = Query(None),
    orden: str = Query("id"),  # Campo por el cual ordenar
    limite: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    query = Libro.all()

    # Filtros
    if titulo:
        query = query.filter(titulo__icontains=titulo)
    if autor:
        query = query.filter(autor__icontains=autor)
    if categoria:
        query = query.filter(categoria=categoria)

    # Ordenamiento dinámico
    orden_campos_validos = {"id", "titulo", "autor", "categoria", "fecha_creacion"}
    if orden not in orden_campos_validos:
        raise HTTPException(status_code=400, detail=f"Orden no válido. Usa uno de: {', '.join(orden_campos_validos)}")

    query = query.order_by(orden)

    # Paginación
    query = query.offset(offset).limit(limite)

    return await query
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
# Endpoint para cambiar el estado de un libro

