# Seção de avaliação humana — texto pronto para o relatório

Gerada em 27/11/2026 a partir das planilhas de `results/human/ratings/` (três avaliadoras, às
cegas), por meio de `python -m eval.agreement`. Saída completa: `results/human/agreement.md`.

**Como ler:** os textos abaixo substituem os trechos `[PENDENTE]` das seções 3.6 e 4.5 e
acrescentam uma frase à seção 5.1. Os números já estão na formatação do relatório (vírgula
decimal). Se as autoras fizerem também a avaliação às cegas da amostra oficial (prazo 30/11),
os textos de 3.6 e 4.5 devem ser trocados pela versão dela, que também permite a correlação
com o juiz automático — neste piloto ela não se aplica.

---

## 3.6 Avaliação humana (substitui a seção inteira)

```latex
Uma avaliação humana piloto foi conduzida com três avaliadoras independentes, às cegas, que
não sabiam qual modelo respondia nem discutiram as notas entre si. Foram avaliadas 20
respostas do protótipo da interface, alimentado por um regulamento sintético de teste, em
três critérios em escala de 1 a 5: correção (se o que a resposta afirma está certo segundo a
fonte citada), utilidade (se um aluno com aquela dúvida ficaria resolvido) e clareza (se é
fácil de ler e entender). Para cada resposta, a avaliadora abriu a fonte citada antes de
notar. São reportadas as médias por critério e a concordância entre avaliadoras pelo alfa de
Krippendorff ordinal.
```

## 4.5 Avaliação humana (substitui a seção inteira)

```latex
A Tabela 6 resume o piloto humano. As médias foram altas nos três critérios: 4,15 em
correção, 3,83 em utilidade e 4,10 em clareza, num intervalo de 1 a 5. A concordância entre
as avaliadoras, medida pelo alfa de Krippendorff ordinal, ficou em 0,46 na correção, 0,43
na utilidade e 0,22 na clareza: abaixo do limiar de 0,67 considerado aceitável. Duas causas
prováveis se somam: as notas se concentram entre 4 e 5, o que reduz a variância que o alfa
mede, e a amostra tem apenas 20 respostas. O resultado indica que o piloto serve como
termômetro, mas não autoriza afirmações fortes sobre a qualidade percebida.

Os comentários das avaliadoras apontaram um problema recorrente e específico: em cinco das
vinte respostas (S01, S06, S10, S19 e S20), notaram afirmações que iam além do que a fonte
citada sustenta — a mesma falha que a métrica automática de fidelidade pune. As duas
recusas corretas (perguntas sem resposta na fonte) foram reconhecidas como conduta
adequada. Essa convergência entre a leitura humana e a métrica automática é o resultado mais
útil do piloto.

\begin{table}[htbp]
\caption{Avaliação humana do protótipo: média das notas e concordância entre as três avaliadoras.}
\label{tab:humana}
\centering
\begin{tabular}{lcc}
\toprule
Critério & Média (1 a 5) & Alfa de Krippendorff \\
\midrule
Correção & 4,15 & 0,46 \\
Utilidade & 3,83 & 0,43 \\
Clareza & 4,10 & 0,22 \\
\bottomrule
\end{tabular}
\end{table}
```

## 5.1 Limitações (frase a acrescentar ao final do parágrafo existente)

```latex
A avaliação humana é um piloto: 20 respostas do protótipo sobre um regulador sintético,
avaliadas às cegas por três pessoas, com concordância entre avaliadoras abaixo de 0,67; a
correlação entre o juiz automático e as notas humanas, prevista no desenho, não pôde ser
calculada nesta versão e depende da avaliação da amostra oficial.
```

---

## Números-chave (para conferir no texto e nos slides)

| Métrica | Valor |
|---|---|
| Avaliadoras | 3, às cegas, independentes |
| Respostas avaliadas | 20 (protótipo/mockup, regulamento sintético) |
| Média correção | 4,15 |
| Média utilidade | 3,83 |
| Média clareza | 4,10 |
| Alfa Krippendorff (correção / utilidade / clareza) | 0,46 / 0,43 / 0,22 |
| Correlação juiz × humano | não aplicável nesta amostra |
| Respostas com "afirma além da fonte" apontadas pelas avaliadoras | 5 de 20 (S01, S06, S10, S19, S20) |

Observação: limiar de 0,67 no alfa vem do roteiro da disciplina (acima de 0,67 aceitável,
acima de 0,8 bom). As notas concentram-se em 4 e 5, o que derruba o alfa mesmo com opiniões
parecidas — vale explicar isso se a banca perguntar.

