# main.py
# Ponto de entrada do jogo.
# Inicia o Pygame, carrega os recursos e roda o loop principal.
# Para rodar: python main.py

import sys
import os
import pygame

# Adiciona a pasta src/ ao caminho para conseguir importar os modulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from config import LARGURA, ALTURA, FPS, TITULO, CHARSET
from jogo import Jogo
from sprites import (
    carregar_logo,
    desenhar_tela_jogo, desenhar_tela_nome,
    desenhar_tela_fim, desenhar_tela_ranking
)


def main():
    pygame.init()
    tela  = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    clock = pygame.time.Clock()

    # --- Fontes ---
    fontes = {
        "grande": pygame.font.SysFont("Arial", 28, bold=True),
        "media":  pygame.font.SysFont("Arial", 21),
        "tile":   pygame.font.SysFont("Arial", 26, bold=True),
        "kb":     pygame.font.SysFont("Arial", 13, bold=True),
        "peq":    pygame.font.SysFont("Arial", 14),
    }

    # --- Carrega a logo da PUC Minas ---
    logo = carregar_logo()

    # --- Botoes ---
    btn_jogar     = pygame.Rect(LARGURA // 2 - 155, ALTURA - 100, 140, 42)
    btn_ranking   = pygame.Rect(LARGURA // 2 + 15,  ALTURA - 100, 140, 42)
    btn_confirmar = pygame.Rect(LARGURA // 2 - 75,  310,          150, 42)
    btn_voltar    = pygame.Rect(LARGURA // 2 - 75,  ALTURA - 80,  150, 42)

    # --- Cria o objeto que guarda o estado do jogo ---
    jogo = Jogo()

    rodando = True
    while rodando:
        mouse = pygame.mouse.get_pos()

        # Atualiza timers a cada frame
        jogo.cursor_timer += 1
        if jogo.erro_timer > 0:
            jogo.erro_timer -= 1

        # --- Leitura de eventos ---
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                rodando = False

            # ---- Tela de jogo ----
            if jogo.tela_atual == "jogo" and evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    jogo.confirmar()

                elif evento.key == pygame.K_BACKSPACE:
                    jogo.apagar()

                elif evento.key == pygame.K_ESCAPE:
                    rodando = False

                else:
                    jogo.digitar(evento.unicode)

            # ---- Tela de nome ----
            if jogo.tela_atual == "nome" and evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    jogo.salvar_nome()

                elif evento.key == pygame.K_BACKSPACE:
                    jogo.nome_jogador = jogo.nome_jogador[:-1]

                else:
                    if evento.unicode.isprintable() and len(jogo.nome_jogador) < 14:
                        jogo.nome_jogador += evento.unicode

            if jogo.tela_atual == "nome" and evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_confirmar.collidepoint(mouse):
                    jogo.salvar_nome()

            # ---- Tela de fim ----
            if jogo.tela_atual == "fim" and evento.type == pygame.MOUSEBUTTONDOWN:

                if btn_jogar.collidepoint(mouse):
                    jogo.reiniciar()

                elif btn_ranking.collidepoint(mouse):
                    jogo.tela_atual = "ranking"

            # ---- Tela de ranking ----
            if jogo.tela_atual == "ranking" and evento.type == pygame.MOUSEBUTTONDOWN:

                if btn_voltar.collidepoint(mouse):
                    jogo.reiniciar()

        # --- Desenho ---
        if jogo.tela_atual == "jogo":
            desenhar_tela_jogo(tela, jogo, logo, fontes, mouse)

        elif jogo.tela_atual == "nome":
            desenhar_tela_nome(tela, jogo, logo, fontes, mouse, btn_confirmar)

        elif jogo.tela_atual == "fim":
            desenhar_tela_fim(tela, jogo, logo, fontes, mouse, btn_jogar, btn_ranking)

        elif jogo.tela_atual == "ranking":
            desenhar_tela_ranking(tela, jogo, logo, fontes, mouse, btn_voltar)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()