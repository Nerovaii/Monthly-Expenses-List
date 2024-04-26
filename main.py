from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Gasto(BaseModel):
    id: Optional[int] = Field(None, alias='_id')
    categoria: str
    descripcion: str
    monto: float

db: List[Gasto] = []

id_ranges = {
    'Mercaderia': (1, 100),
    'Facturas': (101, 200),
    'Ocio': (201, 300),
    'Salud': (301, 400),
    'Transporte': (401, 500)
}

def get_next_id(categoria: str) -> int:
    existing_ids = [g.id for g in db if g.categoria == categoria]
    start, end = id_ranges[categoria]
    for id in range(start, end + 1):
        if id not in existing_ids:
            return id
    raise ValueError("No more IDs available in the category")

@app.post("/gastos/", response_model=Gasto)
def agregar_gasto(gasto: Gasto):
    if gasto.id is None:  # Check if ID is not already set
        next_id = get_next_id(gasto.categoria)
        gasto.id = next_id  # Now safe to assign as the model expects an 'id'
    if gasto.id in [g.id for g in db]:
        raise HTTPException(status_code=400, detail="El ID ya existe")
    db.append(gasto)
    return gasto

@app.delete("/gastos/{gasto_id}", response_model=Gasto)
def eliminar_gasto(gasto_id: int):
    for gasto in db:
        if gasto.id == gasto_id:
            db.remove(gasto)
            return gasto
    raise HTTPException(status_code=404, detail="Gasto no encontrado")

@app.get("/gastos/", response_model=List[Gasto])
def listar_gastos(categoria: Optional[str] = None):
    if categoria:
        return [gasto for gasto in db if gasto.categoria == categoria]
    return db

@app.get("/gastos/{gasto_id}", response_model=Gasto)
def obtener_gasto(gasto_id: int):
    for gasto in db:
        if gasto.id == gasto_id:
            return gasto
    raise HTTPException(status_code=404, detail="Gasto no encontrado")
