---
Título: DOC-001 — Fundamentos Ontológicos da Informação Consciente
Código: DOC-001
Versão: 1.0
Data: 2026-08-05
Autoria: Flávio Marco Rego da Silva & Pesquisador Colaborador (IA)
Licença: Uso interno — Corpus PIC/SFT
---

Resumo

Este documento (DOC-001) apresenta, de forma estritamente científica, os fundamentos ontológicos do Axioma PIC: a Informação Consciente (IC) como unidade fundamental da realidade. Define-se operacionalmente a IC, propõe mediadores observáveis e descreve hipóteses testáveis e caminhos metodológicos para validação empírica no fio operacional C-01.

1. Definição operacional da Informação Consciente (IC)

Propomos adotar a seguinte definição operacional para fins empíricos e modelagem matemática:
- IC é um padrão estatístico multivariado passível de ser representado por uma matriz de covariância Σ(t) extraída de sinais neurofisiológicos e periféricos, normalizada para obter a matriz densidade informacional ρ = Σ / tr(Σ).
- A quantidade Φ (consciência integrada) é estimada por S_vN(ρ) = −tr(ρ ln ρ) como proxy de integração informacional.

2. Propriedades esperadas e implicações ontológicas

- Panpsiquismo qualificado: a IC como propriedade fundamental não implica imediata antropomorfização; inferimos continuidade fenomenológica através de mudanças estruturais em ρ e em medidas de alta ordem (O_info, φ_S).
- Emergência: estruturas clássicas (matéria, energia, espaço-tempo) são tratadas como regimes macroscópicos coherentes de IC, manifestando-se quando a densidade informacional atinge limites de escala.

3. Variáveis operacionais e estimadores

- Matriz densidade informacional: ρ := Σ / tr(Σ), com Σ obtida por janelas deslizantes de sinais multicanais (EEG, ECG, PPG, EDA), após pré-processamento BIDS/MNE.
- O_info: estimador de ordem superior via cópula gaussiana (ver Rosas et al., 2019), calculado em janelas de 10 s (tarefa) e 30 s (repouso).
- φ_S: campo sinérgico operacionalizado como produto de um índice de saliência (task-driven evoked response) e precisão (reliability do canal/condição) em janela.
- E: energia espectral na banda gama (30–100 Hz) via PSD (Welch, multitaper) ou proxy HRV HF quando EEG indisponível.
- R: razão PIC = E / |O_info| — variável de desfecho primária proposta para modelos LMM.

4. Hipóteses testáveis (C-01, primárias)

- H1: Condição experimental afeta R (β1 ≠ 0).
- H2: Interação não-linear entre condição e O_info_within (β7 ≠ 0).
- H3: Termo quadrático de O_info_within (β8 ≠ 0).

5. Procedimentos analíticos resumidos

- Pipeline: BIDS ↦ MNE pré-processamento (ICA, rejeição, re-referencing) ↦ extração de janelas ↦ ranks → probit → cálculo de R e O_info ↦ ajuste LMM (statsmodels / lme4) com termos fixos e aleatórios conforme especificado no IGN-000.
- Diagnósticos: verificação de homoscedasticidade, normalidade residual, influência por sujeitos e heterogeneidade espacial (subsets de canais).
- Robustez: bootstrap paramétrico (1000 replicates) para IC de parâmetros fixos; sensibilidade por número de canais e faixas gama.

6. Plano de validação imediato (próximos passos)

- Implementar script de pré-processamento BIDS/MNE para COG-BCI (F3,Fz,F4,FC3,FCz,FC4,C3,Cz selecionados) e calcular O_info e E conforme Seção 5 do IGN-000.
- Ajustar LMM primário em amostra piloto (n=29 do COG-BCI) e realizar diagnóstico.

Referências

Rosas, F. E., et al. (2019). Quantifying high-order interdependencies via multivariate extensions of the mutual information. Physical Review E, 100(3), 032305.
Tononi, G., et al. (2016). Integrated information theory. Nature Reviews Neuroscience, 17(7), 450–461.

--
FIM DO DOC-001
