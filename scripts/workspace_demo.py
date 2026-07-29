#!/usr/bin/env python3
"""
Protótipo: Núcleo (Global Workspace) + Periféricos (módulos ativo-inferenciais)
"""
import os
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(7)
K = 4
labels = ['Visão', 'Audição', 'Interocepção', 'Linguagem interna']
T = 400
kappa = 0.25
precision_ema = 0.05
ignition_threshold = 2.5
broadcast_gain = 0.5
obs_noise = 0.3
refractory_period = 15


def true_signal(k, t):
    base_freqs = [0.02, 0.035, 0.015, 0.05]
    event_times = [100, 180, 260, 320]
    val = np.sin(2 * np.pi * base_freqs[k] * t)
    if t > event_times[k]:
        val += 1.5
    return val

mu = np.zeros(K)
precision = np.ones(K) * 1.0
err_ema_sq = np.ones(K) * 1.0
history = {
    'mu': np.zeros((T, K)),
    'true': np.zeros((T, K)),
    'salience': np.zeros((T, K)),
    'precision': np.zeros((T, K)),
    'winner': np.full(T, -1),
    'ignition': np.zeros(T, dtype=bool),
}

refractory_until = np.zeros(K, dtype=int)
for t in range(T):
    true_vals = np.array([true_signal(k, t) for k in range(K)])
    obs = true_vals + np.random.randn(K) * obs_noise
    err = obs - mu
    salience = precision * err**2
    mu = mu + kappa * precision * err
    err_ema_sq = (1 - precision_ema) * err_ema_sq + precision_ema * err**2
    precision = 1.0 / (0.1 + err_ema_sq)
    precision = np.clip(precision, 0.1, 5.0)
    eligible = np.array([salience[k] if t >= refractory_until[k] else -1.0 for k in range(K)])
    winner = int(np.argmax(eligible))
    ignite = eligible[winner] > ignition_threshold
    if ignite:
        refractory_until[winner] = t + refractory_period
        for j in range(K):
            if j != winner:
                mu[j] = mu[j] + broadcast_gain * (mu[winner] - mu[j])
    history['mu'][t] = mu
    history['true'][t] = true_vals
    history['salience'][t] = salience
    history['precision'][t] = precision
    history['winner'][t] = winner if ignite else -1
    history['ignition'][t] = ignite

# analysis and save plot
outdir = 'figures'
os.makedirs(outdir, exist_ok=True)
fig, axes = plt.subplots(3,1,figsize=(13,11), sharex=True)
colors = ['tab:blue','tab:orange','tab:green','tab:red']
ax=axes[0]
for k in range(K):
    ax.plot(history['true'][:,k], color=colors[k], alpha=0.4, linewidth=1, label=f'{labels[k]} (real)')
    ax.plot(history['mu'][:,k], color=colors[k], linewidth=1.8, linestyle='--', label=f'{labels[k]} (crença)')
ax.set_ylabel('Valor do sinal')
ax.set_title('Sinal real vs crença')
ax.legend(fontsize=7, ncol=4, loc='upper left')
ax.grid(True, alpha=0.3)

ax=axes[1]
for k in range(K):
    ax.plot(history['salience'][:,k], color=colors[k], linewidth=1.2, label=labels[k])
ax.axhline(y=ignition_threshold, color='black', linestyle=':')
ax.set_ylabel('Saliência')
ax.set_title('Competição por saliência')
ax.legend(fontsize=7, ncol=5, loc='upper left')
ax.grid(True, alpha=0.3)

ax=axes[2]
ignition_steps = np.where(history['ignition'])[0]
for t in ignition_steps:
    k = int(history['winner'][t])
    ax.scatter(t, k, color=colors[k], s=25)
ax.set_yticks(range(K))
ax.set_yticklabels(labels)
ax.set_xlabel('Tempo (passos)')
ax.set_ylabel('Módulo transmitido')
ax.set_title('Eventos de ignição/broadcast')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(outdir,'workspace_demo.png'), dpi=150)
print('Saved figures/workspace_demo.png')
