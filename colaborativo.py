#Simulación de operaciones de Software_FJ, sin base de datos.

#Ejecute 31 operaciones válidas, inválidas y con fallos graves sobre un
#GestorReservas que vive solo en memoria. Demuestra que:

#se aislaron las operaciones: un error no detiene lo que sigue.
#Los errores llegan como Software_FJError con su respectivo mensaje claro.
#Los fallos inesperados se encadenan (raise ... from) y quedan en Software_FJ.log.

#Ejecución desde la raíz del proyecto:  py Software_FJ.py

#Parte cristiam
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

#Parte cristiam
print(f"\n[{numero:02d}] {descripcion}")
valor: T | None = None
try:
    valor = operacion()
except Fase4Error as exc:
    if error_esperado is not None and isinstance(exc, error_esperado):
        contador.rechazos_esperados += 1
        print(f"    ✔  Rechazo controlado: {type(exc)._name}: {exc.mensaje}")
    else:
        contador.discrepancias +1 
        print(f"   ✘ Error no previsto: {type(exc)._name_}: {exc.mensaje}")
except Excepction as exc:
    contador.discrepancias += 1
    print((f"  ✘ Excepcion no controlada: {type(exc)._name_}: {exc}")
    else:
    if error_esperado is None:
        contador.exitos += 1
        print(f"   ✔ Exito: {_detalle(valor)}")
    else: 
        contador.discrepancias += 1  
        print(f"  ✘ se esperaba  {error_esperado._name_}, la operacion tuvo exito")
finally:
    contador.total += 1 
    return valor 

def _imprimir_ resumen(contador: contador) -> None:
    print("\n===El Resumen===")
    print(f"operaciones  ejecutadas: {contador.total}")
    print((f"Exitos:                 {contador.exitos}")
    print(f"Rechazos controlados:    {contador.rechazos_esperados}")
    print(f"Discrepancias:           {contador.discrepancias}")
    print("La aplicacion sigue activa. Detalle en Software_FJ:log")

desf main() -> None:
    for salida in (sys.stdout, sys.stderr):
    reconfigure = getattr(salida, "reconfigure", None)
    if calleble(reconfigure):
        reconfigure(encoding="uft-8", errors="replace")

gestor = GestorReservas()
contador = contador()
print("===  Simulacion Software_FJ (sin base de datos)  ===")
        


