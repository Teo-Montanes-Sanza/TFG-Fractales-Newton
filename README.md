# TFG-Fractales-Newton
Este repositorio contiene los códigos y herramientas interactivas para el estudio de la dinámica compleja y fractales empleados en mi Trabajo de Fin de Grado de Matemática Computacional.

## 📁 Estructura del Proyecto

El código se organiza en la carpeta `src/`, que contiene los siguientes algoritmos:

* **`Plano_Dinamico_General.py`**: Aplicación interactiva que permite la entrada de polinomios para la generación de su plano dinámico. (Figura 4.1 y Figura 4.2)
* **`mandelbrot.py`**: Generación del espacio de parámetros para la familia cuadrática pc(z) = z2 + c. (Figura 4.3)
* **`espacio_parametros.py`**: Generación del espacio de parámetros para la familia cúbica genérica Pa(z) = z(z −1)(z −a). (Figura 4.4)
* **`espacio_parametros_zoom.py`**: Generación del espacio de parámetros para la familia cúbica genérica Pa(z) = z(z −1)(z −a) con zoom en una zona de no convergencia. (Figura 4.5)
* **`Familia_Cubica_Valor_a.py`**: Aplicación interactiva que permite la entrada de valores del parámetro de la familia cúbica genérica para la generación de su plano dinámico. (Figura 4.6 y Figura 4.7)

## ⚙️ Requisitos Técnicos

Para garantizar la reproducibilidad de los resultados, es necesario contar con un entorno de **Python 3.x** y las siguientes librerías:

* **NumPy**: Para el cálculo matricial y operaciones vectorizadas.
* **Matplotlib**: Para el renderizado de gráficos y la interfaz de usuario.
* **SymPy**: Para la manipulación simbólica de funciones complejas.

### Instalación de dependencias:
```bash
pip install numpy matplotlib sympy
