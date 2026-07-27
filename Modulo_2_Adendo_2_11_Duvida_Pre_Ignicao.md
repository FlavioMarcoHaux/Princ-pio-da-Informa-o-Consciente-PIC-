MÓDULO 2 — ADENDO 2.11: DÚVIDA PRÉ-IGNIÇÃO ("SER OU NÃO SER") COMO ESTADO TRANSITÓRIO DE BAIXA PRECISÃO
Versão: 2026-07-07
Autores: Flávio Marco Rego da Silva & Pesquisador Colaborativo
Laboratório: LINC – Laboratório de Pesquisa Interdisciplinar da Consciência
Status: Extensão empírica do Módulo 2 — Hipótese H59 (proposta)

---

2.11.0. Motivação

As Seções 2.3–2.7 já estabelecem que o modelo de inferência ativa + Global
Workspace produz ignições — momentos em que a crença (μ) de um canal
supera um limiar de saliência e é transmitida (broadcast) para os demais
canais. O que não havia sido formalizado até agora é o *período que
antecede* a ignição: o intervalo em que o sistema já está acumulando
evidência a favor de um estado, mas ainda não a resolveu.

Este adendo propõe que a experiência fenomenológica comumente descrita
como dúvida existencial — "Ser ou não Ser?" — corresponde, no formalismo
já existente do PIC/SFT, a um **estado transitório de baixa precisão
anterior à ignição**, e não a um axioma novo ou a uma propriedade
fundamental separada de Φ, φ_S ou O_info.

Esta escolha é deliberada: manter a dúvida como estado transitório evita
introduzir um termo adicional na Lagrangiana unificada (Seção 1.3) que
competiria com o Axioma Central do PIC (Seção 1.1), e evita repetir o
padrão já identificado em revisões anteriores — o de tratar toda
experiência subjetiva nova como merecedora de uma constante de
acoplamento própria.

---

2.11.1. Definição Operacional

Seja precision_ceiling o teto de precisão do modelo (Seção 2.3.2).
Definimos um limiar de confiança:

    θ_confiança = 0.7 × precision_ceiling

Um canal k está em estado de dúvida no instante t se:

    precision_k(t) < θ_confiança

O início da dúvida, doubt_start(k), é o primeiro instante em que essa
condição passa a valer (reiniciado sempre que a confiança é restaurada
antes de uma ignição).

Quando o canal k ignita no instante t (ou seja, salience_k(t) supera
θ_ignition, conforme Seção 2.3.2), definimos a **duração da dúvida**:

    Dúvida(k) = t_ignição − doubt_start(k)

Interpretação: Dúvida(k) mede quantos passos de tempo o sistema
permaneceu em incerteza (baixa confiança) antes de "resolver" essa
incerteza em uma crença transmitida — o momento operacional do
"Eu Sou X, não Y".

Esta métrica não introduz novos parâmetros na Lagrangiana; é calculada
inteiramente a partir de variáveis já definidas em 2.3.2 (precision,
salience, ignition_threshold).

---

2.11.2. Hipótese H59 (proposta, provisória)

| Hipótese | Descrição | Teste | Critério de Refutação |
|---|---|---|---|
| H59 | A duração média da dúvida pré-ignição varia com o tônus vagal (HRV): HRV mais alto associa-se a dúvidas mais curtas ou mais longas de forma sistemática e reprodutível. | Comparação pareada por semente entre grupos com refratário derivado de HRV real (PhysioNet Fantasia) | Diferença entre grupos não é estatisticamente significativa após correção para múltiplas comparações, OU não se replica em amostra independente maior (n ≥ 15 por grupo) |

---

2.11.3. Resultados Preliminares (PhysioNet Fantasia, n=3 jovens, n=2 idosos, 30 sementes)

| Condição | Dúvida média (passos) | Desvio-padrão |
|---|---|---|
| Refratário Fixo (15 passos) | 16.89 | 2.77 |
| Grupo Jovem (Y1, Y2, Y3) | 18.14 | 2.74 |
| Grupo Idoso (O1, O2) | 17.31 | 2.59 |

Testes estatísticos (pareados por semente):

| Comparação | t | p |
|---|---|---|
| Jovem vs. Idoso | 3.042 | 0.0050 |
| Fixo vs. Jovem | −4.021 | 0.0004 |
| Fixo vs. Idoso | −1.323 | 0.1961 |

---

2.11.4. Limitações (obrigatórias antes de qualquer interpretação)

1. **Tamanho amostral**: n=3 (jovem) e n=2 (idoso) são insuficientes para
   qualquer generalização populacional. O p baixo reflete consistência
   *entre sementes de simulação*, não *entre sujeitos humanos reais* —
   esta é a mesma limitação já registrada nas Seções empíricas anteriores
   do Módulo 2 para ignições e erro médio.
2. **Arbitrariedade do limiar θ_confiança**: o valor de 70% do teto de
   precisão foi escolhido por conveniência computacional, não derivado
   de teoria. Resultados devem ser recalculados com valores alternativos
   (ex: 50%, 60%, 80%) como teste de robustez antes de qualquer submissão
   para revisão por pares.
