# sprites.py
# Contem todas as funcoes de desenho do jogo.
# Cuida da tematica de bomba a ser desarmada e exibe a logo da PUC.

import pygame
from config import (
    LARGURA, ALTURA, BRANCO, CINZA_MED, CINZA_CLR, CINZA_ESC,
    VERDE, AMARELO, VERMELHO, DOURADO, AZUL, PRETO, LARANJA,
    TILE, GAP, MARGEM_ESQ, MARGEM_TOP, TAMANHO, MAX_TENTATIVAS,
    CORRETO, PRESENTE, COR_STATUS, IMG_LOGO
)
from dados import calcular_pontuacao


def carregar_logo():
    """Carrega e redimensiona a logo da PUC Minas. Retorna None se nao encontrar."""
    try:
        img = pygame.image.load(IMG_LOGO).convert_alpha()
        return pygame.transform.smoothscale(img, (48, 48))
    except Exception:
        return None


def desenhar_tile(tela, char, status, rect, fonte):
    """Desenha um quadrado da grade com a cor e a letra correspondentes."""
    if status is None:
        cor   = PRETO
        borda = CINZA_MED
    elif status == "ativo":
        cor   = (50, 50, 55)
        borda = BRANCO
    else:
        cor   = COR_STATUS[status]
        borda = cor

    pygame.draw.rect(tela, cor,   rect, border_radius=5)
    pygame.draw.rect(tela, borda, rect, 2, border_radius=5)

    if char:
        texto = fonte.render(char.upper(), True, BRANCO)
        tela.blit(texto, texto.get_rect(center=rect.center))


def desenhar_grade(tela, tentativas, input_atual, game_over, fonte):
    """Desenha todas as 6 linhas da grade."""
    for linha in range(MAX_TENTATIVAS):
        for col in range(TAMANHO):
            x    = MARGEM_ESQ + col * (TILE + GAP)
            y    = MARGEM_TOP + linha * (TILE + GAP)
            rect = pygame.Rect(x, y, TILE, TILE)

            if linha < len(tentativas):
                item = tentativas[linha][col]
                desenhar_tile(tela, item["char"], item["status"], rect, fonte)
            elif linha == len(tentativas) and not game_over:
                char   = input_atual[col] if col < len(input_atual) else ""
                status = "ativo" if char else None
                desenhar_tile(tela, char, status, rect, fonte)
            else:
                desenhar_tile(tela, "", None, rect, fonte)


def desenhar_teclado(tela, tentativas, fonte):
    """Desenha o mini teclado com status conhecido de cada caractere."""
    linhas = [
        list("QWERTYUIOP"),
        list("ASDFGHJKL"),
        list("ZXCVBNM"),
        list("1234567890"),
    ]

    status_char = {}
    for tentativa in tentativas:
        for item in tentativa:
            c  = item["char"]
            st = item["status"]
            if status_char.get(c) != CORRETO:
                if status_char.get(c) != PRESENTE or st == CORRETO:
                    status_char[c] = st

    kw, kh   = 36, 28
    gap      = 3
    inicio_y = MARGEM_TOP + MAX_TENTATIVAS * (TILE + GAP) + 12

    for r, chars in enumerate(linhas):
        largura_total = len(chars) * (kw + gap) - gap
        inicio_x = (LARGURA - largura_total) // 2
        y = inicio_y + r * (kh + gap + 2)

        for i, ch in enumerate(chars):
            x    = inicio_x + i * (kw + gap)
            rect = pygame.Rect(x, y, kw, kh)
            st   = status_char.get(ch)

            if st == CORRETO:
                cor = VERDE
            elif st == PRESENTE:
                cor = AMARELO
            elif st:
                cor = CINZA_ESC
            else:
                cor = (70, 70, 70)

            pygame.draw.rect(tela, cor, rect, border_radius=3)
            txt = fonte.render(ch, True, BRANCO)
            tela.blit(txt, txt.get_rect(center=rect.center))


