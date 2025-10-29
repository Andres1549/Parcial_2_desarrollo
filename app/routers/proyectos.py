from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.db import get_session
from app.models import Proyecto, Empleado
from app.schemas import ProyectoCreate, ProyectoRead, ProyectoUpdate
from app.utils import verificar_existe, conflicto

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.post("/", response_model=ProyectoRead, status_code=201)
def crear_proyecto(data: ProyectoCreate, session: Session = Depends(get_session)):
    existente = session.exec(select(Proyecto).where(Proyecto.nombre == data.nombre)).first()
    if existente:
        conflicto("El nombre del proyecto ya existe")
    gerente = session.get(Empleado, data.id_gerente)
    verificar_existe(gerente, "Gerente")
    if not gerente.estado:
        raise HTTPException(status_code=400, detail="El gerente está inactivo")
    proyecto = Proyecto.from_orm(data)
    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto

@router.get("/", response_model=list[ProyectoRead])
def listar_proyectos(
    estado: bool | None = Query(True),
    presupuesto_min: float | None = Query(None),
    presupuesto_max: float | None = Query(None),
    session: Session = Depends(get_session),
):
    query = select(Proyecto)
    if estado is not None:
        query = query.where(Proyecto.estado == estado)
    if presupuesto_min is not None:
        query = query.where(Proyecto.presupuesto >= presupuesto_min)
    if presupuesto_max is not None:
        query = query.where(Proyecto.presupuesto <= presupuesto_max)
    return session.exec(query).all()

@router.get("/{id}", response_model=ProyectoRead)
def obtener_proyecto(id: int, session: Session = Depends(get_session)):
    proyecto = session.get(Proyecto, id)
    verificar_existe(proyecto, "Proyecto")
    return proyecto

@router.patch("/{proyecto_id}", response_model=ProyectoRead)
def actualizar_proyecto(proyecto_id: int, data: ProyectoUpdate, session: Session = Depends(get_session)):
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(proyecto, field, value)

    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto

@router.delete("/{id}")
def eliminar_proyecto(id: int, session: Session = Depends(get_session)):
    proyecto = session.get(Proyecto, id)
    verificar_existe(proyecto, "Proyecto")
    proyecto.estado = False
    session.add(proyecto)
    session.commit()
    return {"message": "Proyecto mandado al historial"}
