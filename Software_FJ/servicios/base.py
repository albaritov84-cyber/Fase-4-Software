#Añadir aportes C
# Clase abstracta Servicio: base de todos los servicios de Software FJ.

from abc import abstractmethod
from decimal import Decimal, InvalidOperation

from Software_FJ.excepciones import DatosInvalidosError, ParametroFaltanteError
from Software_FJ.modelos.entidad import Entidad

IVA = Decimal("0.19")


def _a_decimal(valor, campo):
    if valor is None:
        raise ParametroFaltanteError(f"El campo '{campo}' es obligatorio")
    try:
        return Decimal(str(valor))
    except InvalidOperation as e:
        raise DatosInvalidosError(f"El campo '{campo}' debe ser numérico", detalle=valor) from e


class Servicio(Entidad):
    def __init__(self, nombre, tarifa_hora):
        super().__init__()
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatosInvalidosError("El nombre del servicio debe tener al menos 3 caracteres")
        tarifa = _a_decimal(tarifa_hora, "tarifa_hora")
        if tarifa <= 0:
            raise DatosInvalidosError("La tarifa por hora debe ser mayor a cero", detalle=tarifa)
        self._nombre = nombre.strip()
        self._tarifa_hora = tarifa
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def habilitar(self):
        self._disponible = True

    def deshabilitar(self):
        self._disponible = False

    @abstractmethod
    def validar_parametros(self, horas):
        pass

    @abstractmethod
    def calcular_costo_base(self, horas):
        pass

    # Sobrecarga con parámetros opcionales:
    #   calcular_costo(2)                         -> costo base
    #   calcular_costo(2, con_iva=True)           -> base + IVA
    #   calcular_costo(2, descuento=0.1)          -> base con descuento
    #   calcular_costo(2, con_iva=True, descuento=0.1)
    def calcular_costo(self, horas, con_iva=False, descuento=0):
        self.validar_parametros(horas)
        descuento = _a_decimal(descuento, "descuento")
        if not Decimal("0") <= descuento <= Decimal("1"):
            raise DatosInvalidosError("El descuento debe estar entre 0 y 1", detalle=descuento)
        costo = self.calcular_costo_base(Decimal(str(horas)))
        costo -= costo * descuento
        if con_iva:
            costo += costo * IVA
        return costo.quantize(Decimal("0.01"))

    def describir(self):
        return f"{self.__class__.__name__} #{self.id}: {self.nombre} | ${self.tarifa_hora}/h"

    def _validar_horas(self, horas, minimo, maximo):
        if horas is None:
            raise ParametroFaltanteError("La duración es obligatoria")
        if isinstance(horas, bool) or not isinstance(horas, (int, float)):
            raise DatosInvalidosError("La duración debe ser un número", detalle=horas)
        if not minimo <= horas <= maximo:
            raise DatosInvalidosError(
                f"La duración debe estar entre {minimo} y {maximo} horas", detalle=horas
            )
