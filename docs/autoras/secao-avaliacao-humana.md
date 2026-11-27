# Avaliação humana — versão breve para o relatório

Decisão (27/11/2026): em vez de seções completas, o relatório recebe um parágrafo curto.
Os dados continuam em `results/human/` (`agreement.md`, `ratings/`), calculados por
`python -m eval.agreement`, caso o professor peça o detalhe.

## Substituição da seção 3.6 (Metodologia)

O texto atual de 3.6 fala em amostra aleatória das respostas oficiais, alfa e correlação com o
juiz — descreve algo que não foi feito assim. Substituir por:

```latex
Uma avaliação humana piloto foi conduzida com três avaliadoras independentes, às cegas, que
atribuíram notas de 1 a 5 para correção, utilidade e clareza a 20 respostas do protótipo da
interface.
```

## Substituição da seção 4.5 (Resultados) — o breve comentário

Versão mínima (3 linhas):

```latex
Na avaliação humana piloto, as três avaliadoras atribuíram em média 4,15 para correção,
3,83 para utilidade e 4,10 para clareza (escala de 1 a 5). A concordância entre elas ficou
baixa (alfa de Krippendorff entre 0,22 e 0,46), o que, com uma amostra de 20 respostas e
notas concentradas entre 4 e 5, faz do resultado um indicativo, não uma medida. Os
comentários convergiram com a métrica automática de fidelidade: em cinco das vinte respostas,
as avaliadoras apontaram afirmações que iam além da fonte citada.
```

Versão curta (se preferir ainda menor):

```latex
Em um piloto com três avaliadoras às cegas sobre 20 respostas do protótipo, as notas médias
foram 4,15 para correção, 3,83 para utilidade e 4,10 para clareza (1 a 5); os comentários
apontaram afirmações além da fonte citada nas mesmas respostas que a métrica automática de
fidelidade penaliza.
```

## Se a banca perguntar

| Pergunta | Resposta curta |
|---|---|
| Quem avaliou? | Três avaliadoras independentes, às cegas (não sabiam qual modelo respondia nem combinaram notas). |
| O que foi avaliado? | 20 respostas do protótipo da interface, alimentado por um regulamento sintético de teste — por isso o piloto, e não uma avaliação da amostra oficial. |
| Por que a concordância é baixa? | Notas concentradas em 4 e 5 (pouca variância) e só 20 respostas: o alfa cai mesmo quando as opiniões são parecidas. |
| Alfa? | Correção 0,46, utilidade 0,43, clareza 0,22 (ordinal; acima de 0,67 seria aceitável). |
| Por que não houve correlação com o juiz? | As respostas avaliadas não são as da amostra oficial, então as notas do juiz não se aplicam a elas. |
| Onde está o dado bruto? | `results/human/ratings/` (planilhas) e `results/human/agreement.md` (cálculo). |
