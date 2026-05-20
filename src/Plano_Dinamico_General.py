import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.widgets import TextBox, Button
import sympy as sp

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Computer Modern Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", 
    "text.usetex": False
})

colores_base = ['black', '#D81B60', '#1E88E5', '#FFC107', '#009688', '#9C27B0', '#FF5722', '#795548']
colores_rgb = np.array([mcolors.to_rgb(c) for c in colores_base])

current_poly_str = "z**3 - 1"
current_poly_latex = "z^3 - 1"
current_matriz = None
current_raices = None
current_criticos = None

def parsear_polinomio(expr_str):
    z = sp.symbols('z')
    try:
        P_sym = sp.sympify(expr_str)
        dP_sym = sp.diff(P_sym, z)
        poly_latex = sp.latex(P_sym)
        poly_p = sp.Poly(P_sym, z)
        coef_p = [complex(c) for c in poly_p.all_coeffs()]
        raices = np.roots(coef_p)
        poly_dp = sp.Poly(dP_sym, z)
        coef_dp = [complex(c) for c in poly_dp.all_coeffs()]
        criticos = np.roots(coef_dp)
        P_func = sp.lambdify(z, P_sym, modules='numpy')
        dP_func = sp.lambdify(z, dP_sym, modules='numpy')
        return P_func, dP_func, raices, criticos, poly_latex
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None, None

def calcular_fractal_granular(P_func, dP_func, raices, resolucion=800, max_iter=50, tolerancia=1e-3):
    z_range = 2.0
    x = np.linspace(-z_range, z_range, resolucion)
    y = np.linspace(-z_range, z_range, resolucion)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    matriz_iteraciones = np.full(Z.shape, max_iter, dtype=float)
    matriz_destinos = np.zeros(Z.shape, dtype=int)
    for i in range(max_iter):
        P_val = P_func(Z)
        dP_val = dP_func(Z)
        dP_val[dP_val == 0] = 1e-15
        convergentes = (np.abs(P_val) < tolerancia) & (matriz_iteraciones == max_iter)
        matriz_iteraciones[convergentes] = i
        Z = Z - P_val / dP_val
        Z[np.isnan(Z) | np.isinf(Z)] = 1e10
    for j, raiz in enumerate(raices):
        matriz_destinos[np.abs(Z - raiz) < 1e-1] = (j % (len(colores_base)-1)) + 1
    imagen_rgb = np.zeros((resolucion, resolucion, 3))
    sombreado = (1.0 - (matriz_iteraciones / max_iter))**2 
    for j in range(len(raices) + 1):
        idx_color = j % len(colores_base)
        mascara = (matriz_destinos == j)
        color = colores_rgb[idx_color]
        if j == 0:
            imagen_rgb[mascara] = color
        else:
            factor_luz = (0.2 + 0.8 * sombreado[mascara])[:, np.newaxis]
            imagen_rgb[mascara] = color * factor_luz
    return imagen_rgb

fig, ax = plt.subplots(figsize=(9, 10))
plt.subplots_adjust(bottom=0.25)
img = ax.imshow(np.zeros((10,10,3)), extent=[-2, 2, -2, 2], origin='lower')

raices_scat = ax.scatter([], [], color='white', edgecolor='black', s=80, zorder=5, label='Raíces')
criticos_scat = ax.scatter([], [], color='white', marker='X', edgecolor='black', s=90, zorder=6, label='Puntos Críticos')

ax.set_xlabel(r"Re(z)", fontsize=14, family='serif')
ax.set_ylabel(r"Im(z)", fontsize=14, family='serif')

axbox_poly = plt.axes([0.15, 0.12, 0.45, 0.05])
text_poly = TextBox(axbox_poly, 'P(z) = ', initial=current_poly_str)

ax_btn_gen = plt.axes([0.65, 0.12, 0.25, 0.05])
btn_gen = Button(ax_btn_gen, 'Generar Imagen', color='#009688', hovercolor='#00796B')
btn_gen.label.set_color('white')
btn_gen.label.set_weight('bold')

ax_btn_save = plt.axes([0.15, 0.04, 0.75, 0.05])
btn_save = Button(ax_btn_save, 'Guardar Imagen', color='#1E88E5', hovercolor='#1565C0')
btn_save.label.set_color('white')
btn_save.label.set_weight('bold')

def accion_generar(event):
    global current_matriz, current_raices, current_criticos, current_poly_str, current_poly_latex
    P_f, dP_f, r_list, c_list, p_latex = parsear_polinomio(text_poly.text)
    if P_f is not None:
        ax.set_title("Calculando plano dinámico...", family='serif')
        fig.canvas.draw_idle()
        plt.pause(0.1)
        current_poly_str, current_poly_latex = text_poly.text, p_latex
        current_raices, current_criticos = r_list, c_list
        current_matriz = calcular_fractal_granular(P_f, dP_f, r_list)
        img.set_data(current_matriz)
        raices_scat.set_offsets(np.column_stack((r_list.real, r_list.imag)))
        criticos_scat.set_offsets(np.column_stack((c_list.real, c_list.imag)))
        ax.legend(loc='upper right', fontsize=10, framealpha=0.8)
        ax.set_title(f"Plano Dinámico: $P(z) = {current_poly_latex}$", fontsize=15, family='serif')
        fig.canvas.draw_idle()

def accion_guardar(event):
    if current_matriz is None: return
    ax.set_title("Guardando imagen...", family='serif')
    fig.canvas.draw_idle()
    plt.pause(0.1)
    
    nombre = f"Plano_Dinamico_{current_poly_str.replace('*','').replace(' ','')}.png"
    fig_save, ax_save = plt.subplots(figsize=(8, 8), dpi=300)
    ax_save.imshow(current_matriz, extent=[-2, 2, -2, 2], origin='lower')
    ax_save.scatter(current_raices.real, current_raices.imag, color='white', edgecolor='black', s=100, zorder=5, label='Raíces')
    ax_save.scatter(current_criticos.real, current_criticos.imag, color='white', marker='X', edgecolor='black', s=110, zorder=10, label='Puntos Críticos')
    ax_save.legend(loc='upper right', fontsize=10)
    ax_save.set_xlabel(r"Re(z)", fontsize=14, family='serif')
    ax_save.set_ylabel(r"Im(z)", fontsize=14, family='serif')
        
    fig_save.savefig(nombre, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig_save)
    ax.set_title(f"¡Imagen guardada como {nombre}!", family='serif')
    fig.canvas.draw_idle()

btn_gen.on_clicked(accion_generar)
btn_save.on_clicked(accion_guardar)
accion_generar(None)
plt.show()
