import numpy as np
import matplotlib.pyplot as plt

# Definir el campo vectorial
def vector_field(X, Y):
    U = Y  # dx/dt = y
    V = -X # dy/dt = -x
    return U, V

# Crear una malla de puntos
x = np.linspace(-3, 3, 20)
y = np.linspace(-3, 3, 20)
X, Y = np.meshgrid(x, y)
U, V = vector_field(X, Y)

# Crear la figura
fig, ax = plt.subplots(figsize=(6, 6))

# Graficar líneas de flujo (campo de direcciones)
stream = plt.streamplot(X, Y, U, V, color='gray', density=1, arrowstyle='->')

# Extraer puntos desde streamplot para usar en quiver
x_lines = []
y_lines = []
u_lines = []
v_lines = []

for line in stream.lines.get_segments():
    x1, y1 = line[0]  # Punto inicial del segmento
    x2, y2 = line[1]  # Punto final del segmento
    x_lines.append(x1)
    y_lines.append(y1)
    u_lines.append(x2 - x1)  # Dirección en x
    v_lines.append(y2 - y1)  # Dirección en y

# Graficar las flechas alineadas con las líneas de flujo
plt.quiver(x_lines, y_lines, u_lines, v_lines, color='red', angles='xy', scale_units='xy', scale=1.5, width=0.007)

# Configuración de la gráfica
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Líneas de flujo con flechas alineadas (quiver)")
plt.grid(alpha=0.3)

# Mostrar la gráfica
plt.show()