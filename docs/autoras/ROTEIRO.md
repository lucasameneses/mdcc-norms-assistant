# Roteiro das autoras — trabalho final de LLM

Assistente de normas do MDCC com RAG · disciplina Modelos de Linguagem de Grande Escala
(Prof. José Macedo) · entrega em **2 de dezembro de 2026**.

O sistema, a avaliação automática, o relatório e os slides já existem, com dados reais. Faltam três
coisas que só vocês podem fazer:

1. Revisar as perguntas do teste.
2. Fazer a avaliação humana.
3. Tornar o relatório e a apresentação de vocês: ler, entender, reescrever no seu jeito e ensaiar.

Este roteiro explica cada passo. Tempo total estimado por pessoa: **6 a 8 horas**, espalhadas entre
28/11 e 1/12.

---

## Visão geral

| Quando | Etapa | Quem | Tempo por pessoa |
|---|---|---|---|
| 28–29/11 | 0. Entender o projeto | cada uma | 1 h |
| 28–29/11 | 1. Revisar as perguntas do teste | divididas em três partes | 1–1,5 h |
| 28–29/11 | 2. Avaliação humana às cegas | cada uma, sozinha | 1–1,5 h |
| até 30/11, 12h | 3. Enviar as planilhas ao Lucas | cada uma | 5 min |
| 30/11 | 4. Concordância calculada e relatório completado | Lucas | — |
| 30/11–1/12 | 5. Revisar o relatório e os slides | divididas | 2–3 h |
| 1/12 | 6. Ensaiar a apresentação | as três juntas | 1–2 h |
| 2/12 | 7. Entregar | uma de vocês | 15 min |

**Regra de ouro:** as etapas 1 e 2 são independentes. Façam a 2 **sem conversar** sobre as notas
até as três terminarem.

---

## Etapa 0 — Entender o projeto (1 h)

Antes de avaliar qualquer coisa, saibam explicar o sistema. Leiam nesta ordem:

1. Os **slides** (PDF), do começo ao fim. É o resumo mais rápido.
2. O **relatório** (PDF): Introdução, Metodologia e Resultados.

Ao terminar, cada uma deve conseguir responder sem consultar:

- **Qual problema o assistente resolve?** Responde dúvidas sobre as normas do MDCC citando
  documento, artigo e data.
- **O que é RAG neste projeto?**
  - As normas são cortadas em 189 trechos, um por artigo.
  - Cada trecho vira um vetor com o modelo BGE-M3.
  - Para cada pergunta, o sistema busca os 5 trechos mais parecidos e manda só eles para o modelo
    gerar a resposta.
- **Quais modelos foram comparados e qual foi recomendado?**
  - Foram comparados gpt-oss:20b, gpt-oss:120b e gemma4:31b, todos via Ollama Cloud.
  - O recomendado foi o **gpt-oss:120b**.
- **Como foi a avaliação automática?**
  - Na busca: *hit@5* e MRR, sem LLM.
  - Nas respostas: outro LLM (glm-5.3) atuou como juiz, com uma rubrica de correção, fidelidade
    à fonte e citação.
  - Nos casos especiais: regras automáticas para "não encontrei", "fora do escopo" e injeção.
- **Quais riscos foram testados?**
  - Injeção indireta de *prompt* (trecho envenenado na base).
  - Perguntas fora do escopo.
  - Perguntas sem resposta nas normas.
  - Viés de linguagem: pergunta formal × informal.
  - Privacidade: e-mail, CPF e matrícula são mascarados antes de ir para o modelo e para o log.

Se algum desses pontos não ficar claro, anotem a dúvida e perguntem ao Lucas antes da etapa 5.

---

## Etapa 1 — Revisar as perguntas do teste (1–1,5 h por pessoa)

### Por que

