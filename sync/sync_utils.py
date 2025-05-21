class Recurso:
    def __init__(self, nombre, contador):
        self.nombre = nombre
        self.contador = int(contador)
        self.cola_espera = []


class Accion:
    def __init__(self, pid, tipo, recurso, ciclo):
        self.pid = pid
        self.tipo = tipo.upper()  # READ, WRITE, WAIT, SIGNAL
        self.recurso = recurso
        self.ciclo = int(ciclo)


class ProcesoSincronizado:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid
        self.bt = int(bt)
        self.at = int(at)
        self.priority = int(priority)
        self.estado = "NEW"  # NEW, READY, WAITING, ACCESSED, DONE
        self.remaining = int(bt)
        self.historial = []  # Lista de tuplas (ciclo, estado)


def leer_procesos(path):
    procesos = []
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                pid, bt, at, pr = linea.strip().split(",")
                procesos.append(
                    ProcesoSincronizado(pid.strip(), bt.strip(), at.strip(), pr.strip())
                )
    return procesos


def leer_recursos(path):
    recursos = {}
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                nombre, contador = linea.strip().split(",")
                recursos[nombre.strip()] = Recurso(nombre.strip(), contador.strip())
    return recursos


def leer_acciones(path):
    acciones = []
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                pid, tipo, recurso, ciclo = linea.strip().split(",")
                acciones.append(
                    Accion(pid.strip(), tipo.strip(), recurso.strip(), ciclo.strip())
                )
    return sorted(acciones, key=lambda a: a.ciclo)
