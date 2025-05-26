import sys
from enum import Enum, auto

# Definição da enumeração para tipos de tokens
class TokenType(Enum):
    T_ENOIS         = auto()  # Token para a palavra reservada "ÉNOIS"
    T_PARTIU        = auto()  # Token para a palavra reservada "PARTIU"
    T_BAGULHOS      = auto()  # Token para a palavra reservada "BAGULHOS"
    T_VIRGULA       = auto()  # Token para o símbolo de vírgula
    T_PONTO_VIRGULA = auto()  # Token para o símbolo de ponto e vírgula
    T_SEPA          = auto()  # Token para a palavra reservada "SEPA"
    T_NAOFOI        = auto()  # Token para a palavra reservada "NÃOFOI"
    T_FIMSEPA       = auto()  # Token para a palavra reservada "FIMSEPA"
    T_MANDAENQUANTO = auto()  # Token para a palavra reservada "MANDAENQUANTO"
    T_PARAMANDA     = auto()  # Token para a palavra reservada "PARAMANDA"
    T_MANDALEMBRAR  = auto()  # Token para a palavra reservada "MANDALEMBRAR"
    T_SETA          = auto()  # Token para o símbolo de atribuição "<-"
    T_ATEALILA      = auto()  # Token para a palavra reservada "ATEALILA"
    T_DESENCANA     = auto()  # Token para a palavra reservada "DESENCANA"
    T_OLHA          = auto()  # Token para a palavra reservada "OLHA"
    T_ABRE_PAR      = auto()  # Token para o símbolo de abertura de parênteses
    T_FECHA_PAR     = auto()  # Token para o símbolo de fechamento de parênteses
    T_FALA          = auto()  # Token para a palavra reservada "FALA"
    T_MAIOR         = auto()  # Token para o operador relacional ">"
    T_MENOR         = auto()  # Token para o operador relacional "<"
    T_MAIOR_IGUAL   = auto()  # Token para o operador relacional ">="
    T_MENOR_IGUAL   = auto()  # Token para o operador relacional "<="
    T_IGUAL         = auto()  # Token para o operador relacional "=="
    T_DIFERENTE     = auto()  # Token para o operador relacional "<>"
    T_MAIS          = auto()  # Token para o operador aritmético "+"
    T_MENOS         = auto()  # Token para o operador aritmético "-"
    T_VEZES         = auto()  # Token para o operador aritmético "*"
    T_DIVIDIDO      = auto()  # Token para o operador aritmético "/"
    T_RESTO         = auto()  # Token para o operador aritmético "%"
    T_ELEVADO       = auto()  # Token para o operador aritmético "**"
    T_NUMERO        = auto()  # Token para números (inteiros ou decimais)
    T_ID            = auto()  # Token para identificadores (nomes de variáveis)
    T_STRING        = auto()  # Token para strings literais
    T_FIM_FONTE     = auto()  # Token para o fim do arquivo fonte
    T_ERRO_LEX      = auto()  # Token para erros léxicos
    T_NULO          = auto()  # Token para valor nulo

# Dicionário de palavras reservadas mapeadas para seus respectivos tipos de token
PALAVRAS_RESERVADAS = {
    "ÉNOIS"        : TokenType.T_ENOIS,
    "PARTIU"       : TokenType.T_PARTIU,
    "BAGULHOS"     : TokenType.T_BAGULHOS,
    "SEPA"         : TokenType.T_SEPA,
    "NÃOFOI"       : TokenType.T_NAOFOI,
    "FIMSEPA"      : TokenType.T_FIMSEPA,
    "MANDAENQUANTO": TokenType.T_MANDAENQUANTO,
    "PARAMANDA"    : TokenType.T_PARAMANDA,
    "MANDALEMBRAR" : TokenType.T_MANDALEMBRAR,
    "ATEALILA"     : TokenType.T_ATEALILA,
    "DESENCANA"    : TokenType.T_DESENCANA,
    "OLHA"         : TokenType.T_OLHA,
    "FALA"         : TokenType.T_FALA,
}

# Dicionário de símbolos de um caractere mapeados para seus respectivos tipos de token
SINGLE_SYMBOLS = {
    ',' : TokenType.T_VIRGULA,
    ';' : TokenType.T_PONTO_VIRGULA,
    '(' : TokenType.T_ABRE_PAR,
    ')' : TokenType.T_FECHA_PAR,
    '+' : TokenType.T_MAIS,
    '-' : TokenType.T_MENOS,
    '*' : TokenType.T_VEZES,
    '/' : TokenType.T_DIVIDIDO,
    '%' : TokenType.T_RESTO,
}

