import numpy as np
import matplotlib.pyplot as plt

# Definir el campo vectorial
def vector_field(X, Y):
# hiperbole
#    U = Y  # dx/dt = y
#    V = -X # dy/dt = -x
# circular
#    U = 1/2 * Y  # dx/dt = y
#    V = 1/2 * X # dy/dt = -x
# un pendulo
#    U = Y  # dx/dt = y
#    V = -np.sin(X) # dy/dt = -x
# un pendulo amortiguado
    U = Y  # dx/dt = y
    V = -np.sin(X) - 0.5*Y# dy/dt = -x
    return U, V

# Crear una malla de puntos
x = np.linspace(-6, 6, 40)
y = np.linspace(-6, 6, 40)
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

scale_factor = 2  # Factor para alargar las flechas

for line in stream.lines.get_segments():
    x1, y1 = line[0]  # Punto inicial del segmento
    x2, y2 = line[1]  # Punto final del segmento
    dx = x2 - x1
    dy = y2 - y1
    norm = np.sqrt(dx**2 + dy**2)  # Normalizar la dirección

    if norm > 0:
        dx /= norm
        dy /= norm
        dx *= scale_factor  # Aumentar la longitud de las flechas
        dy *= scale_factor

    x_lines.append(x1)
    y_lines.append(y1)
    u_lines.append(dx)
    v_lines.append(dy)

# Graficar las flechas tangentes a las líneas de flujo
#plt.quiver(x_lines[::2], y_lines[::2], u_lines[::2], 
#           v_lines[::2], color='blue', alpha = 0.5, angles='xy', scale_units='xy', scale=2, width=0.002)

# Configuración de la gráfica
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlim(-6, 6)
plt.ylim(-6, 6)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Líneas de flujo con flechas tangentes y más largas")
plt.grid(alpha=0.3)

# Mostrar la gráfica
plt.show()
plt.savefig("grafico.png")