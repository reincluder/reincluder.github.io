import feedparser
import ollama
from slugify import slugify
from datetime import datetime
import os

# CONFIGURAÇÃO
RSS_URLS = [
    "http://feeds.feedburner.com/TechCrunch/", # Exemplo. Troque pelos seus RSS depois
    "https://hnrss.org/newest?q=AI+neurodiversity"
]
# MODELO OTIMIZADO PARA CPU
MODELO = "llama3.2:1b"
OUTPUT_DIR = "content/posts"

def gerar_resumo(titulo, conteudo):
    prompt = f"""
    Aja como um especialista em tecnologia assistiva e neurodiversidade.
    Analise o seguinte texto:
    Título: {titulo}
    Conteúdo: {conteudo}

    Tarefa:
    1. Resuma a ferramenta/notícia em 2 parágrafos curtos.
    2. Explique COMO isso ajuda alguém com TDAH ou Autismo.
    3. Dê uma nota de 1 a 10 para utilidade prática.

    Responda APENAS em Markdown. Português do Brasil. Sem introduções.
    """
    
    try:
        response = ollama.chat(model=MODELO, messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    except Exception as e:
        return f"Erro ao processar IA: {str(e)}"

def processar_feeds():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Iniciando varredura com modelo: {MODELO} (CPU Mode)...")

    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            print(f"Lendo feed: {url}...")
            
            # Pega o primeiro item do feed
            if len(feed.entries) > 0:
                entry = feed.entries[0]
                titulo = entry.title
                link = entry.link
                desc = entry.description if 'description' in entry else entry.summary
                
                print(f"Processando: {titulo}")
                resumo_ia = gerar_resumo(titulo, desc)
                
                slug = slugify(titulo)
                filename = f"{OUTPUT_DIR}/{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"
                
                md_content = f"""---
title: "{titulo}"
date: {datetime.now().isoformat()}
draft: false
---

# Análise (re)includer

[Fonte Original]({link})

{resumo_ia}

---
*Gerado via IA Local ({MODELO})*
"""
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(md_content)
                print(f"Sucesso! Arquivo salvo em: {filename}")
            else:
                print("Feed vazio ou ilegível.")
                
        except Exception as e:
            print(f"Erro ao ler feed {url}: {e}")

if __name__ == "__main__":
    processar_feeds()