# Dicionário de símbolos de dois caracteres mapeados para seus respectivos tipos de token
DUAL_SYMBOLS = {
    '**' : TokenType.T_ELEVADO,
    '<-' : TokenType.T_SETA,
    '>=' : TokenType.T_MAIOR_IGUAL,
    '<=' : TokenType.T_MENOR_IGUAL,
    '<>' : TokenType.T_DIFERENTE,
    '==' : TokenType.T_IGUAL
}

# Classe que representa um token com tipo, lexema, linha e coluna
class Token:
    def __init__(self, tipo: TokenType, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    # Método para formatar a representação em string do token
    def __str__(self):
        return f"{self.tipo.name} | {self.lexema} | linha {self.linha} | coluna {self.coluna}"

# Classe responsável pela análise léxica do código fonte
class LexicoCria:
    def __init__(self, fonte):
        # Inicializa o analisador léxico com o arquivo fonte
        self.fonte = fonte
        self.linhas = []
        # Lê todas as linhas do arquivo fonte
        with open(fonte, encoding="utf-8") as f:
            self.linhas = f.readlines()
        self.linha = 0  # Linha atual no arquivo
        self.coluna = 0  # Coluna atual na linha
        self.atual = ''  # Caractere atual sendo processado
        self.fim = False  # Indicador de fim do arquivo
        self.tokens = []  # Lista para armazenar os tokens gerados
        self.erro = None  # Armazena mensagem de erro léxico, se houver

    # Avança para o próximo caractere no arquivo fonte
    def avancar(self):
        if self.fim:
            self.atual = ''
            return
        if self.linha >= len(self.linhas):
            self.atual = ''
            self.fim = True
            return
        if self.coluna >= len(self.linhas[self.linha]):
            self.linha += 1
            self.coluna = 0
            if self.linha >= len(self.linhas):
                self.atual = ''
                self.fim = True
                return
        if self.linha < len(self.linhas) and self.coluna < len(self.linhas[self.linha]):
            self.atual = self.linhas[self.linha][self.coluna]
            self.coluna += 1
        else:
            self.atual = ''
            self.fim = True

    # Retorna o próximo caractere sem avançar a posição
    def look(self):
        if self.fim or self.linha >= len(self.linhas):
            return ''
        if self.coluna < len(self.linhas[self.linha]):
            return self.linhas[self.linha][self.coluna]
        return ''

    # Gera o próximo token a partir do código fonte
    def proximo_token(self):
        # Ignora espaços em branco e caracteres vazios
        while not self.fim and (self.atual.isspace() or self.atual == ''):
            self.avancar()

        # Se chegou ao fim do arquivo, retorna token de fim de fonte
        if self.fim:
            return Token(TokenType.T_FIM_FONTE, '<EOF>', self.linha+1, self.coluna+1)

        inicio_linha = self.linha
        inicio_coluna = self.coluna

        # --- SUPORTE A STRING LITERAL ---
        # Processa strings literais delimitadas por aspas
        if self.atual == '"':
            lex = ''
            inicio_linha_str = self.linha
            inicio_coluna_str = self.coluna
            self.avancar()
            while not self.fim and self.atual != '"':
                lex += self.atual
                self.avancar()
            if self.atual == '"':
                self.avancar()
                return Token(TokenType.T_STRING, lex, inicio_linha_str+1, inicio_coluna_str)
            self.erro = f"Erro Léxico: String não fechada (linha {inicio_linha_str+1}, coluna {inicio_coluna_str})"
            return Token(TokenType.T_ERRO_LEX, lex, inicio_linha_str+1, inicio_coluna_str)

        # Identificador ou palavra reservada
        if (self.atual.isalpha() or self.atual in 'ÉÁÍÓÚÃÇÕÊÂÔÀÑ'):
            lex = self.atual
            self.avancar()
            # Continua coletando caracteres válidos para identificadores
            while not self.fim and (self.atual.isalnum() or self.atual == '_' or self.atual in 'ÇÃÕÉÍÓÚÊÂÔÀÑ'):
                lex += self.atual
                self.avancar()
            # Verifica se é uma palavra reservada ou um identificador
            tipo_token = PALAVRAS_RESERVADAS.get(lex.upper(), TokenType.T_ID)
            return Token(tipo_token, lex, inicio_linha+1, inicio_coluna)

        # Número (inteiro ou decimal)
        if self.atual.isdigit():
            lex = self.atual
            self.avancar()
            # Coleta dígitos para números inteiros
            while not self.fim and self.atual.isdigit():
                lex += self.atual
                self.avancar()
            # Verifica se há parte decimal
            if not self.fim and self.atual == '.':
                lex += self.atual
                self.avancar()
                while not self.fim and self.atual.isdigit():
                    lex += self.atual
                    self.avancar()
            return Token(TokenType.T_NUMERO, lex, inicio_linha+1, inicio_coluna)

        # Símbolos de dois caracteres
        lookahead = self.look()
        if self.atual + lookahead in DUAL_SYMBOLS:
            lex = self.atual + lookahead
            tipo_token = DUAL_SYMBOLS[lex]
            self.avancar()
            self.avancar()
            return Token(tipo_token, lex, inicio_linha+1, inicio_coluna)

        # Símbolos de um caractere
        if self.atual in SINGLE_SYMBOLS:
            tipo_token = SINGLE_SYMBOLS[self.atual]
            lex = self.atual
            self.avancar()
            return Token(tipo_token, lex, inicio_linha+1, inicio_coluna)

        # Operadores relacionais unitários e símbolos compostos
        if self.atual == '>':
            self.avancar()
            if self.atual == '=':
                self.avancar()
                return Token(TokenType.T_MAIOR_IGUAL, '>=', inicio_linha+1, inicio_coluna)
            return Token(TokenType.T_MAIOR, '>', inicio_linha+1, inicio_coluna)
        if self.atual == '<':
            self.avancar()
            if self.atual == '-':
                self.avancar()
                return Token(TokenType.T_SETA, '<-', inicio_linha+1, inicio_coluna)
            elif self.atual == '=':
                self.avancar()
                return Token(TokenType.T_MENOR_IGUAL, '<=', inicio_linha+1, inicio_coluna)
            elif self.atual == '>':
                self.avancar()
                return Token(TokenType.T_DIFERENTE, '<>', inicio_linha+1, inicio_coluna)
            return Token(TokenType.T_MENOR, '<', inicio_linha+1, inicio_coluna)
        if self.atual == '=':
            self.avancar()
            if self.atual == '=':
                self.avancar()
                return Token(TokenType.T_IGUAL, '==', inicio_linha+1, inicio_coluna)
            return Token(TokenType.T_IGUAL, '=', inicio_linha+1, inicio_coluna)

        # Potência **
        if self.atual == '*':
            self.avancar()
            if self.atual == '*':
                self.avancar()
                return Token(TokenType.T_ELEVADO, '**', inicio_linha+1, inicio_coluna)
            return Token(TokenType.T_VEZES, '*', inicio_linha+1, inicio_coluna)

        # Caso nenhum padrão seja reconhecido, retorna erro léxico
        erro_lexema = self.atual
        self.avancar()
        self.erro = f"Erro Léxico na linha {inicio_linha+1}, coluna {inicio_coluna}: símbolo inválido: {erro_lexema}"
        return Token(TokenType.T_ERRO_LEX, erro_lexema, inicio_linha+1, inicio_coluna)

    # Executa a análise léxica completa do arquivo fonte
    def analisar(self):
        self.avancar()
        while True:
            token = self.proximo_token()
            self.tokens.append(token)
            print(token)
            # Para quando encontra fim do arquivo ou erro léxico
            if token.tipo == TokenType.T_FIM_FONTE or token.tipo == TokenType.T_ERRO_LEX:
                break
        
        # Salva os tokens gerados em um arquivo de saída
        output_file = self.fonte.rsplit('.', 1)[0] + '.lex'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Análise Léxica - Arquivo: {}\n".format(self.fonte))
                f.write("----------------------------------------\n")
                for token in self.tokens:
                    f.write(str(token) + '\n')
                if self.erro:
                    f.write("----------------------------------------\n")
                    f.write("Erro encontrado: {}\n".format(self.erro))
                else:
                    f.write("----------------------------------------\n")
                    f.write("Análise léxica terminada sem erros.\n")
            print(f"Saída léxica salva em: {output_file}")
        except IOError as e:
            print(f"Erro ao salvar o arquivo {output_file}: {e}")

# Ponto de entrada do programa
if __name__ == '__main__':
    # Verifica se o argumento do arquivo foi fornecido
    if len(sys.argv) != 2:
        print("Uso: python lexico_cria.py <arquivo.cria>")
        sys.exit(1)
    # Cria instância do analisador léxico e executa a análise
    lexico = LexicoCria(sys.argv[1])
    lexico.analisar()