# Moqueca — scanner (analisador léxico)

Protótipo didático feito para a Avaliação Processual do 2º bimestre de 2026 da disciplina
**Linguagens Formais e Compiladores** (Sistemas de Informação — Multivix Vitória).

A **Moqueca** é uma mini-linguagem de atribuições e expressões aritméticas. O nome é uma
homenagem à moqueca capixaba, e os exemplos usam custos de uma receita:

```
porcao = (peixe + camarao + temperos) / pessoas;
mostra porcao * 1.10;
```

O `scanner.py` lê o código, ignora espaços e quebras de linha e mostra os tokens na ordem de
leitura, com tipo, lexema, linha e coluna. Quando encontra um caractere que não pertence à
linguagem, informa um erro léxico e continua a leitura.

## Requisitos

- Python 3.7 ou superior (não usa bibliotecas externas)

## Como executar

No Windows use `python`; no Linux/macOS, `python3`.

```bash
python scanner.py "resultado = (4 + 2) * 3;"   # analisa uma linha
python scanner.py -f exemplos/caso3.moq        # analisa um arquivo
python scanner.py                              # pede a linha pelo teclado
```

## Tokens reconhecidos

| Tipo | Padrão | Exemplos |
|---|---|---|
| PALAVRA_RESERVADA | `mostra` | `mostra` |
| IDENTIFICADOR | `[a-zA-Z_][a-zA-Z0-9_]*` | `preco`, `nota1`, `_aux` |
| NUMERO | `[0-9]+(\.[0-9]+)?` | `10`, `45.50` |
| ATRIBUICAO | `=` | `=` |
| OP_SOMA | `+` | `+` |
| OP_SUB | `-` | `-` |
| OP_MULT | `*` | `*` |
| OP_DIV | `/` | `/` |
| ABRE_PAR | `(` | `(` |
| FECHA_PAR | `)` | `)` |
| PONTO_VIRGULA | `;` | `;` |

Espaços, tabulações e quebras de linha são ignorados. Qualquer outro caractere (por exemplo
`ç`, `@`, `#`) gera um **erro léxico**.

## Casos de teste usados no relatório

| Caso | Arquivo | Entrada | Situação |
|---|---|---|---|
| 1 | `exemplos/caso1.moq` | `resultado = (4 + 2) * 3;` | válido |
| 2 | `exemplos/caso2.moq` | `preco = custo + custo * lucro / 100 - desconto;` | válido |
| 3 | `exemplos/caso3.moq` | programa de 3 linhas com `mostra` e `mostrador` | válido |
| 4 | `exemplos/caso4.moq` | `preço = 10;` | erro léxico (`ç`) |
| 5 | `exemplos/caso5.moq` | `dobro = valor * 2; # calcula o dobro` | erro léxico (`#`) |
| 6 | `exemplos/caso6.moq` | `media = (nota1 + nota2 / 2;` | erro sintático (falta `)`) |
| 7 | `exemplos/caso7.moq` | `x = 2y + 1;` | erro sintático (`2y`) |

Os casos 6 e 7 passam pelo scanner sem erro: todos os caracteres formam tokens válidos.
O problema está na ordem dos tokens, e isso só seria detectado pelo analisador sintático.

## Estrutura

```
scanner.py      scanner da linguagem Moqueca
exemplos/       casos de teste (.moq)
ast/            ASTs das duas expressões analisadas no relatório (Graphviz)
```
