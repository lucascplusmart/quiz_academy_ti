from os import system
from time import sleep
from rich import print, box
from rich.align import Align
from rich.table import Table
from rich.console import Console
from getch import getch # py-getch

from core.banner import Banner
from core.database.database import DataUser
from core.functions import Functions
from core.trees.trees import Trees
from core.features import Features
from core.screens import Screens

console = Console()
func = Functions()
bann = Banner()
db = DataUser()
feat = Features()
screens = Screens()

class Menus: # classe do menu principal e ranking
    def __init__(self):
        self.choice = 0
    
    def opening(self):
        pass
        
        
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