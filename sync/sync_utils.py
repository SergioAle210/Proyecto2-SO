from collections import deque


class Recurso:

    def __init__(self, nombre: str, capacidad: int):
        self.nombre = nombre
        self.capacidad = int(capacidad)
        self.disponibles = self.capacidad
        self.en_uso = []
        self.cola_espera = deque()

    def _wake_up(self, ciclo_destino):
        """
        Ciclo en el que el proceso empezará realmente a usar el recurso.
        Normalmente 'ciclo_actual + 1' cuando lo llamamos desde end_cycle.
        """
        while self.disponibles > 0 and self.cola_espera:
            proc, auto_rel = self.cola_espera.popleft()
            self.disponibles -= 1
            self.en_uso.append((proc, auto_rel))
            proc.marca(ciclo_destino, f"ACCESSED_{self.nombre}")

    def acquire(self, proc, ciclo, auto_release=True):

        if self.disponibles > 0:
            self.disponibles -= 1
            self.en_uso.append((proc, auto_release))
            proc.marca(ciclo, f"ACCESSED_{self.nombre}")
        else:
            proc.marca(ciclo, f"WAITING_{self.nombre}")
            self.cola_espera.append((proc, auto_release))

    def signal(self, ciclo):

        self.disponibles += 1
        self._wake_up(ciclo)

    def end_cycle(self, ciclo_actual):
        # libera los accesos de 1 ciclo
        liberados = [(p, a) for (p, a) in self.en_uso if a]
        for p, _ in liberados:
            self.en_uso.remove((p, True))
            self.disponibles += 1
        # despierta *para el ciclo siguiente*
        self._wake_up(ciclo_actual + 1)


class Accion:

    def __init__(self, pid, tipo, recurso, ciclo):
        self.pid = pid
        self.tipo = tipo.strip().upper()
        self.recurso = recurso.strip()
        self.ciclo = int(ciclo)


class ProcesoSincronizado:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid.strip()
        self.bt = int(bt)
        self.at = int(at)
        self.priority = int(priority)
        self.estado = "NEW"
        self.historial = []  # [(ciclo, estado)]

    def marca(self, ciclo, estado):
        self.estado = estado
        self.historial.append((ciclo, estado))


def leer_procesos(path):
    with open(path, encoding="utf-8") as f:
        return [
            ProcesoSincronizado(*map(str.strip, linea.split(",")))
            for linea in f
            if linea.strip()
        ]


def leer_recursos(path):
    recursos = {}
    with open(path, encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                nombre, capacidad = map(str.strip, linea.split(","))
                recursos[nombre] = Recurso(nombre, int(capacidad))
    return recursos


def leer_acciones(path):
    with open(path, encoding="utf-8") as f:
        acciones = [
            Accion(*map(str.strip, linea.split(","))) for linea in f if linea.strip()
        ]
    return sorted(acciones, key=lambda a: a.ciclo)
