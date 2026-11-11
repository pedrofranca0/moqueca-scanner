"""
Scanner (analisador léxico) da mini-linguagem Moqueca.

Disciplina: Linguagens Formais e Compiladores - Multivix Vitória
Avaliação Processual - 2º bimestre de 2026

O scanner lê o código-fonte caractere por caractere e agrupa os caracteres
em tokens (tipo + lexema). Espaços, tabulações e quebras de linha são
ignorados. Um caractere que não pertence a nenhum padrão é informado como
erro léxico e a leitura continua a partir do caractere seguinte.

Como usar:
    python scanner.py "resultado = (4 + 2) * 3;"   analisa a linha informada
    python scanner.py -f exemplos/caso3.moq         analisa um arquivo .moq
    python scanner.py                               pede uma linha pelo teclado
"""

import sys
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Tabelas da linguagem
# ---------------------------------------------------------------------------

# Palavras reservadas. Elas têm o mesmo formato de um identificador, mas
# recebem um tipo próprio (têm prioridade sobre IDENTIFICADOR).
PALAVRAS_RESERVADAS = {
    "mostra": "PALAVRA_RESERVADA",
}

# Tokens formados por um único caractere (operadores e pontuação).
SIMBOLOS = {
    "=": "ATRIBUICAO",
    "+": "OP_SOMA",
    "-": "OP_SUB",
    "*": "OP_MULT",
    "/": "OP_DIV",
    "(": "ABRE_PAR",
    ")": "FECHA_PAR",
    ";": "PONTO_VIRGULA",
}

# Caracteres que o scanner ignora (a quebra de linha é tratada à parte).
ESPACOS = " \t\r"


@dataclass
class Token:
    tipo: str     # categoria do token, por exemplo IDENTIFICADOR
    lexema: str   # texto exato encontrado no código-fonte
    linha: int    # linha onde o lexema começa
    coluna: int   # coluna onde o lexema começa


@dataclass
class ErroLexico:
    caractere: str
    linha: int
    coluna: int

    def __str__(self):
        return (f"linha {self.linha}, coluna {self.coluna}: "
                f"caractere desconhecido '{self.caractere}'")


def eh_letra(c):
    """Letras sem acento (a-z, A-Z) e o sublinhado."""
    return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_"


def eh_digito(c):
    return "0" <= c <= "9"


def eh_alfanumerico(c):
    """Caracteres que podem continuar um identificador."""
    return eh_letra(c) or eh_digito(c)


# ---------------------------------------------------------------------------
# Análise léxica
# ---------------------------------------------------------------------------

def analisar(codigo):
    """Percorre o código e devolve uma lista com Tokens e ErrosLexicos,
    na mesma ordem em que foram encontrados."""
    saida = []
    i = 0              # posição atual no texto
    fim = len(codigo)
    linha = 1
    coluna = 1

    while i < fim:
        c = codigo[i]

        # Espaços e tabulações: só avançam a coluna.
        if c in ESPACOS:
            i += 1
            coluna += 1
            continue

        # Quebra de linha: próxima linha, volta para a coluna 1.
        if c == "\n":
            i += 1
            linha += 1
            coluna = 1
            continue

        inicio = i   # posição onde o lexema começa

        if eh_letra(c):
            # IDENTIFICADOR ou PALAVRA_RESERVADA: [a-zA-Z_][a-zA-Z0-9_]*
            # Lê o maior lexema possível (regra do maior casamento).
            while i < fim and eh_alfanumerico(codigo[i]):
                i += 1
            lexema = codigo[inicio:i]
            # Se o lexema estiver na tabela de palavras reservadas, ela vence.
            tipo = PALAVRAS_RESERVADAS.get(lexema, "IDENTIFICADOR")
            saida.append(Token(tipo, lexema, linha, coluna))

        elif eh_digito(c):
            # NUMERO: [0-9]+(\.[0-9]+)?
            while i < fim and eh_digito(codigo[i]):
                i += 1
            # O ponto só entra no número se houver um dígito depois dele.
            if i + 1 < fim and codigo[i] == "." and eh_digito(codigo[i + 1]):
                i += 1
                while i < fim and eh_digito(codigo[i]):
                    i += 1
            saida.append(Token("NUMERO", codigo[inicio:i], linha, coluna))

        elif c in SIMBOLOS:
            # Operadores e pontuação: um caractere só.
            i += 1
            saida.append(Token(SIMBOLOS[c], c, linha, coluna))

        else:
            # Nenhum padrão reconhece o caractere: erro léxico.
            # Recuperação simples: descarta o caractere e segue em frente.
            i += 1
            saida.append(ErroLexico(c, linha, coluna))

        coluna += i - inicio

    return saida


# ---------------------------------------------------------------------------
# Entrada e saída
# ---------------------------------------------------------------------------

def imprimir_resultado(codigo, saida):
    print("=== Scanner da linguagem Moqueca ===")
    print("Código analisado:")
    for numero, texto in enumerate(codigo.splitlines(), start=1):
        print(f"  {numero:>2} | {texto}")
    print()
    print(f"  {'#':>3}  {'LIN:COL':<8} {'TIPO':<18} LEXEMA")
    print(f"  {'-' * 3}  {'-' * 8} {'-' * 18} {'-' * 12}")

    qtd_tokens = 0
    erros = []
    for item in saida:
        posicao = f"{item.linha}:{item.coluna}"
        if isinstance(item, Token):
            qtd_tokens += 1
            print(f"  {qtd_tokens:>3}  {posicao:<8} "
                  f"{item.tipo:<18} {item.lexema}")
        else:
            erros.append(item)
            print(f"  {'!!':>3}  {posicao:<8} {'ERRO LÉXICO':<18} "
                  f"{item.caractere}   <- caractere desconhecido")

    print()
    print(f"Resumo: {qtd_tokens} token(s) reconhecido(s), "
          f"{len(erros)} erro(s) léxico(s).")
    for erro in erros:
        print(f"  Erro léxico na {erro}")


def ler_entrada(argumentos):
    """Decide de onde vem o código: argumento, arquivo (-f) ou teclado."""
    if not argumentos:
        return input("Digite uma linha de código Moqueca: ")

    if argumentos[0] in ("-f", "--arquivo"):
        if len(argumentos) < 2:
            print("Informe o nome do arquivo depois de -f.")
            sys.exit(2)
        try:
            # utf-8-sig ignora o BOM que alguns editores do Windows colocam
            with open(argumentos[1], encoding="utf-8-sig") as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {argumentos[1]}")
            sys.exit(2)

    return " ".join(argumentos)


def main():
    codigo = ler_entrada(sys.argv[1:])
    saida = analisar(codigo)
    imprimir_resultado(codigo, saida)
    # Termina com código 1 se houve erro léxico (ajuda a automatizar testes).
    houve_erro = any(isinstance(item, ErroLexico) for item in saida)
    sys.exit(1 if houve_erro else 0)


if __name__ == "__main__":
    main()
