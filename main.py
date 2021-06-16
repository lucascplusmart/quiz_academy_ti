from asciimatics.effects import Print, Mirage
from asciimatics.renderers import FigletText, SpeechBubble
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from core.screens import Menus
from core.functions import Functions

from pygame import mixer
from os import system

mixer.init()
menus = Menus()
func = Functions()

# cria animacao inicial, coloca musica pra tocar em loop
def intro(screen):  
    system('mode 80,22 || mode.com 80,22')
    song = mixer.Sound('core/sfx/loop.wav')
    song.play(-1)      
    effects = [
        Mirage(screen, FigletText("Quiz Academy Ti", font='standard'),y=7, colour=Screen.COLOUR_CYAN),

        Print(screen,
                SpeechBubble("Aperte X para iniciar."),
                screen.height-8,
                speed=1, transparent=False)
    ]
    screen.play([Scene(effects, 500)])

Screen.wrapper(intro)
func.sound('menu')

# tamanho do terminal para o quiz
system('mode 65,42 || mode.com 65,42')

# inicia o quiz
menus.menuPrincipal()