def texto_centro(tela, msg, y, fonte, cor=BRANCO):
    """Escreve um texto centralizado horizontalmente na tela."""
    surf = fonte.render(msg, True, cor)
    tela.blit(surf, surf.get_rect(centerx=LARGURA // 2, y=y))


def desenhar_botao(tela, msg, rect, fonte, mouse):
    """Desenha um botao que clareia ao passar o mouse por cima."""
    cor = (100, 160, 210) if rect.collidepoint(mouse) else AZUL
    pygame.draw.rect(tela, cor, rect, border_radius=7)
    txt = fonte.render(msg, True, BRANCO)
    tela.blit(txt, txt.get_rect(center=rect.center))


def desenhar_bomba(tela, tentativas_feitas, fonte_peq):
    """
    Desenha uma bomba no canto superior direito da tela.
    Conforme o jogador erra tentativas, os fios vao sendo cortados.
    Com 6 tentativas, todos os fios estao cortados = bomba explode.
    """
    # Posicao da bomba
    cx, cy = 430, 55   # centro do corpo da bomba
    raio   = 22

    # Corpo da bomba (circulo preto com borda vermelha)
    pygame.draw.circle(tela, (40, 40, 40), (cx, cy), raio)
    pygame.draw.circle(tela, VERMELHO,     (cx, cy), raio, 2)

    # Pavio (linha saindo do topo)
    pygame.draw.line(tela, LARANJA, (cx, cy - raio), (cx + 10, cy - raio - 18), 3)

    # Fios: um por tentativa restante
    # Comeca com 6 fios, perde um a cada tentativa errada
    fios_restantes = MAX_TENTATIVAS - tentativas_feitas
    cores_fios = [VERDE, AMARELO, LARANJA, VERMELHO, (200, 200, 200), AZUL]

    for i in range(MAX_TENTATIVAS):
        fx = cx - 18 + i * 7
        fy = cy + raio
        if i < fios_restantes:
            # Fio inteiro
            pygame.draw.line(tela, cores_fios[i], (fx, fy), (fx, fy + 12), 2)
        else:
            # Fio cortado (so metade)
            pygame.draw.line(tela, CINZA_ESC, (fx, fy), (fx, fy + 5), 2)

    # Texto de tentativas restantes dentro da bomba
    txt = fonte_peq.render(str(fios_restantes), True, BRANCO)
    tela.blit(txt, txt.get_rect(center=(cx, cy)))


def desenhar_cabecalho(tela, logo, tentativas_feitas, fontes):
    """
    Desenha o cabecalho da tela de jogo:
    logo da PUC + titulo + bomba com fios.
    """
    # Logo da PUC no canto esquerdo
    if logo:
        tela.blit(logo, (12, 8))

    # Titulo centralizado
    texto_centro(tela, "CodeBreaker", 10, fontes["grande"])
    texto_centro(tela, "Desarme a bomba!", 44, fontes["peq"], VERMELHO)
    texto_centro(
        tela,
        f"Tentativa {tentativas_feitas + 1}/{MAX_TENTATIVAS}",
        64, fontes["peq"], CINZA_CLR
    )

    # Bomba no canto direito
    desenhar_bomba(tela, tentativas_feitas, fontes["peq"])

    # Linha separadora
    pygame.draw.line(tela, CINZA_MED, (20, 88), (LARGURA - 20, 88), 1)


def desenhar_tela_jogo(tela, jogo, logo, fontes, mouse):
    """Desenha a tela principal de jogo."""
    tela.fill(PRETO)
    desenhar_cabecalho(tela, logo, len(jogo.tentativas), fontes)
    desenhar_grade(tela, jogo.tentativas, jogo.input_atual, jogo.game_over, fontes["tile"])
    desenhar_teclado(tela, jogo.tentativas, fontes["kb"])

    if jogo.erro_msg and jogo.erro_timer > 0:
        texto_centro(tela, jogo.erro_msg, ALTURA - 45, fontes["peq"], VERMELHO)


def desenhar_tela_nome(tela, jogo, logo, fontes, mouse, btn_confirmar):
    """Tela onde o jogador digita o nome apos desarmar a bomba."""
    tela.fill(PRETO)

    if logo:
        tela.blit(logo, (12, 8))

    texto_centro(tela, "BOMBA DESARMADA!", 80, fontes["grande"], VERDE)
    texto_centro(tela, f"{len(jogo.tentativas)} tentativa(s) — {jogo.pontuacao} pts", 125, fontes["media"], DOURADO)
    texto_centro(tela, "Digite seu nome:", 200, fontes["media"])

    caixa = pygame.Rect(LARGURA // 2 - 120, 235, 240, 46)
    pygame.draw.rect(tela, (40, 40, 40), caixa, border_radius=6)
    pygame.draw.rect(tela, CINZA_MED,    caixa, 2, border_radius=6)
    nome_surf = fontes["media"].render(jogo.nome_jogador, True, BRANCO)
    tela.blit(nome_surf, nome_surf.get_rect(midleft=(caixa.x + 10, caixa.centery)))

    # Cursor piscante
    if jogo.cursor_timer // 30 % 2 == 0:
        cx = caixa.x + 10 + nome_surf.get_width() + 2
        pygame.draw.line(tela, BRANCO, (cx, caixa.y + 8), (cx, caixa.y + 38), 2)

    desenhar_botao(tela, "Confirmar", btn_confirmar, fontes["media"], mouse)


def desenhar_tela_fim(tela, jogo, logo, fontes, mouse, btn_jogar, btn_ranking):
    """Tela de fim de jogo: bomba desarmada ou explodiu."""
    tela.fill(PRETO)

    if logo:
        tela.blit(logo, (12, 8))

    if jogo.venceu:
        texto_centro(tela, "BOMBA DESARMADA!", 50, fontes["grande"], VERDE)
        texto_centro(tela, f"{len(jogo.tentativas)} tentativa(s) — {jogo.pontuacao} pts", 95, fontes["media"], DOURADO)
    else:
        # Desenha um circulo vermelho grande simulando explosao
        pygame.draw.circle(tela, (80, 20, 20), (LARGURA // 2, 65), 40)
        pygame.draw.circle(tela, VERMELHO,     (LARGURA // 2, 65), 40, 3)
        texto_centro(tela, "BOOM!", 48, fontes["grande"], VERMELHO)
        texto_centro(tela, f"O codigo era: {jogo.secreto}", 100, fontes["media"])

    # Grade com as tentativas feitas
    for linha in range(len(jogo.tentativas)):
        for col in range(TAMANHO):
            x    = MARGEM_ESQ + col * (TILE + GAP)
            y    = 145 + linha * (TILE + GAP)
            rect = pygame.Rect(x, y, TILE, TILE)
            item = jogo.tentativas[linha][col]
            desenhar_tile(tela, item["char"], item["status"], rect, fontes["tile"])

    desenhar_botao(tela, "Jogar de novo", btn_jogar,   fontes["media"], mouse)
    desenhar_botao(tela, "Ver ranking",   btn_ranking, fontes["media"], mouse)


def desenhar_tela_ranking(tela, jogo, logo, fontes, mouse, btn_voltar):
    """Tela do ranking com os 10 melhores agentes."""
    tela.fill(PRETO)

    if logo:
        tela.blit(logo, (12, 8))

    texto_centro(tela, "Ranking — Melhores Agentes", 15, fontes["grande"], DOURADO)
    pygame.draw.line(tela, CINZA_MED, (40, 68), (LARGURA - 40, 68), 1)

    if not jogo.ranking:
        texto_centro(tela, "Nenhuma pontuacao ainda.", 200, fontes["media"], CINZA_CLR)
    else:
        for i, entrada in enumerate(jogo.ranking):
            y   = 80 + i * 38
            pts = calcular_pontuacao(entrada["tentativas"])
            cor = DOURADO if i == 0 else BRANCO
            linha_txt = f"{i+1}.  {entrada['nome']:<14}  {entrada['tentativas']} tent.   {pts} pts"
            surf = fontes["media"].render(linha_txt, True, cor)
            tela.blit(surf, (40, y))

    desenhar_botao(tela, "Voltar", btn_voltar, fontes["media"], mouse)