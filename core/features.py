from rich import print
from core import getpass_ak
from rich.console import Console
from core.database.database import DataUser
from core.functions import Functions
from playsound import playsound

db = DataUser()
func = Functions()
console = Console()

class Features:
    def __init__(self):
        pass

    def register(self):
        nomeReg = str(input('Nome completo: '))

        while len(nomeReg) < 10:
            print("[bold red]Informação incompleta. Digite seu nome novamente.")
            nomeReg = str(input('Nome completo: '))

        nickReg = str(input('Nickname: '))

        nickDict = []
        listaNicks = db.consultData_user()

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
            db.add_user(nickReg, nomeReg, senhaReg, dataReg) # cadastra usuario no banco de dados
            func.animation("[bold green]Cadastrando...", 1.35)
            print("[bold green]\nCadastro concluido com sucesso!")
            playsound('core/sfx/point.wav')
            func.reset(0.8)

        else:
            print('[bold red]As senhas não correspondem. Digite sua senha novamente: ')
            senhaReg2 = (getpass_ak.getpass(''))

            if senhaReg2 == senhaReg:
                db.add_user(nickReg, nomeReg, senhaReg, dataReg) # cadastra usuario no banco de dados
                func.animacao("[bold green]Cadastrando...", 1.35)
                print("[bold green]\nCadastro concluído com sucesso!")
                func.reset(0.8)  