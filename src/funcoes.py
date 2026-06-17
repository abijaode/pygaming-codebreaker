# funcoes.py
# Contem a logica pura do jogo: gerar codigo, avaliar palpite, etc.

#** O comando all tem a função de atribuir o valor True/False quando todos os caracteres da variaveis cumprirem alguma funcao**

import random
from config import CHARSET, TAMANHO, CORRETO, PRESENTE, AUSENTE


def gerar_codigo():
    """Sorteia um codigo secreto aleatorio com 5 caracteres (letras e numeros)."""
    return "".join(random.choices(CHARSET, k=TAMANHO))


def avaliar_palpite(secreto, palpite):
    """
    Compara o palpite com o codigo secreto posicao por posicao.

    Retorna uma lista com 5 dicionarios, um por posicao:
        [{"char": "A", "status": "correto"}, ...]

    Regras:
    - Verde   (correto) : caractere certo na posicao certa.
    - Amarelo (presente): caractere existe no codigo mas esta no lugar errado.
    - Cinza   (ausente) : caractere nao existe no codigo.
    """
    secreto = secreto.upper()
    palpite = palpite.upper()

    # Comeca marcando tudo como ausente
    resultado = [{"char": p, "status": AUSENTE} for p in palpite]

    # Primeira passagem: marca as posicoes certas (verde)
    contagem = {}
    for i in range(TAMANHO):
        if palpite[i] == secreto[i]:
            resultado[i]["status"] = CORRETO
        else:
            # Conta os chars do secreto que ainda nao foram acertados
            contagem[secreto[i]] = contagem.get(secreto[i], 0) + 1

    # Segunda passagem: marca os que existem mas estao no lugar errado (amarelo)
    for i in range(TAMANHO):
        if resultado[i]["status"] == AUSENTE:
            char = palpite[i]
            if contagem.get(char, 0) > 0:
                resultado[i]["status"] = PRESENTE
                contagem[char] -= 1  # desconta para nao marcar o mesmo char duas vezes

    return resultado


def palpite_valido(palpite):
    """
    Retorna True se o palpite tem exatamente 5 caracteres
    e todos sao letras A-Z ou digitos 0-9.
    """
    if len(palpite) != TAMANHO:
        return False
    validos = set(CHARSET)
    return all(c.upper() in validos for c in palpite)


def acertou(resultado):
    """Retorna True se todas as posicoes estao com status CORRETO."""
    return all(item["status"] == CORRETO for item in resultado)