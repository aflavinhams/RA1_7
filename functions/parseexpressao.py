# função do parse expressao: valida todos os caracteres e envia para os estados corretos
def parseExpressao(linha):

  # iniciando a lista de tokens final vazia
  tokens = []
  # iniciando na posição zero
  i = 0
  # iniciando o numero de parenteses como 0
  parenteses = 0


  # percorre todas as posições da linha
  while i < len(linha):

    # pega o caractere da posicao atual
    t = linha[i]

    # se t for numero
    if t.isdigit():

      # manda para a funcao estadoNumero
      token, i = estadoNumero(linha, i)
      tokens.append(token)

    # se t for um dos operadores
    elif t in ['+', '-', '*', '/', '%', '^']:

      # manda para a funcao estadoOperador
      token, i = estadoOperador(linha, i)
      tokens.append(token)

    # se t for um parenteses
    elif t in ['(', ')']:

      # manda para a funcao estadoParenteses
      token, i = estadoParenteses(linha, i)

      # se estiver abrindo um parenteses aumenta um no contador
      if token == '(':
        parenteses += 1
      # se estiver fechando um parenteses diminui um no contador
      else:
        parenteses -= 1

      # se o contador for menor que zero entao estao desbalanceados
      # significa que tem mais fechando do que abrindo
      if parenteses < 0:
        raise ValueError("Parênteses desbalanceados")

      tokens.append(token)

    # se t for um caracter alphanumerico
    elif t.isalpha():

      # manda para a funcao estadoComando
      token, i = estadoComando(linha, i)
      tokens.append(token)

    # se t for um espaco vazio
    elif t == ' ':

      # passa para a proxima posicao
      i += 1

    # se nao for nenhum dos caracteres acima
    else:

      # retorna um erro de caractere invalido
      raise ValueError("Caractere inválido: " + t)

  # se no fim o contador dos parenteses for diferente se zero
  # significa que estao desbalanceados
  if parenteses != 0:
    raise ValueError("Parênteses desbalanceados")

  return tokens


# funcao que valida numeros
def estadoNumero(linha, i):

  # inicio o numero sem nada
  numero = ''
  # inicio um contador de pontos como false
  ponto = False

  # percorro toda a linha a partir da posicao que recebi de parametro
  while i < len(linha):

    # pego o char da posicao atual
    c = linha[i]

    # se for um numero
    if c.isdigit():

      # acrescento ao numero e ando uma posicao
      numero += c
      i += 1

    # se for um ponto
    elif c == '.':

      # se ponto ja for true significa que tem mais de um, retorna erro
      if ponto:
        raise ValueError("Ponto repetido")

      # define ponto como true, acrescenta ao numero e anda uma posicao
      ponto = True
      numero += c
      i += 1

    # se nao for numero nem ponto da um break no while
    else:
      break

  return numero, i

# funcao que valida operadores
def estadoOperador(linha, i):

  # pego o char da posicao atual
  operador = linha[i]

  # verificcando para caso da divisao inteira
  # se / vier seguido de outro /, eu salvo // no comando e pulo pra proxima posicao
  if operador == '/' and i + 1 < len(linha) and linha[i+1] == '/':
    operador == '//'
    i += 1

  # valido se é um dos operadores válidos
  if operador not in ['+', '-', '*', '/', '//', '%', '^']:
    raise ValueError("Operador inválido: " + operador)

  # retorno o operador e mando pra proxima posicao
  return operador, i + 1

# funcao que valida parenteses
def estadoParenteses(linha, i):

  # pego o char da posicao atual
  parentese = linha[i]

  # valido se é um parenteses
  if parentese not in ['(', ')']:
    raise ValueError("Parêntese inválido")

  # retorno o parentese e mando pra proxima posicao
  return parentese, i + 1

# funcao que valida os comandos especiais
def estadoComando(linha, i):

  # inicio o comando vazio
  comando = ''

  # percorro a linha ate o final se for um char alphanumerico maiusculo
  while i < len(linha) and linha[i].isalpha() and linha[i].isupper():

    # adiciono ao meu comando e pulo pra proxima posicao
    comando += linha[i]
    i += 1

  # se não for um comando valido retorna erro
  if comando == '':
    raise ValueError("Comando inválido")

  return comando, i

# funcoes de testes
def testes_validos():
  
  print(parseExpressao("3 4 //"))

  print(parseExpressao("3.14 2 * MEM"))

  print(parseExpressao("(3 + 2)"))

def teste_dois_pontos():

  print(parseExpressao("3.14.5"))

def  teste_caractere_invalido():

  parseExpressao("3 4 @")

def teste_parenteses_desbalanceados():

  parseExpressao("(3 + 2")

testes_validos()