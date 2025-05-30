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
        # ordenar las acciones por ciclo
        acciones = sorted(self.acciones, key=lambda a: a.ciclo)
        idx = 0  # siguiente acción pendiente

        # se repite mientras queden acciones SIN despachar
        #   o algún recurso tenga procesos usando o esperando
        cond_recursos = lambda: any(
            r.en_uso or r.cola_espera for r in self.recursos.values()
        )

        while idx < len(acciones) or cond_recursos():
            # 1) despachar todas las acciones programadas para este ciclo
            while idx < len(acciones) and acciones[idx].ciclo == self.ciclo:
                acc = acciones[idx]
                idx += 1
                proc = self.procesos[acc.pid]
                rec = self.recursos[acc.recurso]
                if acc.tipo in ("READ", "WRITE"):
                    rec.acquire(proc, self.ciclo, auto_release=True)

            # 2) fin de ciclo: libera y despierta
            for rec in self.recursos.values():
                rec.end_cycle(self.ciclo)

            self.ciclo += 1

        # marca de finalización
        for p in self.procesos.values():
            p.marca(self.ciclo, "DONE")
        return list(self.procesos.values())
