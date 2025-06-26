@echo off

:: Verifica se foi passado um argumento
if "%1"=="" (
    echo Uso: win_exec.bat arquivo.cria
    exit /b 1
)

:: Verifica se o arquivo .cria existe
if not exist "%1" (
    echo Erro: Arquivo %1 nao encontrado!
    exit /b 1
)

:: Roda o analisador léxico
python lexico.py "%1"

:: Verifica se o arquivo .lex foi gerado
set "LEX_FILE=%~n1.lex"
if not exist "%LEX_FILE%" (
    echo Erro: Arquivo %LEX_FILE% nao foi gerado!
    exit /b 1
)

:: Roda o analisador sintático
python sintatico.py "%LEX_FILE%"

:: Verifica se o arquivo .syn foi gerado
set "SYN_FILE=%~n1.syn"
if not exist "%SYN_FILE%" (
    echo Erro: Arquivo %SYN_FILE% nao foi gerado!
    exit /b 1
)

:: Roda o analisador semântico e gerador de código
python semantico_e_codigo.py "%LEX_FILE%"