import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.widgets import TextBox, Button
from matplotlib.ticker import MultipleLocator

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Computer Modern Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "text.usetex": False 
})

colores_base = ['black', '#D81B60', '#1E88E5', '#FFC107']
colores_rgb = np.array([mcolors.to_rgb(c) for c in colores_base])

current_a = -0.5 + 0.5j
camera_center = 0.0 + 0.0j
estado_camara = "_CO"
current_matriz = None
current_limites = None

def calcular_fractal_newton_granular(a_val, x_min, x_max, y_min, y_max, resolucion=800, max_iter=50, tolerancia=1e-3):
    x = np.linspace(x_min, x_max, resolucion)
    y = np.linspace(y_min, y_max, resolucion)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    matriz_iteraciones = np.full(Z.shape, max_iter, dtype=float)
    matriz_destinos = np.zeros(Z.shape, dtype=int)
    
    for i in range(max_iter):
        P = Z * (Z - 1) * (Z - a_val)
        dP = 3 * Z**2 - 2 * (a_val + 1) * Z + a_val
        dP[dP == 0] = 1e-15
        
        convergentes = (np.abs(P) < tolerancia) & (matriz_iteraciones == max_iter)
        matriz_iteraciones[convergentes] = i
        
        Z = Z - P / dP
        Z[np.isnan(Z) | np.isinf(Z)] = 1e10
        
    matriz_destinos[np.abs(Z - 0) < 1e-1] = 1 
    matriz_destinos[np.abs(Z - 1) < 1e-1] = 2 
    matriz_destinos[np.abs(Z - a_val) < 1e-1] = 3 
    
    imagen_rgb = np.zeros((resolucion, resolucion, 3))
    sombreado = (1.0 - (matriz_iteraciones / max_iter))**2
    
    for j in range(1, 4):
        mascara = (matriz_destinos == j)
        color = colores_rgb[j]
        factor_luz = (0.2 + 0.8 * sombreado[mascara])[:, np.newaxis]
        imagen_rgb[mascara] = color * factor_luz

    return imagen_rgb

fig, ax = plt.subplots(figsize=(9, 10))
plt.subplots_adjust(bottom=0.3) 

def renderizar_y_actualizar(nuevo_centro):
    global camera_center, current_matriz, current_limites
    camera_center = nuevo_centro
    
    xi, xf = camera_center.real - 2.0, camera_center.real + 2.0
    yi, yf = camera_center.imag - 2.0, camera_center.imag + 2.0
    
    current_matriz = calcular_fractal_newton_granular(current_a, xi, xf, yi, yf)
    current_limites = (xi, xf, yi, yf)
    
    img.set_data(current_matriz)
    img.set_extent([xi, xf, yi, yf])
    ax.set_xlim(xi, xf)
    ax.set_ylim(yi, yf)
    
    raices_scat.set_offsets(np.array([[0,0], [1,0], [current_a.real, current_a.imag]]))
    z_cr_actual = (current_a + 1) / 3
    critico_scat.set_offsets(np.array([[z_cr_actual.real, z_cr_actual.imag]]))
    
    ax.set_title(f"Plano Dinámico de la Familia Cúbica con $a = {current_a.real} + {current_a.imag}i$", fontsize=15, family='serif')
    fig.canvas.draw_idle()

img = ax.imshow(np.zeros((10,10,3)), origin='lower') 
raices_scat = ax.scatter([], [], color='white', edgecolor='black', s=100, zorder=5, label='Raíces')
critico_scat = ax.scatter([], [], color='white', marker='X', edgecolor='black', s=120, zorder=10, label='Punto Crítico')

ax.set_xlabel(r"$Re(z)$", fontsize=14, family='serif')
ax.set_ylabel(r"$Im(z)$", fontsize=14, family='serif')
ax.legend(loc="upper right", fontsize=10, prop={'family': 'serif'})
ax.xaxis.set_major_locator(MultipleLocator(0.5))
ax.yaxis.set_major_locator(MultipleLocator(0.5))

renderizar_y_actualizar(camera_center)

