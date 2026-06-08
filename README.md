# CodeBreaker

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

> **Observação ao professor:** Este projeto foi desenvolvido com maior agilidade pois o aluno já possuía uma versão anterior do jogo implementada em linguagem C, desenvolvida como exercício pessoal durante estudos no Ibmec. A lógica central (avaliação de palpites, ranking e sistema de pontuação) foi reescrita do zero em Python, seguindo os conceitos e a estrutura exigidos pela disciplina.

## Integrantes do grupo

- Lucas Abijaode Alvarenga

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

CodeBreaker é um jogo de adivinhação alfanumérica inspirado no Termo/Wordle. Um código secreto de 5 caracteres é gerado aleatoriamente a cada partida, usando letras (A-Z) e dígitos (0-9). O jogador tenta descobrir o código em até 6 tentativas e recebe feedback visual colorido a cada tentativa: verde para caractere certo na posição certa, amarelo para caractere presente em posição errada e cinza para caractere ausente. Ao vencer, o jogador salva seu nome no ranking.

## Objetivo do jogador

Descobrir o código secreto de 5 caracteres alfanuméricos em no máximo 6 tentativas, usando o feedback de cores para eliminar possibilidades e afunilar o palpite correto.

## Regras do jogo

- O código secreto tem 5 caracteres sorteados aleatoriamente do conjunto A-Z e 0-9.
- O jogador tem até 6 tentativas para adivinhar o código.
- A cada tentativa, cada posição recebe uma cor de feedback:
  - Verde: caractere certo na posição certa.
  - Amarelo: caractere existe no código mas está em outra posição.
  - Cinza: caractere não existe no código.
- O teclado virtual é atualizado com os status conhecidos de cada caractere.
- Acertar em menos tentativas gera mais pontos.
- Ao vencer, o jogador digita o nome para salvar no ranking.
- Se esgotar as 6 tentativas sem acertar, o código secreto é revelado.

## Controles

- Letras (A-Z) e dígitos (0-9): digitar o palpite
- Backspace: apagar o último caractere
- Enter: confirmar o palpite
- ESC: sair do jogo

## Como executar o projeto

### 1. Clonar o repositório
git clone https://github.com/abijaode/pygaming.git
cd pygaming
pip install -r requirements.txt
py -3.12 main.py

## Como executar os testes
py -3.12 -m pytest

## Checklist mínimo para entrega

- [x] Preencher este README com nome final, descrição real, regras e controles do jogo.
- [x] Atualizar `docs/proposta.MD` com a proposta do grupo.
- [x] Garantir que o jogo executa com `python main.py`.
- [x] Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.