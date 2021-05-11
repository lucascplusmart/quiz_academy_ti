# importando bibliotecas standart do python
from os import system, name
from time import sleep
from random import choice

# bibliotecas baixadas
from rich import box, print
from rich.console import Console
from rich.table import Table
from getch import getch # py-getche
from tabulate import tabulate
from core import getpass_ak

# importando arquivos do banco de dados e das artes ASCII
from core.banner import printB, finalizado
from core.database import *

# inicia o console do rich
console = Console()

#---------------------------------------------------------------------------


# Funcionalidades

# Funcoes Perguntas
def perguntaFeita():
    global listaFeita

    listaFeita = [] # lista  das perguntas/COD que o usuario já fez
    result = consultData_content_user(LoginID)
    for linha in result:
        listaFeita.append(linha["COD"])   

# Perguntas(COD) que o usuario não fez 
def perguntaNaoFeita():
    global listaNaoFeita

    listaNaoFeita = []
    result = consultData_content()
    for linha in result:
        if (linha["COD"] not in listaFeita):
            listaNaoFeita.append(linha["COD"])

# pega o necessário pra funcao da pergunta rodar
def prePergunta():
    perguntaFeita()
    perguntaNaoFeita()
    codigo()
    pergunta(cod)

def sairPerg():
    print('\n1. Continuar', '\n2. Sair\n')
    escolha=0
    while escolha !='2':
        escolha = str(input('\n -> '))
        if escolha == '1':
            limpaTela()
            prePergunta()

        elif escolha == '2':
            animacao("[bold cyan]Saindo...", 0.6)
            abrirPrimeiraTela(0.6)

        else:
            print("[bold red]\nEscolha inválida.")

# pega quantidade de perguntas ja feitas, o codigo das perguntas nao feitas e retorna mensagem se respondeu todas.
def codigo():
    global cod
    qtd = len(listaNaoFeita)

    if qtd>=1:
        cod = choice(listaNaoFeita)

    else:
        print('\n')
        animacao("[bold green]",2) 
        print("[bold green]Você respondeu todas as perguntas, é um expert nesse assunto!")
        sleep(1.3)
        finalizado()
        abrirPrimeiraTela(4)

# funcoes de utilidades, sair de tela, timer, limpar tela, animacao

def abrirMenu(tempo):
    sleep(tempo)
    limpaTela()
    Menu() 

def abrirPrimeiraTela(tempo):
    sleep(tempo)
    limpaTela()
    primeiraTela()

def abrirPergunta(tempo):
    sleep(tempo)
    limpaTela()
    prePergunta()

def abrirPerfil(tempo):
    sleep(tempo)
    limpaTela()
    perfil()

def abrirRkgTela(tempo):
    sleep(tempo)
    limpaTela()
    rankingTela()

def abrirRkgMenu(tempo):
    sleep(tempo)
    limpaTela()
    rankingMenu()

def sair(tempo):
    animacao("[bold cyan]Saindo...", tempo)
    print('\nAté mais! :)')
    sleep(0.5)    
    exit()

def logoff(tempo):
    animacao("[bold cyan]Saindo...", tempo)
    limpaTela()
    abrirMenu(0)    

def reset(tempo):
    sleep(tempo)
    limpaTela()

def linhas():
    print('_' * 30)

def animacao(texto, tempo):
    with console.status(texto) as status:
        sleep(tempo)

def limpaTela():
    system('cls || clear')
    printB()

# -------------------------------------------------------------------------

#Funcoes Login e Cadastro

