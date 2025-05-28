# Proyecto 2

Este proyecto consiste en un simulador educativo desarrollado en Python con interfaz gráfica utilizando `Tkinter`. El simulador permite representar el comportamiento de algoritmos clásicos de **calendarización de procesos** y mecanismos de **sincronización** como _mutex_ y _semáforos_.

---

## Estructura del Proyecto

```
Proyecto2-SO/

│

├── main.py                  # Punto de entrada principal del simulador

├── .gitignore               # Ignora archivos no relevantes para el control de versiones

│

├── gui/                     # Contiene la interfaz gráfica principal del simulador

│   └── interfaz.py          # Implementación completa del GUI con Tkinter

│

├── scheduler/               # Lógica de los algoritmos de calendarización

│   ├── fifo.py              # Algoritmo First-In First-Out

│   ├── sjf.py               # Algoritmo Shortest Job First

│   ├── srt.py               # Algoritmo Shortest Remaining Time

│   ├── round_robin.py       # Algoritmo Round Robin (con quantum configurable)

│   ├── priority.py          # Algoritmo de planificación por prioridad

│   └── utils.py             # Funciones utilitarias comunes (leer procesos, calcular métricas, etc.)

│

├── sync/                    # Módulos para simulación de sincronización

│   ├── mutex.py             # Simulación con mecanismos de exclusión mutua (mutex)

│   ├── semaforo.py          # Simulación con semáforos

│   └── sync_utils.py        # Funciones para cargar recursos, procesos y acciones

│

├── data/                    # Carpeta recomendada para colocar los archivos de entrada (.txt)

│   ├── procesos_calendarizacion.txt    # Formato para calendarización

│   ├── procesos_sincronizacion.txt     # Procesos para sincronización

│   ├── recursos.txt                    # Recursos disponibles

│   └── acciones.txt                    # Acciones que simulan accesos a recursos
```

---

## Requisitos

- Python 3.8 o superior
- Sistema operativo compatible (Windows, macOS, Linux)
- Librerías estándar (`tkinter`, `random`, `copy`, etc.)

---

## Instrucciones de Ejecución

### 1. Clonar el repositorio o abrir el directorio

```bash
git clone https://github.com/tu-usuario/Proyecto2-SO.git

cd Proyecto2-SO
```

### 2. Ejecutar el simulador

```bash
python main.py
```

> Asegúrate de tener Python agregado a tu PATH.

---

## Formatos de Archivos de Entrada

### Procesos para Calendarización

Archivo: `procesos_calendarizacion.txt`

```
PID, Tiempo de Ejecución (BT), Tiempo de Llegada (AT), Prioridad

P1, 5, 0, 2

P2, 3, 1, 1

...
```

### Procesos para Sincronización

Archivo: `procesos_sincronizacion.txt`

```
PID, Tiempo de Ejecución (BT), Tiempo de Llegada (AT), Prioridad

P1, 4, 0, 2

...
```

### Recursos

Archivo: `recursos.txt`

```
NombreRecurso, CantidadDisponible

R1, 2

R2, 1

...
```

### Acciones

Archivo: `acciones.txt`

```
PID, TipoAccion (READ/WRITE), NombreRecurso, CicloDeAcceso

P1, READ, R1, 2

P2, WRITE, R2, 3

...
```

---

## Funcionalidades

- Interfaz intuitiva con botones de carga, simulación y limpieza.
- Simulación visual dinámica de los algoritmos de planificación.
- Representación visual de procesos y recursos con leyenda de colores.
- Métricas de evaluación (tiempo de espera promedio y turnaround promedio).
- Soporte para múltiples algoritmos seleccionados simultáneamente.
- Visualización de sincronización con estados ACCESSED / WAITING.

---

## Recomendaciones

- Asegúrate de que los archivos `.txt` estén bien formateados.
- Para sincronización, es obligatorio cargar procesos, recursos y acciones.
- La cantidad de recursos debe coincidir con los nombres utilizados en las acciones.

---

## Créditos

Proyecto desarrollado para el curso de **Sistemas Operativos**.

Autor: Sergio Orellana

---

¡Gracias por revisar el simulador!
