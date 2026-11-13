# Aporte Deisy Suescun
# Software_FJ/gestor.py

import logging

from Software_FJ.modelos.entidad import (
    DatosInvalidosError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    ReservaConflictoError,
)
from Software_FJ.modelos.cliente import Cliente
from Software_FJ.modelos.reserva import Reserva
from Software_FJ.servicios.base import Servicio

log = logging.getLogger("Software_FJ")

class GestorReservas:
    def __init__(self):
        self.reservas = []
        self.clientes = []
        self.servicios = []
    @property
    def clientes(self):
        return tuple(self.clientes)

    @property
    def servicios(self):
        return tuple(self.servicios)
    @property
    def reservas(self):
        return tuple(self.reservas)

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Solo se puede registrar objetos cliente.", detalle=type(cliente).__name__)
        if any(c.documento == cliente.documento for c in self._clientes):
            raise OperacionNoPermitidaError(f"ya existe el cliente con ese documento", detalle=cliente.documento)
        self.clientes.append(cliente)
        log.info(f"Cliente registrado: %s", cliente.describir())
        return cliente
    
    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Solo se puede registrar objetos servicio.", detalle=type(servicio).__name__)
        self.servicios.append(servicio)
        log.info(f"Servicio registrado: %s", servicio.describir())
        return servicio
    @staticmethod
    def _buscar_(lista, id_buscado, tipo):
        for elemento in lista:
            if elemento.id == id_buscado:
                return elemento
        raise EntidadNoEncontradaError(f"No se encontró {tipo} con id {id_buscado}.", detalle=id_buscado)
    def buscar_cliente(self, id_cliente):
        return self._buscar_(self.clientes, id_cliente, "cliente")

    def buscar_servicio(self, id_servicio):
        return self._buscar_(self.servicios, id_servicio, "servicio")

    def buscar_reserva(self, id_reserva):
        return self._buscar_(self.reservas, id_reserva, "reserva")

    def crear_reserva(self, id_cliente, id_servicio, fecha_inicio, fecha_fin, horas):
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        if not servicio.disponible:
            raise OperacionNoPermitidaError(f"El servicio {servicio.nombre} no está disponible para reservas.", detalle=servicio.nombre)
        for r in self._reservas:
            if r.cliente == cliente and r.servicio == servicio and r.estado!= Reserva.ESTADO_CANCELADA:
                raise ReservaConflictoError(
                    f"{cliente.nombre} ya tiene una reserva activa para el servicio {servicio.nombre}.", detalle=(r.id, id_servicio)
                )
        reserva = Reserva(cliente, servicio, fecha_inicio, fecha_fin, horas)
        self.reservas.append(reserva)
        log.info(f"Reserva creada: %s", reserva.describir())
        return reserva
    def confirmar_reserva(self, id_reserva):
        reserva = self.buscar_reserva(id_reserva)
        reserva.confirmar()
        return reserva
    def cancelar_reserva(self, id_reserva):
        reserva = self.buscar_reserva(id_reserva)
        reserva.cancelar()
        return reserva
    def procesar_reserva(self, id_reserva, con_iva=False, descuento=0.0):
        reserva = self.buscar_reserva(id_reserva)
        reserva.procesar(con_iva, descuento)
        return reserva
        
