from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.db import get_session
from app.models import Empleado, Proyecto, Asignacion
from app.schemas import AsignacionBase

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def asignar_empleado(asignacion: AsignacionBase, session: Session = Depends(get_session)):
    empleado = session.get(Empleado, asignacion.id_empleado)
    proyecto = session.get(Proyecto, asignacion.id_proyecto)

    if not empleado or not proyecto:
        raise HTTPException(status_code=404, detail="Empleado o proyecto no encontrado")

    if proyecto.id_gerente == asignacion.id_empleado:
        raise HTTPException(
            status_code=400,
            detail="El empleado es el gerente del proyecto y no puede asignarse como trabajador."
        )

    existente = session.exec(
        select(Asignacion)
        .where(Asignacion.id_empleado == asignacion.id_empleado)
        .where(Asignacion.id_proyecto == asignacion.id_proyecto)
    ).first()

    if existente:
        raise HTTPException(status_code=409, detail="El empleado ya está asignado a este proyecto")

    nueva_asignacion = Asignacion.from_orm(asignacion)
    session.add(nueva_asignacion)
    session.commit()
    session.refresh(nueva_asignacion)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Empleado asignado correctamente",
            "data": {
                "id": nueva_asignacion.id,
                "id_empleado": nueva_asignacion.id_empleado,
                "id_proyecto": nueva_asignacion.id_proyecto,
            },
        },
    )


@router.delete("/{id_empleado}/{id_proyecto}", status_code=status.HTTP_200_OK)
def desasignar_empleado(id_empleado: int, id_proyecto: int, session: Session = Depends(get_session)):
    asignacion = session.exec(
        select(Asignacion)
        .where(Asignacion.id_empleado == id_empleado)
        .where(Asignacion.id_proyecto == id_proyecto)
    ).first()

    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    session.delete(asignacion)
    session.commit()
    return {"message": "Empleado desasignado correctamente"}
