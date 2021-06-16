from core.quiz import StartQuiz, CheckQuiz
from core.functions import Functions
from core.database.database import DataUser
from core.trees.trees import Trees
from core.banner import Banner
from core import getpass_ak

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

from getch import getch
from rich import print, box
from time import sleep
from os import system

quiz = StartQuiz()
func = Functions()
db = DataUser()
console = Console()
bann = Banner() 
check = CheckQuiz()

# classe contendo todas as telas do projeto
class Screens:
    def __init__(self):
        self.choice = 0

    def firstScreen(self, idUser):
        sctree.firstScreenTree()

        while True:
            r = db.consultData_user_id(idUser) # pega score atualizado
            nick = r[0]['nickname']
            score = r[0]['score']

            dados = f"[bold white]Nome: [bold green]{nick}[/bold green]\n[bold white]Score: [bold green]{score}"
            func.caixa = (dados)

            while self.choice != '9':
                print()
                print("[bold white][ [bold cyan]1 [bold white]] - Iniciar".center(99))
                print("[bold white][ [bold cyan]2 [bold white]] - Perfil".center(99))
                print("[bold white][ [bold cyan]3 [bold white]] - Ranking".center(99))
                print("[bold white][ [bold cyan]9 [bold white]] - Sair".center(97))
                print('\n')
                print('Escolha uma opção -> '.center(68))

                self.choice = input()

                if self.choice == '1':
                    func.clear()
                    bann.banner()
                    func.sound('menu')
                    check.checkQuiz(idUser)
                    
                elif self.choice == '2':
                    func.sound('menu')
                    profile.profile(idUser)                    
                
                elif self.choice == '3':
                    func.sound('menu')
                    func.clear()
                    screens.rankingFirstScreen()                    
                
                elif self.choice == '9':
                    func.sound('menu')
                    exit()

                else:
                    print('[bold red]\nEscolha inválida. Tente novamente')
                    func.sound('error')
                    sctree.firstScreenTree()
    
    def rankingFirstScreen(self):
        bann.banner()
        print()
        console = Console()
        tree = Trees("ranking", "# Ranking")
        tree.createTrees()
        tree.showTrees()

        listaRanking = db.consultData_ranking_user()
        cont = 1

        # cria tabela de ranking
        table = Table(show_header=True, header_style="bold green", box=box.DOUBLE_EDGE, width=40, title_style='dim')
        table.add_column("Rank", style="bold", width=2,)
        table.add_column("Nickname", style="bold", width=10, justify="center")
        table.add_column("Score", justify="right", style="bold", width=3)

        for t in listaRanking: 
            nickRkg = (t['nickname']) 
            scoreRkg = (t['score'])

            table.add_row(""+str(cont)+"º", nickRkg, str(scoreRkg))
            cont+=1
        
        alignTable = Align(table, align="center")

        console.print(alignTable)
        print('')
        print("Pressione qualquer tecla para voltar...".center(65))

        voltar=getch()
        if voltar != '':
            func.sound('menu')
            print("\n")
            func.clear()
            bann.banner()

screens = Screens()

# cria um arquivo .md (markdown) pra cada tela, printa nome da tela
class ScreenTrees():
    def __init__(self):
        pass
    
    def firstScreenTree(self):
        func.clear()
        bann.banner()
        print()
        tree = Trees("quiz", "# Quiz")
        tree.createTrees()
        tree.showTrees()
    
    def menuTree(self):
        func.clear()
        bann.banner()
        print()
        tree = Trees("menu_principal", "# Menu")
        tree.createTrees()
        tree.showTrees()
    

    def profileTree(self):
        func.clear()
        bann.banner()
        print()
        tree = Trees("profile", "# Perfil")
        tree.createTrees()
        tree.showTrees()

sctree = ScreenTrees()

