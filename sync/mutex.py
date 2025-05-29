class MutexSimulador:
    """
    Mutex clásico: READ y WRITE son accesos de 1 solo ciclo.
    """

    def __init__(self, procesos, recursos, acciones):
        self.procesos = {p.pid: p for p in procesos}
        self.recursos = recursos
        self.acciones = acciones
        self.ciclo = 0

    def ejecutar(self):
        tiempo_fin = max(a.ciclo for a in self.acciones) + 5

        while self.ciclo <= tiempo_fin:
            # procesar acciones del ciclo
            for acc in (a for a in self.acciones if a.ciclo == self.ciclo):
                proc = self.procesos[acc.pid]
                rec = self.recursos[acc.recurso]
                if acc.tipo in ("READ", "WRITE"):
                    rec.acquire(proc, self.ciclo, auto_release=True)

            # fin de ciclo: libera auto_release y despierta
            for rec in self.recursos.values():
                rec.end_cycle(self.ciclo)

            self.ciclo += 1

        # marca de finalización
        for p in self.procesos.values():
            p.marca(self.ciclo, "DONE")

        return list(self.procesos.values())
