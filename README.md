# RA1_7

## PUCPR - Pontifícia Universidade Católica do Paraná

Disciplina: Construção de Interpretadores

Professor: Frank Coelho de Alcantara

## Alunas:
  - Ana Flávia Martins dos Santos (Github: aflavinhams)
  - Isabella Vanderlinde Berkembrock (Github: berkembrockisabella)
  - Michele Cristina Otta (Github: micheleotta)
  - Yejin Chung (Github: Chungyejin)

## Como compilar?
O projeto foi executado em Python, logo, não é necessária compilação.

## Como executar?
Executar com o comando 

python main.py arquivosTeste/teste.txt

## Como testar? 
Executar o programa passando como argumento um arquivo de teste contendo expressões em RPN.

## Sobre o projeto:
Este projeto tem como objetivo implementar um analisador léxico baseado em Autômatos Finitos Determinísticos (AFD) para processar expressões aritméticas em notação polonesa reversa (RPN). A partir das expressões lidas de um arquivo de entrada, o programa realiza a tokenização e gera código Assembly compatível com a arquitetura ARMv7, que será executado no simulador CPULATOR.

## Estrutura do projeto:
- main.py: responsável pela execução
- functions/: implementação de todas as funções
- arquivosTeste/: arquivos com os testes para entrada
