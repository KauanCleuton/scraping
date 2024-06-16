import os
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import sqlite3
import re

def scrape_and_download_music(url):
    try:
        # Enviar uma solicitação GET para a URL do vídeo
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        # Verificar se a requisição foi bem sucedida
        if response.status_code != 200:
            print(f'Falha ao acessar {url}. Código de status: {response.status_code}')
            return

        # Parsear o conteúdo HTML com BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar o título do vídeo
        title_elem = soup.find('meta', property='og:title')
        if title_elem:
            title = title_elem['content']
        else:
            title = 'Título não encontrado'

        # Remover caracteres inválidos do título do vídeo
        title = re.sub(r'[\\/:*?"<>|]', '', title)

        # Apenas manter a primeira parte do título para o diretório
        primeiro_nome = title.split()[0]
        diretorio_base = 'musicas'
        diretorio_musica = os.path.join(diretorio_base, primeiro_nome)
        os.makedirs(diretorio_musica, exist_ok=True)

        # Criar um objeto YouTube
        yt = YouTube(url)

        # Baixar o áudio (mp3)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        audio_path = os.path.join(diretorio_musica, f'{primeiro_nome}.mp3')
        audio_stream.download(output_path=audio_path)

        # Baixar o vídeo (mp4)
        video_stream = yt.streams.filter(file_extension='mp4').first()
        video_path = os.path.join(diretorio_musica, f'{title}.mp4')
        video_stream.download(output_path=video_path)

        # Retornar o caminho do arquivo de áudio baixado, título completo do vídeo e diretório base
        return diretorio_musica, title, diretorio_base

    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        return None, None, None

# URL do vídeo musical do YouTube que queremos fazer scraping e download
url = str(input('Digite a URL da Música: '))

# Chamar a função para fazer o scraping e download da música
caminho_diretorio, titulo_musica, diretorio_base = scrape_and_download_music(url)

if caminho_diretorio:
    print(f'Música baixada com sucesso em {caminho_diretorio}')
else:
    print('Falha ao baixar a música')

# Função para criar o banco de dados e tabela
def criar_banco_dados():
    try:
        # Conectar ao banco de dados (será criado se não existir)
        conn = sqlite3.connect('musicas.db')

        # Criar cursor
        cursor = conn.cursor()

        # Criar tabela se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS musicas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            titulo TEXT NOT NULL,
                            caminho_audio TEXT NOT NULL,
                            caminho_video TEXT NOT NULL
                          )''')

        # Commit das alterações
        conn.commit()

        # Fechar a conexão
        conn.close()
        print('Banco de dados criado com sucesso.')

    except Exception as e:
        print(f'Erro ao criar banco de dados: {e}')

# Função para inserir música no banco de dados
def inserir_musica(titulo, caminho_video):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('musicas.db')
        cursor = conn.cursor()

        # Inserir música na tabela
        cursor.execute('''INSERT INTO musicas (titulo, caminho_audio, caminho_video)
                          VALUES (?, ?, ?)''', (titulo, f'{caminho_video}.mp3', caminho_video))

        # Commit da transação
        conn.commit()

        # Fechar a conexão
        conn.close()
        print(f'Música "{titulo}" inserida no banco de dados.')

    except Exception as e:
        print(f'Erro ao inserir música no banco de dados: {e}')

# Criar o banco de dados e a tabela (executar apenas uma vez)
criar_banco_dados()

# Inserir a música baixada no banco de dados
if caminho_diretorio and titulo_musica and diretorio_base:
    # print(f'{caminho_diretorio}\{titulo_musica}\{titulo_musica}')
    caminho_video = os.path.join(f'{caminho_diretorio}\{titulo_musica}\{titulo_musica}')
    inserir_musica(titulo_musica, caminho_video)
