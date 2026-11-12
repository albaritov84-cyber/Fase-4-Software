#anexo por mi parte, Cristiam 
#Servicios especializados: sala, alquiler de equipo y asesoría.

from decimal import Decimal

from Software_FJ.excepciones import DatosInvalidosError, ParametroFaltanteError
from Software_FJ.servicios.base import Servicio


class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo", detalle=capacidad)
        self._capacidad = capacidad

    def validar_parametros(self, horas):
        self._validar_horas(horas, 1, 12)

    def calcular_costo_base(self, horas):
        return self.tarifa_hora * horas

    def describir(self):
        return f"{super().describir()} | Sala para {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    SEGURO = Decimal("15000")

    def __init__(self, nombre, tarifa_hora, tipo_equipo):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ParametroFaltanteError("El tipo de equipo es obligatorio")
        self._tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, horas):
        self._validar_horas(horas, 1, 72)

    def calcular_costo_base(self, horas):
        return self.tarifa_hora * horas + self.SEGURO

    def describir(self):
        return f"{super().describir()} | Equipo: {self._tipo_equipo} (seguro ${self.SEGURO})"


class Asesoria(Servicio):
    RECARGO = Decimal("0.15")

    def __init__(self, nombre, tarifa_hora, especialidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ParametroFaltanteError("La especialidad es obligatoria")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, horas):
        self._validar_horas(horas, 1, 8)

    def calcular_costo_base(self, horas):
        base = self.tarifa_hora * horas
        return base + base * self.RECARGO

    def describir(self):
        return f"{super().describir()} | Especialidad: {self._especialidad}"
