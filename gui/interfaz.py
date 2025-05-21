import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import random
from copy import deepcopy

from scheduler.utils import leer_procesos, calcular_metricas
from scheduler.fifo import fifo
from scheduler.sjf import sjf
from scheduler.srt import srt
from scheduler.round_robin import round_robin
from scheduler.priority import priority

from sync.sync_utils import (
    leer_procesos as leer_procesos_sync,
    leer_recursos,
    leer_acciones,
)
from sync.mutex import MutexSimulador
from sync.semaforo import SemaforoSimulador


class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistemas Operativos - UVG 2025")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1e1e1e")
        self.procesos = []
        self.recursos = {}
        self.acciones = []
        self.colors = {}

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 11), foreground="white")
        self.style.configure("Black.TButton", font=("Arial", 11), foreground="black")
        self.style.configure("TLabel", font=("Arial", 11), foreground="white")
        self.style.configure("TRadiobutton", background="#1e1e1e", foreground="white")
        self.style.configure("TCheckbutton", background="#1e1e1e", foreground="white")

        container = tk.Frame(self.root, bg="#1e1e1e")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.modo_var = tk.StringVar(value="calendarizacion")
        self.top_frame = tk.Frame(container, bg="#1e1e1e")
        self.top_frame.pack(fill="x")

        self.left_panel = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.left_panel.pack(side="left", fill="y", padx=20)

        self.control_panel = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.control_panel.pack(side="left", fill="y", expand=True)

        self.canvas_frame = tk.Frame(container, bg="#1e1e1e")
        self.canvas_frame.pack(fill="both", expand=True, pady=10)

        tk.Label(
            self.left_panel,
            text="Modo de Simulación:",
            bg="#1e1e1e",
            fg="white",
            font=("Arial", 12, "bold"),
        ).pack(pady=5)
        ttk.Radiobutton(
            self.left_panel,
            text="Calendarización",
            variable=self.modo_var,
            value="calendarizacion",
            command=self.actualizar_modo,
        ).pack(anchor="w")
        ttk.Radiobutton(
            self.left_panel,
            text="Sincronización",
            variable=self.modo_var,
            value="sincronizacion",
            command=self.actualizar_modo,
        ).pack(anchor="w")

        self.sync_selector = tk.Frame(self.left_panel, bg="#1e1e1e")
        self.sync_tipo = tk.StringVar(value="mutex")
        ttk.Label(
            self.sync_selector,
            text="Tipo de sincronización:",
            background="#1e1e1e",
            foreground="white",
        ).pack(pady=5)
        ttk.Radiobutton(
            self.sync_selector, text="Mutex", variable=self.sync_tipo, value="mutex"
        ).pack(anchor="w")
        ttk.Radiobutton(
            self.sync_selector,
            text="Semáforo",
            variable=self.sync_tipo,
            value="semaforo",
        ).pack(anchor="w")

        self.algoritmos = {
            "FIFO": fifo,
            "SJF": sjf,
            "SRT": srt,
            "Round Robin": round_robin,
            "Priority": priority,
        }

        self.simulacion_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        tk.Label(
            self.simulacion_frame,
            text="Seleccione uno o más algoritmos:",
            bg="#1e1e1e",
            fg="white",
            font=("Arial", 12),
        ).pack(pady=5)
        self.algoritmo_vars = {}
        for nombre in self.algoritmos:
            var = tk.BooleanVar(value=(nombre == "FIFO"))
            self.algoritmo_vars[nombre] = var
            ttk.Checkbutton(
                self.simulacion_frame,
                text=nombre,
                variable=var,
                command=self.actualizar_vista,
            ).pack(anchor="w", padx=20)

        self.quantum_frame = tk.Frame(self.simulacion_frame, bg="#1e1e1e")
        self.quantum_label = tk.Label(
            self.quantum_frame, text="Quantum:", bg="#1e1e1e", fg="white"
        )
        self.quantum_label.pack(side="left")
        self.quantum_entry = tk.Entry(self.quantum_frame, width=5)
        self.quantum_entry.insert(0, "3")
        self.quantum_entry.pack(side="left")
        self.quantum_frame.pack(pady=5)
        self.quantum_frame.pack_forget()

        self.boton_cargar = ttk.Button(
            self.control_panel,
            text="Cargar Procesos",
            command=self.cargar_procesos,
            style="Black.TButton",
        )
        self.boton_cargar.pack(pady=5)
        self.boton_simular = ttk.Button(
            self.control_panel,
            text="Simular",
            command=self.simular,
            style="Black.TButton",
        )
        self.boton_simular.pack(pady=5)
        self.boton_limpiar = ttk.Button(
            self.control_panel,
            text="Limpiar Procesos",
            command=self.limpiar_procesos,
            style="Black.TButton",
        )
        self.boton_limpiar.pack(pady=5)

        self.canvas = tk.Canvas(
            self.canvas_frame, height=200, bg="white", scrollregion=(0, 0, 5000, 200)
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_x = tk.Scrollbar(
            self.canvas_frame, orient="horizontal", command=self.canvas.xview
        )
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.config(xscrollcommand=self.scroll_x.set)

        self.actualizar_modo()

    def actualizar_modo(self):
        modo = self.modo_var.get()
        if modo == "calendarizacion":
            self.simulacion_frame.pack(fill="x", pady=10)
            self.sync_selector.pack_forget()
        else:
            self.simulacion_frame.pack_forget()
            self.sync_selector.pack(fill="x", pady=10)

    def actualizar_vista(self):
        if self.algoritmo_vars["Round Robin"].get():
            self.quantum_frame.pack(pady=5)
        else:
            self.quantum_frame.pack_forget()

    def cargar_procesos(self):
        modo = self.modo_var.get()
        archivo = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
        if not archivo:
            return
        if modo == "calendarizacion":
            self.procesos = leer_procesos(archivo)
        else:
            if "procesos" in archivo:
                self.procesos = leer_procesos_sync(archivo)
            elif "recursos" in archivo:
                self.recursos = leer_recursos(archivo)
            elif "acciones" in archivo:
                self.acciones = leer_acciones(archivo)
        self.colors = {p.pid: self.generar_color() for p in self.procesos}
        messagebox.showinfo("Éxito", "Archivo cargado correctamente.")

    def limpiar_procesos(self):
        self.procesos = []
        self.canvas.delete("all")
        messagebox.showinfo(
            "Limpieza", "Los procesos han sido eliminados y el canvas ha sido limpiado."
        )

    def generar_color(self):
        return f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}"

    def simular(self):
        self.canvas.delete("all")
        modo = self.modo_var.get()
        if modo == "calendarizacion":
            if not self.procesos:
                messagebox.showwarning("Error", "Primero carga un archivo de procesos.")
                return
            for nombre, activo in self.algoritmo_vars.items():
                if activo.get():
                    funcion = self.algoritmos[nombre]
                    if nombre == "Round Robin":
                        try:
                            quantum = int(self.quantum_entry.get())
                            if quantum <= 0:
                                raise ValueError
                        except ValueError:
                            messagebox.showerror(
                                "Error",
                                "Quantum inválido. Ingrese un número entero > 0.",
                            )
                            continue
                        resultado = funcion(deepcopy(self.procesos), quantum)
                    else:
                        resultado = funcion(deepcopy(self.procesos))
                    self.dibujar_gantt(resultado)
                    avg_wt, avg_tat = calcular_metricas(resultado)
                    messagebox.showinfo(
                        f"Métricas ({nombre})",
                        f"Tiempo de Espera Promedio: {avg_wt:.2f} ciclos\nTurnaround Time Promedio: {avg_tat:.2f} ciclos",
                    )
        else:
            if not self.procesos or not self.recursos or not self.acciones:
                messagebox.showerror(
                    "Error", "Faltan procesos, recursos o acciones para simular."
                )
                return
            tipo = self.sync_tipo.get()
            if tipo == "mutex":
                simulador = MutexSimulador(self.procesos, self.recursos, self.acciones)
            else:
                simulador = SemaforoSimulador(
                    self.procesos, self.recursos, self.acciones
                )
            resultado = simulador.ejecutar()
            self.dibujar_sync(resultado)

    def dibujar_gantt(self, procesos):
        escala = 25
        x = 10
        timeline = []
        for p in procesos:
            for t in range(p.start_time, p.end_time):
                timeline.append((p.pid, t))
        for pid, ciclo in timeline:
            self.root.update()
            color = self.colors.get(pid, "#cccccc")
            self.canvas.create_rectangle(
                x, 40, x + escala, 100, fill=color, outline="black"
            )
            self.canvas.create_text(x + escala // 2, 70, text=pid, font=("Arial", 9))
            self.canvas.create_text(
                x, 110, text=str(ciclo), anchor="n", font=("Arial", 8)
            )
            x += escala
            time.sleep(0.03)
        if timeline:
            self.canvas.create_text(
                x, 110, text=str(timeline[-1][1] + 1), anchor="n", font=("Arial", 8)
            )

    def dibujar_sync(self, procesos):
        escala = 25
        x = 10
        for p in procesos:
            for ciclo, estado in p.historial:
                self.root.update()
                color = "green" if estado == "ACCESSED" else "red"
                self.canvas.create_rectangle(
                    x, 40, x + escala, 100, fill=color, outline="black"
                )
                self.canvas.create_text(
                    x + escala // 2, 70, text=p.pid, font=("Arial", 9)
                )
                self.canvas.create_text(
                    x, 110, text=str(ciclo), anchor="n", font=("Arial", 8)
                )
                x += escala
                time.sleep(0.03)
        if procesos and procesos[0].historial:
            self.canvas.create_text(
                x,
                110,
                text=str(procesos[0].historial[-1][0] + 1),
                anchor="n",
                font=("Arial", 8),
            )
