def priority(procesos):
    """
    Algoritmo de planificación por prioridad (no expropiativo).
    Selecciona el proceso con mayor prioridad disponible en cada ciclo.
    """
    procesos = sorted(procesos, key=lambda p: p.at)
    tiempo = 0
    completados = 0
    n = len(procesos)
    resultado = []

    while completados < n:
        # Filtrar procesos que hayan llegado y no hayan terminado
        disponibles = [p for p in procesos if p.at <= tiempo and not p.finished]

        if disponibles:
            # Menor valor de prioridad = más prioritario
            actual = min(disponibles, key=lambda p: (p.priority, p.at))
            actual.start_time = tiempo
            tiempo += actual.bt
            actual.end_time = tiempo
            actual.finished = True
            resultado.append(actual)
            completados += 1
        else:
            tiempo += 1

    return resultado
