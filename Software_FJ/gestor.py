# Aporte Deisy Suescun
from datetime import datetime
from typing import callable, TypeVar

# Definimos variables de tipo genérico para las funciones
T = TypeVar("T")

class Contador:
    """Datos de la simulación."""

    def __init__(self)-> None:
        self.total: int = 0
        self.exitos: int = 0
        self.rechazos_esperados: int = 0
        # Casos en los que el resultado no coincide con lo previcto.
        self.discrepancias: int = 0
def _f(día: int, hora: int = 0) -> datetime:
    """Fecha de noviembre de 2026para reducir ruido en las opereciones."""
    return datetime(2026, 11, día, hora)
def _id(reserva: Reserva | None) -> int:
    """Devuelve el ID de la reserva previa. Si no existe, lanza un error de forma controlada."""
    if reserva is None:
        raise OperacionNoPermitidaError("Paso omitido: La reserva previa no se creó.")
    return reserva.id
def _detalle(valor: object) -> str:
    """Texto descifrable para mostrar el resultado de una operación."""
    if isinstance(valor, (Entidad, Reserva)):
        return valor.describir()
    if valor is None:
        return "operación completada."
    return str(valor)

def ejecutar(
    contador: Contador,
    numero: int,
    descripcion: str,
    operacion: callable[[], T],
    error_esperado: type[Fase4Error] | None = None,
) -> T | None:
    """Ejecuta una operación controlando sus resultados, excepciones y estadísticas."""
    contador.total += 1
    print(f"\n[Operación {numero}] {descripcion}")

    try:
        resultado = operacion()
    except Exception as ex:
        if error_esperado and isinstance(ex, error_esperado):
            contador.rechazos_esperados += 1
            print(f"  -> Rechazo esperado: {_detalle(ex)}")
            return None
        else:
            contador.discrepancias += 1
            print(f"  -> [ERROR INESPERADO]: {_detalle(ex)}")
            return None
    else:
        contador.exitos += 1
        print(f"  -> Éxito: {_detalle(resultado)}")
        return resultado
    finally:
        pass
