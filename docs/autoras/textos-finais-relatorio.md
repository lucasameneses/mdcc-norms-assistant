# Textos finais para o relatório — substituem os [PENDENTE]

Versão final, 27/11/2026. Decisão: avaliação humana e revisão de perguntas entram como
parágrafos breves e honestos (piloto), sem comparação completa. Os dados por trás de cada
número estão no repositório, calculados por scripts próprios, caso o professor peça.

| Onde está hoje | Substituir por | Seção |
|---|---|---|
| `[PENDENTE: confirmar se as autoras revisaram as perguntas sugeridas]` | Texto 1 | 3.5 (p. 11) |
| Seção 3.6 inteira | Texto 2 | 3.6 (p. 11) |
| `[PENDENTE: Médias por critério, alfa...]` (seção inteira) | Texto 3 | 4.5 (p. 14) |
| Fim do parágrafo inicial de 5.1 | Texto 4 | 5.1 (p. 15) |

---

## Texto 1 — Revisão das perguntas (fica no lugar do [PENDENTE] da seção 3.5)

```latex
A revisão por pares das perguntas foi executada como piloto — três revisoras, 38 perguntas
cada, decidindo manter, corrigir ou remover com justificativa — sobre o conjunto de um
protótipo anterior do assistente. A revisão linha a linha do conjunto final permanece como
trabalho futuro; neste, a garantia de qualidade é a verificação automática de que cada
evidência aparece literalmente no documento.
```

## Texto 2 — Avaliação humana (substitui a seção 3.6 inteira)

```latex
Uma avaliação humana piloto foi conduzida com três avaliadoras independentes, às cegas, que
atribuíram notas de 1 a 5 para correção, utilidade e clareza a 20 respostas do protótipo da
interface.
```

## Texto 3 — Resultado da avaliação humana (substitui a seção 4.5 inteira)

```latex
Na avaliação humana piloto, as três avaliadoras atribuíram em média 4,15 para correção,
3,83 para utilidade e 4,10 para clareza (escala de 1 a 5). A concordância entre elas ficou
baixa (alfa de Krippendorff entre 0,22 e 0,46), o que, com uma amostra de 20 respostas e
notas concentradas entre 4 e 5, faz do resultado um indicativo, não uma medida. Os
comentários convergiram com a métrica automática de fidelidade: em cinco das vinte
respostas, as avaliadoras apontaram afirmações que iam além da fonte citada — as mesmas
que a métrica automática penaliza.
```

## Texto 4 — Limitações (acrescentar ao parágrafo de 5.1)

```latex
A avaliação humana é um piloto: 20 respostas do protótipo, avaliadas às cegas por três
pessoas, com concordância abaixo do limiar usual, e a revisão das perguntas também ocorreu
sobre o conjunto do protótipo; nenhum dos dois substitui a mesma avaliação sobre o
conjunto final.
```

**Ajuste recomendado no início de 5.1:** o relatório diz hoje "O conjunto de avaliação foi
escrito por alunas do próprio programa". Como as perguntas foram sugeridas por LLM e a
revisão delas foi só piloto, sugerimos: "O conjunto de avaliação reúne dúvidas reais de
alunos do programa, mas suas perguntas foram sugeridas por um LLM e verificadas apenas
automaticamente, o que pode concentrá-las nos trechos mais fáceis de recuperar."

---

## Números por trás dos textos (para defender na banca)

| Pergunta | Resposta curta |
|---|---|
| Quem avaliou/revisou? | Três pessoas independentes, às cegas, sem combinarem notas; os arquivos não registram quem é quem. |
| O que foi avaliado? | 20 respostas do protótipo da interface, que usava um regulamento sintético de teste — por isso piloto. |
| Por que o alfa é baixo? | Notas concentradas em 4 e 5 (pouca variância) e só 20 respostas: o alfa cai mesmo com opiniões parecidas. |
| Alfa de Krippendorff? | Correção 0,46, utilidade 0,43, clareza 0,22 (ordinal; aceitável acima de 0,67). |
| E a revisão das perguntas? | 114 perguntas revisadas, 38 por revisora: 94 mantidas, 14 para corrigir, 6 para remover — sobre o conjunto do protótipo. |
| Onde está o dado bruto? | `results/human/ratings/` (notas), `results/human/agreement.md` (cálculo), planilhas de revisão em `dist/`. |

## Falta pouco para a versão final — checklist

- [ ] Colar os quatro textos acima no relatório (fonte LaTeX) e recompilar o PDF.
- [ ] Capa: nomes e matrículas corretos.
- [ ] Conferir a referência da LGPD (Lei nº 13.709/2018) — nunca foi verificada.
- [ ] Declaração de uso de IA e de ajuda externa (combinar o formato com o professor).
- [ ] Slide de "próximos passos": trocar "avaliação humana" por "revisão completa das
      perguntas e avaliação humana sobre o conjunto final".
- [ ] Ensaio (ROTEIRO, etapa 6) e entrega em 2/12.

Depois disso, não há mais nada pendente no repositório: sistema, avaliação automática,
dados humanos e textos estão commitados e reproduzíveis.
