from typing import Optional, List
from pydantic import BaseModel, Field

class EmpleadoBase(BaseModel):
    nombre: str
    especialidad: str
    salario: float = Field(ge=0)
    estado: bool = True

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoRead(EmpleadoBase):
    id: int
    class Config:
        from_attributes = True

class ProyectoBase(BaseModel):
    nombre: str
    descripcion: str
    presupuesto: float = Field(ge=0)
    id_gerente: int
    estado: bool = True

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoRead(ProyectoBase):
    id: int
    class Config:
        from_attributes = True

class AsignacionBase(BaseModel):
    id_empleado: int
    id_proyecto: int