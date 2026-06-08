# Proposta Inicial — CodeBreaker

## Nome do jogo
CodeBreaker

## Integrantes do grupo
* Lucas Abijaode Alvarenga

## Tipo de jogo
Jogo de adivinhação alfanumérica — estilo Termo/Wordle com códigos de 5 caracteres (letras A-Z e dígitos 0-9).

## Descrição geral
O jogador tenta descobrir um código secreto de 5 caracteres gerado aleatoriamente a cada partida. A cada tentativa, o jogo fornece feedback visual colorido: verde para caractere certo na posição certa, amarelo para caractere presente em posição errada e cinza para caractere ausente.

## Objetivo do jogador
Descobrir o código secreto em no máximo 6 tentativas.

## Regras principais
1. O código secreto tem 5 caracteres sorteados aleatoriamente do conjunto A-Z e 0-9.
2. O jogador tem até 6 tentativas para adivinhar o código.
3. A cada tentativa, cada posição recebe uma cor de feedback:
   - Verde: caractere certo na posição certa.
   - Amarelo: caractere existe no código mas está em outra posição.
   - Cinza: caractere não existe no código.
4. O teclado virtual é atualizado com os status conhecidos de cada caractere.

## Condição de vitória
Acertar os 5 caracteres em qualquer uma das 6 tentativas.

## Condição de derrota ou encerramento
Usar todas as 6 tentativas sem acertar. O código secreto é revelado ao final.

## Elementos previstos
- Grade 6x5 de tiles coloridos
- Teclado virtual alfanumérico com cores de status
- Sistema de pontuação por tentativas usadas
- Tela de ranking salvo em arquivo
- Campo para digitar o nome ao vencer

## Controles previstos
- Teclado físico: digitar caracteres, Backspace para apagar, Enter para confirmar
- Mouse: clicar nos botões de tela

## Estruturas de dados que poderão ser utilizadas
- Lista de listas: grade de tentativas
- Dicionário: resultado por posição `{"char": str, "status": str}`
- Dicionário: status conhecido por caractere para o teclado visual
- Lista de dicionários: ranking dos jogadores

## Uso previsto de arquivos
- `data/ranking.txt`: leitura e escrita do ranking no formato `Nome;tentativas`

## Testes planejados
- Geração de código: tamanho correto, caracteres válidos, aleatoriedade
- Avaliação de palpite: acerto total, ausência total, presença, duplicatas, case-insensitive
- Validação do palpite: tamanho e caracteres inválidos
- Verificação de vitória
- Pontuação: decrescente, casos limite
- Ranking: ordenação, limite de 10 entradas, nome vazio

## Principais dificuldades esperadas
- Tratar corretamente caracteres duplicados na lógica de avaliação
- Organizar a renderização do Pygame em funções claras e separadas

## Escopo mínimo para a entrega final
- Jogo funcional com grade, feedback colorido, vitória e derrota
- Sistema de pontuação
- Ranking salvo em arquivo texto
- Teclado visual com atualização de status
- Testes cobrindo toda a lógica principal