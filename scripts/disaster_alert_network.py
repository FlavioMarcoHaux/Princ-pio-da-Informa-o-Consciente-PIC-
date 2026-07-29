#!/usr/bin/env python3
"""
Rede de sensores para alerta antecipado de desastre — protótipo real

Sem holon, sem telepatia, sem phi_S. Apenas:
  - Deteccao de anomalia estatistica (z-score sobre linha de base movel)
  - Fusao de dois canais reais: fisiologico (HRV, proxy de estresse) e
    ambiental (temperatura)
  - Corroboracao espacial: exige concordancia entre varios sensores antes
    de promover a um alerta de comunidade
"""
import os
import numpy as np
import matplotlib.pyplot as plt

# parametros
N_NODES = 20
T = 4320
DIURNAL_PERIOD = 1440
BASELINE_WINDOW = 60
Z_THRESHOLD = 2.5
CORROBORATION_MIN = 4
CALIBRATION_END = 2880
EVENT_START = 3200
EVENT_RAMP = 80

# simulate nodes
np.random.seed(42)

def simulate_node_data(node_id, seed):
    rng = np.random.RandomState(seed)
    t = np.arange(T)
    temp_baseline = 25 + 3*np.sin(2*np.pi*t/DIURNAL_PERIOD) + rng.randn(T)*0.5
    hrv_baseline = 55 + rng.randn(T)*6
    temp = temp_baseline.copy()
    hrv = hrv_baseline.copy()
    delay = rng.randint(-15,15)
    intensity = rng.uniform(0.7,1.3)
    for i, tt in enumerate(t):
        if tt > EVENT_START + delay:
            progress = min(1.0, (tt - EVENT_START - delay) / EVENT_RAMP)
            temp[i] += intensity * 6.0 * progress
            hrv[i] -= intensity * 20.0 * progress
    return temp, hrv

nodes_temp = []
nodes_hrv = []
for n in range(N_NODES):
    temp, hrv = simulate_node_data(n, seed=100+n)
    nodes_temp.append(temp)
    nodes_hrv.append(hrv)
nodes_temp = np.array(nodes_temp)
nodes_hrv = np.array(nodes_hrv)

# edge detection

def fit_diurnal_model(series, calib_end):
    t_calib = np.arange(calib_end)
    X = np.column_stack([np.ones(calib_end), np.sin(2*np.pi*t_calib/DIURNAL_PERIOD), np.cos(2*np.pi*t_calib/DIURNAL_PERIOD)])
    coef, _, _, _ = np.linalg.lstsq(X, series[:calib_end], rcond=None)
    t_full = np.arange(T)
    X_full = np.column_stack([np.ones(T), np.sin(2*np.pi*t_full/DIURNAL_PERIOD), np.cos(2*np.pi*t_full/DIURNAL_PERIOD)])
    return X_full @ coef

node_alerts = np.zeros((N_NODES, T), dtype=bool)
node_risk = np.zeros((N_NODES, T))

for n in range(N_NODES):
    temp_model = fit_diurnal_model(nodes_temp[n], CALIBRATION_END)
    hrv_model = fit_diurnal_model(nodes_hrv[n], CALIBRATION_END)
    temp_resid = nodes_temp[n] - temp_model
    hrv_resid = nodes_hrv[n] - hrv_model
    temp_resid_sd = temp_resid[:CALIBRATION_END].std() + 1e-6
    hrv_resid_sd = hrv_resid[:CALIBRATION_END].std() + 1e-6
    for t in range(T):
        z_temp = temp_resid[t] / temp_resid_sd
        z_hrv = -hrv_resid[t] / hrv_resid_sd
        risk = max(z_temp, 0) + max(z_hrv, 0)
        node_risk[n, t] = risk
        node_alerts[n, t] = risk > Z_THRESHOLD

n_alerting = node_alerts.sum(axis=0)
community_alert = n_alerting >= CORROBORATION_MIN

# outputs
outdir = 'figures'
os.makedirs(outdir, exist_ok=True)
import matplotlib.pyplot as plt
fig, axes = plt.subplots(4,1,figsize=(13,13), sharex=True)
ax=axes[0]
for n in range(min(6,N_NODES)):
    ax.plot(nodes_temp[n], alpha=0.6)
ax.axvline(EVENT_START, color='red', linestyle='--')
ax.set_ylabel('Temperatura (°C)')
ax.set_title('Sinal ambiental bruto (6 de 20 nos)')
ax.grid(True, alpha=0.3)

ax=axes[1]
for n in range(min(6,N_NODES)):
    ax.plot(nodes_hrv[n], alpha=0.6)
ax.axvline(EVENT_START, color='red', linestyle='--')
ax.set_ylabel('HRV (ms)')
ax.set_title('Sinal fisiologico bruto (RMSSD-like)')
ax.grid(True, alpha=0.3)

ax=axes[2]
ax.plot(n_alerting, color='darkorange')
ax.axhline(CORROBORATION_MIN, color='black', linestyle=':')
ax.axvline(EVENT_START, color='red', linestyle='--')
ax.set_ylabel('Nos alertando')
ax.set_title('Contagem de nos em alerta local')
ax.grid(True, alpha=0.3)

ax=axes[3]
ax.fill_between(range(T), community_alert.astype(int), color='crimson', alpha=0.4)
ax.plot(node_alerts[0].astype(int)*0.5, color='steelblue', alpha=0.7)
ax.axvline(EVENT_START, color='red', linestyle='--')
ax.set_ylabel('Alerta (0/1)')
ax.set_xlabel('Tempo (min)')
ax.set_title('Sensor unico vs. rede com corroboracao')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(outdir,'disaster_alert_network.png'), dpi=150)
print('Saved figures/disaster_alert_network.png')