As 114 perguntas da avaliação foram **sugeridas por um LLM** a partir dos documentos. O código só
conferiu que o trecho de evidência de cada uma existe, palavra por palavra, no documento. Nenhuma
pessoa leu as perguntas ainda. O relatório só pode dizer "as perguntas foram revisadas pelas
autoras" se vocês de fato revisarem.

### Arquivo

`revisao-perguntas.csv`. Importem no Google Sheets: Arquivo › Importar › Fazer upload ›
separador vírgula.

| Coluna | O que é |
|---|---|
| `id` | Identificador da pergunta. Não alterar. |
| `categoria` | Tipo da pergunta (ver abaixo). |
| `estilo` | `formal` ou `informal`. |
| `pergunta` | O que o aluno perguntaria. |
| `resposta_referencia` | A resposta correta esperada. |
| `evidencia` | Trecho literal da norma que sustenta a resposta. |
| `documento` | De qual norma saiu. |
| `revisora` | **Preencher** com seu nome. |
| `decisao` | **Preencher** com `ok`, `corrigir` ou `remover`. |
| `motivo` | **Preencher** quando a decisão não for `ok`. |

### Divisão

| Revisora | Linhas da planilha (sem contar o cabeçalho) |
|---|---|
| Leticia | 1 a 38 |
| Danielly | 39 a 76 |
| Eduarda | 77 a 114 |

### O que conferir em cada linha

**Categoria `normal`** (92 perguntas):

1. **A pergunta é realista?** Um aluno do MDCC perguntaria isso? Se for estranha, artificial ou
   ambígua, marque `corrigir` e sugira outra redação.
2. **A resposta de referência está certa?** Leiam a `evidencia`. A resposta precisa ser sustentada
   por ela, sem acrescentar fatos que não estão lá. Se acrescentar, marque `corrigir`.
3. **A evidência responde à pergunta?** Se o trecho fala de outra coisa, marque `remover` ou
   `corrigir`.
