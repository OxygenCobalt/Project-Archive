#!/usr/bin/env python3

if __name__ == '__main__':
    import sys
    import subprocess
    import time

    print('Loading Rects Fight V2.0...', end='', flush=True)
    # Check if pygame is installed, if not install pygame
    # If os is not windows, then tell to manually install
    if str(sys.platform) == 'win32':
        try:
            import pygame
        except ModuleNotFoundError:
            print('X')
            print('Pygame is not installed! Installing...')
            subprocess.call(['py', '-m', 'pip', 'install', 'pygame']) # Try to install pygame w/pip
            print('Finished, continuing...')
            import pygame
    else:
        try:
            import pygame
        except ModuleNotFoundError:
            print('YOU ARE USING LINUX/MAC, PLEASE INSTALL PYGAME MANUALLY')
            time.sleep(3)
            sys.exit()

    # Import Game Module [Which Loads Sprites, Global, Media, etc.]
    sys.path.insert(0, './src')
    import game

    print('Done')

    pygame.init()

    game.title_screen() # Title Sequence
    game.mode_select() # Mode Select
    game.char_select() # Character Select
    while game.public.superloop: # Way to repeat fight sequence
        game.main() # Main fight sequence
    pygame.quit()

# OxygenCobalt