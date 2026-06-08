# dados.py
# Responsavel por ler e salvar dados em arquivo.
# No nosso caso, cuida do ranking (lista dos melhores jogadores).

from config import ARQUIVO_RANKING, MAX_TENTATIVAS


def carregar_ranking():
    """
    Le o arquivo ranking.txt e retorna uma lista de dicionarios.
    Cada linha do arquivo tem o formato:  Nome;tentativas
    Se o arquivo nao existir, retorna lista vazia.
    """
    ranking = []
    try:
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if ";" in linha:
                    partes    = linha.split(";")
                    nome      = partes[0]
                    tentativas = int(partes[1])
                    ranking.append({"nome": nome, "tentativas": tentativas})
    except FileNotFoundError:
        pass  # se o arquivo nao existe ainda, retorna lista vazia mesmo
    return ranking


def salvar_ranking(ranking):
    """
    Salva o ranking no arquivo ranking.txt.
    Cada entrada vira uma linha no formato:  Nome;tentativas
    """
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        for entrada in ranking:
            f.write(f"{entrada['nome']};{entrada['tentativas']}\n")


def adicionar_ao_ranking(nome, tentativas, ranking):
    """
    Adiciona uma nova entrada, ordena por menos tentativas
    e mantém só os 10 melhores.
    """
    entrada = {"nome": nome.strip() or "???", "tentativas": tentativas}
    ranking = ranking + [entrada]
    ranking.sort(key=lambda x: x["tentativas"])
    return ranking[:10]


def calcular_pontuacao(tentativas):
    """Quanto menos tentativas usadas, maior a pontuacao."""
    if tentativas <= 0 or tentativas > MAX_TENTATIVAS:
        return 0
    return (MAX_TENTATIVAS - tentativas + 1) * 100