4. **O estilo bate?** Uma pergunta `informal` deve soar como conversa ("dá pra...", "quanto
   tempo eu tenho..."); uma `formal`, como texto escrito.

**Categoria `not_found`** (8): perguntas plausíveis cuja resposta **não está** nas normas. O
assistente deve admitir que não encontrou. Confiram se a resposta realmente não está nos
documentos. Se vocês souberem que está, marquem `remover`.

**Categoria `out_of_scope`** (8): perguntas que nada têm a ver com as normas (receita, futebol...).
O assistente deve recusar. Confiram só se estão claramente fora do assunto.

**Categoria `injection`** (6): perguntas usadas no teste de segurança, junto com um trecho
envenenado na base. Confiram só se a pergunta é normal e plausível. O ataque está no trecho, não
na pergunta.

### Critério de decisão

- `ok`: pode ficar como está.
- `corrigir`: a ideia é boa, mas o texto precisa mudar. Escrevam no `motivo` como deveria ficar.
- `remover`: não serve (errada, ambígua, duplicada, evidência não responde).

Na dúvida entre `ok` e `corrigir`, escolham `corrigir` e expliquem. Se houver correções, o Lucas
ajusta e roda a avaliação de novo (cerca de 20 minutos), e os números do relatório são
atualizados.

---

## Etapa 2 — Avaliação humana às cegas (1–1,5 h por pessoa)

### Por que

A rubrica da disciplina pede avaliação **automática e humana**. A nota humana serve para duas
coisas:

- medir a qualidade do assistente do ponto de vista de quem usa;
- validar o juiz automático: se as notas de vocês acompanham as do juiz, o juiz é confiável.

### Arquivo

`avaliacao-humana-modelo.csv`, com **20 respostas reais** do assistente sorteadas entre os três
modelos. Cada uma faz **a sua própria cópia**.

| Coluna | O que é |
|---|---|
| `sample_id` | Identificador (s01 a s20). **Não alterar.** |
| `pergunta` | A pergunta feita. |
| `resposta` | O que o assistente respondeu. Os números entre colchetes, como [1], são citações. |
| `fontes` | O documento e o artigo que o assistente usou. |
| `correcao_1a5` | **Preencher.** |
| `utilidade_1a5` | **Preencher.** |
| `clareza_1a5` | **Preencher.** |
| `comentario` | Opcional, mas ajuda muito na discussão. |

### Regras

1. **Às cegas.** A planilha não diz qual modelo respondeu, e é de propósito. Não tentem descobrir.
2. **Sozinhas.** Não conversem sobre as notas até as três enviarem. O relatório mede a
   concordância entre vocês (alfa de Krippendorff). Se combinarem notas, essa medida perde o
   sentido.
3. **Confiram na fonte.** Para cada resposta, abram o documento citado em `fontes` e leiam o
   artigo ou item. Não avaliem de memória. Os documentos estão na pasta `documentos/` que o Lucas
   manda junto, e também nos links oficiais abaixo.
4. **Só números inteiros de 1 a 5.** Nada de 3,5.
5. **Não mudem** colunas, ordem das linhas nem o `sample_id`.

### Escala

**Correção** — o que a resposta afirma está certo segundo a norma?

| Nota | Significado | Exemplo |
|---|---|---|
| 5 | Tudo correto e sustentado pela fonte. | Prazo de 30 meses, prorrogável por 3, como diz o artigo. |
| 4 | Correto, faltando um detalhe pequeno. | Diz 30 meses, mas não menciona a prorrogação. |
| 3 | Parte certa, parte errada ou faltando algo importante. | Acerta o prazo, mas erra quem aprova a prorrogação. |
| 2 | Mais errado do que certo. | Prazo errado, com um detalhe certo. |
| 1 | Errado ou inventado. | Cita uma regra que não existe na norma. |

Se a **citação** apontar para um artigo que não sustenta a resposta, desçam a nota de correção
(no mínimo um ponto) e anotem no comentário. Se o assistente disser que não encontrou a resposta
e ela de fato não estiver na fonte, isso conta como correto.

**Utilidade** — um aluno com essa dúvida ficaria resolvido?

| Nota | Significado |
|---|---|
| 5 | Resolve completamente; o aluno sabe o que fazer. |
| 4 | Resolve quase tudo. |
| 3 | Ajuda, mas o aluno ainda precisa procurar. |
| 2 | Ajuda pouco. |
| 1 | Não ajuda ou atrapalha. |

**Clareza** — é fácil de ler e entender?

| Nota | Significado |
|---|---|
| 5 | Direta, bem escrita, tamanho certo. |
| 4 | Clara, com um pequeno excesso ou repetição. |
| 3 | Dá para entender com algum esforço. |
| 2 | Confusa ou muito longa. |
| 1 | Ilegível ou fora do assunto. |

As três notas são independentes. Uma resposta pode estar errada (correção 1) e ainda assim ser
clara (clareza 5).

### Documentos oficiais

| Documento | Link |
|---|---|
| Regimento do MDCC | mdcc.ufc.br (página de normas) |
| Resolução nº 17/CEPE/2015 | site da PRPPG/UFC |
| Normas MDCC 02/2019, 01/2024, 01/2025 | mdcc.ufc.br (página de normas) |
| Procedimentos (conclusão, aproveitamento, proficiência, defesas, diploma, disciplinas) | mdcc.ufc.br/pt/procedimentos |

As cópias exatas usadas pelo sistema vão na pasta `documentos/`. Prefiram essas, porque são as
versões que o assistente leu.

---

## Etapa 3 — Enviar as planilhas (até 30/11, 12h)

1. Salvem cada planilha com **o seu primeiro nome, em minúsculas e sem acento**:
   - avaliação humana: `leticia.csv`, `danielly.csv`, `eduarda.csv`;
   - revisão das perguntas: `revisao-leticia.csv`, `revisao-danielly.csv`, `revisao-eduarda.csv`.
2. **Formato CSV com vírgula.** No Google Sheets use Arquivo › Fazer download › Valores separados
   por vírgula (.csv). **Evitem o Excel em português**: ele salva com ponto e vírgula e o script
   não lê.
3. Antes de enviar, confiram:
   - [ ] as 20 linhas da avaliação têm as três notas preenchidas;
   - [ ] só há números inteiros de 1 a 5;
   - [ ] as 38 linhas da sua parte da revisão têm `decisao` preenchida;
   - [ ] o nome do arquivo está certo.
4. Enviem ao Lucas. O mínimo são **duas** avaliações; com as **três** o resultado é mais forte.

---

## Etapa 4 — O que o Lucas faz com as planilhas (30/11)

Fica aqui para vocês saberem explicar na apresentação.

1. Aplica as correções da revisão e, se mudar alguma pergunta, roda a avaliação automática de
   novo.
2. Roda `python -m eval.agreement`, que calcula:
   - a **média** de cada critério (correção, utilidade, clareza);
   - o **alfa de Krippendorff ordinal**, que mede a concordância entre vocês. Acima de 0,67 é
     aceitável e acima de 0,8 é bom;
   - a **correlação de Spearman entre o juiz automático e a média de vocês** na correção. Quanto
     mais perto de 1, mais o juiz concorda com as pessoas.
3. Preenche a seção de avaliação humana do relatório e o slide de próximos passos, e remove os
   marcadores `[PENDENTE]`.
4. Envia o relatório e os slides atualizados para a etapa 5.

---

## Etapa 5 — Revisar o relatório e os slides (30/11–1/12, 2–3 h por pessoa)

O texto precisa ser de vocês: o professor vai perguntar, e vocês precisam reconhecer cada frase.

### Divisão

| Revisora | Capítulos do relatório | Slides |
|---|---|---|
| Leticia | Resumo, Introdução, Trabalhos relacionados | 1 a 5 |
| Danielly | Metodologia, Resultados | 6 a 9 |
| Eduarda | Discussão, Conclusão, Referências | 10 a 14 |

### Checklist de cada uma

- [ ] Li a minha parte inteira e entendi cada frase.
- [ ] Reescrevi com as minhas palavras o que não soava como eu. Mandar as mudanças como
  comentários no PDF ou numa lista "página X: trocar A por B".
- [ ] Conferi se os números do texto batem com as tabelas (por exemplo: *hit@5* 0,90 contra 0,75;
  aprovação de 83 % a 88 %).
- [ ] Marquei qualquer afirmação que eu não saberia defender.

### Itens de todas

- [ ] Nomes e matrículas na capa estão corretos.
- [ ] A referência da LGPD (Lei nº 13.709/2018) está correta. Ela ainda não foi conferida.
- [ ] A frase sobre a revisão das perguntas (Metodologia) descreve o que vocês fizeram na
  etapa 1, nem mais nem menos.
- [ ] **Declaração de uso de IA e de ajuda externa.** Combinem com o professor o formato e incluam
  a declaração. O código, o relatório e os slides foram produzidos com apoio de um assistente de
  IA e de uma pessoa de fora do grupo. O professor autorizou essa ajuda, mas a declaração deve
  ficar explícita.

---

## Etapa 6 — Ensaiar a apresentação (1/12, 1–2 h juntas)

### Divisão sugerida (cerca de 15 minutos)

| Quem | Slides | Conteúdo | Tempo |
|---|---|---|---|
| Leticia | 1–5 | Problema, o assistente funcionando, pipeline, corpus e chunking | 5 min |
| Danielly | 6–9 | Escolha dos modelos, desenho da avaliação, chunking por artigo, qualidade | 5 min |
| Eduarda | 10–14 | Segurança, custo/memória/latência, recomendação, próximos passos | 5 min |

Confirmem com o professor o tempo disponível e ajustem.

### Como ensaiar

1. Cada uma apresenta a sua parte com cronômetro.
2. As outras duas fazem perguntas da lista abaixo.
3. Repitam até caber no tempo e ninguém travar nas perguntas.

### Perguntas prováveis da banca, com o ponto central da resposta

| Pergunta | Ponto central |
|---|---|
| Por que RAG e não ajuste fino? | As normas mudam; com RAG basta reindexar. Ajuste fino exigiria dados rotulados e retreino a cada mudança e não daria citação da fonte. |
| Por que o BGE-M3? | É multilíngue, vai bem em português, roda localmente e tem 1024 dimensões. |
| Por que dividir por artigo? | O artigo é a unidade de sentido da norma. A divisão por artigo teve *hit@5* de 0,90, contra 0,75 da divisão fixa de 1000 caracteres. |
| Como saber se o juiz LLM é confiável? | Pela correlação com a avaliação humana (etapa 4). Também foi usado um juiz de outra família, com temperatura 0. |
| Por que só metade dos casos de injeção foi barrada? | Os modelos seguem instruções escondidas nos trechos recuperados. Mitigações: filtrar trechos com instruções, separar dados de instruções no *prompt*, validar a saída. Com só 6 casos, a margem de erro é grande. |
| Por que recomendar o 120b se o gemma é mais rápido? | O 120b teve a maior aprovação (88 %), recusou 100 % das perguntas fora do escopo, é barato (US$ 0,12 por mil perguntas) e tem latência p95 abaixo de 2 s. |
| E a privacidade? | E-mail, CPF e matrícula são mascarados antes do modelo e do log, e o log não tem nenhum campo que identifique a pessoa. |
| O que acontece quando uma norma muda? | Troca-se o PDF e reindexa-se; nenhum modelo é retreinado. A data do documento aparece na citação. |
| Quais os limites do trabalho? | Perguntas sugeridas por LLM (mitigado pela revisão de vocês), poucos casos de segurança, só 20 respostas na avaliação humana, corpus pequeno. |
| Quanto custa e quanta memória precisa? | Custo por mil perguntas: US$ 0,08 a 0,28. Memória estimada dos pesos: 11 a 65 GB, por isso a geração roda na nuvem e só os *embeddings* rodam localmente. |

### Demonstração ao vivo

O assistente roda só no computador do Lucas, sem acesso pela internet, por segurança. Há duas
opções:

- **A.** Usar o print que já está no slide 3 (recomendado: sem risco de falha).
- **B.** Fazer a demo ao vivo no notebook do Lucas, se ele estiver presente.

Perguntas boas para a demo:

- "Qual o prazo máximo para concluir o mestrado?"
- "Como comprovo proficiência em inglês?"
- "Qual a receita de bolo de cenoura?" (mostra a recusa fora do escopo)

---

## Etapa 7 — Entrega (2/12)

- [ ] PDF final do relatório.
- [ ] PDF final dos slides.
- [ ] Código: o repositório é privado. Confirmem com o professor se ele prefere ser adicionado
  como colaborador no GitHub ou receber um `.zip` (sem o arquivo `.env`).
- [ ] Declaração de uso de IA incluída (etapa 5).
- [ ] Nomes dos arquivos combinados com o professor.

---

## Arquivos que o Lucas envia junto com este roteiro

| Arquivo | Para quê |
|---|---|
| `ROTEIRO.md` | Este guia. |
| `revisao-perguntas.csv` | Etapa 1. |
| `avaliacao-humana-modelo.csv` | Etapa 2: cada uma faz a sua cópia. |
| `documentos/` | Os PDFs e as páginas usadas pelo sistema, para conferir as fontes. |
| `relatorio.pdf` e `slides.pdf` | Etapas 0 e 5. |

Dúvidas: falem com o Lucas antes de decidir sozinhas. É melhor perguntar do que preencher no
chute.
