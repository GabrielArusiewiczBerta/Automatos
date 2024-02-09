# Gabriel Arusiewicz Berta 00343479
# Gleydson Campos  00343897
# Giovanni Cabreira Mialnez 00337962

import re


# =====================================================================
# PARTE 1
# =====================================================================
def func1():
    def ler_automato(file_path):
        tuplas_3_elementos = []
        # Abre o arquivo e lê a linha
        with open(file_path, 'r') as file:
            line = file.readline()

             # Encontrar o padrão dentro das chaves {}
            pattern = re.compile(r'{(.*?)}')

             # Encontrar todas as correspondências do padrão na linha
            matches = re.findall(pattern, line)

             # Separar cada correspondência em uma lista e armazenar em uma lista principal
            variables = [list(map(str.strip, match.split(','))) for match in matches]
            
            entrada = line

            # Verificar se encontrou correspondência e extrair o valor
            # Como o valor da posição inicial não segue um padrão igual os outros valor vamos caça-lo
            finalmente = ""
            achou = 0
            flagDois = 0
            # Vamos percorrer até achar o segundo fecha chaves que é onde vamos encontrar o inicio do valor desejado
            for i in entrada:
                if i == '}':
                    achou += 1
                elif achou == 2:
                    if i == ',':
                        flagDois += 1
                    # Após usarmos duas flags para delimitar onde começa (segundo }) e onde acaba (segunda , depois do segundo })
                    # Então agora pegamos esses valroes e o colocamos na variavel que será devolvida ao usuario
                    if i != ',' and flagDois < 2:
                        finalmente = finalmente + i

            # Pula a segunda linha
            file.readline()

            # Processa as linhas restantes
            for linha in file:
                # Remove os caracteres '{', '}', '(', ')' e '\n' e divide os elementos da 3-upla
                elementos_3upla = linha.replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace('\n', '').split(',')
                if elementos_3upla:
                    tuplas_3_elementos.append(tuple(elementos_3upla))

        # Inicializa o dicionário de transições
        transicoes = {}

        # Processa as 3-uplas
        for elemento_3upla in tuplas_3_elementos:
            estado_origem, simbolo, estado_destino = elemento_3upla
            transicoes[(estado_origem, simbolo)] = estado_destino

        # Retorna os resultados
        alfabeto_final = [caracter[1:] if caracter.startswith('{') else caracter for caracter in variables[0]]
        return None, alfabeto_final, variables[1], finalmente, variables[2], transicoes

    # Solicita o nome do arquivo ao usuário com extensão .txt
    nome_arquivo_usuario = input(
        "Digite o nome do arquivo (sem extensão, será adicionado automaticamente .txt): ") + ".txt"

    # Chama a função para ler o automato
    nome_automato, alfabeto, estados, estado_inicial, estados_finais, transicoes = ler_automato(nome_arquivo_usuario)
    print("AFD = " + str(alfabeto), estados, estado_inicial, estados_finais, transicoes)

    def minimizar_afd(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        # Criar uma tabela de equivalência para os pares de estados
        # Inicializa a tabela com todos os casos falsos
        tabela_equivalencia = [[False] * len(estados) for _ in range(len(estados))]

        # Inicializar a tabela marcando os pares onde i está em estados de aceitação e j não está (ou vice-versa)
        for i in range(len(estados)):
            for j in range(i + 1, len(estados)):
                if (estados[i] not in estados_aceitacao and estados[j] not in estados_aceitacao) or \
                        (estados[j] not in estados_aceitacao and estados[i] not in estados_aceitacao):
                    tabela_equivalencia[i][j] = tabela_equivalencia[j][i] = True
                elif (estados[i] in estados_aceitacao and estados[j] in estados_aceitacao) or \
                        (estados[j] in estados_aceitacao and estados[i] in estados_aceitacao):
                    tabela_equivalencia[i][j] = tabela_equivalencia[j][i] = True

        # Percorrer a tabela e verifica se os pares são distintos
        for i in range(len(estados)):
            for j in range(i + 1, len(estados)):
                if tabela_equivalencia[i][j]:
                    for symbol in alfabeto:
                        if estados[i] in estados_aceitacao and estados[j] not in estados_aceitacao or \
                                estados[j] in estados_aceitacao and estados[i] not in estados_aceitacao:
                            tabela_equivalencia[i][j] = tabela_equivalencia[j][i] = False

        # Percorrer a tabela e a linguagem total e verifica os casos
        for i in range(len(estados)):
            for j in range(i + 1, len(estados)):
                if tabela_equivalencia[i][j]:
                    for zymbolo in alfabeto:
                        for symbol in alfabeto:

                            # se a transição do estado[i] da sua linguagem for distinguivel, remove da tabela de equivalência
                            if (transicoes.get((estados[i], symbol))) in estados_aceitacao and transicoes.get((estados[i], zymbolo)) not in estados_aceitacao or \
                                    (transicoes.get((estados[i], zymbolo))) in estados_aceitacao and transicoes.get((estados[i], symbol)) not in estados_aceitacao:
                                        tabela_equivalencia[i][j] = tabela_equivalencia[j][i] = False

                            # se a transição do estado[i] for igual a transição do estado[j], mantém na tabela de equivalência
                            elif (transicoes.get((estados[i], zymbolo)) == transicoes.get((estados[j], zymbolo))):
                                tabela_equivalencia[i][j] = tabela_equivalencia[j][i] = True

                            # verifica toda a linguagem se o estados[i] e estados[j] possuem equivalência, se um dos estados forem disntinguíveis, remove da tabela de equivalência
                            elif transicoes.get((transicoes.get((estados[i], symbol)),zymbolo)) in estados_aceitacao and transicoes.get((transicoes.get((estados[i], zymbolo)), symbol)) not in estados_aceitacao or \
                                    transicoes.get((transicoes.get((estados[i], zymbolo)),symbol)) in estados_aceitacao and transicoes.get((transicoes.get((estados[i], symbol)), zymbolo)) not in estados_aceitacao or \
                                    transicoes.get((transicoes.get((estados[j], symbol)),zymbolo)) in estados_aceitacao and transicoes.get((transicoes.get((estados[i], zymbolo)), symbol)) not in estados_aceitacao or \
                                    transicoes.get((transicoes.get((estados[j], zymbolo)),symbol)) in estados_aceitacao and transicoes.get((transicoes.get((estados[i], symbol)), zymbolo)) not in estados_aceitacao:
                                        tabela_equivalencia[i][j] = tabela_equivalencia[j][i] = False

        # Construir gupos de estados equivalentes
        grupos_equivalentes = []
        estados_visitados = set()

        # Obtém o indíce dos estados
        for i in range(len(tabela_equivalencia)):
            if i not in estados_visitados:
                grupo_atual = {i}
                estados_visitados.add(i)

                # para todo estado[i] e estado[j] que estiver na tabela equivalencia, une-os
                for j in range(i + 1, len(tabela_equivalencia)):
                    if tabela_equivalencia[i][j]:
                        grupo_atual.add(j)
                        estados_visitados.add(j)

                grupos_equivalentes.append(grupo_atual)

        # Construir um novo conjunto de estados minimizado
        estados_minimizados = []

        for grupo in grupos_equivalentes:
            representante = estados[min(grupo)]
            estados_minimizados.append(representante)

        # Criar novo conjunto de transições minimizado
        transicoes_minimizadas = {}

        for representante in estados_minimizados:
            for simbolo in alfabeto:
                transicao_original = transicoes.get((representante, simbolo), None)

                if transicao_original is not None:
                    # Encontrar o representante do grupo de estados equivalentes do estado original
                    index_original = estados.index(transicao_original)
                    grupo_destino = next(i for i, grupo_destino in enumerate(grupos_equivalentes) if index_original in grupo_destino)
                    estado_destino = estados_minimizados[grupo_destino]

                    # Atualizar a transição minimizada
                    transicoes_minimizadas[(representante, simbolo)] = estado_destino

        # Identificar novo estado inicial e estados de aceitação minimizados
        estado_inicial_minimizado = estados_minimizados[grupos_equivalentes.index(next(grupo for grupo in grupos_equivalentes if estados.index(estado_inicial) in grupo))]
        estados_aceitacao_minimizados = set()

        # Adicionar aos estados de aceitação minimizados apenas os estados equivalentes que eram de aceitação
        for grupo in grupos_equivalentes:
            if any(estados[estado] in estados_aceitacao for estado in grupo):
                estados_aceitacao_minimizados.update(estados[estado] for estado in grupo)

        # Remover os estados que não foram minimizados e coloca em ordem os estados
        estados_aceitacao_minimizados = {estado for estado in estados_aceitacao_minimizados if estado in estados_minimizados}
        estados_aceitacao_minimizados = sorted(estados_aceitacao_minimizados)

        # Geração da tabela de equivalência
        print("\nTabela de Equivalência:")
        print("\t" + "   \t".join(estados))
        for i, row in enumerate(tabela_equivalencia):
            print(f"{estados[i]}\t", end="")
            for col in row:
                print(col, end="\t")
            print()

        # Geração dos grupos equivalentes
        print("\nGrupos Equivalentes:")
        for grupo in grupos_equivalentes:
            estados_modificados = [{'q' + str(estado)} for estado in grupo]
            print(estados_modificados)


        print("\nEstados minimizados:", estados_minimizados)
        print("Transições minimizadas:", transicoes_minimizadas)
        print("Estado inicial minimizado:", estado_inicial_minimizado)
        print("Estados de aceitação minimizados:", estados_aceitacao_minimizados)

        return estados_minimizados, alfabeto, transicoes_minimizadas, estado_inicial_minimizado, estados_aceitacao_minimizados

    minimizar_afd(estados, alfabeto, transicoes, estado_inicial, estados_finais)


# =====================================================================
# PARTE 2
# =====================================================================


def testaPalavras():
    def ler_automato(file_path):
        tuplas_3_elementos = []
        # Abre o arquivo e lê a linha
        with open(file_path, 'r') as file:
            line = file.readline()

            # Encontrar o padrão dentro das chaves {}
            pattern = re.compile(r'{(.*?)}')

            # Encontrar todas as correspondências do padrão na linha
            matches = re.findall(pattern, line)

            # Separar cada correspondência em uma lista e armazenar em uma lista principal
            variables = [list(map(str.strip, match.split(','))) for match in matches]

            entrada = line

            # Como o valor da posição inicial não segue um padrão igual os outros valor vamos caça-lo
            finalmente = ""
            achou = 0
            flagDois = 0
            # Vamos percorrer até achar o segundo fecha chaves que é onde vamos encontrar o inicio do valor desejado
            for i in entrada:
                if i == '}':
                    achou += 1
                elif achou == 2:
                    if i == ',':
                        flagDois += 1
                    # Após usarmos duas flags para delimitar onde começa (segundo }) e onde acaba (segunda , depois do segundo })
                    # Então agora pegamos esses valroes e o colocamos na variavel que será devolvida ao usuario
                    if i != ',' and flagDois < 2:
                        finalmente = finalmente + i

            # Pula a segunda linha
            file.readline()
            # Processa as linhas restantes
            for linha in file:
                # Utiliza expressão regular para encontrar elementos entre chaves
                match = re.match(r"\((.*?)\)", linha)
                if match:
                    elementos_3upla = match.group(1).split(',')
                    tuplas_3_elementos.append(tuple(elementos_3upla))

            # Retorna os resultados
        alfabeto_final = [caracter[1:] if caracter.startswith('{') else caracter for caracter in variables[0]]
        return None, alfabeto_final, variables[1], finalmente, variables[2], tuplas_3_elementos

    # Solicita o nome do arquivo ao usuário com extensão .txt
    nome_arquivo_usuario = input(
        "Digite o nome do arquivo (sem extensão, será adicionado automaticamente .txt): ") + ".txt"

    # Chama a função para ler o automato
    nome_automato, alfabeto, estados, estado_inicial, estados_finais, tuplas_3_elementos = ler_automato(
        nome_arquivo_usuario)

    nome_arquivo = input("Digite o nome do arquivo (sem a extensão): ")
    nome_arquivo = f"{nome_arquivo}.txt"

    try:
        with open(nome_arquivo, 'r') as arquivo:
            # Leia o conteúdo do arquivo
            conteudo = arquivo.read()

        # Divida as palavras com base na vírgula
        entrada_total = conteudo.split(',')

    except FileNotFoundError:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    # Vamos resolver este problema usando uma recursão
    def recucando(estados_finais, tuplas_3_elementos, char, estado_atual):

        # Uma variavel local só para ir somando o quanto temos
        aq = 0

        # Se não temos mais palavras na fita e estamos em um estado de aceitação então aceitamos
        if len(char) == 0:
            if estado_atual in estados_finais:
                return 1

        # Vamos percorrer todos os caminhos, partindo do estado atual, que aceitam a nossa palavra que está sendo lida da fita
        if len(char) > 0:
            # Procuramos por todas as transições
            for est in tuplas_3_elementos:
                # Se o estado é uma transição do estado atual
                if est[0] == estado_atual:
                    # então vemos se ele aceita a nossa palavra que está sendo lida na fita
                    if est[1] == char[0]:
                        # se for o caso vamos para esse estado e continumaos a busca
                        passando = char[1:]
                        aq += recucando(estados_finais, tuplas_3_elementos, passando, est[2])

        return aq

    # para cada palavra pegamos a lista de caracteres dela
    for lista in entrada_total:
        lista_chars = list(lista)
        # Esta é nossa flag para sabermos se a palvra pertence ou não a linguagem
        tot = 0
        tot = recucando(estados_finais, tuplas_3_elementos, lista_chars, estado_inicial)
        if tot > 0:
            print("A PALAVRA", lista_chars, "PERTENCE A LINGUAGEM")
        else:
            print("A PALAVRA", lista_chars, "NÃO PERTENCE A LINGUAGEM")


# ===============================================================
# PARTE 3
# =====================================================================


def acharVazio():
    def ler_automato(file_path):
        tuplas_3_elementos = []
        # Abre o arquivo e lê a linha
        with open(file_path, 'r') as file:
            line = file.readline()

            # Encontrar o padrão dentro das chaves {}
            pattern = re.compile(r'{(.*?)}')

            # Encontrar todas as correspondências do padrão na linha
            matches = re.findall(pattern, line)

            # Separar cada correspondência em uma lista e armazenar em uma lista principal
            variables = [list(map(str.strip, match.split(','))) for match in matches]

            entrada = line

            # Verificar se encontrou correspondência e extrair o valor
            # Como o valor da posição inicial não segue um padrão igual os outros valor vamos caça-lo
            finalmente = ""
            achou = 0
            flagDois = 0
            # Vamos percorrer até achar o segundo fecha chaves que é onde vamos encontrar o inicio do valor desejado
            for i in entrada:
                if i == '}':
                    achou += 1
                elif achou == 2:
                    if i == ',':
                        flagDois += 1
                    # Após usarmos duas flags para delimitar onde começa (segundo }) e onde acaba (segunda , depois do segundo })
                    # Então agora pegamos esses valroes e o colocamos na variavel que será devolvida ao usuario
                    if i != ',' and flagDois < 2:
                        finalmente = finalmente + i

            # Pula a segunda linha
            file.readline()
            # Processa as linhas restantes
            for linha in file:
                # Utiliza expressão regular para encontrar elementos entre chaves
                match = re.match(r"\((.*?)\)", linha)
                if match:
                    elementos_3upla = match.group(1).split(',')
                    tuplas_3_elementos.append(tuple(elementos_3upla))

            # Retorna os resultados
        alfabeto_final = [caracter[1:] if caracter.startswith('{') else caracter for caracter in variables[0]]
        return None, alfabeto_final, variables[1], finalmente, variables[2], tuplas_3_elementos

    # Solicita o nome do arquivo ao usuário com extensão .txt
    nome_arquivo_usuario = input(
        "Digite o nome do arquivo (sem extensão, será adicionado automaticamente .txt): ") + ".txt"

    # Chama a função para ler o automato
    nome_automato, alfabeto, estados, estado_inicial, estados_finais, tuplas_3_elementos = ler_automato(
        nome_arquivo_usuario)

    # Decide se a linguagem gerada pelo AFD é vazia
    def linguagemVazia(upla, inicial, alfabeto, final):

        vazio = 0
        ja_passei = []

        def recurssando(upla, inicial, alfabeto, final, ja_passei):

            # verifica se já passamos por algum estado, fazemos isso para evitar loop entre estados
            ja_passei.append(inicial)

            estados_alcancados = []
            temp = 0

            # Verifica se o estado inicial também é um estado final, se for o caso o automato aceita a palavra vazia
            for k in final:
                if k == inicial:
                    return 1

            # Achando todos os estado alcançados pelo estado inicial
            # percorre todas os elementos da lista de 3-uplas
            for achar in upla:
                # Se achar alguma transição que começe com o estado inicial
                if achar[0] == inicial:
                    # Então ve se a transição envolve algum simbolo do alfabeto
                    for i in alfabeto:
                        # Se esse for o caso coloca esse estado em uma lista
                        if achar[1] == i and achar[2] != inicial:
                            # Agora vamo ver se já não vizitamos esse estado
                            if achar[2] not in ja_passei:
                                estados_alcancados.append(achar[2])

            # vamos fazer o mesmo para cada estado que achamdos
            for i in estados_alcancados:
                temp += recurssando(upla, i, alfabeto, final, ja_passei)

            return temp

        vazio = recurssando(upla, inicial, alfabeto, final, ja_passei)
        if vazio > 0:
            print("LINGUAGEM NÃO VAZIA")
        else:
            print("LINGUAGEM VAZIA")

    linguagemVazia(tuplas_3_elementos, estado_inicial, alfabeto, estados_finais)


# =====================================================================
# MAIN
# =====================================================================


# Um simples menu
looping = 0
while looping < 4:
    looping = int(input(
        "Escolha uma busca:\n - 1 SIMPLIFICAR AUTOMATO\n - 2 TESTAR LISTA DE PALAVRAS\n - 3 AUTOMATO VAZIO?\n - 4 SAIR\n"))
    if looping == 1:
        func1()
    elif looping == 2:
        testaPalavras()

    elif looping == 3:
        acharVazio()