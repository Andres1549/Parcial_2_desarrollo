from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.db import get_session
from app.models import Empleado, Proyecto
from app.schemas import EmpleadoCreate, EmpleadoRead, EmpleadoUpdate
from app.utils import verificar_existe, conflicto

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post("/", response_model=EmpleadoRead, status_code=201)
def crear_empleado(data: EmpleadoCreate, session: Session = Depends(get_session)):
    empleado = Empleado.from_orm(data)
    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado

@router.get("/", response_model=list[EmpleadoRead])
def listar_empleados(
    especialidad: str | None = Query(None),
    estado: bool | None = Query(True),
    session: Session = Depends(get_session),
):
    query = select(Empleado)
    if especialidad:
        query = query.where(Empleado.especialidad == especialidad)
    if estado is not None:
        query = query.where(Empleado.estado == estado)
    empleados = session.exec(query).all()
    return empleados

@router.get("/{id}", response_model=EmpleadoRead)
def obtener_empleado(id: int, session: Session = Depends(get_session)):
    empleado = session.get(Empleado, id)
    verificar_existe(empleado, "Empleado")
    return empleado

@router.patch("/{empleado_id}", response_model=EmpleadoRead)
def actualizar_empleado(empleado_id: int, data: EmpleadoUpdate, session: Session = Depends(get_session)):
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(empleado, field, value)

    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado

@router.delete("/{id}")
def eliminar_empleado(id: int, session: Session = Depends(get_session)):
    empleado = session.get(Empleado, id)
    verificar_existe(empleado, "Empleado")
    proyectos = session.exec(select(Proyecto).where(Proyecto.id_gerente == id, Proyecto.estado == True)).all()
    if proyectos:
        raise HTTPException(status_code=400, detail="No se puede eliminar un gerente con proyectos activos.")
    empleado.estado = False
    session.add(empleado)
    session.commit()
    return {"message": "Empleado enviado al historial"}
