# C.R.I.A - Código Rápido, Inteligente e Autêntico

Bem-vindo ao **C.R.I.A - Código Rápido, Inteligente e Autêntico**, o compilador mais *descolado* do bairro! 😎 Desenvolvido com um toque de humor carioca e muito energético, o C.R.I.A faz análise léxica e sintática de arquivos `.cria` com palavras reservadas tão *maneiras* quanto "ÉNOIS", "PARTIU" e "MANDAENQUANTO". Se você quer um compilador que mistura gírias com precisão técnica, tá no lugar certo, *parça*!

## O que é o C.R.I.A?

O C.R.I.A é um analisador léxico e sintático para a linguagem de programação **C.R.I.A - Código Rápido, Inteligente e Autêntico**, que é fictícia, mas cheia de *estilo*. Ele pega seu código `.cria`, faz uma análise léxica (transforma em tokens) e depois verifica se a sintaxe tá *de boa*. Tudo isso com mensagens de erro que te dizem exatamente onde você pisou na bola (ou no "BAGULHOS").

- **lexico.py**: Faz a análise léxica, transformando seu código em uma lista de tokens. Se encontrar algo estranho, ele grita "Erro Léxico!" e aponta a linha e coluna.
- **sintatico.py**: Pega os tokens gerados e verifica se a estrutura do programa faz sentido. Se não, ele te avisa com um "Erro sintático, meu *consagrado*!"
- **teste.cria**: Um arquivo de exemplo pra você testar o C.R.I.A e sentir o poder das gírias programáveis.

## Como rodar essa *zoeira* organizada?

Pra facilitar sua vida, criamos dois scripts que fazem o trabalho pesado de rodar o C.R.I.A, seja no Linux/Mac ou no Windows. Só precisa passar o arquivo `.cria` que você quer analisar (como o `teste.cria` que já vem no pacote). Vamos ao passo a passo:

### Pré-requisitos
- Python 3.x instalado (porque, né, Python é *vida*).
- Um arquivo `.cria` (tipo o `teste.cria` que tá aí pra você brincar).
- Vontade de programar com *estilo*.

### Passos para executar
1. **Clone ou baixe este repositório.**
   - Se você tá perdido, é só dar um `git clone` ou baixar o ZIP. Simples, né?

2. **Escolha seu sistema operacional e rode o script correspondente:**
   - **Linux/Mac**: Use o `lin_exec.sh`.
     ```bash
     ./lin_exec.sh teste.cria
     ```
   - **Windows**: Use o `win_exec.bat`.
     ```bat
     win_exec.bat teste.cria
     ```

3. **O que acontece?**
   - O script roda primeiro o `lexico.py`, que gera um arquivo `.lex` com os tokens (ex.: `teste.lex`).
   - Depois, o `sintatico.py` usa esse `.lex` pra verificar a sintaxe e cria um arquivo `.syn` com o resultado (ex.: `teste.syn`).
   - Se tudo der certo, você verá mensagens como "Análise léxica terminada sem erros" e "Análise sintática terminada sem erros". Se não, o C.R.I.A vai te contar onde tá o problema (com linha e coluna, porque ele é *educado*).

4. **Cheque os resultados:**
   - Abra o arquivo `.lex` pra ver os tokens gerados.
   - Abra o arquivo `.syn` pra ver se a sintaxe tá *de boa* ou se tem erros pra consertar.

### Exemplo com teste.cria
Temos um arquivo de teste, o `teste.cria`, pronto pra você experimentar. Ele tem um código básico na linguagem C.R.I.A. Só rodar:
```bash
./lin_exec.sh teste.cria  # Linux/Mac
```
ou
```bat
win_exec.bat teste.cria  # Windows
```

E pronto! O C.R.I.A vai analisar o código e te mostrar o que achou. Se der erro, não chora, é só corrigir o código e mandar de novo!

## Estrutura dos arquivos de saída
- **`nome_do_arquivo.lex`**: Lista todos os tokens encontrados, com tipo, lexema, linha e coluna. Se tiver erro léxico, ele aparece aqui.
- **`nome_do_arquivo.syn`**: Mostra o resultado da análise sintática. Se tudo estiver certo, você ganha um "Análise sintática terminada sem erros". Se não, uma lista de erros sintáticos com linha e coluna.

## Dicas pra não se enrolar
- Certifique-se de que o arquivo `.cria` existe e tá no formato certo (palavras reservadas como "ÉNOIS", "PARTIU", etc.).
- Se der erro no script, confira se o Python tá no PATH do seu sistema.
- Quer criar seu próprio `.cria`? Use o `teste.cria` como base e solte a criatividade com "SEPA", "FALA" e "MANDALEMBRAR"!

## Problemas? Manda um *grito*!
Se o C.R.I.A te deixar na mão (o que é raro, porque ele é *brabo*), verifica se:
- O Python tá instalado direitinho.
- O arquivo `.cria` tá no mesmo diretório que os scripts.
- Você passou o nome do arquivo corretamente.

Se ainda assim der *ruim*, é só chamar que a gente tenta te ajudar (ou pelo menos te consola).

## Aviso final
O C.R.I.A é um projeto pra aprender e se divertir. Então, bora programar com *estilo*, soltar um "ÉNOIS" e mandar ver! 🚀