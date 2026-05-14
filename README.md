# TFG-Fractales-Newton
Este repositorio contiene los códigos y herramientas interactivas para el estudio de la dinámica compleja y fractales empleados en mi Trabajo de Fin de Grado de Matemática Computacional.

## 📁 Estructura del Proyecto

El código se organiza en la carpeta `src/`, que contiene los siguientes módulos:

* **`mandelbrot.py`**: Algoritmo para el cálculo del conjunto de Mandelbrot (espacio de parámetros de la familia cuadrática) utilizando tiempo de escape y coloreado suavizado.
* **`espacio_parametros.py`**: Generación de mapas de parámetros para familias de polinomios de tercer grado.
* **`espacio_parametros_zoom.py`**: Herramienta optimizada para el análisis de regiones de alta sensibilidad y detalle fractal.
* **`Espacio_Parametros_General.py`**: Script basado en la librería `SymPy` que permite la entrada simbólica de polinomios arbitrarios para su análisis dinámico.
* **`Familia_Cubica_Valor_a.py`**: Aplicación interactiva que permite variar los parámetros de la familia cúbica y desplazar la cámara sobre el plano complejo en tiempo real.

## ⚙️ Requisitos Técnicos

Para garantizar la reproducibilidad de los resultados, es necesario contar con un entorno de **Python 3.x** y las siguientes librerías científicas:

* **NumPy**: Para el cálculo matricial y operaciones vectorizadas.
* **Matplotlib**: Para el renderizado de gráficos y la interfaz de usuario.
* **SymPy**: Para la manipulación simbólica de funciones complejas.

### Instalación de dependencias:
```bash
pip install numpy matplotlib sympy
