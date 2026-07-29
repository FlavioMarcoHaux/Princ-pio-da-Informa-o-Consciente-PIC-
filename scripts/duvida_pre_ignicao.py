#!/usr/bin/env python3
"""
"Ser ou não ser?" formalizado: DURAÇÃO DA DÚVIDA PRÉ-IGNIÇÃO

Extensão do modelo de inferência ativa + Global Workspace (Módulo 2, PIC/SFT).
"""
import os
import numpy as np
from scipy.interpolate import interp1d
from scipy import stats

K = 4
T = 400
kappa = 0.25
precision_ema = 0.05
ignition_threshold = 2.5
broadcast_gain_normal = 0.5
obs_noise = 0.3
precision_ceiling_normal = 5.0
N_SEEDS = 30
CONFIDENCE_THRESHOLD = 0.7 * precision_ceiling_normal


def true_signal(k, t):
    base_freqs = [0.02, 0.035, 0.015, 0.05]
    event_times = [100, 180, 260, 320]
    val = np.sin(2 * np.pi * base_freqs[k] * t)
    if t > event_times[k]:
        val += 1.5
    return val


def sliding_rmssd(rr_series, window=60, step=30):
    diffs = np.diff(rr_series) * 1000
    vals = []
    for i in range(0, len(diffs) - window, step):
        w = diffs[i:i + window]
        vals.append(np.sqrt(np.mean(w ** 2)))
    return np.array(vals)


def hrv_to_refractory(hrv_series, min_ref=8, max_ref=30):
    hrv_norm = (hrv_series - hrv_series.min()) / (hrv_series.max() - hrv_series.min() + 1e-9)
    return np.round(max_ref - (max_ref - min_ref) * hrv_norm).astype(int)


def load_subject(path):
    rr = np.loadtxt(path)
    rmssd = sliding_rmssd(rr)
    x_old = np.linspace(0, 1, len(rmssd))
    x_new = np.linspace(0, 1, T)
    rmssd_interp = interp1d(x_old, rmssd, kind='linear')(x_new)
    return rr, rmssd, rmssd_interp


def run_simulation_with_doubt(seed, refractory_series=None, refractory_fixed=15):
    np.random.seed(seed)
    mu = np.zeros(K)
    precision = np.ones(K) * 1.0
    err_ema_sq = np.ones(K) * 1.0
    refractory_until = np.zeros(K, dtype=int)

    doubt_start = np.full(K, -1, dtype=int)
    doubt_durations = []
    ignitions = 0
    abs_err_sum = 0.0

    for t in range(T):
        ref_period = refractory_series[t] if refractory_series is not None else refractory_fixed
        true_vals = np.array([true_signal(k, t) for k in range(K)])
        obs = true_vals + np.random.randn(K) * obs_noise
        err = obs - mu
        salience = precision * err ** 2
        mu = mu + kappa * precision * err
        err_ema_sq = (1 - precision_ema) * err_ema_sq + precision_ema * err ** 2
        precision = np.clip(1.0 / (0.1 + err_ema_sq), 0.1, precision_ceiling_normal)

        for k in range(K):
            if precision[k] < CONFIDENCE_THRESHOLD and doubt_start[k] == -1:
                doubt_start[k] = t
            elif precision[k] >= CONFIDENCE_THRESHOLD:
                doubt_start[k] = -1

        eligible = np.array([salience[k] if t >= refractory_until[k] else -1.0 for k in range(K)])
        winner = int(np.argmax(eligible))
        ignite = eligible[winner] > ignition_threshold

        if ignite:
            ignitions += 1
            if doubt_start[winner] != -1:
                duration = t - doubt_start[winner]
                doubt_durations.append(duration)
            refractory_until[winner] = t + ref_period
            doubt_start[winner] = -1
            for j in range(K):
                if j != winner:
                    mu[j] = mu[j] + broadcast_gain_normal * (mu[winner] - mu[j])

        abs_err_sum += np.mean(np.abs(mu - true_vals))

    mean_doubt = np.mean(doubt_durations) if doubt_durations else 0.0
    return ignitions, abs_err_sum / T, mean_doubt


if __name__ == '__main__':
    # try to load subjects from data/raw/ fallback to root
    base_paths = ['data/raw/', 'data/']
    subjects_young = ['fantasia_Y1_RR_intervals.txt', 'fantasia_Y2_RR_intervals.txt', 'fantasia_Y3_RR_intervals.txt']
    subjects_old = ['fantasia_O1_RR_intervals.txt', 'fantasia_O2_RR_intervals.txt']

    print('='*70)
    print('DURAÇÃO DA DÚVIDA PRÉ-IGNIÇÃO: JOVEM vs. IDOSO (HRV real)')
    print('='*70)

    young_doubt, young_ign, young_err = [], [], []
    for f in subjects_young:
        loaded = False
        for bp in base_paths:
            path = bp + f
            if os.path.exists(path):
                _, _, hrv_interp = load_subject(path)
                loaded = True
                break
        if not loaded:
            print(f'Warning: subject {f} not found in data/raw/ or data/. Skipping')
            continue
        refr = hrv_to_refractory(hrv_interp)
        ign, err, doubt = run_simulation_with_doubt(refractory_series=refr)
        young_doubt.append(doubt)
        print(f"{f}: duração média da dúvida = {doubt.mean():.2f} passos")

    old_doubt = []
    for f in subjects_old:
        loaded = False
        for bp in base_paths:
            path = bp + f
            if os.path.exists(path):
                _, _, hrv_interp = load_subject(path)
                loaded = True
                break
        if not loaded:
            print(f'Warning: subject {f} not found. Skipping')
            continue
        refr = hrv_to_refractory(hrv_interp)
        ign, err, doubt = run_simulation_with_doubt(refractory_series=refr)
        old_doubt.append(doubt)
        print(f"{f}: duração média da dúvida = {doubt.mean():.2f} passos")

    ign_fixed, err_fixed, doubt_fixed = run_simulation_with_doubt(refractory_series=None)

    print('\n' + '='*70)
    print('RESUMO POR GRUPO (média entre sujeitos, 30 sementes)')
    print('='*70)
    print(f"REFRATÁRIO FIXO:    dúvida média = {doubt_fixed.mean():.2f} ± {doubt_fixed.std():.2f} passos")

    # save a small report
    outdir = 'figures'
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir,'duvida_report.txt'),'w') as fh:
        fh.write('Dúvida fixo: %.3f\n' % doubt_fixed.mean())
    print('Saved figures/duvida_report.txt')
