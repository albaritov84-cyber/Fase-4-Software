#Aportes santiago
# Reserva: une cliente, servicio, duración y estado.
 
import logging
 
from Software_FJ.excepciones import (
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ProgramaFJError,
    ReservaConflictoError,
)
from Software_FJ.modelos.cliente import Cliente
from Software_FJ.modelos.entidad import Entidad
from Software_FJ.servicios.base import Servicio
 
log = logging.getLogger("Software_FJ")
 
 
class Reserva(Entidad):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
 
    def __init__(self, cliente, servicio, horas):
        super().__init__()
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva necesita un cliente y un servicio")
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente no es válido", detalle=type(cliente).__name__)
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio no es válido", detalle=type(servicio).__name__)
        servicio.validar_parametros(horas)
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = self.PENDIENTE
 
    @property
    def cliente(self):
        return self._cliente
 
    @property
    def servicio(self):
        return self._servicio
 
    @property
    def horas(self):
        return self._horas
 
    @property
    def estado(self):
        return self._estado
 
    def confirmar(self):
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}"
            )
        if not self._servicio.disponible:
            raise ReservaConflictoError(f"El servicio '{self._servicio.nombre}' no está disponible")
        self._estado = self.CONFIRMADA
        log.info("Reserva #%s confirmada", self.id)
 
    def cancelar(self):
        if self._estado == self.CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada")
        self._estado = self.CANCELADA
        log.info("Reserva #%s cancelada", self.id)
 
    def calcular_costo_total(self, con_iva=False, descuento=0):
        return self._servicio.calcular_costo(self._horas, con_iva, descuento)
 
    def procesar(self, con_iva=False, descuento=0):
        # El costo se calcula antes de confirmar para no dejar una reserva confirmada sin cobro válido
        try:
            costo = self.calcular_costo_total(con_iva, descuento)
            self.confirmar()
        except ProgramaFJError:
            log.warning("Reserva #%s no se pudo procesar", self.id)
            raise
        except Exception as e:
            raise OperacionNoPermitidaError(f"Fallo inesperado procesando la reserva #{self.id}") from e
        else:
            log.info("Reserva #%s procesada, costo total %s", self.id, costo)
            return costo
        finally:
            log.info("Reserva #%s terminó el proceso en estado %s", self.id, self._estado)
 
    def describir(self):
        return (
            f"Reserva #{self.id}: {self._cliente.nombre} -> {self._servicio.nombre} | "
            f"{self._horas} h | {self._estado}"
        )
