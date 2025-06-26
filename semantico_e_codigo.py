import sys
from enum import Enum, auto

class TokenType(Enum):
    T_ENOIS         = auto()
    T_PARTIU        = auto()
    T_BAGULHOS      = auto()
    T_VIRGULA       = auto()
    T_PONTO_VIRGULA = auto()
    T_SEPA          = auto()
    T_NAOFOI        = auto()
    T_FIMSEPA       = auto()
    T_MANDAENQUANTO = auto()
    T_PARAMANDA     = auto()
    T_MANDALEMBRAR  = auto()
    T_SETA          = auto()
    T_ATEALILA      = auto()
    T_DESENCANA     = auto()
    T_OLHA          = auto()
    T_ABRE_PAR      = auto()
    T_FECHA_PAR     = auto()
    T_FALA          = auto()
    T_MAIOR         = auto()
    T_MENOR         = auto()
    T_MAIOR_IGUAL   = auto()
    T_MENOR_IGUAL   = auto()
    T_IGUAL         = auto()
    T_DIFERENTE     = auto()
    T_MAIS          = auto()
    T_MENOS         = auto()
    T_VEZES         = auto()
    T_DIVIDIDO      = auto()
    T_RESTO         = auto()
    T_ELEVADO       = auto()
    T_NUMERO        = auto()
    T_ID            = auto()
    T_STRING        = auto()
    T_FIM_FONTE     = auto()
    T_ERRO_LEX      = auto()
    T_NULO          = auto()