def Registro():
    global dataReg
    global nomeReg

    nomeReg = str(input('\nNome completo: '))

    while len(nomeReg) < 10:
        print("[bold red]Informação incompleta. Digite seu nome novamente.")
        nomeReg = str(input('Nome completo: '))

    nickReg = str(input('Nickname: '))

    nickDict = []
    listaNicks=consultData_user()

    for i in listaNicks:
        nicknames = (i['nickname']) # pega lista de nicks no banco de dados
        nickDict.append(nicknames)

    while nickReg in nickDict: # vê se o nick já está cadastrado
        print("[bold red]Nickname já cadastrado. Tente novamente")
        nickReg = str(input('Nickname: '))

    dataReg = str(input("Data de nascimento: "))
    while len(dataReg) < 10:
        print("[bold red]Informação incompleta. Tente novamente.") 
        dataReg=str(input('Data de nascimento: '))

    senhaReg = (getpass_ak.getpass('Crie uma senha com 6 caracteres: '))
    while len(senhaReg) < 6:
        print("[bold red]A senha precisa ter no mínimo 6 caracteres.")
        senhaReg = (getpass_ak.getpass('Senha: '))

    senhaReg2 = (getpass_ak.getpass('Confirme sua senha: '))
    while len(senhaReg2) < 6:
        print("[bold red]A senha precisa ter no mínimo 6 caracteres.")
        senhaReg2 = (getpass_ak.getpass('Confirme sua senha: '))

    if senhaReg2 == senhaReg:
        add_user(nickReg, nomeReg, senhaReg, dataReg) # cadastra usuario no banco de dados
        animacao("[bold green]Cadastrando...", 1.35)
        print("[bold green]\nCadastro concluido com sucesso!")
        reset(0.8)

    else:
        print('[bold red]As senhas não correspondem. Digite sua senha novamente: ')
        senhaReg2 = (getpass_ak.getpass(''))

        if senhaReg2 == senhaReg:
            add_user(nickReg, nomeReg, senhaReg, dataReg) # cadastra usuario no banco de dados
            animacao("[bold green]Cadastrando...", 1.35)
            print("[bold green]\nCadastro concluído com sucesso!")
            reset(0.8)
    
def Login():
    
    listaUsuarios = consultData_user() # pega lista de usuarios
    usuariosDict = {} # cria um dicionario pra guardar o nick e a senha do login
    usuariosDictScore = {}
    usuarioDictID = {}

    for t in listaUsuarios: 
        listaNick = (t['nickname']) # lista de nicks do banco de dados
        listaSenha = (t['senha'])  
        listaScore = (t['score']) 
        listaID = (t['ID'])

        usuariosDict[listaNick] = listaSenha # coloca nick como key e senha como value
        usuariosDictScore[listaNick] = listaScore 
        usuarioDictID[listaNick] = listaID

    global nickLogin # pra usar o nick (ou nome) quando fizer login
    global scoreLogin
    global LoginID

    nickLogin = str(input('\nNickname: ')) 
    senhaLogin = getpass_ak.getpass('Senha: ')

    if nickLogin in usuariosDictScore: 
        scoreLogin = usuariosDictScore[nickLogin]

    if nickLogin in usuarioDictID: 
        LoginID = usuarioDictID[nickLogin]    

    # checa se os dados de login estão corretos
    if nickLogin in usuariosDict and usuariosDict[listaNick] == senhaLogin:
        animacao("[bold green]Entrando...", 1.35)

        print("[bold green]\nLogin feito com sucesso!")  
        abrirPrimeiraTela(0.6)

    else:
        animacao("[bold red] ", 1.35)
        print('[bold red]\nUsuário não existe ou senha incorreta.')
        reset(0.8)

# ---------------------------------------------

# submenus

