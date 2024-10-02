import re

def criar_estadoAFND(nome): # Função para criar o estado AFND
    novo_estado = {
        'nome' : nome, # Nome do estado
        'se_h': [], # Lista de transições se vazio (representada por 'h')
        'se_1': [], # Lista de transições se leu 1
        'se_0': [] # Lista de transições se leu 0
    }
    AFND.append(novo_estado)

def transicao_AFND(nome,lido,transicao): # Função para adicionar as transições a lista
    for estado in AFND:
        # Lido é para o estado lido na transição , transicao é para aonde vai , nome é aonde esta
        if(estado['nome'] == nome):
            if(lido == '1'):
                estado['se_1'].append(transicao)
            if(lido == '0'):
                estado['se_0'].append(transicao)
            if(lido == 'h'):
                estado['se_h'].append(transicao) # Transição vazia

def lerAFND(arquivo):
    with open(arquivo + ".txt", "r") as f:
        estados_string = f.readline().rstrip() # Pega a primeira linha do arquivo (contem os estados)
        estados_separados = re.split(r'\s+', estados_string)
        for estado in estados_separados:
            # Criar os estados
            criar_estadoAFND(estado) 
        inicial = f.readline().rstrip()
        global EstadoInicial # Pega a segunda linha com o estado incial
        EstadoInicial = inicial
        global EstadoFinal # Estado Final
        finais_string = f.readline().rstrip()
        finais_separados = re.split(r'\s', finais_string)
        for final in finais_separados:
            # Salva os estados finais no array
            EstadoFinal.append(final) 
        for linha in f:
            componentes = re.split(r'\s', linha)
            transicao_AFND(componentes[0],componentes[1],componentes[2])

def converter_AFND_AFD():
    global EstadoInicial
    # Tratamento do estado inicial
    vdd_estado_inicial = transicao_vazia([EstadoInicial]) # Faz o caminho de transição Vazia
    vdd_estado_inicial = sorted(list(set(vdd_estado_inicial) | set([EstadoInicial]))) # Junta transição vazia com estado inicial (organizado e sem repetidos)
    nome_estado_inicial = "".join(vdd_estado_inicial) # Da o nome do estado inicial (todos os estados q ele é composto)
    global EstadoInicialAFD
    EstadoInicialAFD = nome_estado_inicial # Salva o estado inicial separadamente (para maquina de estados)
    criar_Estado_Composto(nome_estado_inicial, vdd_estado_inicial) #finalmente salva o estado inicial no dicionario
    estados_criados = 1
    while estados_criados > 0:
        estados_criados = 0 #Ele loopa tentando criar estados frutos das transições dos estados
        for estado in AFD:
            if estado['se_1'] == 'não testado':
                passo_vazio = transicao_vazia(estado['estados_superposicao'])
                passos_primario = list(set(passo_vazio) | set(estado['estados_superposicao']))
                passos_um , passos_zero = transicao_normal(passos_primario)
                if passos_um:
                    passos_um = sorted(list(set(passos_um) | set(transicao_vazia(passos_um))))
                    nome_passos_um = "".join(passos_um)
                    estado['se_1'] = nome_passos_um
                    n_tem = 1
                    for x in AFD:
                        if nome_passos_um == x['nome']:
                            n_tem = 0
                    if n_tem == 1:
                        criar_Estado_Composto(nome_passos_um, passos_um)
                        estados_criados += 1 # Se um estado novo foi criado o loop continua para passar por ele
                else:
                    estado['se_1'] = 'testado'
                if passos_zero:
                    passos_zero = sorted(list(set(passos_zero) | set(transicao_vazia(passos_zero))))
                    nome_passos_zero = "".join(passos_zero)
                    estado['se_0'] = nome_passos_zero
                    n_tem = 1
                    for x in AFD:
                        if nome_passos_zero == x['nome']:
                            n_tem = 0
                    if n_tem == 1:
                        criar_Estado_Composto(nome_passos_zero, passos_zero)
                        estados_criados += 1
                else:
                    estado['se_0'] = 'testado'

def transicao_vazia(estados): # Recebe array dos estados compostos
    caminhovazio = []
    for estado in estados:
        for transicao in AFND:
            if transicao['nome'] == estado:
                if transicao['se_h']:
                    # Se_H é array tem q pegar cada valor individual do array e n o array inteiro , NÃO PODE TER VALOR REPETIDO NO caminhovazio
                     for destino in transicao['se_h']:
                        repete = 0
                        for x in caminhovazio:
                            if(destino == x):
                                repete += 1
                        if repete == 0:
                            caminhovazio.append(destino)
    if caminhovazio:
        caminhovazio_tamanho = 0
        while len(caminhovazio) != caminhovazio_tamanho:
            caminhovazio_tamanho = len(caminhovazio)
            for estado in caminhovazio:
                for transicao in AFND:
                    if transicao['nome'] == estado:
                        if transicao['se_h']:
                            for destino in transicao['se_h']:
                                repete = 0
                                for x in caminhovazio:
                                    if (destino == x):
                                        repete += 1
                                if repete == 0:
                                    caminhovazio.append(destino)
    return caminhovazio # Retorna todos os caminhos q passa por passar em vazio

