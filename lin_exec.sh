#!/bin/bash

# Verifica se foi passado um argumento
if [ $# -ne 1 ]; then
    echo "Uso: ./lin_exec.sh <arquivo.cria>"
    exit 1
fi

# Verifica se o arquivo .cria existe
if [ ! -f "$1" ]; then
    echo "Erro: Arquivo $1 não encontrado!"
    exit 1
fi

# Roda o analisador léxico
python3 lexico.py "$1"

# Verifica se o arquivo .lex foi gerado
LEX_FILE="${1%.cria}.lex"
if [ ! -f "$LEX_FILE" ]; then
    echo "Erro: Arquivo $LEX_FILE não foi gerado!"
    exit 1
fi

# Roda o analisador sintático
python3 sintatico.py "$LEX_FILE"

# Verifica se o arquivo .syn foi gerado
SYN_FILE="${1%.cria}.syn"
if [ ! -f "$SYN_FILE" ]; then
    echo "Erro: Arquivo $SYN_FILE não foi gerado!"
    exit 1
fi

# Roda o analisador semântico e gerador de código
python3 semantico_e_codigo.py "$LEX_FILE"