# scheduler/utils.py


class Proceso:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid  # ID del proceso
        self.bt = int(bt)  # Burst Time
        self.at = int(at)  # Arrival Time
        self.priority = int(priority)  # Prioridad (menor número = mayor prioridad)
        self.timeline = []

        # Atributos necesarios para todos los algoritmos
        self.remaining = int(bt)  # Tiempo restante (para RR y SRT)
        self.start_time = None  # Cuándo inicia su ejecución
        self.end_time = None  # Cuándo termina su ejecución
        self.first_run = True  # Para marcar el primer ciclo (RR, SRT)
        self.finished = False  # Bandera para saber si ya terminó


def leer_procesos(path):
    """
    Lee el archivo de procesos y devuelve una lista de objetos Proceso.
    Formato por línea: <PID>, <BT>, <AT>, <Priority>
    """
    procesos = []
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                pid, bt, at, pr = linea.strip().split(",")
                procesos.append(
                    Proceso(pid.strip(), bt.strip(), at.strip(), pr.strip())
                )
    return procesos


def calcular_metricas(procesos):
    """
    Calcula el tiempo de espera promedio y turnaround time promedio.
    - Waiting Time = Start Time - Arrival Time
    - Turnaround Time = End Time - Arrival Time
    """
    total_wt = 0
    total_tat = 0
    n = len(procesos)

    for p in procesos:
        tat = p.end_time - p.at
        wt = tat - p.bt
        total_wt += wt
        total_tat += tat

    avg_wt = total_wt / n
    avg_tat = total_tat / n
    return avg_wt, avg_tat
