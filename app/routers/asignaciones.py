from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models import Asignacion, Empleado, Proyecto
from app.schemas import AsignacionBase
from app.utils import verificar_existe, conflicto

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])

@router.post("/", status_code=201)
def asignar_empleado(data: AsignacionBase, session: Session = Depends(get_session)):
    empleado = session.get(Empleado, data.id_empleado)
    proyecto = session.get(Proyecto, data.id_proyecto)
    verificar_existe(empleado, "Empleado")
    verificar_existe(proyecto, "Proyecto")
    if not empleado.estado or not proyecto.estado:
        raise HTTPException(status_code=400, detail="Empleado o proyecto inactivo")
    existente = session.get(Asignacion, (data.id_empleado, data.id_proyecto))
    if existente:
        conflicto("Empleado ya asignado a este proyecto")
    session.add(Asignacion(**data.dict()))
    session.commit()
    return {"message": "Empleado asignado correctamente"}

@router.delete("/")
def desasignar_empleado(data: AsignacionBase, session: Session = Depends(get_session)):
    asignacion = session.get(Asignacion, (data.id_empleado, data.id_proyecto))
    verificar_existe(asignacion, "Asignación")
    session.delete(asignacion)
    session.commit()
    return {"message": "Empleado desasignado correctamente"}

@router.get("/empleado/{id_empleado}")
def proyectos_de_empleado(id_empleado: int, session: Session = Depends(get_session)):
    empleado = session.get(Empleado, id_empleado)
    verificar_existe(empleado, "Empleado")
    query = select(Proyecto).join(Asignacion).where(Asignacion.id_empleado == id_empleado, Proyecto.estado == True)
    return session.exec(query).all()

@router.get("/proyecto/{id_proyecto}")
def empleados_de_proyecto(id_proyecto: int, session: Session = Depends(get_session)):
    proyecto = session.get(Proyecto, id_proyecto)
    verificar_existe(proyecto, "Proyecto")
    query = select(Empleado).join(Asignacion).where(Asignacion.id_proyecto == id_proyecto, Empleado.estado == True)
    return session.exec(query).all()
