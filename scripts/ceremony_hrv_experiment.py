#!/usr/bin/env python3
"""
Protótipo v2: Núcleo + Periféricos, com "modo cerimônia" (REBUS) e
período refratário dirigido por HRV (dado sintético-placeholder).

IMPORTANTE: a série de HRV usada aqui é SINTÉTICA — um placeholder gerado
para ter a forma estatística plausível de uma série real de RMSSD (ruído
suave, faixa 20-80ms). Assim que você tiver dados reais (export do
Oura/Whoop/Apple Health em CSV, ou via conector), troque a função
`load_hrv_series()` para ler o arquivo real. O resto do código não muda.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# ============================================================
# PARÂMETROS FIXOS
# ============================================================
K = 4
labels = ['Visão', 'Audição', 'Interocepção', 'Linguagem interna']
T = 400
kappa = 0.25
precision_ema = 0.05
ignition_threshold = 2.5
broadcast_gain_normal = 0.5
obs_noise = 0.3
refractory_period_default = 15
precision_ceiling_normal = 5.0

# caminhos relativos para dados
possible_rr_paths = [
    'data/raw/fantasia_Y1_RR_intervals.txt',
    'data/raw/fantasia_Y1_RR_intervals-1.txt',
    'fantasia_Y1_RR_intervals.txt',
]

rr_path = None
for p in possible_rr_paths:
    if os.path.exists(p):
        rr_path = p
        break

if rr_path is None:
    raise FileNotFoundError('Arquivo de HRV não encontrado. Coloque fantasia_Y1_RR_intervals.txt em data/raw/ ou na raiz do repositório.')

# ============================================================
# funções auxiliares
# ============================================================

def true_signal(k, t):
    base_freqs = [0.02, 0.035, 0.015, 0.05]
    event_times = [100, 180, 260, 320]
    val = np.sin(2 * np.pi * base_freqs[k] * t)
    if t > event_times[k]:
        val += 1.5
    return val


def load_hrv_series(T, seed=99):
    """
    PLACEHOLDER. Gera uma série de RMSSD sintética (20-80 ms) via passeio
    aleatório suavizado, só para ter a forma estatística de HRV real.
    SUBSTITUA esta função por leitura de CSV real quando disponível, ex:
        df = pd.read_csv('hrv_export.csv')
        return df['rmssd'].values
    """
    rng = np.random.RandomState(seed)
    raw = rng.randn(T).cumsum()
    raw = (raw - raw.min()) / (raw.max() - raw.min())  # normaliza [0,1]
    kernel = np.ones(20) / 20
    smooth = np.convolve(raw, kernel, mode='same')
    smooth = (smooth - smooth.min()) / (smooth.max() - smooth.min())
    return 20 + 60 * smooth


def hrv_to_refractory(hrv_series, min_ref=8, max_ref=30):
    hrv_norm = (hrv_series - hrv_series.min()) / (hrv_series.max() - hrv_series.min() + 1e-9)
    return np.round(max_ref - (max_ref - min_ref) * hrv_norm).astype(int)


def run_simulation(seed=7, ceremony_window=None, ceremony_gain=0.05,
                    ceremony_precision_ceiling=1.5,
                    refractory_series=None, refractory_fixed=refractory_period_default):
    np.random.seed(seed)
    mu = np.zeros(K)
    precision = np.ones(K) * 1.0
    err_ema_sq = np.ones(K) * 1.0
    refractory_until = np.zeros(K, dtype=int)

    hist = {
        'mu': np.zeros((T, K)), 'true': np.zeros((T, K)),
        'salience': np.zeros((T, K)), 'ignition': np.zeros(T, dtype=bool),
        'winner': np.full(T, -1), 'abs_err': np.zeros((T, K)),
    }

    for t in range(T):
        in_ceremony = ceremony_window is not None and ceremony_window[0] <= t <= ceremony_window[1]
        bgain = ceremony_gain if in_ceremony else broadcast_gain_normal
        p_ceiling = ceremony_precision_ceiling if in_ceremony else precision_ceiling_normal
        ref_period = refractory_series[t] if refractory_series is not None else refractory_fixed

        true_vals = np.array([true_signal(k, t) for k in range(K)])
        obs = true_vals + np.random.randn(K) * obs_noise

        err = obs - mu
        salience = precision * err**2
        mu = mu + kappa * precision * err
        err_ema_sq = (1 - precision_ema) * err_ema_sq + precision_ema * err**2
        precision = np.clip(1.0 / (0.1 + err_ema_sq), 0.1, p_ceiling)
        eligible = np.array([salience[k] if t >= refractory_until[k] else -1.0 for k in range(K)])
        winner = int(np.argmax(eligible))
        ignite = eligible[winner] > ignition_threshold
        if ignite:
            refractory_until[winner] = t + ref_period
            for j in range(K):
                if j != winner:
                    mu[j] = mu[j] + bgain * (mu[winner] - mu[j])
        hist['mu'][t] = mu
        hist['true'][t] = true_vals
        hist['salience'][t] = salience
        hist['winner'][t] = winner if ignite else -1
        hist['ignition'][t] = ignite
        hist['abs_err'][t] = np.abs(mu - true_vals)
    return hist


# ============================================================
# Experimentos e plots (mantive a lógica original, apenas caminhos relativos)
# ============================================================

if __name__ == '__main__':
    # carregar hrv (tenta caminhos relativos)
    try:
        rr = np.loadtxt(rr_path)
    except Exception:
        rr = None

    hrv_series = load_hrv_series(T) if rr is None else None
    if rr is not None:
        # calcular RMSSD real se houver arquivo de RR
        from scipy.interpolate import interp1d
        def sliding_rmssd(rr_series, window=60, step=30):
            diffs = np.diff(rr_series) * 1000
            vals = []
            for i in range(0, len(diffs) - window, step):
                w = diffs[i:i+window]
                vals.append(np.sqrt(np.mean(w**2)))
            return np.array(vals)
        rmssd_real = sliding_rmssd(rr)
        x_old = np.linspace(0,1,len(rmssd_real))
        x_new = np.linspace(0,1,T)
        hrv_series = interp1d(x_old, rmssd_real, kind='linear')(x_new)

    refractory_from_hrv = hrv_to_refractory(hrv_series) if hrv_series is not None else None

    hist_fixed = run_simulation(seed=7, refractory_series=None)
    hist_real = run_simulation(seed=7, refractory_series=refractory_from_hrv)

    # plots -> salva em figures/
    outdir = 'figures'
    os.makedirs(outdir, exist_ok=True)
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(3,1,figsize=(13,10))
    ax = axes[0]
    if rr is not None:
        ax.plot(rr[:2000]*1000, color='darkred', linewidth=0.7)
        ax.set_ylabel('RR (ms)')
    else:
        ax.text(0.5, 0.5, 'RR data not available', ha='center')
    ax.grid(True,alpha=0.3)

    ax = axes[1]
    if hrv_series is not None:
        ax.plot(hrv_series, color='crimson')
        ax.set_ylabel('RMSSD (ms)', color='crimson')
    ax2 = ax.twinx()
    if refractory_from_hrv is not None:
        ax2.plot(refractory_from_hrv, color='navy', alpha=0.6)
        ax2.set_ylabel('Refratário (passos)', color='navy')
    ax.grid(True,alpha=0.3)

    ax = axes[2]
    ign_fixed = np.where(hist_fixed['ignition'])[0]
    ign_real = np.where(hist_real['ignition'])[0]
    for t in ign_fixed:
        ax.scatter(t,0,color='green', s=15, alpha=0.6)
    for t in ign_real:
        ax.scatter(t,1,color='crimson', s=15, alpha=0.6)
    ax.set_yticks([0,1]); ax.set_yticklabels(['Refratário fixo','Refratário via HRV'])
    ax.set_xlabel('Tempo (passos)')
    ax.grid(True,alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(outdir,'ceremony_hrv_experiment.png'), dpi=150)
    print('Saved figures/ceremony_hrv_experiment.png')
