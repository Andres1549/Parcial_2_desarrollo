from fastapi import FastAPI
from app.db import init_db
from app.routers import empleados, proyectos, asignaciones

app = FastAPI(title="Sistema de gestión de proyectos")

init_db()

app.include_router(empleados.router)
app.include_router(proyectos.router)
app.include_router(asignaciones.router)

@app.get("/")
def root():
    return {"message": "API de gestión de proyectos activa"}
