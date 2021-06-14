import os
from time import sleep
from rich import print
from rich.console import Console
from rich.align import Align

console = Console()

class Banner:

    def __init__(self):
        self.width = os.get_terminal_size().columns

    def banner(self):
        print_banner="""                                                                        
       █▀█ █ █ █ ▀█   ▄▀█ █▀▀ ▄▀█ █▀▄ █▀▀ █▀▄▀█ █▄█  ▀█▀ █
       ▀▀█ █▄█ █ █▄   █▀█ █▄▄ █▀█ █▄▀ ██▄ █ ▀ █  █    █  █
               """
        frase = "[bold green] Minions do TI "
        print_banner2=" "+"_"*18 + frase + "[bold white]_"*18+""

        align = Align(print_banner, align='center')
        align2 = Align(print_banner2, align='center')

        console.print(align)
        console.print(align2)

    def game_over(self):
        print(""" 
                       ▄▀▄▀▀▀▀▄▀▄
                       █        ▀▄      ▄
                      █  ▀  ▀     ▀▄▄  █ █
                      █ ▄ █▀ ▄       ▀▀  █
                      █  ▀▀▀▀            █
                      █                  █
                      █                  █
                       █  ▄▄  ▄▄▄▄ ▄▄   █
                       █ ▄▀█ ▄▀  █ ▄▀█ ▄▀
                        ▀   ▀     ▀   ▀
        """)
        print()
        print("[bold green]Aguarde nossas novas funcionalidades!".center(75))
        sleep(3)
        exit()