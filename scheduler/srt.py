def srt(procesos):
    """
    Algoritmo Shortest Remaining Time (SRT).
    En cada ciclo selecciona el proceso con el menor tiempo restante (remaining).
    Interrumpe si llega un proceso con menor tiempo.
    """
    procesos = sorted(procesos, key=lambda p: p.at)
    tiempo = 0
    completados = 0
    n = len(procesos)
    en_ejecucion = None
    resultado = []

    while completados < n:
        # Filtrar procesos disponibles y no terminados
        disponibles = [p for p in procesos if p.at <= tiempo and p.remaining > 0]

        if disponibles:
            # Elegir el de menor tiempo restante
            actual = min(disponibles, key=lambda p: p.remaining)

            if actual.first_run:
                actual.start_time = tiempo
                actual.first_run = False

            actual.remaining -= 1
            tiempo += 1

            # Si terminó
            if actual.remaining == 0:
                actual.end_time = tiempo
                actual.finished = True
                resultado.append(actual)
                completados += 1
        else:
            # Si no hay procesos listos, avanzamos el tiempo
            tiempo += 1

    return resultado
