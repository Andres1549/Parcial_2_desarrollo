from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Asignacion(SQLModel, table=True):
    id_empleado: Optional[int] = Field(default=None, foreign_key="empleado.id", primary_key=True)
    id_proyecto: Optional[int] = Field(default=None, foreign_key="proyecto.id", primary_key=True)

class Proyecto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    descripcion: str
    presupuesto: float = Field(ge=0)
    id_gerente: int = Field(foreign_key="empleado.id")
    estado: bool = Field(default=True)

    gerente: Optional["Empleado"] = Relationship(back_populates="proyectos_gerenciados")
    empleados: List["Empleado"] = Relationship(back_populates="proyectos", link_model=Asignacion)

class Empleado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    especialidad: str
    salario: float = Field(ge=0)
    estado: bool = Field(default=True)

    proyectos: List[Proyecto] = Relationship(back_populates="empleados", link_model=Asignacion)
    proyectos_gerenciados: List[Proyecto] = Relationship(back_populates="gerente")