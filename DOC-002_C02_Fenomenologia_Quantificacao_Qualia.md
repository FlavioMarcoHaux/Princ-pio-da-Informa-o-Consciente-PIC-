---
title: DOC-002 — Fenomenologia da Consciência e Quantificação de Qualia
cell: C-02
agent: A-01
subagent: S-01
date: 2026-08-05
authors: ["Flávio Marco Rego da Silva", "Agente Colaborador (IA)"]
---

# DOC-002 — Fenomenologia da Consciência e Quantificação de Qualia (C-02 / A-01 / S-01)

Resumo

Este documento aborda a operacionalização fenomenológica dos estados conscientes (qualia) no contexto do framework PIC/SFT. Propõe medidas comportamentais e fisiológicas que funcionam como proxies quantificáveis de características fenomenológicas e descreve protocolos experimentais e métricas para validar essas proxies.

1. Objetivos

- Definir quais aspectos fenomenológicos são relevantes para medir (intensidade, valência, espacialidade, unidade/permeabilidade).
- Propor instrumentos e índices empíricos para mapear esses aspectos em dados (EEG, ECG, pupila, relatos subjetivos).
- Fornecer rotinas analíticas para transformar relatórios subjetivos em variáveis continuas (PCA, IRT, escalonamento).

2. Conceitos Fenomenológicos-alvo

- Intensidade (I): força subjetiva da experiência — medida via escala contínua (0–1) ou VAS.
- Valência (V): positivo ↔ negativo — medidas auto-relato (PANAS) e proxies fisiológicos (correntes valência-asimétricas EEG frontal).
- Spatialidade/Boundedness (B): sensação de limites do self — questionários específicos e análise de coerência de rede neural.
- Unidade/Discontinuity (U): sensação de unidade — LZC de padrões de ignição, sincronização global.

3. Instrumentos e Proxies Operacionais

- Escalas subjetivas: VAS para intensidade; modified EDI para corporeidade; custom items para boundednes.
- Experience Sampling (mini-NYC-Q / RSME): amostragens rápidas durante tarefas.
- Physiological proxies:
  - EEG: Φ-proxies (LZC de ignições), O_info (sinergia vs redundância), PSD gama (E).
  - ECG/HRV: RMSSD e HF power como indicador de estado interoceptivo e regulação autonômica.
  - Pupillometry: dilatação média como proxy de esforço/alerteza.
- Behavioral: RT distributions, error rates, sustained attention metrics (PVT).

4. Transformação de Relatos Subjetivos

- Normalização (0–1) e correção por ordem/efeito de sessão.
- Redução dimensional: PCA/FA para extrair fatores (ex.: Engajamento, Vividness, Distancing).
- IRT para itens com escalas ordinal; uso para comparabilidade entre idiomas/populações.

5. Mapeamento para φ_S e Φ

- φ_S (campo sinérgico) = f(normalized_saliência × normalized_precisão × subject_factor)
- Φ-proxy = g(LZC(ignitions), entropy_measures, global_sync)
- Teste convergente: correlação parcial entre Φ-proxy e φ_S controlando por E e ordem

6. Protocolo Experimental Proposto (Resumo)

- Condições: Baseline (EO/EC), Task baixa carga, Task alta carga (N-Back 2-back / MATB-difficult), Estado meditativo (5–10 min)
- Medidas: EEG 64ch + ECG + pupila + questionários (RSME, mini-NYC-Q)
- Janelas: tarefas 10s/2s; resting 30s/5s
- Análises primárias: R ~ condição + ordem + φ_S + (1|sujeito)

7. Critérios de Validação

- Convergência entre proxies fenom. (report + physiology) (r > 0.4 esperado).
- Reprodutibilidade across sessions (ICC > 0.5).
- Sensibilidade a manipulações experimentais (efeito de condição significativo em LMM).

8. Limitações e Considerações Éticas

- Relatos subjetivos são influenciados por idioma e cultura; traduções validadas são necessárias.
- Medidas fisiológicas são proxies; inferências fenomenológicas precisam ser trianguladas.
- Informed consent/privacidade: garantir anonimização e clareza sobre uso dos dados.

Referências selecionadas

- Bach, D. R., et al. (2013). Mechanisms of fear and processing in the brain. Trends Cogn Sci.
- Smallwood, J., & Schooler, J. W. (2015). The science of mind-wandering. Annu Rev Psychol.
- Tononi, G., et al. (2016). Integrated information theory. Nature Rev. Neurosci.

---

*DOC-002 gerado automaticamente a partir do IGN-000 v5.0 e IGN-002.*
