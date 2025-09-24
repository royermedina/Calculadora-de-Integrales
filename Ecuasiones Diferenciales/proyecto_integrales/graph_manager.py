"""
Clase especializada para manejar gráficos matemáticos
"""
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sympy import *

class GraphManager:
    """Clase especializada para manejar gráficos matemáticos"""
    
    def __init__(self, graph_frame, btn_cerrar_grafico):
        self.graph_frame = graph_frame
        self.btn_cerrar_grafico = btn_cerrar_grafico
        self.current_canvas = None
    
    def crear_grafico(self, funcion_str, pasos_actuales=None):
        """Crear gráfico de la función y su integral"""
        try:
            if not funcion_str:
                messagebox.showwarning("Advertencia", "Ingresa una función para graficar")
                return
            
            # Limpiar frame anterior
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            # Crear figura con tamaño más compacto
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6))
            fig.patch.set_facecolor('#0d1117')
            
            # Parsear función
            x = Symbol('x')
            funcion = parse_expr(funcion_str, transformations='all')
            
            # Crear función numérica
            func_lambdified = lambdify(x, funcion, 'numpy')
            
            # Rango de valores
            x_vals = np.linspace(-5, 5, 1000)
            
            try:
                y_vals = func_lambdified(x_vals)
                
                # Gráfico de la función original
                ax1.plot(x_vals, y_vals, color='#58a6ff', linewidth=2, label=f'f(x) = {funcion}')
                ax1.grid(True, alpha=0.3, color='#30363d')
                ax1.set_facecolor('#0d1117')
                ax1.tick_params(colors='#f0f6fc', labelsize=8)
                ax1.set_title('Función Original', color='#f0f6fc', fontsize=10, fontweight='bold')
                ax1.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='#f0f6fc', fontsize=8)
                
                # Intentar graficar la integral
                if pasos_actuales:
                    try:
                        integral_result = integrate(funcion, x)
                        integral_lambdified = lambdify(x, integral_result, 'numpy')
                        y_integral = integral_lambdified(x_vals)
                        
                        ax2.plot(x_vals, y_integral, color='#22c55e', linewidth=2, 
                                label=f'∫f(x)dx = {integral_result}')
                        ax2.grid(True, alpha=0.3, color='#30363d')
                        ax2.set_facecolor('#0d1117')
                        ax2.tick_params(colors='#f0f6fc', labelsize=8)
                        ax2.set_title('Función Integral', color='#f0f6fc', fontsize=10, fontweight='bold')
                        ax2.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='#f0f6fc', fontsize=8)
                    except:
                        ax2.text(0.5, 0.5, 'Integral no graficable', transform=ax2.transAxes,
                                ha='center', va='center', color='#7d8590', fontsize=10)
                        ax2.set_facecolor('#0d1117')
                
            except Exception as e:
                ax1.text(0.5, 0.5, f'Error al graficar:\n{str(e)}', transform=ax1.transAxes,
                        ha='center', va='center', color='#ef4444', fontsize=9)
                ax1.set_facecolor('#0d1117')
            
            plt.tight_layout()
            
            # Integrar con tkinter
            self.current_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(fill='both', expand=True)
            
            # Mostrar botón de cerrar gráfico
            self.btn_cerrar_grafico.pack(side='right', padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el gráfico: {str(e)}")
    
    def cerrar_grafico(self):
        """Cerrar el gráfico actual y mostrar placeholder"""
        # Limpiar widgets del frame de gráficos
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Restaurar placeholder
        placeholder = tk.Label(self.graph_frame, text="📈\nEl gráfico aparecerá aquí\ncuando resuelvas una integral", 
                font=("Segoe UI", 11), fg='#7d8590', bg='#0d1117')
        placeholder.pack(expand=True)
        
        # Ocultar botón de cerrar
        self.btn_cerrar_grafico.pack_forget()
        
        # Limpiar referencia al canvas
        self.current_canvas = None
