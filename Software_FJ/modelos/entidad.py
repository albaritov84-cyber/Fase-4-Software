# Clase abstracta base de clientes, servicios y reservas.

from abc import ABC, abstractmethod
from datetime import datetime
from itertools import count

_contador_ids = count(1)


class Entidad(ABC):
    def __init__(self):
        self._id = next(_contador_ids)
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        pass

    def __eq__(self, otro):
        if not isinstance(otro, Entidad):
            return NotImplemented
        return type(self) is type(otro) and self._id == otro._id

    def __hash__(self):
        return hash((type(self).__name__, self._id))

    def __str__(self):
        return self.describir()
