from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://postgres:postgres@db:5432/tesisdb"
engine = create_engine(DATABASE_URL)


class Tesis(BaseModel):
    titulo: str
    estudiante: str
    director: str
    linea_investigacion: str
    estado: str


class Avance(BaseModel):
    descripcion: str
    porcentaje_avance: int
    observaciones: str


@app.get("/")
def inicio():
    return {"mensaje": "API activa"}


@app.get("/tesis")
def listar_tesis():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM tesis ORDER BY id"))
        return [dict(row._mapping) for row in res]


@app.post("/tesis")
def crear_tesis(tesis: Tesis):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO tesis (titulo, estudiante, director, linea_investigacion, estado)
            VALUES (:titulo, :estudiante, :director, :linea_investigacion, :estado)
        """), tesis.model_dump())
        conn.commit()
    return {"ok": True}


@app.get("/tesis/{tesis_id}/avances")
def listar_avances(tesis_id: int):
    with engine.connect() as conn:
        res = conn.execute(text("""
            SELECT * FROM avances WHERE tesis_id = :id
        """), {"id": tesis_id})
        return [dict(row._mapping) for row in res]


@app.post("/tesis/{tesis_id}/avances")
def crear_avance(tesis_id: int, avance: Avance):
    data = avance.model_dump()
    data["tesis_id"] = tesis_id

    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO avances (tesis_id, descripcion, porcentaje_avance, observaciones)
            VALUES (:tesis_id, :descripcion, :porcentaje_avance, :observaciones)
        """), data)
        conn.commit()

    return {"ok": True}
