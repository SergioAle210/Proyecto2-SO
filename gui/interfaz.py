import tkinter as tk
from tkinter import filedialog, messagebox
from scheduler.utils import leer_procesos, calcular_metricas
from scheduler.fifo import fifo
from scheduler.sjf import sjf
from scheduler.round_robin import round_robin
from tkinter import ttk

import time


class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador SO 2025 - UVG")
        self.root.geometry("850x500")
        self.procesos = []

        self.boton_cargar = tk.Button(
            root, text="Cargar Procesos", command=self.cargar_procesos
        )

        self.algoritmos = {"FIFO": fifo, "SJF": sjf, "Round Robin": round_robin}
        self.algoritmo_var = tk.StringVar()
        self.algoritmo_selector = ttk.Combobox(
            root, textvariable=self.algoritmo_var, values=list(self.algoritmos.keys())
        )

        self.quantum_frame = tk.Frame(root)
        self.quantum_label = tk.Label(self.quantum_frame, text="Quantum:")
        self.quantum_label.pack(side="left")
        self.quantum_entry = tk.Entry(self.quantum_frame, width=5)
        self.quantum_entry.pack(side="left")
        self.quantum_frame.pack(pady=5)
        self.quantum_frame.pack_forget()  # Oculto por defecto

        self.algoritmo_selector.bind("<<ComboboxSelected>>", self.actualizar_vista)

        self.algoritmo_selector.set("FIFO")  # Valor por defecto
        self.algoritmo_selector.pack(pady=10)

        self.boton_cargar.pack(pady=10)

        self.boton_simular = tk.Button(root, text="Simular", command=self.simular)
        self.boton_simular.pack(pady=10)

        self.canvas = tk.Canvas(
            root, height=100, bg="white", scrollregion=(0, 0, 3000, 100)
        )
        self.canvas.pack(fill="both", expand=True)

        self.scroll_x = tk.Scrollbar(
            root, orient="horizontal", command=self.canvas.xview
        )
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.config(xscrollcommand=self.scroll_x.set)

    def cargar_procesos(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
        if archivo:
            self.procesos = leer_procesos(archivo)
            messagebox.showinfo(
                "Carga Exitosa", f"Se cargaron {len(self.procesos)} procesos."
            )

    def simular(self):
        if not self.procesos:
            messagebox.showwarning("Error", "Primero carga un archivo de procesos.")
            return

        algoritmo_nombre = self.algoritmo_var.get()
        if algoritmo_nombre not in self.algoritmos:
            messagebox.showerror("Error", "Selecciona un algoritmo válido.")
            return

        self.canvas.delete("all")
        algoritmo_funcion = self.algoritmos[algoritmo_nombre]

        if algoritmo_nombre == "Round Robin":
            try:
                quantum = int(self.quantum_entry.get())
                if quantum <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Error", "Quantum inválido. Ingresa un número entero mayor a 0."
                )
                return
            procesos_resultado = algoritmo_funcion(self.procesos, quantum)
        else:
            procesos_resultado = algoritmo_funcion(self.procesos)

        procesos_resultado = algoritmo_funcion(self.procesos)
        self.dibujar_gantt(procesos_resultado)

        avg_wt, avg_tat = calcular_metricas(procesos_resultado)
        messagebox.showinfo(
            f"Métricas - {algoritmo_nombre}",
            f"Tiempo de Espera Promedio: {avg_wt:.2f} ciclos\n"
            f"Turnaround Time Promedio: {avg_tat:.2f} ciclos",
        )

    def dibujar_gantt(self, procesos):
        escala = 30
        x = 10

        for proceso in procesos:
            inicio = proceso.start_time
            duracion = proceso.bt
            for t in range(duracion):
                self.root.update()
                self.canvas.create_rectangle(
                    x, 20, x + escala, 70, fill="skyblue", outline="black"
                )
                self.canvas.create_text(x + escala // 2, 45, text=proceso.pid)
                self.canvas.create_text(x, 80, text=str(inicio + t), anchor="n")
                x += escala
                time.sleep(0.2)

        self.canvas.create_text(x, 80, text=str(procesos[-1].end_time), anchor="n")

    def actualizar_vista(self, event):
        algoritmo = self.algoritmo_var.get()
        if algoritmo == "Round Robin":
            self.quantum_frame.pack(pady=5)
        else:
            self.quantum_frame.pack_forget()