# classe contendo perfil, cadastro e login
class Profile:

    def __init__(self):
        self.choice = 0
    
    def register(self):
        nomeReg = str(input('Nome completo: '))

        while len(nomeReg) < 10:
            print("[bold red]Informação incompleta. Digite seu nome novamente.")
            func.sound('error')
            nomeReg = str(input('Nome completo: '))

        nickReg = str(input('Nickname: '))

        nickDict = []
        listaNicks = db.consultData_user()

        for i in listaNicks:
            nicknames = (i['nickname']) # pega lista de nicks no banco de dados
            nickDict.append(nicknames)

        while nickReg in nickDict: # vê se o nick já está cadastrado
            print("[bold red]Nickname já cadastrado. Tente novamente")
            func.sound('error')
            nickReg = str(input('Nickname: '))

        dataReg = str(input("Data de nascimento: "))
        while len(dataReg) < 10:
            print("[bold red]Informação incompleta. Tente novamente.") 
            func.sound('error')
            dataReg=str(input('Data de nascimento: '))

        senhaReg = (getpass_ak.getpass('Crie uma senha com 6 caracteres: '))
        while len(senhaReg) < 6:
            print("[bold red]A senha precisa ter no mínimo 6 caracteres.")
            func.sound('error')
            senhaReg = (getpass_ak.getpass('Senha: '))

        senhaReg2 = (getpass_ak.getpass('Confirme sua senha: '))
        while len(senhaReg2) < 6:
            print("[bold red]A senha precisa ter no mínimo 6 caracteres.")
            func.sound('error')
            senhaReg2 = (getpass_ak.getpass('Confirme sua senha: '))

        if senhaReg2 == senhaReg:
            db.add_user(nickReg, nomeReg, senhaReg, dataReg) # cadastra usuario no banco de dados
            print()
            func.animation("[bold green]Cadastrando...", 1.35)
            print("[bold green]\nCadastro concluido com sucesso!")
            func.sound('point')
            func.reset(0.8)

        else:
            while senhaReg2 != senhaReg:
                print('[bold red]As senhas não correspondem. Digite sua senha novamente: ')
                func.sound('error')
                senhaReg2 = (getpass_ak.getpass('Senha: '))

            if senhaReg2 == senhaReg:
                db.add_user(nickReg, nomeReg, senhaReg, dataReg) # cadastra usuario no banco de dados
                func.animacao("[bold green]Cadastrando...", 1.35)
                print("[bold green]\nCadastro concluído com sucesso!")
                func.sound('point')
                func.reset(0.8)  

    def login(self):
        
            listaUsuarios = db.consultData_user() # pega lista de usuarios
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

            nickLogin = (input('Nickname: ')) 
            senhaLogin = getpass_ak.getpass('Senha: ')

            if nickLogin in usuariosDictScore: 
                scoreLogin = usuariosDictScore[nickLogin]

            if nickLogin in usuarioDictID: 
                LoginID = usuarioDictID[nickLogin]    

            # checa se os dados de login estão corretos
            if nickLogin in usuariosDict and usuariosDict[listaNick] == senhaLogin:
                print()
                func.animation("[bold green]Entrando...", 1.35)
                print()
                print("[bold green]Login feito com sucesso!")  
                func.sound('point')
                sleep(1.2)
                func.clear()
                screens = Screens()
                screens.firstScreen(LoginID)

            else:
                func.animation("[bold red] ", 1.35)
                print('[bold red]\nUsuário não existe ou senha incorreta.')
                func.sound('error')
                func.reset(0.8)    

    def profile(self, idUser):
        sctree.profileTree()
        r = db.consultData_user_id(idUser)
        
        nick= r[0]['nickname']
        nome = r[0]['nome']
        senhaLogin = r[0]['senha']
        tamSenha = len(senhaLogin)
        senha = '*'*tamSenha
        print()
        
        # caixa com os dados do usuario
        data = f"[bold white]Nome: [bold green]{nome}[/bold green]\n[bold white]Nickname: [bold green]{nick}[/bold green]\n[bold white]Senha: [bold green]{senha}"
        painel = [Panel(data)]
        caixa = Columns(painel)
        caixa_center = Align(caixa, align="center")
        console.print(caixa_center)
        print('\n')
    
        print('[bold white][ [bold cyan]1 [bold white]] - Trocar nickname'.center(98))
        print('[bold white][ [bold cyan]2 [bold white]] - Trocar senha'.center(95))
        print('[bold white][ [bold cyan]3 [bold white]] - [bold red]Deletar conta'.center(105))
        print('[bold white][ [bold cyan]9 [bold white]] - Voltar'.center(90))

        while self.choice != '9':
            self.choice = (input('\n-> '))

            if self.choice == '1':
                func.sound('menu')
                nickDict = []
                listaNicks = db.consultData_user()
                escolhaLog = 0

                novoNick=(input('\nDigite seu novo nick: '))

                for i in listaNicks:
                    nicknames = (i['nickname'])
                    nickDict.append(nicknames)

                while novoNick in nickDict: 
                    print("[bold red]Nickname já cadastrado. Tente novamente")
                    func.sound('error')
                    novoNick = (input('Digite seu novo nick: '))

                while escolhaLog != 'N' or escolhaLog != 'n':
                    print("Você tem certeza que deseja trocar de nick? (S/N)")
                    escolhaLog = (input())

                    if escolhaLog == 'S' or escolhaLog == 's':
                        func.animation("Trocando nick...", 1)
                        print("\n[bold green]Mudança de nick feita com sucesso!")
                        func.sound('point')
                        sleep(0.5)
                        db.updata_user(novoNick, senhaLogin, idUser)
                        func.clear()
                
                        menu.menuPrincipal()

                    elif escolhaLog == 'N'or escolhaLog == 'n':
                        func.sound('menu')
                        func.animation("[bold cyan]Cancelando...",1)
                        profile.profile(idUser)

                    else:
                        print("[bold red]Opção inválida. Tente novamente")

            elif self.choice == '2':
                func.sound('menu')
                senhaAtual = 0
                while senhaAtual!=senhaLogin:
                    senhaAtual = getpass_ak.getpass('\nDigite sua senha atual: ')

                    if senhaAtual == senhaLogin:
                        novaSenha = getpass_ak.getpass('\nDigite sua nova senha: ')

                        while len(novaSenha) < 6:
                            print("[bold red]A senha precisa ter no mínimo 6 caracteres!")
                            func.sound('error')
                            novaSenha = getpass_ak.getpass('\nDigite sua nova senha: ')

                        while novaSenha == senhaLogin:
                            print("[bold red]As senhas não podem ser iguais!")
                            func.sound('error')
                            novaSenha = getpass_ak.getpass('\nDigite sua nova senha: ')

                        db.updata_user(nick, novaSenha, idUser)
                        func.animation("[bold green]Trocando senha...", 1.2)
                        print("\n[bold green]Senha trocada com sucesso!")
                        func.sound('point')
                        sleep(0.5)
                        func.clear()
                        menu.menuPrincipal()

                    elif senhaAtual != senhaLogin:
                        print("[bold red]Senha incorreta. Tente novamente.")
                        func.sound('error')
                        
                
            elif self.choice == '3':
                func.sound('menu')
                escolhaDel = 0

                while escolhaDel != 'N' or escolhaDel != 'n':
                    print("Você tem certeza? (S/N)")
                    escolhaDel = input()

                    if escolhaDel == 'S' or escolhaDel == 's':
                        func.sound('menu')
                        func.animation("[bold red]Deletando conta...", 1)
                        db.del_user(idUser)
                        
                        print("[bold green]Conta deletada com sucesso!")
                        func.sound('point')
                        sleep(0.6)
                        func.clear()
                        menu.menuPrincipal()

                    elif escolhaDel == 'N' or escolhaDel == 'n':
                        func.animation("[bold cyan]Cancelando...",0.6)
                        profile.profile(idUser)

                    else:
                        print("[bold red]Opção inválida.")  
                        func.sound('error')
            
            elif self.choice == '9':
                func.sound('menu')
                print()
                func.animation("[bold cyan]Voltando...", 0.7)
                screens.firstScreen(idUser)

            else:
                print("[bold red]Opção Inválida. Tente novamente.")
                func.sound('error')
                screens.firstScreen(idUser)

