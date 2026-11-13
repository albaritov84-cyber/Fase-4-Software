# Simulación de operaciones de Software_FJ, sin base de datos.
#trabajo realizado por Santiago Rojas, Cristiam Lopez, Lorena Correa.
# Ejecuta 31 operaciones válidas, inválidas y con fallos graves sobre un
# GestorReservas que vive solo en memoria. Demuestra que:
#   - las operaciones están aisladas: un error no detiene lo que sigue.
#   - los errores llegan como Software_FJError con un mensaje claro.
#   - los fallos inesperados se encadenan (raise ... from) y quedan en Software_FJ.log.
#
# Ejecución desde la raíz del proyecto:  py Software_FJ.py
 
 
from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
import logging
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
from Software_FJ.modelos.cliente import Cliente
from Software_FJ.modelos.entidad import Entidad
from Software_FJ.modelos.reserva import Reserva
from Software_FJ.servicios.base import Servicio
from Software_FJ.servicios.concretos import AlquilerEquipo, Asesoria, ReservaSala
 
T = TypeVar("T")
 
log = logging.getLogger("Software_FJ")
resumen = {"exitosas": 0, "controladas": 0, "graves": 0}
 
CATEGORIAS = {
    DatosInvalidosError: "Datos inválidos",
    ParametroFaltanteError: "Parámetro faltante",
    EntidadNoEncontradaError: "No encontrado",
    OperacionNoPermitidaError: "Operación no permitida",
    ReservaConflictoError: "Conflicto de reserva",
}
 
 
def configurar_log():
    logging.basicConfig(
        filename="Software_FJ.log",
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
 
 
def categoria(error):
    for clase, nombre in CATEGORIAS.items():
        if isinstance(error, clase):
            return nombre
    return "Error del sistema"
 
 
def ejecutar(descripcion: str, operacion: Callable[[], T]):
    # Cada operación corre aislada: pase lo que pase, el programa sigue con la siguiente
    numero = sum(resumen.values()) + 1
    try:
        resultado = operacion()
    except Software_FJError as e:
        resumen["controladas"] += 1
        log.error("Op %02d '%s' -> %s: %s", numero, descripcion, type(e).__name__, e, exc_info=bool(e.__cause__))
        print(f"[{numero:02d}] {descripcion}\n     ERROR controlado ({categoria(e)}): {e}")
    except Exception as e:
        # Error que el sistema no esperaba: se encadena con el original y se registra completo
        try:
            raise Software_FJError(f"Fallo inesperado en '{descripcion}'") from e
        except Software_FJError as encadenado:
            resumen["graves"] += 1
            log.exception("Op %02d: %s", numero, encadenado)
            print(
                f"[{numero:02d}] {descripcion}\n"
                f"     FALLO GRAVE controlado: {encadenado} | causa: {type(e).__name__}: {e}"
            )
    else:
        resumen["exitosas"] += 1
        log.info("Op %02d '%s' OK", numero, descripcion)
        print(f"[{numero:02d}] {descripcion}\n     OK: {resultado}")
        return resultado
    finally:
        log.info("Op %02d terminada", numero)
    return None
 
 
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
 
    configurar_log()
    inicio = datetime.now()
    log.info("===== Inicio de la simulación =====")
    print("=== SIMULACIÓN SOFTWARE FJ (sin base de datos) ===\n")
 
    gestor = GestorReservas()
    d = {}
    facturado = [Decimal("0")]
 
    def alta_cliente(clave, crear):
        c = gestor.registrar_cliente(crear())
        d[clave] = c
        return c.describir()
 
    def alta_servicio(clave, crear):
        s = gestor.registrar_servicio(crear())
        d[clave] = s
        return s.describir()
 
    def nueva_reserva(clave, cliente, servicio, horas):
        r = gestor.crear_reserva(d[cliente].id, d[servicio].id, horas)
        d[clave] = r
        return r.describir()
 
    def procesar(clave, con_iva=False, descuento=0):
        costo = gestor.procesar_reserva(d[clave].id, con_iva, descuento)
        facturado[0] += costo
        return f"costo total ${costo:,.2f} | {d[clave].describir()}"
 
    def reservar_con_servicio_apagado():
        d["asesoria"].deshabilitar()
        return gestor.crear_reserva(d["maria"].id, d["asesoria"].id, 2)
 
    # ---------- Clientes (4 válidos, 4 inválidos) ----------
    ejecutar("Registrar cliente válido: Ana", lambda: alta_cliente(
        "ana", lambda: Cliente("ana maria lopez", "1053123456", "ana@correo.com", "300 123 4567")))
    ejecutar("Registrar cliente válido: Carlos", lambda: alta_cliente(
        "carlos", lambda: Cliente("carlos ruiz", "80123456", "carlos@correo.com", "3105556677")))
    ejecutar("Registrar cliente válido: Luisa", lambda: alta_cliente(
        "luisa", lambda: Cliente("luisa gomez", "1020304050", "luisa@correo.com", "320-111-2233")))
    ejecutar("Registrar cliente válido: Maria", lambda: alta_cliente(
        "maria", lambda: Cliente("maria torres", "52123456", "maria@correo.com", "3157778899")))
    ejecutar("Cliente con nombre demasiado corto", lambda: alta_cliente(
        "x", lambda: Cliente("Al", "1234567", "al@correo.com", "3001112233")))
    ejecutar("Cliente con correo mal escrito", lambda: alta_cliente(
        "x", lambda: Cliente("Pedro Perez", "1234567", "pedro.correo.com", "3001112233")))
    ejecutar("Cliente con documento con letras", lambda: alta_cliente(
        "x", lambda: Cliente("Pedro Perez", "12AB567", "pedro@correo.com", "3001112233")))
    ejecutar("Cliente creado con datos incompletos", lambda: alta_cliente(
        "x", lambda: Cliente.desde_diccionario({"nombre": "Pedro Perez"})))
 
    # ---------- Servicios (3 válidos, 4 inválidos) ----------
    ejecutar("Crear servicio válido: sala", lambda: alta_servicio(
        "sala", lambda: ReservaSala("Sala Ejecutiva", 50000, 10)))
    ejecutar("Crear servicio válido: equipo", lambda: alta_servicio(
        "equipo", lambda: AlquilerEquipo("Proyector 4K", 20000, "Proyector")))
    ejecutar("Crear servicio válido: asesoría", lambda: alta_servicio(
        "asesoria", lambda: Asesoria("Asesoría en Software", 80000, "Desarrollo de software")))
    ejecutar("Servicio con tarifa negativa", lambda: alta_servicio(
        "x", lambda: ReservaSala("Sala Mini", -5000, 4)))
    ejecutar("Servicio con tarifa que no es número", lambda: alta_servicio(
        "x", lambda: AlquilerEquipo("Portátil", "mucho", "Portátil")))
    ejecutar("Sala con capacidad cero", lambda: alta_servicio(
        "x", lambda: ReservaSala("Sala Vacía", 30000, 0)))
    ejecutar("Equipo sin tipo definido", lambda: alta_servicio(
        "x", lambda: AlquilerEquipo("Cámara", 15000, "   ")))
 
    # ---------- Reservas (exitosas y fallidas) ----------
    ejecutar("Reserva de sala para Ana (2 h)", lambda: nueva_reserva("r1", "ana", "sala", 2))
    ejecutar("Reserva de equipo para Carlos (4 h)", lambda: nueva_reserva("r2", "carlos", "equipo", 4))
    ejecutar("Reserva de asesoría para Luisa (3 h)", lambda: nueva_reserva("r3", "luisa", "asesoria", 3))
    ejecutar("Procesar reserva de Ana con IVA y 10% de descuento", lambda: procesar("r1", True, 0.10))
    ejecutar("Procesar reserva de Carlos sin impuestos", lambda: procesar("r2"))
    ejecutar("Cancelar reserva de Luisa", lambda: gestor.cancelar_reserva(d["r3"].id).describir())
    ejecutar("Cancelar de nuevo la misma reserva", lambda: gestor.cancelar_reserva(d["r3"].id))
    ejecutar("Reservar con un cliente que no existe", lambda: gestor.crear_reserva(9999, d["sala"].id, 2))
    ejecutar("Reservar un servicio que no existe", lambda: gestor.crear_reserva(d["ana"].id, 8888, 2))
    ejecutar("Reservar sala por 20 horas (fuera de rango)", lambda: nueva_reserva("x", "maria", "sala", 20))
    ejecutar("Ana intenta reservar otra vez la misma sala", lambda: nueva_reserva("x", "ana", "sala", 1))
    ejecutar("Reservar un servicio deshabilitado", reservar_con_servicio_apagado)
 
    # ---------- Fallos graves (errores que nadie esperaba) ----------
    ejecutar("Instanciar la clase abstracta Entidad", lambda: Entidad())
    ejecutar("Instanciar la clase abstracta Servicio", lambda: Servicio("Abstracto", 1000))
    ejecutar("Leer una reserva fuera de la lista", lambda: gestor.reservas[99])
    ejecutar("Cálculo inconsistente: división entre cero", lambda: Decimal("100") / Decimal("0"))
 
    # ---------- Resumen ----------
    total = sum(resumen.values())
    estados = {}
    for r in gestor.reservas:
        estados[r.estado] = estados.get(r.estado, 0) + 1
    duracion = (datetime.now() - inicio).total_seconds()
 
    print("\n=== RESUMEN ===")
    print(f"Operaciones ejecutadas: {total}")
    print(f"  Exitosas: {resumen['exitosas']}")
    print(f"  Errores controlados: {resumen['controladas']}")
    print(f"  Fallos graves (encadenados): {resumen['graves']}")
    print(f"Clientes: {len(gestor.clientes)} | Servicios: {len(gestor.servicios)} | Reservas: {len(gestor.reservas)}")
    print(f"Reservas {Reserva.CONFIRMADA.lower()}s: {estados.get(Reserva.CONFIRMADA, 0)} | "
          f"{Reserva.CANCELADA.lower()}s: {estados.get(Reserva.CANCELADA, 0)}")
    print(f"Total facturado: ${facturado[0]:,.2f}")
    print(f"Duración: {duracion:.2f} s | Detalle completo en Software_FJ.log")
    log.info("===== Fin de la simulación: %s =====", resumen)
 
 
if __name__ == "__main__":
    main()
        


