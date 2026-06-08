# tests/test_logica.py
# Testes das funcoes de logica do jogo.
# Execute com: python -m pytest tests/ -v

import sys
import os

# Permite importar os modulos de dentro da pasta src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from funcoes import gerar_codigo, avaliar_palpite, palpite_valido, acertou
from dados import adicionar_ao_ranking, calcular_pontuacao
from config import CORRETO, PRESENTE, AUSENTE, TAMANHO, MAX_TENTATIVAS


# --- Testes de gerar_codigo ---

def test_codigo_tem_tamanho_certo():
    """O codigo gerado deve ter exatamente 5 caracteres."""
    assert len(gerar_codigo()) == TAMANHO

def test_codigo_so_tem_chars_validos():
    """Todos os caracteres devem ser letras A-Z ou digitos 0-9."""
    import string
    validos = set(string.ascii_uppercase + string.digits)
    for _ in range(20):
        for char in gerar_codigo():
            assert char in validos

def test_codigos_sao_aleatorios():
    """Gera 50 codigos e verifica que nao sao todos iguais."""
    codigos = {gerar_codigo() for _ in range(50)}
    assert len(codigos) > 1


# --- Testes de avaliar_palpite ---

def test_tudo_correto():
    """Palpite igual ao secreto: todas as posicoes devem ser CORRETO."""
    resultado = avaliar_palpite("AB3D5", "AB3D5")
    assert all(r["status"] == CORRETO for r in resultado)

def test_tudo_ausente():
    """Nenhum char em comum: todas as posicoes devem ser AUSENTE."""
    resultado = avaliar_palpite("AAAAA", "BBBBB")
    assert all(r["status"] == AUSENTE for r in resultado)

def test_char_presente():
    """Char que existe no secreto mas na posicao errada deve ser PRESENTE."""
    resultado = avaliar_palpite("ABCDE", "BAAAA")
    assert resultado[0]["status"] == PRESENTE

def test_nao_marca_presente_demais():
    """Se o secreto tem 1 'A' e o palpite tem 3 'A', so 1 deve ser marcado."""
    resultado = avaliar_palpite("BAAAA", "AAAAA")
    corretos = sum(1 for r in resultado if r["status"] == CORRETO)
    assert corretos == 4

def test_maiusculo_minusculo():
    """Letras minusculas e maiusculas devem ser tratadas igual."""
    resultado = avaliar_palpite("AB3D5", "ab3d5")
    assert all(r["status"] == CORRETO for r in resultado)

def test_com_digitos():
    """Deve funcionar normalmente com digitos."""
    resultado = avaliar_palpite("12345", "12345")
    assert all(r["status"] == CORRETO for r in resultado)


# --- Testes de palpite_valido ---

def test_palpite_valido_correto():
    assert palpite_valido("AB3D5") is True

def test_palpite_curto_demais():
    assert palpite_valido("ABC") is False

def test_palpite_longo_demais():
    assert palpite_valido("AB3D5X") is False

def test_palpite_com_char_invalido():
    assert palpite_valido("AB!D5") is False

def test_palpite_minusculo_valido():
    assert palpite_valido("ab3d5") is True


# --- Testes de acertou ---

def test_acertou_true():
    resultado = [{"char": c, "status": CORRETO} for c in "AB3D5"]
    assert acertou(resultado) is True

def test_acertou_false():
    resultado = [{"char": "A", "status": CORRETO}] * 4
    resultado.append({"char": "X", "status": AUSENTE})
    assert acertou(resultado) is False


# --- Testes de calcular_pontuacao ---

def test_pontuacao_maxima():
    """Acertar na 1a tentativa da pontuacao maxima."""
    assert calcular_pontuacao(1) == MAX_TENTATIVAS * 100

def test_pontuacao_minima():
    """Acertar na ultima tentativa da pontuacao minima."""
    assert calcular_pontuacao(MAX_TENTATIVAS) == 100

def test_pontuacao_zero():
    assert calcular_pontuacao(0) == 0

def test_pontuacao_decresce():
    """Mais tentativas usadas = menos pontos."""
    pontos = [calcular_pontuacao(i) for i in range(1, MAX_TENTATIVAS + 1)]
    assert pontos == sorted(pontos, reverse=True)


# --- Testes de ranking ---

def test_adicionar_entrada():
    ranking = adicionar_ao_ranking("Lucas", 3, [])
    assert len(ranking) == 1
    assert ranking[0]["nome"] == "Lucas"

def test_ranking_ordenado():
    """Menos tentativas = posicao melhor no ranking."""
    ranking = []
    ranking = adicionar_ao_ranking("Bob",   5, ranking)
    ranking = adicionar_ao_ranking("Alice", 2, ranking)
    ranking = adicionar_ao_ranking("Carol", 4, ranking)
    assert ranking[0]["nome"] == "Alice"
    assert ranking[2]["nome"] == "Bob"

def test_ranking_maximo_10():
    """O ranking guarda no maximo 10 entradas."""
    ranking = []
    for i in range(15):
        ranking = adicionar_ao_ranking(f"Jogador{i}", i + 1, ranking)
    assert len(ranking) == 10

def test_nome_vazio_vira_interrogacao():
    ranking = adicionar_ao_ranking("", 3, [])
    assert ranking[0]["nome"] == "???"