def perfil():
    #updata_user()
    r = consultData_user_id(LoginID)

    nome = r[0]['nome']
    senhaLogin = r[0]['senha']

    print(nome)
    print(nickLogin)
    print('\n1. Trocar nick')
    print('2. Trocar senha')
    print('3. Deletar conta')
    print('9. Voltar')
    escolha=0

    while escolha !='3':
        escolha=str(input('-> '))
        
        if escolha=='1':
            print(nickLogin)
            novoNick=str(input('\nDigite novo nick: '))
            nickDict = []
            listaNicks=consultData_user()

            for i in listaNicks:
                nicknames = (i['nickname'])
                nickDict.append(nicknames)

            while novoNick in nickDict: 
                print("[bold red]Nickname já cadastrado. Tente novamente")
                novoNick = str(input('Digite seu novo nick: '))
            print("Você tem certeza que deseja trocar de nick? (S/N)")
            escolhaLog=getch()
            if escolhaLog=='S' or 's':
                animacao("Trocando nick...", 1)
                print("[bold green]Mudança de nick feita com sucesso!")

        elif escolha=='2':
            # se for senha incorreta WHILE
            senhaAtual=str(input('\nDigite sua senha atual: '))
            if senhaAtual == senhaLogin:
                novaSenha=str(input('\nDigite sua nova senha: '))
                while len(novaSenha)<6:
                    print("[bold red]A senha precisa ter no mínimo 6 caracteres!")
                    novaSenha=str(input('\nDigite sua nova senha: '))
                if novaSenha == senhaLogin:
                    print("[bold red]As senhas não podem ser iguais!")
                    novaSenha=str(input('\nDigite sua nova senha: '))
                else:
                    updata_user(nickLogin, novaSenha, LoginID)
            else:
                print("[bold red]Senha incorreta.")
            
        elif escolha=='3':
            print("Você tem certeza? (S/N)")
            escolhaDel=getch()
            if escolhaDel=='S' or escolhaDel=='s':
                animacao("[bold red]Deletando conta...", 1)
                del_user(LoginID)
                print("[bold green]Conta deletada com sucesso!")
                abrirMenu(0.9)
            else:
                animacao("",0)
                abrirPrimeiraTela(0.7)
        
        elif escolha=='9':
            animacao("[bold cyan]Voltando...", 0.7)
            abrirPrimeiraTela(0)
            

def rankingTela():
    
    listaRanking = consultData_ranking_user()
    cont = 1

    print('\n')

    # cria tabela de rank
    table = Table(show_header=True, header_style="bold green", box=box.DOUBLE_EDGE)
    table.add_column("Rank", style="dim", width=4)
    table.add_column("   Nickname", style="dim", width=14)
    table.add_column("Pts", justify="right", style="dim", width=3)

    for t in listaRanking: 
        listaNickRkg = (t['nickname']) 
        listaScoreRkg = (t['score'])

        table.add_row(""+str(cont)+"º", listaNickRkg, str(listaScoreRkg))
        cont+=1

    console.print(table)   
    
    print('\nPressione qualquer tecla para voltar...')
    
    voltar = getch()

    if voltar != '':
        abrirPrimeiraTela(0.5)
    else:
        abrirPrimeiraTela(0.5) 

def rankingMenu():
    print("menu/ranking")
    listaRanking = consultData_ranking_user()
    cont = 1
    print('\n')

    # cria tabela de ranking
    table = Table(show_header=True, header_style="bold green", box=box.DOUBLE_EDGE, )
    table.add_column("Rank", style="dim", width=4)
    table.add_column("   Nickname", style="dim", width=14)
    table.add_column("Pts", justify="right", style="dim", width=3)

    for t in listaRanking: 
        listaNickRkg = (t['nickname']) 
        listaScoreRkg = (t['score'])

        table.add_row(""+str(cont)+"º", listaNickRkg, str(listaScoreRkg))
        cont+=1

    console.print(table)

    print("\nPressione qualquer tecla para voltar...")

    voltar=getch()
    if voltar != '':
        abrirMenu(0)
    else:
        abrirMenu(0) 

#---------------------------------------------------------------------

# Funcao principal da Pergunta

