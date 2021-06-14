from os import system
from time import sleep
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from playsound import playsound

console = Console()

class Functions:
    def __init__(self):
        pass
    
    def clear(self):
        system('cls || clear')

    def animation(self, text, timer):
        with console.status(text, spinner='simpleDots') as status:
            sleep(timer)

    def lines(self):
        print('\n' + '_' * 65)

    def caixa(self, text):
        data = text 

        painel = [Panel(data)]
        console.print(Columns(painel))
    
    def loop(self):
        playsound('core/sfx/loop.wav')
    
    def sound(self, type):
        playsound(f'core/sfx/{type}.wav')

    def reset(self, timer):
        sleep(timer)
        func.clear()

func = Functions()
    