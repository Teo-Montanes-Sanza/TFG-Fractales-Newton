import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import warnings

# Ignorar warnings numéricos de desbordamiento en fractales
warnings.filterwarnings("ignore")

# Configuración de tipografía para los gráficos (Estilo LaTeX para tu memoria)
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "Times New Roman", "DejaVu Serif"],
})
# Paleta original de 4 colores exactos de tu TFG
COLORES_TFG = ListedColormap(['black', '#D81B60', '#1E88E5', '#FFC107'])

class AutoAnalizadorNewtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto-Analizador de Espacios de Parámetros (Newton)")
        self.root.geometry("900x850")
        
        # --- ESTILOS VISUALES MODERNOS ---
        style = ttk.Style()
        style.theme_use('clam') # Tema más limpio
        
        # Fuentes principales
        fuente_normal = ("Segoe UI", 11)
        fuente_negrita = ("Segoe UI", 11, "bold")
        fuente_mate = ("Consolas", 12)
        
        style.configure(".", font=fuente_normal, background="#F5F6F8")
        style.configure("TFrame", background="#F5F6F8")
        style.configure("TLabelframe", background="#F5F6F8", borderwidth=2)
        style.configure("TLabelframe.Label", font=fuente_negrita, foreground="#1E88E5", background="#F5F6F8")
        
        style.configure("BotonAccion.TButton", font=("Segoe UI", 11, "bold"), padding=8, background="#1E88E5", foreground="white")
        style.map("BotonAccion.TButton", background=[("active", "#1565C0")])
        
        style.configure("BotonRapido.TButton", font=("Segoe UI", 10), padding=5)
        
        self.root.configure(bg="#F5F6F8")

        # --- PANEL DE CONTROL ---
        frame_inputs = ttk.LabelFrame(self.root, text="Introducción de la Familia Paramétrica", padding=(15, 15))
        frame_inputs.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)
        
        # Entrada de la Función
        frame_formula = ttk.Frame(frame_inputs)
        frame_formula.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_formula, text="Función f(z, c):", font=fuente_negrita).pack(side=tk.LEFT, padx=5)
        self.entrada_funcion = ttk.Entry(frame_formula, width=40, font=fuente_mate)
        self.entrada_funcion.insert(0, "z*(z-1)*(z-c)")
        self.entrada_funcion.pack(side=tk.LEFT, padx=10)
        
        self.btn_generar = ttk.Button(frame_formula, text="Analizar y Generar Fractal", style="BotonAccion.TButton", command=self.procesar_y_dibujar)
        self.btn_generar.pack(side=tk.LEFT, padx=15)

        # Botones de Acceso Rápido
        frame_rapido = ttk.Frame(frame_inputs)
        frame_rapido.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_rapido, text="Cargar rápidos:", font=("Segoe UI", 10, "italic")).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_rapido, text="Familia Cuadrática", style="BotonRapido.TButton", 
                   command=lambda: self.cargar_formula("(z-1)*(z-c)")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_rapido, text="Familia Cúbica TFG", style="BotonRapido.TButton", 
                   command=lambda: self.cargar_formula("z*(z-1)*(z-c)")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_rapido, text="Cúbica Canónica", style="BotonRapido.TButton", 
                   command=lambda: self.cargar_formula("z**3 - 3*z + c")).pack(side=tk.LEFT, padx=5)

        # --- PANEL DE RESULTADOS MATEMÁTICOS ---
        frame_resultados = ttk.LabelFrame(self.root, text="Análisis Matemático Automático", padding=(15, 10))
        frame_resultados.pack(side=tk.TOP, fill=tk.X, padx=15, pady=5)

        self.lbl_raices = ttk.Label(frame_resultados, text="Raíces (Soluciones): Esperando análisis...", font=("Segoe UI", 11))
        self.lbl_raices.pack(anchor="w", pady=3)
        
        self.lbl_critico = ttk.Label(frame_resultados, text="Punto Crítico Libre (Semilla): Esperando análisis...", font=fuente_negrita, foreground="#D81B60")
        self.lbl_critico.pack(anchor="w", pady=3)

        self.lbl_modo = ttk.Label(frame_resultados, text="Modo de renderizado: Esperando...", font=("Segoe UI", 10, "italic"), foreground="#424242")
        self.lbl_modo.pack(anchor="w", pady=3)

        # --- PANEL DEL GRÁFICO ---
        self.frame_grafico = tk.Frame(self.root, bg="#F5F6F8")
        self.frame_grafico.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        self.fig.patch.set_facecolor('#F5F6F8') # Fondo del gráfico a juego con la UI
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def cargar_formula(self, formula):
        """Escribe la fórmula automáticamente en la entrada de texto."""
        self.entrada_funcion.delete(0, tk.END)
        self.entrada_funcion.insert(0, formula)

    def procesar_y_dibujar(self):
        self.btn_generar.config(state="disabled", text="Calculando álgebra...")
        self.root.update()
        
        func_str = self.entrada_funcion.get()
        z, c = sp.symbols('z c')
        
        try:
            expr_func = sp.sympify(func_str)
            d1 = sp.diff(expr_func, z)
            d2 = sp.diff(d1, z)
            
            raices_simbolicas = sp.solve(expr_func, z)
            txt_raices = ", ".join([str(sp.simplify(r)) for r in raices_simbolicas])
            self.lbl_raices.config(text=f"Raíces (P(z)=0): {txt_raices}")
            
            # DETECCIÓN DE FÓRMULAS DE CARDANO
            raices_complejas = len(txt_raices) > 50 or "sqrt" in txt_raices or "**(1/3)" in txt_raices
            
            if raices_complejas:
                self.lbl_modo.config(text="Modo: Raíces complejas (Cardano) detectadas. Renderizando por Velocidad para evitar cortes de rama.")
            else:
                self.lbl_modo.config(text="Modo: Raíces simples detectadas. Renderizando por Destino (Estilo TFG original).")

            puntos_criticos = sp.solve(d2, z)
            
            if not puntos_criticos:
                self.lbl_critico.config(text="Punto Crítico Libre: NINGUNO (Grado < 3)")
                self.ax.clear()
                self.fig.patch.set_facecolor('#F5F6F8')
                self.canvas.draw()
                messagebox.showinfo("Teorema de Cayley", "Esta función cuadrática no tiene puntos críticos libres.\n\nEl espacio de parámetros es trivial (no hay caos).")
                self.btn_generar.config(state="normal", text="Analizar y Generar Fractal")
                return
            
            pto_critico = sp.simplify(puntos_criticos[0])
            self.lbl_critico.config(text=f"Punto Crítico Libre (P''(z)=0): {pto_critico}")
            
            operador_iter = z - (expr_func / d1)
            
            self.btn_generar.config(text="Iterando Newton en plano complejo...")
            self.root.update()
            
            self.ax.clear()
            self.calcular_fractal(z, c, operador_iter, pto_critico, raices_simbolicas, func_str, expr_func, raices_complejas)
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la ecuación.\nDetalle: {str(e)}")
        finally:
            self.btn_generar.config(state="normal", text="Analizar y Generar Fractal")

    def evaluar_simbolico_numpy(self, expr_simbolica, c_simbolico, matriz_C):
        func_np = sp.lambdify((c_simbolico,), expr_simbolica, modules=['numpy'])
        evaluado = func_np(matriz_C)
        if np.isscalar(evaluado):
            return np.ones_like(matriz_C) * evaluado
        return evaluado.astype(complex)

    def calcular_fractal(self, z, c, operador_iter, pto_critico, raices_simbolicas, func_str, expr_func, raices_complejas):
        resolucion = 700
        max_iter = 40
        tolerancia = 1e-3 
        
        c_min, c_max = -15.5, 15.5
        c_im_min, c_im_max = -15.5, 15.5
        
        x = np.linspace(c_min, c_max, resolucion)
        y = np.linspace(c_im_min, c_im_max, resolucion)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        
        iterador_np = sp.lambdify((z, c), operador_iter, modules=['numpy'])
        poly_np = sp.lambdify((z, c), expr_func, modules=['numpy'])
        
        Z = self.evaluar_simbolico_numpy(pto_critico, c, C)
        
        matriz_colores = np.zeros(Z.shape, dtype=int)
        
        if raices_complejas:
            # MODO 2: Coloreado por iteraciones (Mandelbrot style)
            matriz_iteraciones = np.full(Z.shape, -1, dtype=int)
            mask = np.full(Z.shape, True, dtype=bool)
            
            for i in range(max_iter):
                P_val = poly_np(Z[mask], C[mask])
                converged_in_step = np.abs(P_val) < tolerancia
                
                converged_global = np.zeros(Z.shape, dtype=bool)
                converged_global[mask] = converged_in_step
                matriz_iteraciones[converged_global] = i
                mask[converged_global] = False
                
                if not np.any(mask):
                    break
                    
                Z_next = iterador_np(Z[mask], C[mask])
                Z[mask] = np.where(np.isnan(Z_next) | np.isinf(Z_next), Z[mask], Z_next)
                
            exterior = matriz_iteraciones != -1
            matriz_colores[exterior] = (matriz_iteraciones[exterior] % 3) + 1
            
        else:
            # MODO 1: Coloreado sólido por destino (Tu TFG Original)
            for _ in range(max_iter):
                Z_next = iterador_np(Z, C)
                Z = np.where(np.isnan(Z_next) | np.isinf(Z_next), Z, Z_next)
                
            for i, raiz_expr in enumerate(raices_simbolicas):
                raiz_matriz = self.evaluar_simbolico_numpy(raiz_expr, c, C)
                dist = np.abs(Z - raiz_matriz)
                matriz_colores[dist < tolerancia] = (i % 3) + 1
                
        self.ax.imshow(matriz_colores, extent=(c_min, c_max, c_im_min, c_im_max), cmap=COLORES_TFG, origin='lower')
        self.ax.set_title(f"Espacio de Parámetros (Newton)\n$f(z) = {func_str}$", fontsize=14)
        self.ax.set_xlabel(r"$Re(c)$", fontsize=12)
        self.ax.set_ylabel(r"$Im(c)$", fontsize=12)
        self.fig.patch.set_facecolor('white')

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoAnalizadorNewtonApp(root)
    root.mainloop()