axbox_real = plt.axes([0.10, 0.18, 0.10, 0.05])
axbox_imag = plt.axes([0.30, 0.18, 0.10, 0.05])
text_real = TextBox(axbox_real, '$Re(a)$ ', initial=str(current_a.real))
text_imag = TextBox(axbox_imag, '$Im(a)$ ', initial=str(current_a.imag))

ax_btn_gen = plt.axes([0.45, 0.18, 0.22, 0.05])
btn_gen = Button(ax_btn_gen, 'Generar Imagen', color='#009688', hovercolor='#00796B')
btn_gen.label.set_color('white')
btn_gen.label.set_weight('bold')

ax_btn_save = plt.axes([0.70, 0.18, 0.22, 0.05])
btn_save = Button(ax_btn_save, 'Guardar Imagen', color='#1E88E5', hovercolor='#1565C0')
btn_save.label.set_color('white')
btn_save.label.set_weight('bold')

ax_btn_orig = plt.axes([0.10, 0.08, 0.35, 0.05])
btn_orig = Button(ax_btn_orig, 'Centrar en el Origen (0,0)')

ax_btn_zcr = plt.axes([0.55, 0.08, 0.35, 0.05])
btn_zcr = Button(ax_btn_zcr, 'Centrar en el Punto Crítico')

def leer_parametro():
    try:
        return float(text_real.text) + 1j * float(text_imag.text)
    except ValueError:
        return None

def accion_generar(event):
    global current_a
    val_a = leer_parametro()
    if val_a is None:
        ax.set_title("Error: Introduce números válidos")
        fig.canvas.draw_idle()
        return

    current_a = val_a
    ax.set_title("Generando el Nuevo Plano Dinámico...", family='serif')
    fig.canvas.draw_idle()
    plt.pause(0.1) 
    renderizar_y_actualizar(camera_center)

def accion_guardar(event):
    ax.set_title("Guardando imagen...", family='serif')
    fig.canvas.draw_idle()
    plt.pause(0.1)
    
    xi, xf, yi, yf = current_limites
    nombre_archivo = f"Fam_Cubica_Plano_Dim_a_{current_a.real}_{current_a.imag}{estado_camara}.png"
    
    fig_save, ax_save = plt.subplots(figsize=(8, 8), dpi=300)
    ax_save.imshow(current_matriz, extent=[xi, xf, yi, yf], origin='lower')
    ax_save.set_xlim(xi, xf)
    ax_save.set_ylim(yi, yf)
    
    z_cr_actual = (current_a + 1) / 3
    ax_save.scatter([0, 1, current_a.real], [0, 0, current_a.imag], color='white', edgecolor='black', s=100, zorder=5, label='Raíces')
    ax_save.scatter([z_cr_actual.real], [z_cr_actual.imag], color='white', marker='X', edgecolor='black', s=110, zorder=10, label='Punto Crítico')
    
    ax_save.set_xlabel(r"$Re(z)$", fontsize=14, family='serif')
    ax_save.set_ylabel(r"$Im(z)$", fontsize=14, family='serif')
    ax_save.xaxis.set_major_locator(MultipleLocator(0.5))
    ax_save.yaxis.set_major_locator(MultipleLocator(0.5))
    ax_save.legend(loc="upper right", fontsize=10, prop={'family': 'serif'})
    
    fig_save.savefig(nombre_archivo, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig_save)
    
    ax.set_title(f"Imagen guardada como {nombre_archivo}", family='serif')
    fig.canvas.draw_idle()

def mover_a_origen(event):
    global estado_camara
    estado_camara = "_CO"
    ax.set_title("Moviendo cámara a (0,0)...", family='serif')
    fig.canvas.draw_idle()
    plt.pause(0.1)
    renderizar_y_actualizar(0.0 + 0.0j)

def mover_a_critico(event):
    global estado_camara
    estado_camara = "_CPC"
    centro_critico = (current_a + 1) / 3
    ax.set_title("Moviendo cámara al Punto Crítico...", family='serif')
    fig.canvas.draw_idle()
    plt.pause(0.1)
    renderizar_y_actualizar(centro_critico)

btn_gen.on_clicked(accion_generar)
btn_save.on_clicked(accion_guardar)
btn_orig.on_clicked(mover_a_origen)
btn_zcr.on_clicked(mover_a_critico)

plt.show()
