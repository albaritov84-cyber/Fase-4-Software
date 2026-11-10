# Cliente con datos privados y validación estricta en cada atributo.

import re

from Software_FJ.excepciones import DatosInvalidosError, ParametroFaltanteError
from Software_FJ.modelos.entidad import Entidad

PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def _texto_obligatorio(valor, campo):
    if valor is None:
        raise ParametroFaltanteError(f"El campo '{campo}' es obligatorio")
    if not isinstance(valor, str):
        raise DatosInvalidosError(
            f"El campo '{campo}' debe ser texto", detalle=f"se recibió {type(valor).__name__}"
        )
    valor = valor.strip()
    if not valor:
        raise ParametroFaltanteError(f"El campo '{campo}' no puede estar vacío")
    return valor


class Cliente(Entidad):
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @classmethod
    def desde_diccionario(cls, datos):
        # Encadena el KeyError original para que quede en el log
        try:
            return cls(datos["nombre"], datos["documento"], datos["correo"], datos["telefono"])
        except KeyError as e:
            raise ParametroFaltanteError(f"Falta el dato {e} para crear el cliente") from e
        except TypeError as e:
            raise DatosInvalidosError("Los datos del cliente deben venir en un diccionario") from e

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = _texto_obligatorio(valor, "nombre")
        if len(valor) < 3:
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres")
        if not all(c.isalpha() or c in " .'-" for c in valor):
            raise DatosInvalidosError("El nombre solo puede tener letras y espacios", detalle=valor)
        self._nombre = valor.title()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = _texto_obligatorio(valor, "documento")
        if not valor.isdigit():
            raise DatosInvalidosError("El documento debe contener solo números", detalle=valor)
        if not 6 <= len(valor) <= 12:
            raise DatosInvalidosError("El documento debe tener entre 6 y 12 dígitos", detalle=valor)
        self._documento = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        valor = _texto_obligatorio(valor, "correo").lower()
        if not PATRON_CORREO.match(valor):
            raise DatosInvalidosError("El correo no tiene un formato válido", detalle=valor)
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = _texto_obligatorio(valor, "telefono")
        limpio = valor.replace(" ", "").replace("-", "")
        if not limpio.isdigit() or len(limpio) != 10:
            raise DatosInvalidosError("El teléfono debe tener 10 dígitos", detalle=valor)
        self._telefono = limpio

    def describir(self):
        return (
            f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
            f"Correo: {self.correo} | Tel: {self.telefono}"
        )

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre={self.nombre!r})"
