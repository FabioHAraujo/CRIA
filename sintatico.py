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

# Classe responsável pela análise sintática do arquivo léxico
class SintaticoCria:
    def __init__(self, arquivo_lex):
        # Inicializa o analisador sintático com o arquivo de tokens
        self.tokens = []
        self.erros = []  # Lista para armazenar erros sintáticos
        self.posicao = 0  # Posição atual na lista de tokens
        self.arquivo_lex = arquivo_lex
        self.carregar_tokens()  # Carrega os tokens do arquivo

    # Carrega os tokens do arquivo gerado pela análise léxica
    def carregar_tokens(self):
        try:
            with open(self.arquivo_lex, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                for linha in linhas:
                    linha = linha.strip()
                    if linha and not linha.startswith(('Análise Léxica', '---', 'Erro encontrado')):
                        try:
                            partes = linha.split(' | ')
                            if len(partes) != 4:
                                continue
                            tipo_str, lexema, linha_str, coluna_str = partes
                            tipo = TokenType[tipo_str]
                            linha_num = int(linha_str.split()[-1])
                            coluna_num = int(coluna_str.split()[-1])
                            self.tokens.append(Token(tipo, lexema, linha_num, coluna_num))
                        except (ValueError, KeyError):
                            continue
        except IOError as e:
            self.erros.append(f"Erro ao ler o arquivo {self.arquivo_lex}: {e}")
            self.tokens.append(Token(TokenType.T_FIM_FONTE, '<EOF>', 1, 1))

    # Retorna o token atual na análise
    def token_atual(self):
        return self.tokens[self.posicao] if self.posicao < len(self.tokens) else Token(TokenType.T_FIM_FONTE, '<EOF>', 1, 1)

    # Avança para o próximo token
    def avancar(self):
        self.posicao += 1

    # Verifica se o token atual é do tipo esperado
    def espera(self, tipo_esperado):
        token = self.token_atual()
        if token.tipo == tipo_esperado:
            self.avancar()
            return True
        self.erros.append(f"Erro sintático na linha {token.linha}, coluna {token.coluna}: "
                        f"Esperado {tipo_esperado.name}, encontrado {token.tipo.name} ({token.lexema})")
        return False

    # Verifica a estrutura geral do programa
    def programa(self):
        if not self.espera(TokenType.T_ENOIS):
            return False
        if not self.declaracoes():
            return False
        if not self.bloco():
            return False
        if not self.espera(TokenType.T_PARTIU):
            return False
        if self.token_atual().tipo != TokenType.T_FIM_FONTE:
            self.erros.append(f"Erro sintático na linha {self.token_atual().linha}, coluna {self.token_atual().coluna}: "
                            f"Esperado fim do arquivo, encontrado {self.token_atual().tipo.name}")
            return False
        return True

    # Verifica a seção de declarações de variáveis
    def declaracoes(self):
        if self.token_atual().tipo == TokenType.T_BAGULHOS:
            self.avancar()
            if not self.lista_variaveis():
                return False
            if not self.espera(TokenType.T_PONTO_VIRGULA):
                return False
        return True

    # Verifica a lista de variáveis declaradas
    def lista_variaveis(self):
        if not self.espera(TokenType.T_ID):
            return False
        while self.token_atual().tipo == TokenType.T_VIRGULA:
            self.avancar()
            if not self.espera(TokenType.T_ID):
                return False
        return True

    # Verifica um bloco de comandos
    def bloco(self):
        while self.token_atual().tipo in {TokenType.T_ID, TokenType.T_SEPA, TokenType.T_MANDAENQUANTO,
                                        TokenType.T_MANDALEMBRAR, TokenType.T_OLHA, TokenType.T_FALA}:
            if not self.comando():
                return False
        return True

    # Identifica e verifica o tipo de comando
    def comando(self):
        token = self.token_atual()
        if token.tipo == TokenType.T_ID:
            return self.comando_atribuicao()
        elif token.tipo == TokenType.T_SEPA:
            return self.comando_se()
        elif token.tipo == TokenType.T_MANDAENQUANTO:
            return self.comando_enquanto()
        elif token.tipo == TokenType.T_MANDALEMBRAR:
            return self.comando_para()
        elif token.tipo == TokenType.T_OLHA:
            return self.comando_ler()
        elif token.tipo == TokenType.T_FALA:
            return self.comando_escrever()
        else:
            self.erros.append(f"Erro sintático na linha {token.linha}, coluna {token.coluna}: "
                            f"Comando inválido: {token.tipo.name} ({token.lexema})")
            return False

    # Verifica o comando de atribuição
    def comando_atribuicao(self):
        if not self.espera(TokenType.T_ID):
            return False
        if not self.espera(TokenType.T_SETA):
            return False
        if not self.expressao():
            return False
        if not self.espera(TokenType.T_PONTO_VIRGULA):
            return False
        return True

    # Verifica o comando de controle "se"
    def comando_se(self):
        if not self.espera(TokenType.T_SEPA):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if not self.condicao():
            return False
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        if not self.bloco():
            return False
        if self.token_atual().tipo == TokenType.T_NAOFOI:
            self.avancar()
            if not self.bloco():
                return False
        if not self.espera(TokenType.T_FIMSEPA):
            return False
        return True

    # Verifica o comando de repetição "enquanto"
    def comando_enquanto(self):
        if not self.espera(TokenType.T_MANDAENQUANTO):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if not self.condicao():
            return False
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        if not self.bloco():
            return False
        if not self.espera(TokenType.T_PARAMANDA):
            return False
        return True

    # Verifica o comando de repetição "para"
    def comando_para(self):
        if not self.espera(TokenType.T_MANDALEMBRAR):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if not self.espera(TokenType.T_ID):
            return False
        if not self.espera(TokenType.T_SETA):
            return False
        if not self.expressao():
            return False
        if not self.espera(TokenType.T_PONTO_VIRGULA):
            return False
        if not self.condicao():
            return False
        if not self.espera(TokenType.T_PONTO_VIRGULA):
            return False
        if not self.espera(TokenType.T_ID):
            return False
        if not self.espera(TokenType.T_SETA):
            return False
        if not self.expressao():
            return False
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        if not self.bloco():
            return False
        if not self.espera(TokenType.T_DESENCANA):
            return False
        return True

    # Verifica o comando de leitura
    def comando_ler(self):
        if not self.espera(TokenType.T_OLHA):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if not self.espera(TokenType.T_ID):
            return False
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        if not self.espera(TokenType.T_PONTO_VIRGULA):
            return False
        return True

    # Verifica o comando de escrita
    def comando_escrever(self):
        if not self.espera(TokenType.T_FALA):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if self.token_atual().tipo == TokenType.T_STRING:
            self.avancar()
        else:
            if not self.expressao():
                return False
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        if not self.espera(TokenType.T_PONTO_VIRGULA):
            return False
        return True

    # Verifica uma condição (expressão relacional)
    def condicao(self):
        if not self.expressao():
            return False
        if self.token_atual().tipo not in {TokenType.T_MAIOR, TokenType.T_MENOR, TokenType.T_MAIOR_IGUAL,
                                        TokenType.T_MENOR_IGUAL, TokenType.T_IGUAL, TokenType.T_DIFERENTE}:
            self.erros.append(f"Erro sintático na linha {self.token_atual().linha}, coluna {self.token_atual().coluna}: "
                            f"Esperado operador relacional, encontrado {self.token_atual().tipo.name}")
            return False
        self.avancar()
        if not self.expressao():
            return False
        return True

    # Verifica uma expressão aritmética
    def expressao(self):
        if not self.termo():
            return False
        while self.token_atual().tipo in {TokenType.T_MAIS, TokenType.T_MENOS, TokenType.T_VEZES,
                                        TokenType.T_DIVIDIDO, TokenType.T_RESTO, TokenType.T_ELEVADO}:
            self.avancar()
            if not self.expressao():
                return False
        return True

    # Verifica um termo em uma expressão
    def termo(self):
        token = self.token_atual()
        if token.tipo == TokenType.T_NUMERO or token.tipo == TokenType.T_ID:
            self.avancar()
            return True
        elif token.tipo == TokenType.T_ABRE_PAR:
            self.avancar()
            if not self.expressao():
                return False
            if not self.espera(TokenType.T_FECHA_PAR):
                return False
            return True
        else:
            self.erros.append(f"Erro sintático na linha {token.linha}, coluna {token.coluna}: "
                            f"Esperado número, identificador ou '(', encontrado {token.tipo.name}")
            return False

    # Salva o resultado da análise sintática em um arquivo
    def salvar_resultado(self):
        output_file = self.arquivo_lex.rsplit('.', 1)[0] + '.syn'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Análise Sintática - Arquivo: {self.arquivo_lex}\n")
                f.write("----------------------------------------\n")
                if not self.erros:
                    f.write("Análise sintática terminada sem erros.\n")
                else:
                    f.write("Erros sintáticos encontrados:\n")
                    for erro in self.erros:
                        f.write(f"{erro}\n")
                f.write("----------------------------------------\n")
            print(f"Saída sintática salva em: {output_file}")
        except IOError as e:
            print(f"Erro ao salvar o arquivo {output_file}: {e}")

    # Executa a análise sintática completa
    def analisar(self):
        if self.erros:  # Verifica erros ao carregar tokens
            self.salvar_resultado()
            return
        if self.programa():
            print("Análise sintática terminada sem erros.")
        else:
            print("Erros sintáticos encontrados.")
        self.salvar_resultado()

# Ponto de entrada do programa
if __name__ == '__main__':
    # Verifica se o argumento do arquivo foi fornecido
    if len(sys.argv) != 2:
        print("Uso: python sintatico_cria.py <arquivo.lex>")
        sys.exit(1)
    # Cria instância do analisador sintático e executa a análise
    sintatico = SintaticoCria(sys.argv[1])
    sintatico.analisar()