def transicao_normal(estados):
    caminho_um = []
    caminho_zero = []
    for estado in estados:
        for transicao in AFND:
            if transicao['nome'] == estado:
                if transicao['se_1']:
                    # Se_H é array tem q pegar cada valor individual do array e n o array inteiro , NÃO PODE TER VALOR REPETIDO NO caminhovazio
                     for destino in transicao['se_1']:
                        repete = 0
                        for x in caminho_um:
                            if(destino == x):
                                repete += 1
                        if repete == 0:
                            caminho_um.append(destino)
    for estado in estados:
        for transicao in AFND:
            if transicao['nome'] == estado:
                if transicao['se_0']:
                    # Se_H é array tem q pegar cada valor individual do array e n o array inteiro , NÃO PODE TER VALOR REPETIDO NO caminhovazio
                     for destino in transicao['se_0']:
                        repete = 0
                        for x in caminho_zero:
                            if(destino == x):
                                repete += 1
                        if repete == 0:
                            caminho_zero.append(destino)
    return caminho_um , caminho_zero

def criar_Estado_Composto(nome, estados): # Criar um valor no dicionario de estados compostos (AFD)
    novo_estado = {
        'nome' : nome,
        'estados_superposicao' : estados,
        'se_1': 'não testado',
        'se_0': 'não testado'
    }
    AFD.append(novo_estado)

def salvar_AFD(arqv):
    with open(arqv + "_AFD.txt",'x') as salvar:
        linha_0 = ""
        for estado in AFD:
            linha_0 = linha_0 + estado['nome'] + " "
        salvar.write(linha_0 + "\n")
        global EstadoInicialAFD
        salvar.write(EstadoInicialAFD + "\n")
        linha_2 = ""
        for estado in EstadoFinalAFD:
            linha_2 = linha_2 + estado + " "
        salvar.write(linha_2 + "\n")
        # Inserir as transições 
        for estado in AFD:
            if estado['se_1'] != 'testado':
                salvar.write(estado['nome'] + " 1 " + estado['se_1'] + "\n")
            if estado['se_0'] != 'testado':
                salvar.write(estado['nome'] + " 0 " + estado['se_0'] + "\n")

def definir_Estado_Final_AFD():
    global EstadoFinal, EstadoFinalAFD
    for finalN in EstadoFinal:
        for estado in AFD:
            for subEstado in estado['estados_superposicao']:
                if finalN == subEstado:
                    EstadoFinalAFD.append(estado['nome'])
    EstadoFinalAFD = sorted(list(set(EstadoFinalAFD))) # Set tira repetido , list faz isso voltar a ser uma lista , sorted e pra organizar 

def maquina_AFD(palavra):
    EstadoAtual = EstadoInicialAFD
    for letra in palavra:
        if letra == "1":
            for estado in AFD:
                if estado['nome'] == EstadoAtual:
                    EstadoAtual = estado['se_1']
                    break
        elif letra == "0":
            for estado in AFD:
                if estado['nome'] == EstadoAtual:
                    EstadoAtual = estado['se_0']
                    break
        else:
            return "não aceito"
        if EstadoAtual == "testado":
            return "não aceito"
    for finais in EstadoFinalAFD:
        if finais == EstadoAtual:
            return "aceito"
    return "não aceito"

def testar_texto(arquivo):
    with open(arquivo + ".txt",'r') as palavras:
        with open(arquivo + "_Resultado.txt", 'x') as resultado:
            for palavra in palavras:
                resultado.write(palavra.strip() + " " + maquina_AFD(palavra.strip()) + "\n")

def limpar_memoria():
    global EstadoFinal, EstadoFinalAFD ,EstadoInicial, EstadoInicialAFD, AFD, AFND
    AFND = [] # Array de dicionarios de estados AFND
    AFD = [] # Array de dicionarios de estados AFD
    EstadoInicial = "NULL"
    EstadoInicialAFD = "NULL"
    EstadoFinal = []
    EstadoFinalAFD = []

AFND = [] # Array de dicionarios de estados AFND
AFD = [] # Array de dicionarios de estados AFD
EstadoInicial = "NULL"
EstadoInicialAFD = "NULL"
EstadoFinal = []
EstadoFinalAFD = []
while True:
    print ("------------------------\n"+"Codigo AFND,escolha o que deseja fazer\n" + "Opção 1 Converter AFND para AFD\n" +
            "Opção 2 usar o AFD para testar\n" + "Opção 3 fechar o programa")
    if not AFD: print("Sem AFD na memoria\n")
    else : print("Com AFD na memoria\n")
    op = input("Opção : ")
    if op == '1':
        limpar_memoria()
        arqv = input("digite o nome do arquivo AFND (sem .txt) : ")
        lerAFND(arqv)
        converter_AFND_AFD()
        definir_Estado_Final_AFD()
        salvar = input("Deseja salvar o arquivo AFD? (s/n) : ")
        if salvar == 's':
            nome = input("Digite um nome para o arquivo : ")
            salvar_AFD(nome)
    elif op == '2' and not AFD:
        print("Não tem AFD salvo na memoria por favor carregue um \n")
    elif op == '2' and AFD:
        arqv = input("Digite o nome do arquivo : ")
        testar_texto(arqv)
    elif op == '3':
        break