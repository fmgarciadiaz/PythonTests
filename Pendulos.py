import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# Parámetros del sistema (modificables)
N = 6                      # Número total de péndulos
L1 = 0.8                   # Longitud grupo 1 (m)
L2 = 1.2                   # Longitud grupo 2 (m)
m = 0.1                    # Masa de los péndulos (kg)
k = 8.0                    # Constante de acoplamiento (N/m)
g = 9.81                   # Gravedad (m/s²)
F0 = 0.8                   # Amplitud de fuerza externa (N)
omega_f = 5.0              # Frecuencia de fuerza externa (rad/s)
gamma = 0.1                # Coeficiente de amortiguamiento (solo para péndulos 2 a N)
t_max = 50.0               # Tiempo máximo de simulación (s)
d_separation = 1.5         # Separación horizontal entre péndulos (m)

# Configuración de grupos (primera mitad grupo 1, segunda mitad grupo 2)
half_N = N // 2
lengths = np.array([L1] * half_N + [L2] * (N - half_N))
omega0_sq = g / lengths   # g/L para cada péndulo
alpha = k / (m * lengths) # Coeficiente de acoplamiento ajustado

# Condiciones iniciales (todos en reposo)
theta0 = np.zeros(N)       # Ángulos iniciales (rad)
omega0 = np.zeros(N)       # Velocidades angulares iniciales (rad/s)
y0 = np.concatenate([theta0, omega0])

# Función para las ecuaciones de movimiento
def equations(t, y):
    theta = y[:N]
    omega = y[N:]
    dtheta_dt = omega
    domega_dt = np.zeros(N)
    
    # Primer péndulo (forzado externamente SIN amortiguamiento)
    domega_dt[0] = -omega0_sq[0] * theta[0] + alpha[0] * (theta[1] - theta[0]) + (F0/(m*lengths[0])) * np.cos(omega_f*t)
    
    # Péndulos intermedios (con amortiguamiento)
    for i in range(1, N-1):
        domega_dt[i] = -omega0_sq[i] * theta[i] - gamma * omega[i] + alpha[i] * (theta[i-1] - 2*theta[i] + theta[i+1])
    
    # Último péndulo (con amortiguamiento)
    if N > 1:
        domega_dt[N-1] = -omega0_sq[N-1] * theta[N-1] - gamma * omega[N-1] + alpha[N-1] * (theta[N-2] - theta[N-1])
    
    return np.concatenate([dtheta_dt, domega_dt])

# Resolver las ecuaciones diferenciales
sol = solve_ivp(equations, [0, t_max], y0, t_eval=np.linspace(0, t_max, 2000), rtol=1e-6)
theta_sol = sol.y[:N]
omega_sol = sol.y[N:]
t_sol = sol.t

# Configuración de la animación
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [2, 1]})

# Configurar subplot para animación
ax1.set_xlim(-1, N * d_separation + 1)
ax1.set_ylim(-max(L1, L2)*1.5, 0.5)
ax1.set_aspect('equal')
ax1.grid(True)
ax1.set_title(f'{N} Péndulos Acoplados con Fuerza Externa ($\omega_f$ = {omega_f} rad/s)')
ax1.set_xlabel('Posición X (m)')
ax1.set_ylabel('Posición Y (m)')

# Configurar subplot para gráfico de energía
ax2.set_xlim(0, t_max)
ax2.grid(True)
ax2.set_title('Energía del Sistema')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Energía Total (J)')

# Crear elementos de la animación
pendulums = []
masses = []
springs = []
energy_line, = ax2.plot([], [], 'b-', lw=2, label='Energía Total')
energy_text = ax2.text(0.02, 0.95, '', transform=ax2.transAxes)
ax2.legend(loc='upper right')

# Posiciones de los puntos de anclaje
anchors_x = np.arange(0, N * d_separation, d_separation)

for i in range(N):
    # Líneas de los péndulos con colores según grupo
    color = 'blue' if i < half_N else 'green'
    pendulum_line, = ax1.plot([], [], '-', lw=2, color=color)
    pendulums.append(pendulum_line)
    
    # Masas
    mass_circle = Circle((0, 0), 0.05, fc=color, zorder=3)
    ax1.add_patch(mass_circle)
    masses.append(mass_circle)
    
    # Resortes (entre masas)
    if i < N-1:
        spring_line, = ax1.plot([], [], 'r--', alpha=0.7)
        springs.append(spring_line)

# Texto para mostrar el tiempo
time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)

# Función para calcular energía
def calculate_energy(theta, omega):
    # Energía cinética
    kinetic = 0.5 * m * (lengths**2) * (omega**2)
    
    # Energía potencial gravitatoria
    potential = 0.5 * m * g * lengths * (theta**2)
    
    # Energía de acoplamiento (resortes)
    spring = 0
    for i in range(N-1):
        spring += 0.5 * k * (d_separation * (theta[i+1] - theta[i]))**2
    
    return np.sum(kinetic) + np.sum(potential) + spring

# Calcular energía para todos los tiempos
energy = np.array([calculate_energy(theta_sol[:, i], omega_sol[:, i]) for i in range(len(t_sol))])
# Ajustar el límite del eje y de energía
ax2.set_ylim(0, max(energy) * 1.1)

# Función de inicialización
def init():
    for line in pendulums:
        line.set_data([], [])
    for circle in masses:
        circle.center = (0, 0)
    for line in springs:
        line.set_data([], [])
    time_text.set_text('')
    energy_line.set_data([], [])
    energy_text.set_text('')
    return pendulums + masses + springs + [time_text, energy_line, energy_text]

# Función de animación
def animate(frame):
    t = t_sol[frame]
    theta = theta_sol[:, frame]
    omega = omega_sol[:, frame]
    
    for i in range(N):
        # Calcular posición de la masa
        x = anchors_x[i] + lengths[i] * np.sin(theta[i])
        y = -lengths[i] * np.cos(theta[i])
        
        # Actualizar péndulo
        pendulums[i].set_data([anchors_x[i], x], [0, y])
        masses[i].center = (x, y)
    
    # Actualizar resortes
    for i in range(len(springs)):
        x1 = anchors_x[i] + lengths[i] * np.sin(theta[i])
        y1 = -lengths[i] * np.cos(theta[i])
        x2 = anchors_x[i+1] + lengths[i+1] * np.sin(theta[i+1])
        y2 = -lengths[i+1] * np.cos(theta[i+1])
        springs[i].set_data([x1, x2], [y1, y2])
    
    # Actualizar gráfico de energía
    energy_line.set_data(t_sol[:frame+1], energy[:frame+1])
    energy_text.set_text(f'Energía: {energy[frame]:.4f} J')
    time_text.set_text(f'Tiempo: {t:.2f} s')
    
    return pendulums + masses + springs + [time_text, energy_line, energy_text]

# Crear la animación
ani = animation.FuncAnimation(fig, animate, frames=len(t_sol),
                              init_func=init, blit=True, interval=20)

plt.tight_layout()
plt.show()