3. **Ausência de validação fenomenológica**: nada neste adendo mede
   dúvida subjetiva humana relatada (ex: escalas de incerteza
   autorrelatada). A métrica é inteiramente derivada da simulação; a
   ponte com a experiência humana de "Ser ou não Ser" permanece uma
   interpretação, não um dado.
4. **Fixo vs. Idoso não é significativo** (p=0.1961) — o padrão não é
   uniforme entre comparações, o que pesa contra uma conclusão forte
   sobre o efeito do envelhecimento especificamente.

O valor deste adendo está na **metodologia**: uma forma operacional,
falseável e replicável de medir "duração da dúvida" dentro do formalismo
já existente. A conclusão sobre jovens vs. idosos permanece hipótese
aberta, não achado consolidado.

---

2.11.5. Código para Reprodução

```python
#!/usr/bin/env python3
"""
"Ser ou não ser?" formalizado: DURAÇÃO DA DÚVIDA PRÉ-IGNIÇÃO
================================================================
Extensão do modelo de inferência ativa + Global Workspace (Módulo 2, PIC/SFT).

Ideia: a "dúvida" (Ser ou não Ser) não é um axioma novo — é um ESTADO
TRANSITÓRIO já presente no modelo: o período em que a saliência de um
canal está subindo mas ainda não cruzou o limiar de ignição (theta).

Definimos:
  - "Dúvida" = intervalo de tempo em que a precisão do canal está abaixo
    de um valor de "confiança" (ex: 70% do teto), antes da ignição
  - "Esclarecimento" = o passo t em que ignite = True (a crença "vence")
  - Duração da dúvida = número de passos entre o início da baixa
    confiança e o momento da ignição

Isso é MEDÍVEL a partir do código original do Módulo 2, sem novo termo na
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
# CARREGAR DADOS REAIS (PhysioNet Fantasia)
# ============================================================
base = '/mnt/user-data/uploads/'
subjects_young = ['fantasia_Y1_RR_intervals.txt', 'fantasia_Y2_RR_intervals.txt', 'fantasia_Y3_RR_intervals.txt']
subjects_old = ['fantasia_O1_RR_intervals.txt', 'fantasia_O2_RR_intervals.txt']

print("=" * 70)
print("DURAÇÃO DA DÚVIDA PRÉ-IGNIÇÃO: JOVEM vs. IDOSO (HRV real)")
print("=" * 70)
print(f"Limiar de confiança usado: precisão < {CONFIDENCE_THRESHOLD:.2f} (70% do teto)\n")

young_doubt = []
for f in subjects_young:
    _, _, hrv_interp = load_subject(base + f)
    refr = hrv_to_refractory(hrv_interp)
    ign, err, doubt = run_multi_seed_doubt(refractory_series=refr)
    young_doubt.append(doubt)
    print(f"{f}: duração média da dúvida = {doubt.mean():.2f} passos (desvio={doubt.std():.2f})")

old_doubt = []
for f in subjects_old:
    _, _, hrv_interp = load_subject(base + f)
    refr = hrv_to_refractory(hrv_interp)
    ign, err, doubt = run_multi_seed_doubt(refractory_series=refr)
    old_doubt.append(doubt)
    print(f"{f}: duração média da dúvida = {doubt.mean():.2f} passos (desvio={doubt.std():.2f})")

ign_fixed, err_fixed, doubt_fixed = run_multi_seed_doubt(refractory_series=None)

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
t1, p1 = stats.ttest_rel(doubt_young_avg, doubt_old_avg)
print(f"Dúvida: jovem vs idoso -> t={t1:.3f}, p={p1:.4f}")
t2, p2 = stats.ttest_rel(doubt_fixed, doubt_young_avg)
print(f"Dúvida: fixo vs jovem  -> t={t2:.3f}, p={p2:.4f}")
t3, p3 = stats.ttest_rel(doubt_fixed, doubt_old_avg)
print(f"Dúvida: fixo vs idoso  -> t={t3:.3f}, p={p3:.4f}")
```

---

2.11.6. Conexão com Outros Módulos

| Módulo | Conexão |
|---|---|
| Módulo 1 (Axiomática) | A dúvida é tratada como estado transitório de precisão/saliência, não como termo novo na Lagrangiana — preserva o Axioma Central sem expansão. |
| Módulo 2 (Sustentação) | Extensão direta das Seções 2.3–2.7; usa as mesmas variáveis (precision, salience, ignition_threshold) já definidas. |
| Módulo 7 (Epistemologia) | Oferece uma ponte formal e testável entre a fenomenologia da indecisão existencial e o formalismo IIT/inferência ativa, sem recorrer a analogias teológicas não-falseáveis. |

---

2.11.7. Próximos Passos Recomendados

1. Testar robustez do resultado com θ_confiança em {0.5, 0.6, 0.8} do teto.
2. Ampliar amostra (PhysioNet Fantasia tem mais sujeitos disponíveis além de Y1–Y3, O1–O2).
3. Aplicar correção para múltiplas comparações (ex: Bonferroni) antes de reportar p-valores como significativos, dado que três testes foram feitos sobre os mesmos dados.
4. Caso o padrão se sustente em amostra maior, considerar validação cruzada com escalas fenomenológicas de incerteza autorrelatada (ex: adaptação de escalas de tolerância à ambiguidade já validadas na literatura psicométrica).
