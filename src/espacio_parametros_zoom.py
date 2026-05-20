import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "text.usetex": False
})

def espacio_parametros_newton_granular(resolucion=1500, max_iter=150, tolerancia=1e-4):
    a_min, a_max = 0.400, 0.600
    a_im_min, a_im_max = 2.150, 2.350
    
    x = np.linspace(a_min, a_max, resolucion)
    y = np.linspace(a_im_min, a_im_max, resolucion)
    X, Y = np.meshgrid(x, y)
    
    A = X + 1j * Y

    Z = (A + 1) / 3

    matriz_iteraciones = np.full(A.shape, max_iter, dtype=float)
    matriz_destinos = np.zeros(A.shape, dtype=int)
    
    for i in range(max_iter):
        P = Z * (Z - 1) * (Z - A)
        dP = 3 * Z**2 - 2 * (A + 1) * Z + A
        
        dP[dP == 0] = 1e-15
        
        convergentes = (np.abs(P) < tolerancia) & (matriz_iteraciones == max_iter)
        matriz_iteraciones[convergentes] = i
        
        Z = Z - P / dP
        Z[np.isnan(Z) | np.isinf(Z)] = 1e10 

    dist_0 = np.abs(Z - 0)
    dist_1 = np.abs(Z - 1)
    dist_A = np.abs(Z - A)
    
    matriz_destinos[dist_0 < tolerancia] = 1
    matriz_destinos[dist_1 < tolerancia] = 2
    matriz_destinos[dist_A < tolerancia] = 3
    
    colores_base = ['black', '#D81B60', '#1E88E5', '#FFC107']
    colores_rgb = np.array([mcolors.to_rgb(c) for c in colores_base])
    imagen_rgb = np.zeros((resolucion, resolucion, 3))
    
    sombreado = (1.0 - (matriz_iteraciones / max_iter))**2
    
    for j in range(1, 4):
        mascara = (matriz_destinos == j)
        color = colores_rgb[j]
        
        factor_luz = (0.2 + 0.8 * sombreado[mascara])[:, np.newaxis]
        imagen_rgb[mascara] = color * factor_luz
        
    return imagen_rgb, (a_min, a_max, a_im_min, a_im_max)

print("Calculando el espacio de parámetros...")
imagen_rgb, extension = espacio_parametros_newton_granular(resolucion=2000)

plt.figure(figsize=(10, 10), dpi=300)
plt.imshow(imagen_rgb, extent=extension, origin='lower')

plt.xlabel(r"$Re(a)$", fontsize=14, family='serif')
plt.ylabel(r"$Im(a)$", fontsize=14, family='serif')

plt.savefig("Figura4.5.png", bbox_inches='tight', pad_inches=0.05)
print("Imagen con zoom guardada")
plt.show()
