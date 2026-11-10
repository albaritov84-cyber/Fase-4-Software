#Simulación de operaciones de Software_FJ, sin base de datos.

#Ejecute 31 operaciones válidas, inválidas y con fallos graves sobre un
#GestorReservas que vive solo en memoria. Demuestra que:

#se aislaron las operaciones: un error no detiene lo que sigue.
#Los errores llegan como Software_FJError con su respectivo mensaje claro.
#Los fallos inesperados se encadenan (raise ... from) y quedan en Software_FJ.log.

#Ejecución desde la raíz del proyecto:  py Software_FJ.py


from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
import sys
from typing import TypeVar

from Software_FJ.excepciones import (
    DatosInvalidosError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaConflictoError,
    ProgramaFJError as Software_FJError,
)
from Software_FJ.gestor import GestorReservas
from Software_FJ.modelos.entidad import Entidad
from Software_FJ.modelos.reserva import Reserva
from Software_FJ.servicios.base import Servicio
from Software_FJ.servicios.concretos import AlquilerEquipo, Asesoria, ReservaSala


