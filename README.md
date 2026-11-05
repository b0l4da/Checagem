# Checagem de Títulos: código completo

Tudo funciona numa página só (`dist/checagem.html`), publicada no claude.ai. A pasta `src/` tem o mesmo código separado por assunto, para ler e editar com mais facilidade.

## Organização

```
checagem-titulos/
├── dist/
│   └── checagem.html            ← arquivo único (é o que está publicado no claude.ai)
├── src/
│   ├── index.html               ← estrutura das telas (menu, abas, formulários, tabelas)
│   ├── css/
│   │   ├── 01-checagem.css      ← visual geral: cores, menu lateral, cards, tabelas, gráfico
│   │   └── 02-borderos.css      ← visual da aba Borderôs e Cedentes (escopo #bord-app)
│   └── js/
│       ├── 00-observacao-expandir.js ← clicar na observação para expandir ou recolher
│       ├── 01-checagem.js       ← Registrar, Resumo, Follow-up, perfis e banco de dados
│       ├── 02-borderos.js       ← leitura da tabulação, classificação e tela de borderôs
│       └── 03-cedentes-tratativas.js ← consultar e lançar tratativas de cedentes
├── build.py                     ← junta src/ em dist/checagem.html
└── LEIA-ME.md
```

Para alterar: edite os arquivos de `src/` e rode `python3 build.py`. O arquivo `dist/checagem.html` é recriado.

## Menu (abas)

| Aba | O que tem | Arquivo principal |
|---|---|---|
| Registrar (principal) | Colar planilha, adicionar, editar e apagar título; tabela "Títulos do período" com busca e ordenação | 01-checagem.js |
| Resumo e cedentes | Indicadores, barra de status, gráfico de rosca, Vencem hoje, Últimas atualizações, Por cedente | 01-checagem.js |
| Borderôs e Cedentes | Tabulação do dia (Harpia, Securitizadora), filtros, importar tabulação, tratativas de cedentes | 02-borderos.js / 03-cedentes-tratativas.js |
| Follow-up | Sacados em aberto, do último alterado para o mais antigo, com etiquetas de prioridade | 01-checagem.js |

Cabeçalho: período (Semana, Mês com seletor mm/aaaa, Tudo) e, para a administradora, o seletor de pessoa (Minha checagem, cada pessoa ou Equipe).

## Regras de negócio

- **Encerrado:** status finalizado, mercadoria entregue, recompra ou sem retorno; observação "fax finalizado"; ou vencimento já passou. O resto fica **em aberto**.
- **Identificação de um título:** nº + sacado + cedente. Repetir esses três dados atualiza o título, não cria outro.
- **Planilha antiga:** se a data da tratativa colada for anterior à registrada, o título não é sobrescrito.
- **Período:** um título entra em Semana ou Mês se a data da tratativa **ou** a data da última alteração cair no período. A busca procura em todos.
- **Ordenação:** o último alterado vem primeiro em todas as tabelas.
- **Datas:** sempre dd/mm/aaaa.
- **Ordem das colunas ao colar:** Sacado · Nº · Status · Observação · Tentativas · Cedente · Data da tratativa · Valor · Vencimento (opcional).

## Banco de dados (claude.ai)

| Caminho | Conteúdo | Quem acessa |
|---|---|---|
| `pessoas/{id}` | registro da pessoa | a própria pessoa e a dona |
| `pessoas/{id}/titulos/{titulo}` | títulos com histórico | a própria pessoa (lê e grava); a dona lê todos |
| `dias/{aaaa-mm-dd}` | borderôs do dia | todos com acesso à página |
| `cedentes/{id}` | tratativas de cedentes | todos com acesso à página |
| `config/tipos` | tipos de tratativa | todos com acesso à página |

Campos de um título: `sacado, titulo, status, obs, tentativas, cedente, dataOp (data da tratativa), vencimento, valor, primeiroRegistro, ultimaAtualizacao, atualizadoEm, historico[]`.

## Automações (tarefas agendadas)

- **Sexta às 16h32:** Excel da semana, um por pessoa e um consolidado da equipe.
- **Dia 1 às 7h35:** resumo do mês anterior em documento, mais um Excel.

## Observações

- O código funciona dentro do claude.ai, porque usa `claude.use("db")` e `claude.use("user")`. Fora dele, a página abre, mas não salva.
- Login próprio com e-mail e senha depende do caminho 2 (Supabase + Vercel). Esta organização em `src/` já serve de ponto de partida para essa migração.
