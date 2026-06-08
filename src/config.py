# config.py
# Guarda todas as configuracoes do jogo em um so lugar.
# Assim, se quiser mudar algo (cor, tamanho, som),
# basta alterar aqui sem precisar mexer nos outros arquivos.

import string
import os

# Caminho base do projeto (pasta raiz)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Janela ---
LARGURA  = 500
ALTURA   = 680
FPS      = 60
TITULO   = "CodeBreaker — Desarme a Bomba"

# --- Regras do jogo ---
TAMANHO        = 5
MAX_TENTATIVAS = 6

# Caracteres validos: letras A-Z e digitos 0-9
CHARSET = list(string.ascii_uppercase + string.digits)

# --- Status de cada posicao apos avaliar o palpite ---
CORRETO  = "correto"
PRESENTE = "presente"
AUSENTE  = "ausente"

# --- Cores (R, G, B) ---
PRETO     = (18,  18,  18)
BRANCO    = (255, 255, 255)
CINZA_ESC = (58,  58,  60)
CINZA_MED = (90,  90,  90)
CINZA_CLR = (130, 130, 130)
VERDE     = (83,  141, 78)
AMARELO   = (181, 159, 59)
VERMELHO  = (220, 80,  80)
DOURADO   = (255, 215,  0)
AZUL      = (70,  130, 180)
LARANJA   = (210, 100,  20)  # cor de fio da bomba

# Mapeia cada status para a cor correspondente
COR_STATUS = {
    CORRETO:  VERDE,
    PRESENTE: AMARELO,
    AUSENTE:  CINZA_ESC,
}

# --- Grade de tiles ---
TILE       = 58
GAP        = 7
MARGEM_ESQ = (LARGURA - (TILE * TAMANHO + GAP * (TAMANHO - 1))) // 2
MARGEM_TOP = 110

# --- Caminhos dos arquivos ---
ARQUIVO_RANKING = os.path.join(BASE, "data", "ranking.txt")

# Sons
SOM_BEEP    = os.path.join(BASE, "assets", "sons", "beep.wav")
SOM_CORRETO = os.path.join(BASE, "assets", "sons", "correto.wav")
SOM_ERRO    = os.path.join(BASE, "assets", "sons", "erro.wav")
SOM_VITORIA = os.path.join(BASE, "assets", "sons", "vitoria.wav")
SOM_DERROTA = os.path.join(BASE, "assets", "sons", "derrota.wav")

# Imagens
IMG_LOGO = os.path.join(BASE, "assets", "imagens", "logo_puc.png")