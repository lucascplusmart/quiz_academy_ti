from os import system, get_terminal_size
from pygame import mixer
from time import sleep
from rich import print
from rich.console import Console
from rich.align import Align

from asciimatics.effects import Print, Mirage
from asciimatics.renderers import FigletText, SpeechBubble
from asciimatics.scene import Scene
from asciimatics.screen import Screen

console = Console()
mixer.init()

# classe com banner e game over
class Banner:

    def __init__(self):
        self.width = get_terminal_size().columns

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

# cria animacao final, coloca musica pra tocar em loop
def end(screen): 
    system('mode 65,22 || mode.com 65,22')     
    effects = [
        Mirage(screen, FigletText("GAME OVER", font='standard'),y=7, colour=Screen.COLOUR_RED),
    ]
    screen.play([Scene(effects, 500)])