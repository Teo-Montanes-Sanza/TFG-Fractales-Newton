import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "text.usetex": False 
})

def mandelbrot_set_sombreado(resolucion=1000, max_iter=80, escape_radius=2):
    x_min, x_max = -2.0, 0.5
    y_min, y_max = -1.25, 1.25
    
    x = np.linspace(x_min, x_max, resolucion)
    y = np.linspace(y_min, y_max, resolucion)
    X, Y = np.meshgrid(x, y)
    
    C = X + 1j * Y
    Z = np.zeros_like(C)
    
    matriz_escape = np.full(C.shape, max_iter, dtype=float)
    mask = np.full(C.shape, True, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + C[mask]
        
        escaped = np.abs(Z) > escape_radius
        
        puntos_fugados = Z[mask & escaped]
        magnitud = np.abs(puntos_fugados)
        
        iteracion_suave = i + 1 - np.log(np.log(magnitud)) / np.log(2)
        
        matriz_escape[mask & escaped] = iteracion_suave
        mask[escaped] = False

    colores_base = ['black', '#D81B60', '#1E88E5', '#FFC107']
    colores_rgb = [mcolors.to_rgb(c) for c in colores_base]
    imagen_rgb = np.zeros((resolucion, resolucion, 3))

    interior = mask

    indices_color = (matriz_escape.astype(int) % 3) + 1

    for j in range(1, 4):
        mascara_color = (indices_color == j) & (~interior)
        color = np.array(colores_rgb[j])
        
        imagen_rgb[mascara_color] = color


    return imagen_rgb, (x_min, x_max, y_min, y_max)

print("Calculando el espacio de parámetros del conjunto de Mandelbrot...")
imagen_rgb, extension = mandelbrot_set_sombreado(resolucion=1500)

plt.figure(figsize=(10, 10), dpi=300)

plt.imshow(imagen_rgb, extent=extension, origin='lower')

plt.xticks(np.arange(-2.0, 0.6, 0.5), fontsize=10, family='serif')
plt.yticks(np.arange(-1.0, 1.5, 0.5), fontsize=10, family='serif')

plt.xlabel(r"$Re(c)$", fontsize=14, family='serif')
plt.ylabel(r"$Im(c)$", fontsize=14, family='serif')

plt.savefig("Figura4.3.png", bbox_inches='tight')
print("¡Imagen guardada con éxito!")
plt.show()
