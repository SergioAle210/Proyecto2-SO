def sjf(procesos):
    """
    Algoritmo Shortest Job First (SJF).
    Selecciona siempre el proceso disponible con el menor Burst Time (BT).
    """
    procesos = sorted(procesos, key=lambda p: p.at)  # Orden inicial por llegada
    tiempo = 0
    completados = 0
    n = len(procesos)
    resultado = []

    while completados < n:
        # Filtrar procesos que ya llegaron y aún no se han ejecutado
        disponibles = [p for p in procesos if p.at <= tiempo and not p.finished]

        if disponibles:
            # Seleccionar el proceso con el menor Burst Time
            actual = min(disponibles, key=lambda p: p.bt)
            actual.start_time = tiempo
            tiempo += actual.bt
            actual.end_time = tiempo
            actual.finished = True
            resultado.append(actual)
            completados += 1
        else:
            # Si no hay procesos disponibles, el CPU espera
            tiempo += 1

    return resultado
