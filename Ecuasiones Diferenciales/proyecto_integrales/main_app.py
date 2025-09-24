"""
Clase principal que coordina todas las funcionalidades de la aplicación
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from sympy import *

from math_solver import MathSolver
from ui_manager import UIManager
from step_renderer import StepRenderer
from graph_manager import GraphManager

class MainApp:
    """Clase principal que coordina todas las funcionalidades de la aplicación"""
    
    def __init__(self, root):
        self.root = root
        
        # Inicializar componentes
        self.ui_manager = UIManager(root)
        self.math_solver = MathSolver()
        
        # Crear panel de resultados usando StepRenderer
        main_container = None
        for child in root.winfo_children():
            if isinstance(child, tk.Frame) and child.cget('bg') == '#0d1117':
                main_container = child
                break
        
        if main_container:
            self.step_renderer = StepRenderer(root)
            result_frame = self.step_renderer.crear_panel_resultados(main_container)
        
        # Crear GraphManager
        self.graph_manager = GraphManager(
            self.ui_manager.graph_frame, 
            self.ui_manager.btn_cerrar_grafico
        )
        
        # Establecer referencias cruzadas
        self.ui_manager.set_step_renderer(self.step_renderer)
        self.ui_manager.set_graph_manager(self.graph_manager)
        self.ui_manager.set_main_app(self)
        
        # Variables de estado
        self.pasos_actuales = []
    
    def resolver_integral(self):
        """Resolver la integral paso a paso"""
        try:
            funcion_str = self.ui_manager.get_funcion_str()
            if not funcion_str:
                messagebox.showerror("Error", "Ingresa una función para integrar")
                return
            
            # Parsear la función
            x = Symbol(self.ui_manager.get_variable_str())
            try:
                funcion = parse_expr(funcion_str, transformations='all')
            except:
                messagebox.showerror("Error", f"No se puede interpretar la función: {funcion_str}")
                return
            
            # Resolver paso a paso usando MathSolver
            pasos, resultado = self.math_solver.resolver_integral_general(funcion, x)
            self.pasos_actuales = pasos
            
            # Mostrar resultados usando StepRenderer
            self.step_renderer.mostrar_pasos_detallados(
                pasos, resultado, funcion_str, self.ui_manager.get_variable_str()
            )
            
            # Si es definida, calcular valor numérico
            if self.ui_manager.get_tipo_integral() == "definida" and resultado:
                self.calcular_integral_definida(funcion, x, resultado)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def calcular_integral_definida(self, funcion, variable, antiderivada):
        """Calcular integral definida con pasos"""
        try:
            limite_inf_str, limite_sup_str = self.ui_manager.get_limites()
            limite_inf = parse_expr(limite_inf_str)
            limite_sup = parse_expr(limite_sup_str)
            
            # Evaluar en los límites
            valor_sup = antiderivada.subs(variable, limite_sup)
            valor_inf = antiderivada.subs(variable, limite_inf)
            resultado_def = simplify(valor_sup - valor_inf)
            
            # Agregar pasos de la integral definida
            pasos_definida = [{
                'titulo': 'Teorema Fundamental del Cálculo',
                'formula': f'F({limite_sup}) - F({limite_inf})',
                'formula_latex': f'F\\left({latex(limite_sup)}\\right) - F\\left({latex(limite_inf)}\\right)',
                'explicacion': 'Evaluamos la antiderivada en los límites de integración.',
                'tipo': 'metodo'
            }, {
                'titulo': 'Evaluación en límite superior',
                'formula': f'F({limite_sup}) = {valor_sup}',
                'formula_latex': f'F\\left({latex(limite_sup)}\\right) = {latex(valor_sup)}',
                'explicacion': f'Sustituimos x = {limite_sup} en la antiderivada.',
                'tipo': 'aplicacion'
            }, {
                'titulo': 'Evaluación en límite inferior',
                'formula': f'F({limite_inf}) = {valor_inf}',
                'formula_latex': f'F\\left({latex(limite_inf)}\\right) = {latex(valor_inf)}',
                'explicacion': f'Sustituimos x = {limite_inf} en la antiderivada.',
                'tipo': 'aplicacion'
            }, {
                'titulo': 'RESULTADO NUMÉRICO',
                'formula': f'{resultado_def}',
                'formula_latex': f'{latex(resultado_def)}',
                'explicacion': 'Resultado de la integral definida.',
                'tipo': 'resultado'
            }]
            
            # Agregar estos pasos a la visualización
            for paso in pasos_definida:
                self.pasos_actuales.append(paso)
            
            # Actualizar visualización
            self.step_renderer.mostrar_pasos_detallados(
                self.pasos_actuales, None, 
                self.ui_manager.get_funcion_str(), 
                self.ui_manager.get_variable_str()
            )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en integral definida: {str(e)}")
    
    def graficar_funcion(self):
        """Crear gráfico de la función y su integral"""
        funcion_str = self.ui_manager.get_funcion_str()
        self.graph_manager.crear_grafico(funcion_str, self.pasos_actuales)
    
    def exportar_solucion(self):
        """Exportar solución a archivo de texto"""
        if not self.pasos_actuales:
            messagebox.showwarning("Advertencia", "Primero resuelve una integral")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")],
                title="Guardar solución"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("SOLUCIONADOR AVANZADO DE INTEGRALES\n")
                    f.write("="*50 + "\n")
                    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Función: {self.ui_manager.get_funcion_str()}\n")
                    f.write(f"Tipo: {self.ui_manager.get_tipo_integral()}\n\n")
                    
                    for i, paso in enumerate(self.pasos_actuales, 1):
                        f.write(f"PASO {i}: {paso['titulo']}\n")
                        f.write("-"*40 + "\n")
                        if 'formula' in paso:
                            f.write(f"Fórmula: {paso['formula']}\n")
                        if 'explicacion' in paso:
                            f.write(f"Explicación: {paso['explicacion']}\n")
                        f.write("\n")
                
                messagebox.showinfo("Éxito", f"Solución guardada en: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def limpiar_todo(self):
        """Limpiar toda la interfaz"""
        # Limpiar campos de entrada
        self.ui_manager.funcion_var.set("")
        self.ui_manager.variable_var.set("x")
        self.ui_manager.limite_inf_var.set("0")
        self.ui_manager.limite_sup_var.set("1")
        self.ui_manager.tipo_integral.set("indefinida")
        
        # Limpiar pasos
        self.step_renderer.limpiar_pasos()
        self.pasos_actuales = []
        
        # Actualizar preview
        self.ui_manager.actualizar_preview()
        
        # Cerrar gráfico si existe
        self.graph_manager.cerrar_grafico()
        
        # Ocultar límites
        self.ui_manager.limites_frame.pack_forget()

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
