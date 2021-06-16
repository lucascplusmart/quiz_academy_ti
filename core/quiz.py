from time import sleep
from random import choice
from tabulate import tabulate

from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich import print

from core.banner import Banner, end
from core.database.database import DataUser, DataContent
from core.functions import Functions

from asciimatics.screen import Screen

user = DataUser()
content = DataContent()
func = Functions()
bann = Banner()

console = Console()

# classe principal, reunindo informações pre-quiz
class PreQuiz:
    def __init__(self):
        self.answeredList = []
        self.notAnsweredList = []
        self.choice = 0
        self.answeredCheck = []
        self.notAnsweredCheck = []

    # lista  das perguntas/COD que o usuario já respondeu
    def answered(self, loginID):
        result = content.consultData_content_user(loginID)
        for r in result:
            self.answeredList.append(r["COD"])  

    # Perguntas(COD) que o usuario não respondeu
    def notAnswered(self):
        result = content.consultData_content()
        for r in result:
            if (r["COD"] not in self.answeredList):
                self.notAnsweredList.append(r["COD"])

        # tira repetições sem transformar em set
        for i in self.answeredList:
            if i not in self.answeredCheck:
                self.answeredCheck.append(i)

        for t in self.notAnsweredList:
            if t not in self.notAnsweredCheck:
                self.notAnsweredCheck.append(t)

        # lista contendo codigo de perguntas nao respondidas
        for x in self.answeredCheck:
            if (x in self.notAnsweredCheck):
                self.notAnsweredCheck.remove(x)
    
    # pega quantidade de perguntas ja feitas, o codigo das perguntas nao feitas e printa uma mensagem se respondeu todas.
    def codeChoice(self, loginID):
        global codeNum
        qty = len(self.notAnsweredCheck)

        # se tiver pelo menos 1 pergunta nao respondida, inicia o quiz
        if qty>=1:
            codeNum = choice(self.notAnsweredCheck)
            start_quiz.startQuiz(loginID)

        # se nao, termina o quiz e printa o game over
        elif qty<=0:
            func.clear()
            bann.banner()
            print()

            func.animation("[bold green]", 2) 
            func.sound('point')
            gameover = "[bold green]\n\nVocê respondeu todas as perguntas, é um expert nesse assunto!"
            gameover_align = Align(gameover, align='center')
            console.print(gameover_align)

            print()
            sleep(1.3)
            bann.game_over()
            Screen.wrapper(end)
            exit()


quiz = PreQuiz()

# classe reunindo o necessário pras perguntas do quiz funcionarem
class CheckQuiz(PreQuiz):

    def checkQuiz(self, loginID):
        quiz.answered(loginID)
        quiz.notAnswered()
        quiz.codeChoice(loginID)

check_quiz = CheckQuiz()

# continuação do quiz, envia os pontos pro banco de dados
class ContinueQuiz(PreQuiz):

    def continueQuiz(self, loginID):
        print()
        func.animation("[bold cyan]Sua resposa está...", 1.3)
    
        if userAnswer == resposta:
            correta = "[bold green]\nCorreta!\n"
            correta_center = Align(correta, align="center")
            print(correta_center)
            func.sound('point')

            sleep(0.6)
            points = "Você ganhou [bold green]5 [bold white]pontos!"
            points_center = Align(points, align="center")
            print(points_center)

            # pega score atual e soma com pontos da pergunta
            r = user.consultData_user_id(loginID) 
            scoreID = r[0]['score']
            pontuacaoTotal = scoreID + pontuacao
            
            user.updata_user_score(pontuacaoTotal, loginID)
            content.add_responde(loginID, codeNum)

        else:
            errada = "[bold red]\nErrada!"
            func.sound('error')
            errada_center = Align(errada, align="center")
            print(errada_center)
            sleep(0.6)

            print(f'\nA resposta correta é a letra [bold green]{resposta}[/bold green].')
            info_center = Align(info, align="center")

            print()
            print(info_center)
            print()
            
            content.add_responde(loginID, codeNum)

        sleep(2.5)
        check_quiz.checkQuiz(loginID)

continue_quiz = ContinueQuiz()

# classe contendo o quiz em si
class QuizAcademy(PreQuiz):
    
    def MainQuiz(self, codeNum, loginID):
        func.clear()
        bann.banner()
        print()
        
        questionsList = content.consultData_content_search(codeNum) # pega lista de perguntas e alternativas
        alternativesList = content.consultData_alternatives(codeNum)

        global resposta
        global userAnswer
        global pontuacao
        global info

        for i in questionsList: # separa cada parte pra printar no quiz
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

        # alinha a tabela de ranking no centro da tela
        title_box = Align(output, align="center") 
        print()
        console.print(title_box)
        print()
    
        # coloca a pergunta no centro da tela
        pergunta_center = Text(pergunta, justify='center')
        print(pergunta_center)
        print()
        func.lines()
        print()
        
        # printa as alternativas
        for i in alternativesList:
            alternativas = (i['opcao'])
            descricao = (i['descricao'])
            alternativas_center = f"{alternativas} - {descricao}"

            alt_center = Text(alternativas_center, justify='left')
            alt_center.stylize("bold green", 0, 1)
            alt_center_teste = Align(alt_center, align='center')

            console.print(alt_center_teste)

        func.lines()

        print('\n1. Responder')
        print('2. Dica')

        self.choice=0

        while self.choice != '9':
            self.choice=input('\n-> ')

            if self.choice == '1':
                userAnswer = input('\nResposta -> ').upper() # upper() caso o usuario digite em minusculo

                if userAnswer =='A' or userAnswer=='B' or userAnswer=='C' or userAnswer=='D':
                    continue_quiz.continueQuiz(loginID)
                else:
                    print("[bold red]\nEscolha inválida.")
                    func.sound('error')

            elif self.choice == '2':
                dica_center = Align(dica, align="center")
                print()
                print(dica_center)
                userAnswer = input('\nResposta -> ').upper()

                if userAnswer =='A' or userAnswer=='B' or userAnswer=='C' or userAnswer=='D':
                    continue_quiz.continueQuiz(loginID)
                else:
                    print("[bold red]\nEscolha inválida.")  
                    func.sound('error')         
            
            else:
                print("[bold red]\nEscolha inválida.")
                func.sound('error')

main_quiz = QuizAcademy()

# inicia o quiz
class StartQuiz(PreQuiz):
    def startQuiz(self, loginID):
        main_quiz.MainQuiz(codeNum, loginID)
    
start_quiz = StartQuiz()

    