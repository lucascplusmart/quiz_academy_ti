from os import system
from time import sleep
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from playsound import playsound
import pygame

pygame.init()

console = Console()

# classe contendo funcoes usadas em todo o quiz
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
    
    def sound(self, name):    
        menu = pygame.mixer.Sound('core/sfx/menu.wav')
        error = pygame.mixer.Sound('core/sfx/error.wav')
        point = pygame.mixer.Sound('core/sfx/point.wav')
        exit_quiz = pygame.mixer.Sound('core/sfx/exit.wav')
        
        if name == 'menu':
            menu.play()
        elif name == 'error':
            error.play()
        elif name == 'point':
            point.play()
        elif name == 'exit':
            exit_quiz.play()
    
    def reset(self, timer):
        sleep(timer)
        func.clear()
    
func = Functions()