# jogo.py
# Controla o estado do jogo e dispara os sons nos momentos certos.

import pygame
from funcoes import gerar_codigo, avaliar_palpite, palpite_valido, acertou
from dados import carregar_ranking, salvar_ranking, adicionar_ao_ranking, calcular_pontuacao
from config import MAX_TENTATIVAS, SOM_BEEP, SOM_CORRETO, SOM_ERRO, SOM_VITORIA, SOM_DERROTA, CORRETO


def carregar_som(caminho):
    """Tenta carregar um som. Retorna None se o arquivo nao existir."""
    try:
        return pygame.mixer.Sound(caminho)
    except Exception:
        return None


class Jogo:
    """
    Guarda todo o estado atual da partida e os sons do jogo.
    """

    def __init__(self):
        # Inicializa o mixer de audio do Pygame
        pygame.mixer.init()

        # Carrega os sons (retorna None se o arquivo nao existir)
        self.som_beep    = carregar_som(SOM_BEEP)
        self.som_correto = carregar_som(SOM_CORRETO)
        self.som_erro    = carregar_som(SOM_ERRO)
        self.som_vitoria = carregar_som(SOM_VITORIA)
        self.som_derrota = carregar_som(SOM_DERROTA)

        self.reiniciar()
        # O ranking persiste entre partidas
        self.ranking = carregar_ranking()

    def tocar(self, som):
        """Toca um som se ele foi carregado corretamente."""
        if som:
            som.play()

    def reiniciar(self):
        """Reseta todos os dados para comecar uma nova partida."""
        self.secreto      = gerar_codigo()
        self.tentativas   = []
        self.input_atual  = ""
        self.game_over    = False
        self.venceu       = False
        self.pontuacao    = 0
        self.erro_msg     = ""
        self.erro_timer   = 0
        self.tela_atual   = "jogo"
        self.nome_jogador = ""
        self.cursor_timer = 0

    def digitar(self, char):
        """Adiciona um caractere ao palpite e toca o beep."""
        from config import CHARSET, TAMANHO
        if char.upper() in CHARSET and len(self.input_atual) < TAMANHO:
            self.input_atual += char.upper()
            self.tocar(self.som_beep)  # beep a cada tecla digitada

    def apagar(self):
        """Remove o ultimo caractere digitado."""
        self.input_atual = self.input_atual[:-1]

    def confirmar(self):
        """
        Valida e processa o palpite atual.
        Toca o som adequado conforme o resultado.
        """
        palpite = self.input_atual.upper()

        if not palpite_valido(palpite):
            self.erro_msg   = "Digite exatamente 5 letras ou numeros."
            self.erro_timer = 140
            self.tocar(self.som_erro)  # som de erro no palpite invalido
            return

        resultado = avaliar_palpite(self.secreto, palpite)
        self.tentativas.append(resultado)
        self.input_atual = ""

        if acertou(resultado):
            self.venceu     = True
            self.game_over  = True
            self.pontuacao  = calcular_pontuacao(len(self.tentativas))
            self.tela_atual = "nome"
            self.tocar(self.som_vitoria)  # som de vitoria ao desarmar a bomba

        elif len(self.tentativas) >= MAX_TENTATIVAS:
            self.game_over  = True
            self.tela_atual = "fim"
            self.tocar(self.som_derrota)  # som de explosao ao perder

        else:
            # Verifica se pelo menos uma letra ficou verde
            tem_correto = any(item["status"] == CORRETO for item in resultado)
            if tem_correto:
                self.tocar(self.som_correto)  # som de acerto parcial

    def salvar_nome(self):
        """Salva a pontuacao no ranking e vai para a tela de fim."""
        self.ranking = adicionar_ao_ranking(
            self.nome_jogador or "Anonimo",
            len(self.tentativas),
            self.ranking
        )
        salvar_ranking(self.ranking)
        self.tela_atual = "fim"