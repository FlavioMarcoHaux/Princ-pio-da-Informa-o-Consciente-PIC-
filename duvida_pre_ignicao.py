#!/usr/bin/env python3
"""
"Ser ou não ser?" formalizado: DURAÇÃO DA DÚVIDA PRÉ-IGNIÇÃO
================================================================
Extensão do modelo de inferência ativa + Global Workspace (Módulo 2, PIC/SFT).

Ideia: a "dúvida" (Ser ou não Ser) não é um axioma novo — é um ESTADO
TRANSITÓRIO já presente no modelo: o período em que a saliência de um
canal está subindo mas ainda não cruzou o limiar de ignição (theta).

Definimos:
  - "Dúvida" = intervalo de tempo em que 0 < salience(k,t) < ignition_threshold
    E a precisão do canal está abaixo de um valor de "confiança" (ex: 70% do teto)
  - "Esclarecimento" = o passo t em que ignite = True (a crença "vence")
  - Duração da dúvida = número de passos entre o início da subida de saliência
    e o momento da ignição

Isso é MEDÍVEL a partir do seu próprio código existente, sem novo termo na
Lagrangiana e sem novo axioma. Comparamos com dados reais de HRV (jovem vs idoso).
"""
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

# Limiar de "confiança" — abaixo disso, o canal está em "dúvida" mesmo
# que a saliência esteja subindo. 70% do teto de precisão.
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
    """
    Roda a simulação original E registra, para cada ignição, quantos passos
    o canal vencedor ficou em estado de "dúvida" antes de ignitar
    (precisão abaixo do limiar de confiança, mas já acumulando saliência).
    """
    np.random.seed(seed)
    mu = np.zeros(K)
    precision = np.ones(K) * 1.0
    err_ema_sq = np.ones(K) * 1.0
    refractory_until = np.zeros(K, dtype=int)

    # Rastreia desde quando cada canal está "em dúvida" (baixa confiança)
    doubt_start = np.full(K, -1, dtype=int)
    doubt_durations = []  # duração da dúvida a cada ignição registrada
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

        # Marca início da "dúvida": precisão abaixo do limiar de confiança
        for k in range(K):
            if precision[k] < CONFIDENCE_THRESHOLD and doubt_start[k] == -1:
                doubt_start[k] = t
            elif precision[k] >= CONFIDENCE_THRESHOLD:
                doubt_start[k] = -1  # "confiança" restaurada, reseta

        eligible = np.array([salience[k] if t >= refractory_until[k] else -1.0 for k in range(K)])
        winner = int(np.argmax(eligible))
        ignite = eligible[winner] > ignition_threshold

        if ignite:
            ignitions += 1
            # Duração da dúvida do canal vencedor até este momento de "esclarecimento"
            if doubt_start[winner] != -1:
                duration = t - doubt_start[winner]
                doubt_durations.append(duration)
            refractory_until[winner] = t + ref_period
            doubt_start[winner] = -1  # esclarecido, reseta a dúvida
            for j in range(K):
                if j != winner:
                    mu[j] = mu[j] + broadcast_gain_normal * (mu[winner] - mu[j])

        abs_err_sum += np.mean(np.abs(mu - true_vals))

    mean_doubt = np.mean(doubt_durations) if doubt_durations else 0.0
    return ignitions, abs_err_sum / T, mean_doubt


def run_multi_seed_doubt(refractory_series=None, refractory_fixed=15, n_seeds=N_SEEDS):
    ign_list, err_list, doubt_list = [], [], []
    for s in range(n_seeds):
        ign, err, doubt = run_simulation_with_doubt(
            seed=1000 + s,
            refractory_series=refractory_series,
            refractory_fixed=refractory_fixed
        )
        ign_list.append(ign)
        err_list.append(err)
        doubt_list.append(doubt)
    return np.array(ign_list), np.array(err_list), np.array(doubt_list)


# ============================================================
# CARREGAR DADOS REAIS
# ============================================================
base = '/mnt/user-data/uploads/'
subjects_young = ['fantasia_Y1_RR_intervals.txt', 'fantasia_Y2_RR_intervals.txt', 'fantasia_Y3_RR_intervals.txt']
subjects_old = ['fantasia_O1_RR_intervals.txt', 'fantasia_O2_RR_intervals.txt']

