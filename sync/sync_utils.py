from collections import deque


class Recurso:

    def __init__(self, nombre: str, capacidad: int):
        self.nombre = nombre
        self.capacidad = int(capacidad)
        self.disponibles = self.capacidad
        self.en_uso = []
        self.cola_espera = deque()

    def _wake_up(self, ciclo):
        """
        Despierta procesos bloqueados siempre que haya cupo libre.
        """
        while self.disponibles > 0 and self.cola_espera:
            proc, auto_rel = self.cola_espera.popleft()
            self.disponibles -= 1
            self.en_uso.append((proc, auto_rel))
            proc.marca(ciclo, "ACCESSED")

    def acquire(self, proc, ciclo, auto_release=True):
        """
        Intenta tomar el recurso.
        auto_release=True  → el recurso se devolverá automáticamente al final del ciclo.
        """
        if self.disponibles > 0:
            self.disponibles -= 1
            self.en_uso.append((proc, auto_release))
            proc.marca(ciclo, "ACCESSED")
        else:
            proc.marca(ciclo, "WAITING")
            self.cola_espera.append((proc, auto_release))

    def signal(self, ciclo):
        """
        SIGNAL (V) de un semáforo: libera un cupo y despierta a quien corresponda.
        """
        self.disponibles += 1
        self._wake_up(ciclo)

    def end_cycle(self, ciclo):
        """
        Al cerrar un ciclo:
        – Libera los accesos marcados como auto_release.
        – Despierta procesos en espera si quedó cupo.
        """
        liberados = [(p, a) for (p, a) in self.en_uso if a]
        for p, _ in liberados:
            self.en_uso.remove((p, True))  # elimina sólo la tupla con auto_release=True
            self.disponibles += 1
        self._wake_up(ciclo)


class Accion:
    """
    tipo : READ | WRITE | WAIT | SIGNAL
    ciclo: instante en que se ejecuta la acción
    """

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