profile = Profile()

# classe do menu principal e ranking             
class Menus: 
    def __init__(self):
        self.choice = 0
        
    def menuPrincipal(self):
        while True:    
            while self.choice != '9': 
                bann.banner()
                print('\n')
                print("[b][ [bold cyan]1[/bold cyan] [b]] - Login".center(92))
                print("[b][ [bold cyan]2[/bold cyan] [b]] - Cadastro".center(95))
                print("[b][ [bold cyan]3[/bold cyan] [b]] - Ranking".center(94))
                print("[b][ [bold cyan]9[/bold cyan] [b]] - Sair".center(92))
                #linhas()
                print('\n')
                print('Escolha uma opção -> '.center(68))

                self.choice = input()

                print()

                if self.choice == '1':
                    func.sound('menu')
                    profile.login()

                elif self.choice == '2':
                    func.sound('menu')
                    profile.register()

                elif self.choice == '3':
                    func.sound('menu')
                    menu.rankingMenu()
        
                elif self.choice =='9':
                    func.sound('menu')
                    func.animation("[bold cyan]Saindo...", 0.8)
                    print('[bold green]\nAté mais! :)')
                    func.sound('exit')
                    sleep(0.5)    
                    exit()

                else:
                    print("[bold red]\nEscolha inválida. Tente novamente")
                    func.sound('error')
                    sleep(0.8)
                    func.clear()

    def rankingMenu(self):
        func.clear()
        bann.banner()
        print()

        console = Console()

        tree = Trees("ranking", "# Ranking")
        tree.createTrees()
        tree.showTrees()

        listaRanking = db.consultData_ranking_user()
        cont = 1

        # cria tabela de ranking
        table = Table(show_header=True, header_style="bold green", box=box.DOUBLE_EDGE, width=40, title_style='dim')
        table.add_column("Rank", style="bold", width=2,)
        table.add_column("Nickname", style="bold", width=10, justify="center")
        table.add_column("Score", justify="right", style="bold", width=3)

        for t in listaRanking: 
            nickRkg = (t['nickname']) 
            scoreRkg = (t['score'])

            table.add_row(""+str(cont)+"º", nickRkg, str(scoreRkg))
            cont+=1
        
        alignTable = Align(table, align="center") # alinha a tabela de ranking no centro da tela
        console.print(alignTable)

        print('\n')
        print("Pressione qualquer tecla para voltar...".center(65))

        voltar=getch()

        if voltar != '':
            print("")
            func.sound('menu')
            func.clear()

menu = Menus()

        