class Token:
    def __init__(self, tipo: TokenType, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        return f"{self.tipo.name} | {self.lexema} | linha {self.linha} | coluna {self.coluna}"

class ErroSemanticoException(Exception):
    pass

class ErroSintaticoException(Exception):
    pass

class ErroLexicoException(Exception):
    pass

class NodoPilhaSemantica:
    def __init__(self, codigo, tipo):
        self.codigo = codigo
        self.tipo = tipo
    
    def getCodigo(self):
        return self.codigo
    
    def getCodigoMinusculo(self):
        return self.codigo.lower()
    
    def getTipo(self):
        return self.tipo

class PilhaSemantica:
    def __init__(self):
        self.pilha = []
    
    def push(self, codigo, tipo):
        self.pilha.append(NodoPilhaSemantica(codigo, tipo))
    
    def pop(self):
        if self.pilha:
            return self.pilha.pop()
        return None
    
    def isEmpty(self):
        return len(self.pilha) == 0

class SemanticoCria:
    def __init__(self, arquivo_lex):
        self.tokens = []
        self.erros = []
        self.posicao = 0
        self.arquivo_lex = arquivo_lex
        self.tabela_simbolos = {}
        self.pilha_semantica = PilhaSemantica()
        self.codigo_python = []
        self.nivel_identacao = 0
        self.ultimo_lexema = ""
        self.linha_atual = 1
        self.carregar_tokens()

    def carregar_tokens(self):
        try:
            with open(self.arquivo_lex, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                for linha in linhas:
                    linha = linha.strip()
                    if linha and not linha.startswith(('Análise Léxica', '---', 'Erro', 'terminada')):
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

    def token_atual(self):
        return self.tokens[self.posicao] if self.posicao < len(self.tokens) else Token(TokenType.T_FIM_FONTE, '<EOF>', 1, 1)

    def avancar(self):
        if self.posicao < len(self.tokens):
            self.ultimo_lexema = self.tokens[self.posicao].lexema
            self.linha_atual = self.tokens[self.posicao].linha
        self.posicao += 1

    def espera(self, tipo_esperado):
        token = self.token_atual()
        if token.tipo == tipo_esperado:
            self.avancar()
            return True
        self.erros.append(f"Erro sintático na linha {token.linha}, coluna {token.coluna}: "
                        f"Esperado {tipo_esperado.name}, encontrado {token.tipo.name} ({token.lexema})")
        return False

    def tabulacao(self, qtd):
        return "    " * qtd

    def insere_na_tabela_simbolos(self, lexema):
        if lexema in self.tabela_simbolos:
            raise ErroSemanticoException(f"Variável {lexema} já declarada! linha: {self.linha_atual}")
        else:
            self.tabela_simbolos[lexema] = 0

    def verifica_se_existe_na_tabela_simbolos(self, lexema):
        if lexema not in self.tabela_simbolos:
            raise ErroSemanticoException(f"Variável {lexema} não está declarada! linha: {self.linha_atual}")
        return True

    def regra_semantica(self, numero_regra):
        print(f"Regra Semântica {numero_regra}")
        
        if numero_regra == 0:  # Início do programa
            self.codigo_python.append("def main():")
            self.nivel_identacao = 1
            self.codigo_python.append(self.tabulacao(self.nivel_identacao) + "# Compilador C.R.I.A")
            self.codigo_python.append("")
            # Inicializar variáveis declaradas
            for var in self.tabela_simbolos:
                self.codigo_python.append(self.tabulacao(self.nivel_identacao) + f"{var} = 0")
            if self.tabela_simbolos:
                self.codigo_python.append("")
            
        elif numero_regra == 1:  # Fim do programa
            # Verifica se há pelo menos um comando no bloco principal
            if not any("pass" in linha or 
                      any(cmd in linha for cmd in ["print", "input", "=", "if", "for", "while"]) 
                      for linha in self.codigo_python[-5:]):
                self.codigo_python.append(self.tabulacao(self.nivel_identacao) + "pass")
            self.nivel_identacao = 0
            self.codigo_python.append("")
            self.codigo_python.append("if __name__ == '__main__':")
            self.codigo_python.append(self.tabulacao(1) + "main()")
            
        elif numero_regra == 2:  # Declaração de variável
            self.insere_na_tabela_simbolos(self.ultimo_lexema)
            
        elif numero_regra == 3:  # Atribuição
            nodo_2 = self.pilha_semantica.pop()  # expressão
            nodo_1 = self.pilha_semantica.pop()  # variável
            self.codigo_python.append(self.tabulacao(self.nivel_identacao) + 
                                    f"{nodo_1.getCodigoMinusculo()} = {nodo_2.getCodigoMinusculo()}")
            
        elif numero_regra == 4:  # Uso de variável
            if self.verifica_se_existe_na_tabela_simbolos(self.ultimo_lexema):
                self.pilha_semantica.push(self.ultimo_lexema, 4)
                
        elif numero_regra == 5:  # Soma
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} + {nodo_2.getCodigoMinusculo()}", 5)
            
        elif numero_regra == 6:  # Subtração
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} - {nodo_2.getCodigoMinusculo()}", 6)
            
        elif numero_regra == 7:  # Multiplicação
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} * {nodo_2.getCodigoMinusculo()}", 7)
            
        elif numero_regra == 8:  # Divisão
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} // {nodo_2.getCodigoMinusculo()}", 8)
            
        elif numero_regra == 9:  # Resto
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} % {nodo_2.getCodigoMinusculo()}", 9)
            
        elif numero_regra == 10:  # Potência
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} ** {nodo_2.getCodigoMinusculo()}", 10)
            
        elif numero_regra == 11:  # Variável em expressão
            if self.verifica_se_existe_na_tabela_simbolos(self.ultimo_lexema):
                self.pilha_semantica.push(self.ultimo_lexema, 11)
                
        elif numero_regra == 12:  # Número
            self.pilha_semantica.push(self.ultimo_lexema, 12)
            
        elif numero_regra == 13:  # Parênteses
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"({nodo_1.getCodigoMinusculo()})", 13)
            
        elif numero_regra == 14:  # Comando LER (OLHA)
            nodo_1 = self.pilha_semantica.pop()
            self.codigo_python.append(self.tabulacao(self.nivel_identacao) + 
                                    f"{nodo_1.getCodigoMinusculo()} = int(input('Informe a variável {nodo_1.getCodigoMinusculo()}: '))")
            
        elif numero_regra == 15:  # Início ENQUANTO (MANDAENQUANTO)
            nodo_1 = self.pilha_semantica.pop()
            self.codigo_python.append(self.tabulacao(self.nivel_identacao) + 
                                    f"while {nodo_1.getCodigoMinusculo()}:")
            self.nivel_identacao += 1
            
        elif numero_regra == 16:  # Fim de bloco
            # Verifica se o último bloco não está vazio
            if (len(self.codigo_python) > 0 and 
                self.codigo_python[-1].strip().endswith(":")):
                self.codigo_python.append(self.tabulacao(self.nivel_identacao) + "pass")
            if self.nivel_identacao > 1:
                self.nivel_identacao -= 1
            
        elif numero_regra == 17:  # Início SE (SEPA)
            nodo_1 = self.pilha_semantica.pop()
            self.codigo_python.append(self.tabulacao(self.nivel_identacao) + 
                                    f"if {nodo_1.getCodigoMinusculo()}:")
            self.nivel_identacao += 1
            
        elif numero_regra == 18:  # SENÃO (NÃOFOI)
            # Primeiro diminui a identação para sair do bloco if
            self.nivel_identacao -= 1
            # Adiciona o else com a identação correta
            self.codigo_python.append(self.tabulacao(self.nivel_identacao) + "else:")
            # Aumenta a identação para o bloco do else
            self.nivel_identacao += 1
            
        elif numero_regra == 19:  # Maior que
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} > {nodo_2.getCodigoMinusculo()}", 19)
            
        elif numero_regra == 20:  # Menor que
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} < {nodo_2.getCodigoMinusculo()}", 20)
            
        elif numero_regra == 21:  # Maior ou igual
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} >= {nodo_2.getCodigoMinusculo()}", 21)
            
        elif numero_regra == 22:  # Menor ou igual
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} <= {nodo_2.getCodigoMinusculo()}", 22)
            
        elif numero_regra == 23:  # Igual
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} == {nodo_2.getCodigoMinusculo()}", 23)
            
        elif numero_regra == 24:  # Diferente
            nodo_2 = self.pilha_semantica.pop()
            nodo_1 = self.pilha_semantica.pop()
            self.pilha_semantica.push(f"{nodo_1.getCodigoMinusculo()} != {nodo_2.getCodigoMinusculo()}", 24)
            
        elif numero_regra == 25:  # Comando ESCREVER (FALA)
            nodo_1 = self.pilha_semantica.pop()
            # Para strings, usar o código original sem conversão para minúsculo
            if nodo_1.getTipo() == 12 and '"' in nodo_1.getCodigo():
                self.codigo_python.append(self.tabulacao(self.nivel_identacao) + 
                                        f"print({nodo_1.getCodigo()})")
            else:
                self.codigo_python.append(self.tabulacao(self.nivel_identacao) + 
                                        f"print({nodo_1.getCodigoMinusculo()})")
            
        elif numero_regra == 30:  # Comando PARA (MANDALEMBRAR)
            nodo_3 = self.pilha_semantica.pop()  # incremento
            nodo_2 = self.pilha_semantica.pop()  # condição
            nodo_1 = self.pilha_semantica.pop()  # valor inicial
            nodo_0 = self.pilha_semantica.pop()  # variável
            
            # Extrai os valores da condição (var <= limite)
            condicao_str = nodo_2.getCodigoMinusculo()
            if "<=" in condicao_str:
                limite = condicao_str.split("<=")[1].strip()
            elif "<" in condicao_str:
                limite = condicao_str.split("<")[1].strip()
            else:
                limite = "10"  # valor padrão
                
            self.codigo_python.append(self.tabulacao(self.nivel_identacao) + 
                                    f"for {nodo_0.getCodigoMinusculo()} in range({nodo_1.getCodigoMinusculo()}, {limite} + 1):")
            self.nivel_identacao += 1

    def programa(self):
        if not self.espera(TokenType.T_ENOIS):
            return False
        # Primeiro processa as declarações para preencher a tabela de símbolos
        if not self.declaracoes():
            return False
        # Depois gera o código inicial com as variáveis já declaradas
        self.regra_semantica(0)
        if not self.bloco():
            return False
        if not self.espera(TokenType.T_PARTIU):
            return False
        self.regra_semantica(1)
        if self.token_atual().tipo != TokenType.T_FIM_FONTE:
            self.erros.append(f"Erro sintático na linha {self.token_atual().linha}, coluna {self.token_atual().coluna}: "
                            f"Esperado fim do arquivo, encontrado {self.token_atual().tipo.name}")
            return False
        return True

    def declaracoes(self):
        if self.token_atual().tipo == TokenType.T_BAGULHOS:
            self.avancar()
            if not self.lista_variaveis():
                return False
            if not self.espera(TokenType.T_PONTO_VIRGULA):
                return False
        return True

    def lista_variaveis(self):
        if not self.espera(TokenType.T_ID):
            return False
        self.regra_semantica(2)
        while self.token_atual().tipo == TokenType.T_VIRGULA:
            self.avancar()
            if not self.espera(TokenType.T_ID):
                return False
            self.regra_semantica(2)
        return True

    def bloco(self):
        tem_comandos = False
        while self.token_atual().tipo in {TokenType.T_ID, TokenType.T_SEPA, TokenType.T_MANDAENQUANTO,
                                        TokenType.T_MANDALEMBRAR, TokenType.T_OLHA, TokenType.T_FALA}:
            if not self.comando():
                return False
            tem_comandos = True
        
        # Se não houver comandos no bloco e estivermos dentro de uma estrutura de controle, adiciona pass
        if not tem_comandos and self.nivel_identacao > 1:
            self.codigo_python.append(self.tabulacao(self.nivel_identacao) + "pass")
        
        return True

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

    def comando_atribuicao(self):
        if not self.espera(TokenType.T_ID):
            return False
        self.regra_semantica(4)
        if not self.espera(TokenType.T_SETA):
            return False
        if not self.expressao():
            return False
        self.regra_semantica(3)
        if not self.espera(TokenType.T_PONTO_VIRGULA):
            return False
        return True

    def comando_se(self):
        if not self.espera(TokenType.T_SEPA):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if not self.condicao():
            return False
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        self.regra_semantica(17)  # Início do if
        if not self.bloco():
            return False
        
        if self.token_atual().tipo == TokenType.T_NAOFOI:
            self.avancar()
            self.regra_semantica(18)  # Início do else
            if not self.bloco():
                return False
            self.regra_semantica(16)  # Fim do else
        else:
            self.regra_semantica(16)  # Fim do if sem else
            
        if not self.espera(TokenType.T_FIMSEPA):
            return False
        return True

    def comando_enquanto(self):
        if not self.espera(TokenType.T_MANDAENQUANTO):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if not self.condicao():
            return False
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        self.regra_semantica(15)
        if not self.bloco():
            return False
        self.regra_semantica(16)
        if not self.espera(TokenType.T_PARAMANDA):
            return False
        return True

    def comando_para(self):
        if not self.espera(TokenType.T_MANDALEMBRAR):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if not self.espera(TokenType.T_ID):
            return False
        self.regra_semantica(4)
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
        self.regra_semantica(30)
        if not self.bloco():
            return False
        self.regra_semantica(16)
        if not self.espera(TokenType.T_DESENCANA):
            return False
        return True

    def comando_ler(self):
        if not self.espera(TokenType.T_OLHA):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if not self.espera(TokenType.T_ID):
            return False
        self.regra_semantica(4)
        self.regra_semantica(14)
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        if not self.espera(TokenType.T_PONTO_VIRGULA):
            return False
        return True

    def comando_escrever(self):
        if not self.espera(TokenType.T_FALA):
            return False
        if not self.espera(TokenType.T_ABRE_PAR):
            return False
        if self.token_atual().tipo == TokenType.T_STRING:
            # Manter o texto original da string sem conversão para minúsculo
            self.pilha_semantica.push(f'"{self.token_atual().lexema}"', 12)
            self.avancar()
        else:
            if not self.expressao():
                return False
        self.regra_semantica(25)
        if not self.espera(TokenType.T_FECHA_PAR):
            return False
        if not self.espera(TokenType.T_PONTO_VIRGULA):
            return False
        return True

    def condicao(self):
        if not self.expressao():
            return False
        if self.token_atual().tipo not in {TokenType.T_MAIOR, TokenType.T_MENOR, TokenType.T_MAIOR_IGUAL,
                                        TokenType.T_MENOR_IGUAL, TokenType.T_IGUAL, TokenType.T_DIFERENTE}:
            self.erros.append(f"Erro sintático na linha {self.token_atual().linha}, coluna {self.token_atual().coluna}: "
                            f"Esperado operador relacional, encontrado {self.token_atual().tipo.name}")
            return False
        
        op = self.token_atual().tipo
        self.avancar()
        if not self.expressao():
            return False
            
        if op == TokenType.T_MAIOR:
            self.regra_semantica(19)
        elif op == TokenType.T_MENOR:
            self.regra_semantica(20)
        elif op == TokenType.T_MAIOR_IGUAL:
            self.regra_semantica(21)
        elif op == TokenType.T_MENOR_IGUAL:
            self.regra_semantica(22)
        elif op == TokenType.T_IGUAL:
            self.regra_semantica(23)
        elif op == TokenType.T_DIFERENTE:
            self.regra_semantica(24)
            
        return True

    def expressao(self):
        if not self.termo():
            return False
        while self.token_atual().tipo in {TokenType.T_MAIS, TokenType.T_MENOS}:
            op = self.token_atual().tipo
            self.avancar()
            if not self.termo():
                return False
            if op == TokenType.T_MAIS:
                self.regra_semantica(5)
            elif op == TokenType.T_MENOS:
                self.regra_semantica(6)
        return True

    def termo(self):
        if not self.fator():
            return False
        while self.token_atual().tipo in {TokenType.T_VEZES, TokenType.T_DIVIDIDO, TokenType.T_RESTO}:
            op = self.token_atual().tipo
            self.avancar()
            if not self.fator():
                return False
            if op == TokenType.T_VEZES:
                self.regra_semantica(7)
            elif op == TokenType.T_DIVIDIDO:
                self.regra_semantica(8)
            elif op == TokenType.T_RESTO:
                self.regra_semantica(9)
        return True

    def fator(self):
        if self.token_atual().tipo == TokenType.T_MENOS:
            self.avancar()
            if not self.fator():
                return False
        else:
            if not self.base():
                return False
            while self.token_atual().tipo == TokenType.T_ELEVADO:
                self.avancar()
                if not self.base():
                    return False
                self.regra_semantica(10)
        return True

    def base(self):
        token = self.token_atual()
        if token.tipo == TokenType.T_ID:
            self.avancar()
            self.regra_semantica(11)
            return True
        elif token.tipo == TokenType.T_NUMERO:
            self.avancar()
            self.regra_semantica(12)
            return True
        elif token.tipo == TokenType.T_ABRE_PAR:
            self.avancar()
            if not self.expressao():
                return False
            if not self.espera(TokenType.T_FECHA_PAR):
                return False
            self.regra_semantica(13)
            return True
        else:
            self.erros.append(f"Erro sintático na linha {token.linha}, coluna {token.coluna}: "
                            f"Esperado número, identificador ou '(', encontrado {token.tipo.name}")
            return False

    def salvar_resultado(self):
        output_file = self.arquivo_lex.rsplit('.', 1)[0] + '.py'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                if not self.erros:
                    for linha in self.codigo_python:
                        f.write(linha + '\n')
                    print(f"Código Python gerado com sucesso em: {output_file}")
                else:
                    f.write("# Erros semânticos encontrados:\n")
                    for erro in self.erros:
                        f.write(f"# {erro}\n")
                    print(f"Erros semânticos salvos em: {output_file}")
        except IOError as e:
            print(f"Erro ao salvar o arquivo {output_file}: {e}")

    def analisar(self):
        try:
            if self.erros:  # Errors from loading tokens
                self.salvar_resultado()
                return
            if self.programa():
                print("Análise semântica terminada sem erros.")
            else:
                print("Erros semânticos encontrados.")
            self.salvar_resultado()
        except ErroSemanticoException as e:
            self.erros.append(str(e))
            print(f"Erro semântico: {e}")
            self.salvar_resultado()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python semantico.py <arquivo.lex>")
        sys.exit(1)
    semantico = SemanticoCria(sys.argv[1])
    semantico.analisar()