def pergunta(num):
    escolha = 0
    resp = 0

    # pega lista de pergunta e alternativa
    listaPergunta = consultData_content_search(num)
    listaAlternativas = consultData_alternatives(num)

    for i in listaPergunta:
        titulo = (i['titulo'])
        resposta = (i['resposta'])
        pergunta = (i['pergunta'])
        pontuacao = (i['pontuacao'])
        dica = (i['dica'])
        info = (i['informacao'])

    # transforma o titulo numa grid
    text = str(titulo)
    table = [[text]]
    output = tabulate(table, tablefmt='fancy_grid')

    print(output)
    print(pergunta)
    linhas()
    
    #printa as alternativas
    for i in listaAlternativas:
        alternativas = (i['opcao'])
        descricao = (i['descricao'])
        print('\n ' + alternativas + ' - ' + descricao)
    linhas()

    print('\n1. Responder')
    print('2. Dica')
    print('9. Sair')

    escolha=0

    while escolha != '9':
        escolha=input('\n-> ')

        if escolha == '1':
            resp = input('\nResposta -> ').upper()

            if resp =='A' or resp=='B' or resp=='C' or resp=='D':
                    continuaPerg(resposta, resp, pontuacao, info)
            else:
                print("[bold red]\nEscolha inválida.")

        elif escolha == '2':
            print('\n' + dica)
            resp = input('\nResposta -> ').upper()

            if resp =='A' or resp=='B' or resp=='C' or resp=='D':
                continuaPerg(resposta, resp, pontuacao, info)   
            else:
                print("[bold red]\nEscolha inválida.")           

        elif escolha == '9':
            animacao("[bold cyan]Saindo...", 0.8)
            abrirPrimeiraTela(0)
        
        else:
            print("[bold red]\nEscolha inválida.")

def continuaPerg(resposta, resp, pontuacao, info):
    animacao("[bold cyan]Sua resposa está...", 1.3)
    
    if resp == resposta:
        print("[bold green]\nCorreta!")

        # pega score atual e soma com pontos da pergunta
        r = consultData_user_id(LoginID) 
        scoreID = r[0]['score']
        pontuacaoTotal = scoreID + pontuacao
        
        updata_user_score(pontuacaoTotal, LoginID)
        add_responde(LoginID, cod)
        sairPerg()

    else:
        print("[bold red]\nErrada!")
        print(f'\nA resposta correta é a letra [bold green]{resposta}.')
        print(f'\n{info}','\n')
        add_responde(LoginID, cod)
        sairPerg()

#-----------------------------------------------------------------

# menu secundário

def primeiraTela():
    escolha = 0
    score = consultData_user_id(LoginID) # pega score atualizado

    while escolha != '9':
        print(f'\nNick: {nickLogin}')
        print('Score: ',score[0]['score'])

        print("\n[bold white][ [bold cyan]1 [bold white]] - Iniciar")
        #print("[bold white][ [bold cyan]2 [bold white]] - Perfil")
        print("[bold white][ [bold cyan]3 [bold white]] - Ranking")
        print("[bold white][ [bold cyan]9 [bold white]] - Sair")
        linhas()

        escolha = str(input('\nEscolha uma opção -> '))

        if escolha == '1':
            abrirPergunta(0.5)

        elif escolha == '2':
            abrirPerfil(0.5)
        
        elif escolha == '3':
            abrirRkgTela(0.5)
        
        elif escolha == '9':
            logoff(0.8)

        else:
            (print('[bold red]\nEscolha inválida. Tente novamente')) 
            abrirPrimeiraTela(0.8)

# menu principal


def Menu():
    escolha = 0
   
    while escolha != '9':      
        print("[bold white]\n\n[ [bold cyan]1 [bold white]] - Login")
        print("[bold white][ [bold cyan]2 [bold white]] - Cadastro")
        print("[bold white][ [bold cyan]3 [bold white]] - Ranking")
        print("[bold white][ [bold cyan]9 [bold white]] - Sair ")
        print('_'*30)
        
        escolha=str(input('\nEscolha uma opção -> '))

        if escolha == '1':
            sleep(0.2)
            Login()         

        elif escolha == '2':
            sleep(0.2)
            Registro()

        elif escolha == '3':
            abrirRkgMenu(0.2)
        
        elif escolha =='9':
            sair(1.2)

        else:
            print("[bold red]\nEscolha inválida. Tente novamente")
            abrirMenu(0.8)



printB()
Menu()
