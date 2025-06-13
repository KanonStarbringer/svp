import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

# Parâmetros fixos
ds = 10  # Passo em metros
Dmax = 1000   # Profundidade máxima (m)
Rmaxkm = 40   # Alcance máximo (km)
Rmax = Rmaxkm * 1000  # Alcance máximo (m)

# Frequência de corte
def frequencia_corte(duto):
    return 1500 / (0.008 * duto ** (3/2))

# Perfil interpolado de velocidade
def velocity_profile(z, depths, speeds):
    return np.interp(z, depths, speeds)

# Sistema de equações diferenciais para traçado de raios
def solver(Y, s, depths, speeds):
    r, z, sr, sz = Y
    c = velocity_profile(z, depths, speeds)
    cc = c * c
    drds = c * sr
    dzds = c * sz
    dcdz = (velocity_profile(z + ds, depths, speeds) - velocity_profile(z - ds, depths, speeds)) / (2 * ds)
    dsrds = 0
    dszds = -dcdz / cc
    return [drds, dzds, dsrds, dszds]

# Parâmetros dos raios
nrays = 30
thetas = np.linspace(-5, 5, nrays)
max_reflections = 50

def plot_ray_paths(depths, speeds, source_pos):
    # Eixo s (distância radial)
    s = np.arange(source_pos[0], Rmax + ds, ds)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, Rmaxkm)
    ax.set_ylim(Dmax, 0)
    ax.set_xlabel('Distância (km)', fontsize=14)
    ax.set_ylabel('Profundidade (m)', fontsize=14)
    ax.grid(True)

    fc = frequencia_corte(depths[1])

    for i in range(nrays):
        sr0 = np.cos(-thetas[i] * np.pi / 180) / speeds[0]
        sz0 = np.sin(-thetas[i] * np.pi / 180) / speeds[0]
        y0 = [source_pos[0], source_pos[1], sr0, sz0]
        y = integrate.odeint(solver, y0, s, args=(depths, speeds))
        r = y[:, 0]
        z = y[:, 1]
        rkm = r / 1000.0
        num_reflections = 0

        while num_reflections < max_reflections:
            reflection_occurred = False
            for j in range(len(z)):
                if z[j] < 0:
                    reflection_occurred = True
                    dz = -z[j]
                    dr = r[j] - r[j - 1]
                    r_new = r[j] + 2 * dr
                    z_new = dz
                    y0 = [r_new, z_new, y[j, 2], -y[j, 3]]
                    y_reflect = integrate.odeint(solver, y0, s[j:], args=(depths, speeds))
                    r_reflect = y_reflect[:, 0]
                    z_reflect = y_reflect[:, 1]
                    rkm = np.concatenate([rkm[:j], r_reflect / 1000.0])
                    z = np.concatenate([z[:j], z_reflect])
                    num_reflections += 1
                    break
            if not reflection_occurred:
                break

        ax.plot(rkm, z, 'k', linewidth=0.5)

    ax.text(Rmaxkm - 0.5, depths[1], f'Freq. de Corte - Camada de Mistura {int(depths[1])} m: {fc:.2f} Hz',
            color='blue', ha='right', va='top', fontsize=10)
    
    return fig

def plot_velocity_profile(depths, speeds):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(speeds, depths, 'o-')
    ax.invert_yaxis()
    ax.set_xlabel('Velocidade do som (m/s)', fontsize=14)
    ax.set_ylabel('Profundidade (m)', fontsize=14)
    
    # Calcular limites do eixo x com margem de 5%
    min_speed = min(speeds)
    max_speed = max(speeds)
    speed_range = max_speed - min_speed
    margin = speed_range * 0.05
    
    ax.set_xlim(min_speed - margin, max_speed + margin)
    ax.set_ylim(Dmax, 0)
    ax.grid(True)
    return fig 
