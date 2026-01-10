# app/Acta/domain/entities.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Curso:
    fullname: str
    shortname: str
    categoryid: int
    startdate: int
    enddate: int
    visible: int

@dataclass
class CursosAEliminar:
    ids: List[int]


@dataclass
class CursosObtener:
    ids: List[int]