#Poner aportes aca Santiago Rojas 

# Excepciones propias del sistema. Todas heredan de ProgramaFJError.


class ProgramaFJError(Exception):
    def __init__(self, mensaje, detalle=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.detalle = detalle

    def __str__(self):
        return f"{self.mensaje} ({self.detalle})" if self.detalle else self.mensaje


class DatosInvalidosError(ProgramaFJError):
    pass


class ParametroFaltanteError(ProgramaFJError):
    pass


class EntidadNoEncontradaError(ProgramaFJError):
    pass


class OperacionNoPermitidaError(ProgramaFJError):
    pass


class ReservaConflictoError(ProgramaFJError):
    pass
