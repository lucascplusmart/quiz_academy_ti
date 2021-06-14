from time import sleep
from random import choice
from tabulate import tabulate
from playsound import playsound
from rich.console import Console
from rich import print
from rich.align import Align
from rich.text import Text

from core.banner import Banner
from core.database.database import DataUser, DataContent
from core.functions import Functions

user = DataUser()
content = DataContent()
func = Functions()
bann = Banner()

console = Console()

class PreQuiz: # classe principal, reunindo informações pre-quiz
    def __init__(self):
        self.answeredList = []
        self.notAnsweredList = []
        self.choice = 0

    # lista  das perguntas/COD que o usuario já respondeu
    def answered(self, loginID):
        global answeredCheck

        result = content.consultData_content_user(loginID)
        for r in result:
            self.answeredList.append(r["COD"])  

    # Perguntas(COD) que o usuario não respondeu
    def notAnswered(self):
        global answeredCheck
        global notAnsweredCheck
        answeredCheck = []
        notAnsweredCheck = []

        result = content.consultData_content()
        for linha in result:
            if (linha["COD"] not in self.answeredList):
                self.notAnsweredList.append(linha["COD"])

        # tira repetições sem transformar em set
        for i in self.answeredList:
            if i not in answeredCheck:
                answeredCheck.append(i)

        for t in self.notAnsweredList:
            if t not in notAnsweredCheck:
                notAnsweredCheck.append(t)

        # lista contendo codigo de perguntas nao respondidas
        for x in answeredCheck:
            if (x in notAnsweredCheck):
                notAnsweredCheck.remove(x)      
    
    # pega quantidade de perguntas ja feitas, o codigo das perguntas nao feitas e printa uma mensagem se respondeu todas.
    def codeChoice(self):
        global codeNum
        qty = len(notAnsweredCheck)

        if qty>=1:
            codeNum = choice(list(notAnsweredCheck))

        else:
            func.animation("[bold green]", 2) 
            playsound('core/sfx/point.wav')
            gameover = "[bold green]\n\nVocê respondeu todas as perguntas, é um expert nesse assunto!"
            gameover_align = Align(gameover, align='center')
            console.print(gameover_align)
            print()
            sleep(1.3)
            bann.game_over()

quiz = PreQuiz()

# classe reunindo o necessário pras perguntas do quiz funcionarem
class CheckQuiz(PreQuiz):

    def checkQuiz(self, loginID):
        quiz.answered(loginID)
        quiz.notAnswered()
        quiz.codeChoice()

check_quiz = CheckQuiz()

# classe para sair ou continuar o quiz
class ExitQuestion(PreQuiz):
    def exitQuestion(self, loginID):
        check_quiz.checkQuiz(loginID)
        print("[b][ [bold cyan]1[/bold cyan] [b]] - Continuar")
        print("[b][ [bold cyan]2[/bold cyan] [b]] - Sair")

        while self.choice !='2':
            self.choice = str(input('\n -> '))

            if self.choice == '1':
                func.sound('menu')
                func.clear()
                start_quiz.startQuiz()

            elif self.choice == '2':
                func.sound('menu')
                func.animation("[bold cyan]Saindo...", 0.6)
                #screens.firstScreen() ARRUMAR ISSO

            else:
                func.sound('menu')
                print("[bold red]Escolha inválida.")

exit_question = ExitQuestion()

# continuação do quiz, envia os pontos pro banco de dados
class ContinueQuiz(PreQuiz):

    def continueQuiz(self, loginID):
        check_quiz.checkQuiz(loginID)
        func.animation("[bold cyan]Sua resposa está...", 1.3)
    
        if userAnswer == resposta:
            print("[bold green]\nCorreta!\n")
            playsound('core/sfx/point.wav')
            sleep(0.6)
            print("Você ganhou [bold green]5 [bold white]pontos!")

            # pega score atual e soma com pontos da pergunta
            r = user.consultData_user_id(loginID) 
            scoreID = r[0]['score']
            pontuacaoTotal = scoreID + pontuacao
            
            user.updata_user_score(pontuacaoTotal, loginID)
            content.add_responde(loginID, codeNum)


        else:
            print("[bold red]\nErrada!")
            sleep(0.6)
            print(f'\nA resposta correta é a letra [bold green]{resposta}[/bold green].')
            info_center = Align(info, align="center")
            print()
            print(info_center)
            print()

            content.add_responde(loginID, codeNum)

        exit_question.exitQuestion(loginID)

continue_quiz = ContinueQuiz()

# classe contendo o quiz em si
class QuizAcademy(PreQuiz):
    
    def MainQuiz(self, codeNum, loginID):
        
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

        title_box = Align(output, align="center") # alinha a tabela de ranking no centro da tela
        print()
        console.print(title_box)
        print()
    
        pergunta_center = Text(pergunta, justify='center')
        print(pergunta_center)
        print()
        func.lines()
        print()
        
        #printa as alternativas
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
        print('9. Sair')

        self.choice=0

        while self.choice != '9':
            self.choice=input('\n-> ')

            if self.choice == '1':
                userAnswer = input('\nResposta -> ').upper() # upper() caso o usuario digite em minusculo

                if userAnswer =='A' or userAnswer=='B' or userAnswer=='C' or userAnswer=='D':
                        continue_quiz.continueQuiz(loginID)
                else:
                    print("[bold red]\nEscolha inválida.")

            elif self.choice == '2':
                dica_center = Align(dica, align="center")
                print()
                print(dica_center)
                userAnswer = input('\nResposta -> ').upper()

                if userAnswer =='A' or userAnswer=='B' or userAnswer=='C' or userAnswer=='D':
                    continue_quiz.continueQuiz(loginID)
                else:
                    print("[bold red]\nEscolha inválida.")           

            elif self.choice == '9':
                func.animation("[bold cyan]Saindo...", 0.8)
                exit() # ARRUMAR ISSO
            
            else:
                print("[bold red]\nEscolha inválida.")

main_quiz = QuizAcademy()

# inicia o quiz
class StartQuiz(PreQuiz):
        
    def startQuiz(self, loginID):
        check_quiz.checkQuiz(loginID)
        main_quiz.MainQuiz(codeNum, loginID)
    
    def endQuiz(self):
        pass

start_quiz = StartQuiz()

    