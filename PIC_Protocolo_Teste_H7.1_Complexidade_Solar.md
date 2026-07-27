# Protocolo de Teste Falseável — H7.1: Complexidade Informacional em Sinais Solares

## 0. O problema com a formulação original (precisa ser corrigido primeiro)

A Previsão 7.1 no documento "O Princípio da Informação Consciente" diz:

> "Algoritmos de complexidade (e.g., complexidade de Lempel-Ziv) [...] aplicados a
> sinais eletromagnéticos [...] do Sol [...] revelarão padrões de informação
> complexa e não-trivial que não podem ser explicados por processos puramente
> estocásticos ou modelos físicos lineares."

**Isso já é esperado pela heliofísica padrão, sem precisar do PIC.**

O dínamo solar é um sistema dinâmico **não-linear e caótico** — isso é ciência
estabelecida desde os anos 1980 (modelos de van der Pol, mapas logísticos
aplicados ao ciclo de manchas solares, turbulência magnetohidrodinâmica). Um
sistema caótico determinístico *sempre* vai exibir complexidade maior que um
modelo estocástico linear simples (ruído branco, passeio aleatório) — isso não
é evidência de consciência ou de Φ, é a assinatura padrão de caos determinístico
em qualquer sistema físico não-linear, incluindo sistemas que ninguém suspeitaria
de ter Φ significativo (turbulência de fluidos, reações químicas oscilantes tipo
Belousov-Zhabotinsky, circuitos eletrônicos caóticos).

**Consequência:** testar "complexidade real vs. modelo estocástico linear" não
distingue PIC de heliofísica padrão. Os dois fazem a mesma previsão. Um teste
que não distingue duas teorias não testa nada.

## 1. Hipótese corrigida (agora genuinamente distintiva)

Para que o teste tenha poder de falsear especificamente o PIC (e não caos comum),
o modelo nulo precisa ser o **melhor modelo caótico não-linear conhecido do
dínamo solar** — não um modelo estocástico ingênuo.

**H7.1-revisada:** A complexidade informacional (proxy: complexidade de
Lempel-Ziv normalizada, LZC) do sinal solar real excede significativamente a
complexidade gerada por um modelo determinístico não-linear ajustado
(ex: mapa não-linear tipo Bracewell/Duhau ou reconstrução por embedding de
Takens com dimensão ótima), reproduzindo o mesmo espectro de potência e a
mesma estrutura de recorrência do sinal real.

**Critério de falsificação:** Se LZC(sinal real) ≈ LZC(modelo caótico ajustado)
dentro do intervalo de confiança, a hipótese PIC específica é refutada — o
sinal é plenamente explicável por dinâmica não-linear conhecida, sem precisar
de nenhum termo Φ_global adicional.

## 2. Dados (públicos, verificáveis por qualquer pessoa)

| Fonte | Dado | Acesso |
|---|---|---|
| NOAA SWPC | Fluxo de raios-X GOES (resolução 1 min) | https://www.swpc.noaa.gov/products/goes-x-ray-flux |
| SILSO (Observatório de Bruxelas) | Número de manchas solares diário/mensal, série desde 1749 | https://www.sidc.be/SILSO/ |
| NASA/NSO | Índices de heliosismologia (GONG) | https://gong.nso.edu/ |

Usar pelo menos 2 séries independentes (ex: raios-X + manchas) para checar
consistência do resultado.

## 3. Método passo a passo

1. **Pré-processar**: normalizar a série, remover tendência sazonal óbvia
   (ciclo de 11 anos), converter em série binária/simbólica para cálculo de LZC
   (padrão na literatura: binarização pela mediana ou por quantis).
2. **Calcular LZC do sinal real.**
3. **Construir três modelos nulos, não um só:**
   - **Nulo A (fraco, já refutado por heliofísica):** ruído branco / AR(1) linear.
   - **Nulo B (surrogate de fase):** mesmo espectro de potência do sinal real,
     fase randomizada (preserva linearidade, destrói não-linearidade).
   - **Nulo C (o que falta no documento original — o mais importante):**
     modelo caótico não-linear ajustado aos dados reais (ex: rede neural
     recorrente pequena treinada só para reproduzir a dinâmica, ou reconstrução
     de atrator por Takens embedding + previsão local).
4. **Gerar 1000+ realizações de cada nulo**, calcular LZC de cada uma,
   construir distribuição empírica.
5. **Comparar LZC(real) contra as três distribuições** — z-score e p-valor
   para cada.

## 4. Interpretação dos resultados possíveis

| Resultado | Interpretação |
|---|---|
| Real > Nulo A e B, mas ≈ Nulo C | **PIC refutado nesta previsão específica.** Caos não-linear padrão explica tudo. |
| Real > Nulo A, B **e** C | Achado genuinamente interessante — mas ainda não prova Φ/consciência. Só mostra que o modelo caótico atual é incompleto. Próximo passo: tentar modelos não-lineares mais sofisticados antes de invocar PIC. |
| Real ≈ todos os nulos | Sinal é mais simples do que se pensava. Refuta tanto PIC quanto a narrativa de "caos rico". |

## 5. Por que isso é mais forte para o PIC, não mais fraco

Se algum dia o resultado "Real > Nulo C" aparecer, de forma replicada em
múltiplas séries e períodos, **isso seria notável de verdade** — porque
eliminaria a explicação mais óbvia (caos determinístico conhecido) antes de
cogitar qualquer coisa nova. Um resultado que sobrevive ao nulo mais rigoroso
tem muito mais peso do que "bateu o ruído branco", que qualquer sistema físico
minimamente estruturado já bate.

## 6. O que este protocolo não resolve

Mesmo que "Real > Nulo C" se confirme estatisticamente, isso mostraria apenas
que **existe estrutura informacional não explicada pelos melhores modelos não-
lineares atuais** — não que essa estrutura é "consciente" no sentido de Φ da
IIT. Ligar excesso de complexidade a Φ/consciência exigiria uma etapa adicional
de definição operacional de Φ para sinais eletromagnéticos, que — como já
apontado nas revisões anteriores do PIC — ainda não existe de forma rigorosa
no framework.
