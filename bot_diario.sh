#!/bin/bash

# Define o caminho do projeto
CD_DIR="$HOME/Projetos/reincluder"
LOG_FILE="$CD_DIR/bot.log"

echo "--- Iniciando Bot: $(date) ---" >> $LOG_FILE

# 1. Entra na pasta
cd $CD_DIR

# 2. Ativa o Python e gera o conteúdo
source venv/bin/activate
echo "Rodando IA..." >> $LOG_FILE
python gerador_conteudo.py >> $LOG_FILE 2>&1

# 3. Constroi o site (na pasta docs)
echo "Construindo site..." >> $LOG_FILE
rm -rf docs
hugo

# 4. Envia para o GitHub
echo "Enviando para nuvem..." >> $LOG_FILE
git add .
git commit -m "Update Diário: $(date +'%Y-%m-%d')"
git push origin main >> $LOG_FILE 2>&1

echo "--- Fim: $(date) ---" >> $LOG_FILE
