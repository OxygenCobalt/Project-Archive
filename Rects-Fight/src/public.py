# public.py
# Poorly named file for variables shared in-game

import pygame

pygame.init()

# Colors/Fonts
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)
BLUE = (91, 154, 255)
ORANGE = (247, 157, 66)
GREEN = (0, 159, 18)
RED = (196, 0, 0)
YELLOW = (255, 238, 0)
PURPLE = (205, 43, 255)

# Major Fonts
# Mostly variations of the same font because pygame just works like that
FONT_BIG = pygame.font.Font(None, 40)
FONT_MEDIUM = pygame.font.Font(None, 35)
FONT_SMALL = pygame.font.SysFont(None, 20, False, True)
FONT_BOLD = pygame.font.SysFont(None, 40, True, False)
FONT_ITALIC = pygame.font.SysFont(None, 40, False, True)
FONT_BOLD_ITALIC = pygame.font.SysFont(None, 40, True, True)

# Variables
superloop = True 
playero_charvalue = None # Character chosen for player 1
playert_charvalue = None # Character chosen for player 2
game_modevalue = None # Mode used [Normal/Tense/Chaos]
screen = pygame.display.set_mode((500, 600))
playarea = pygame.Rect(5, 5, 490, 490) # Rect players are limited in

# Easter egg variables
# Figure out what to do and "REGG FITTE" will show up on the caption.
# What was I trying to do? No idea.
mem = []
mem_ideal = [1, 0, 1, 1]
mem_activate = False

# OxygenCobalt