def round_robin(procesos, quantum):
    """
    Algoritmo Round Robin (RR).
    Usa un quantum fijo para repartir tiempo de CPU de forma equitativa.
    """
    procesos = sorted(procesos, key=lambda p: p.at)
    tiempo = 0
    queue = []
    completados = 0
    n = len(procesos)
    resultado = []
    index = 0

    while completados < n:
        # Agregar procesos que hayan llegado al tiempo actual
        while index < n and procesos[index].at <= tiempo:
            queue.append(procesos[index])
            index += 1

        if not queue:
            tiempo += 1
            continue

        actual = queue.pop(0)

        if actual.first_run:
            actual.start_time = tiempo
            actual.first_run = False

        ejecutar = min(quantum, actual.remaining)
        tiempo += ejecutar
        actual.remaining -= ejecutar

        # Agregar nuevos procesos que hayan llegado durante la ejecución
        while index < n and procesos[index].at <= tiempo:
            queue.append(procesos[index])
            index += 1

        if actual.remaining > 0:
            queue.append(actual)
        else:
            actual.end_time = tiempo
            actual.finished = True
            resultado.append(actual)
            completados += 1

    return resultado
