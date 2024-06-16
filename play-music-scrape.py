import os
import sqlite3
import pygame

# Função para listar músicas no banco de dados
def listar_musicas():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('musicas.db')
        cursor = conn.cursor()

        # Selecionar todas as músicas
        cursor.execute('SELECT id, titulo, caminho_audio FROM musicas')
        rows = cursor.fetchall()

        # Exibir as músicas disponíveis
        if rows:
            print('Músicas disponíveis:')
            for row in rows:
                print(f'{row[0]}. {row[1]}')
        else:
            print('Nenhuma música encontrada no banco de dados.')

        # Fechar a conexão
        conn.close()

        return rows

    except Exception as e:
        print(f'Erro ao listar músicas no banco de dados: {e}')
        return None

# Função para escolher e tocar uma música
def escolher_e_tocar_musica():
    try:
        # Listar músicas disponíveis
        rows = listar_musicas()

        if not rows:
            return

        # Pedir ao usuário para escolher uma música
        musica_id = int(input('Escolha o ID da música que deseja tocar: '))

        # Encontrar o caminho do arquivo de áudio da música escolhida
        caminho_audio = None
        titulo_musica = None
        for row in rows:
            if row[0] == musica_id:
                titulo_musica = row[1]
                caminho_audio = row[2]
                break

        if caminho_audio:
            # Verificar se o arquivo de áudio existe
            if os.path.exists(caminho_audio):
                print(f'Tocando a música "{titulo_musica}"')

                # Inicializar pygame mixer
                pygame.mixer.init()

                # Carregar e tocar a música
                pygame.mixer.music.load(caminho_audio)
                pygame.mixer.music.play()

                # Manter o programa em execução até que a música termine
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            else:
                print(f'Arquivo de áudio não encontrado: {caminho_audio}')
        else:
            print('Música não encontrada.')

    except Exception as e:
        print(f'Erro ao escolher e tocar música: {e}')

# Chamar a função para escolher e tocar uma música
escolher_e_tocar_musica()