print("=" * 70)
print("DURAÇÃO DA DÚVIDA PRÉ-IGNIÇÃO: JOVEM vs. IDOSO (HRV real)")
print("=" * 70)
print(f"Limiar de confiança usado: precisão < {CONFIDENCE_THRESHOLD:.2f} (70% do teto)\n")

young_doubt, young_ign, young_err = [], [], []
for f in subjects_young:
    _, _, hrv_interp = load_subject(base + f)
    refr = hrv_to_refractory(hrv_interp)
    ign, err, doubt = run_multi_seed_doubt(refractory_series=refr)
    young_doubt.append(doubt)
    young_ign.append(ign)
    young_err.append(err)
    print(f"{f}: duração média da dúvida = {doubt.mean():.2f} passos "
          f"(desvio={doubt.std():.2f})")

old_doubt, old_ign, old_err = [], [], []
for f in subjects_old:
    _, _, hrv_interp = load_subject(base + f)
    refr = hrv_to_refractory(hrv_interp)
    ign, err, doubt = run_multi_seed_doubt(refractory_series=refr)
    old_doubt.append(doubt)
    old_ign.append(ign)
    old_err.append(err)
    print(f"{f}: duração média da dúvida = {doubt.mean():.2f} passos "
          f"(desvio={doubt.std():.2f})")

ign_fixed, err_fixed, doubt_fixed = run_multi_seed_doubt(refractory_series=None)

# médias por grupo (pareadas por semente)
doubt_young_avg = np.mean(young_doubt, axis=0)
doubt_old_avg = np.mean(old_doubt, axis=0)

print("\n" + "=" * 70)
print("RESUMO POR GRUPO (média entre sujeitos, 30 sementes)")
print("=" * 70)
print(f"REFRATÁRIO FIXO:    dúvida média = {doubt_fixed.mean():.2f} ± {doubt_fixed.std():.2f} passos")
print(f"GRUPO JOVEM (n=3):  dúvida média = {doubt_young_avg.mean():.2f} ± {doubt_young_avg.std():.2f} passos")
print(f"GRUPO IDOSO (n=2):  dúvida média = {doubt_old_avg.mean():.2f} ± {doubt_old_avg.std():.2f} passos")

print("\n" + "=" * 70)
print("TESTE ESTATÍSTICO (pareado por semente)")
print("=" * 70)
t_stat, p_val = stats.ttest_rel(doubt_young_avg, doubt_old_avg)
print(f"Dúvida: jovem vs idoso -> t={t_stat:.3f}, p={p_val:.4f}")

t_stat2, p_val2 = stats.ttest_rel(doubt_fixed, doubt_young_avg)
print(f"Dúvida: fixo vs jovem  -> t={t_stat2:.3f}, p={p_val2:.4f}")

t_stat3, p_val3 = stats.ttest_rel(doubt_fixed, doubt_old_avg)
print(f"Dúvida: fixo vs idoso  -> t={t_stat3:.3f}, p={p_val3:.4f}")

print("\n" + "=" * 70)
print("INTERPRETAÇÃO")
print("=" * 70)
print("""
Se a duração da dúvida (tempo em baixa confiança antes da ignição) for
sistematicamente diferente entre grupos jovem/idoso, isso sugere que o
tônus vagal (HRV) modula não só QUANTAS ignições ocorrem (já mostrado
no Módulo 2), mas também QUANTO TEMPO o sistema permanece em estado de
incerteza antes de "resolver" a dúvida em uma crença (Eu Sou X, não Y).

Isso é uma métrica adicional, testável e falseável, para operacionalizar
"Ser ou não Ser" dentro do formalismo já existente — sem introduzir novo
axioma, sem conflitar com o Axioma Central do PIC (Módulo 1), e sem
depender do Campo S (que é a parte não-falseável do framework).

LIMITAÇÃO IMPORTANTE: com n=3 (jovem) e n=2 (idoso), qualquer diferença
de grupo aqui está sujeita ao mesmo problema de fragilidade estatística
já identificado nas comparações anteriores do Módulo 2. O valor real
deste script está na METODOLOGIA (como medir "dúvida" operacionalmente),
não ainda na conclusão sobre jovens vs idosos.
""")
