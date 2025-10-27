from fastapi import HTTPException

def verificar_existe(item, nombre="Recurso"):
    if not item:
        raise HTTPException(status_code=404, detail=f"{nombre} no encontrado")

def conflicto(mensaje: str):
    raise HTTPException(status_code=409, detail=mensaje)

def validar_activo(item, nombre="Recurso"):
    if not item.estado:
        raise HTTPException(status_code=400, detail=f"{nombre} inactivo")