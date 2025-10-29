from typing import Optional
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

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    especialidad: Optional[str] = None
    salario: Optional[float] = Field(default=None, ge=0)
    estado: Optional[bool] = None

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

class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    presupuesto: Optional[float] = Field(default=None, ge=0)
    id_gerente: Optional[int] = None
    estado: Optional[bool] = None

class AsignacionBase(BaseModel):
    id_empleado: int
    id_proyecto: int
