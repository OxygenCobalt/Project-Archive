# Game.py
# The main game loop, with stuff that should have been offloaded to other files to be honest.
import pygame
import sys
import public
import dictionaries
import sprites
import functions

pygame.display.set_caption('Rects Fight! 2.1')
pygame.display.set_icon(dictionaries.MEDIA['icon'])

def title_screen():
    # Title Loop
    clock = pygame.time.Clock()
    loop = True

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # Honestly using sys.exit is overkill
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Space starts the game, ends the function by setting loop to false
                    dictionaries.MEDIA['start_sound'].play()
                    loop = False

        public.screen.fill(public.BLACK)
        public.screen.blit(dictionaries.MEDIA['start_screen'], (0, 0)) # Start screen isnt made of seperate elements, rather a static .png file.

        pygame.display.flip()
        clock.tick(60)


def mode_select():
    # Mode select loop

    clock = pygame.time.Clock()
    loop = True
    all_sprites = pygame.sprite.Group()

    # Set up selector sprite
    selector_big = sprites.SelectorBig((110, 200))
    all_sprites.add(selector_big)

    select_int = 0 # Integer used to set the mode [1: Classic, 2: Tense, 3: Chaos]
    mode_choices = ['Classic', 'Tense', 'Chaos']
    mode_desc = ['Carefree fun for all!', 'Difficulty increased!', 'Its all or nothing!'] # Mode description aligns with select value

    # Guidance Texts [With bad names]
    TEXTS1 = public.FONT_BIG.render('Choose Your Difficulty', True, public.WHITE)
    TEXTS2 = public.FONT_BIG.render('Space To Continue', True, public.WHITE)
    txt = public.FONT_BIG.render(
        mode_desc[select_int], True, dictionaries.MODE_VALUES[mode_choices[select_int]]['Color'] # Change text color based on mode selected
    )

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Selector controls/Confirmation Controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    select_int -= 1
                    selector_big.pos[1] -= 100
                if event.key == pygame.K_DOWN:
                    select_int += 1
                    selector_big.pos[1] += 100
                if event.key == pygame.K_SPACE:
                    public.game_modevalue = mode_choices[select_int] # Set mode value to index of mode list
                    dictionaries.PLAYER_MEDIA['Rainbow'].update({'Parameters': [public.game_modevalue]}) # Add the mode value to Rainbows parameters, probably to determine the speed of their ability
                    dictionaries.MODE_VALUES[public.game_modevalue]['Sound'].play() # Play sound corresponding to that mode
                    loop = False # End loop
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    # Wraparound System

                    if select_int == -1: # Overflow
                        select_int = 2
                    elif select_int == 3: # Underflow
                        select_int = 0

                    txt = public.FONT_BIG.render(
                        mode_desc[select_int], True, dictionaries.MODE_VALUES[mode_choices[select_int]]['Color'] # Update text color every time selector is moved
                    )
                    dictionaries.MEDIA['select_sound'].play()
        all_sprites.update()

        # Drawing
        public.screen.fill(public.BLACK)

        # Draw the mode images
        public.screen.blit(dictionaries.MEDIA['classic_card'], (10, 150))
        public.screen.blit(dictionaries.MEDIA['tense_card'], (10, 250))
        public.screen.blit(dictionaries.MEDIA['chaos_card'], (10, 350))

        # Draw the text based on where what the selector is on at the time
        public.screen.blit(txt, dictionaries.MODE_VALUES[mode_choices[select_int]]['Location'])
        all_sprites.draw(public.screen)

        # Draw the guidance text
        public.screen.blit(TEXTS1, (100, 50))
        public.screen.blit(TEXTS2, (120, 500))

        pygame.display.flip()
        clock.tick(60)


def char_select():
    # Character selection loop

    def get(insert):
        # Fetches character information to display on screen

        color = dictionaries.PLAYER_MEDIA[insert[0]]['Color']
        img = dictionaries.PLAYER_MEDIA[insert[0]]['Image']
        txt = public.FONT_BIG.render(insert[0], True, color)
        abiltxt = public.FONT_BIG.render('Ability: ' + str(insert[1]), True, color) # Create Ability text based on the imformation given
        return img, txt, abiltxt

    clock = pygame.time.Clock()
    loop = True
    color_choices = [ # List of character/ability information
        ('Blue', 'Big Bullet'),
        ('Orange', 'Big Bullet'),
        ('Green', 'Split Bullet'),
        ('Yellow', 'Split Bullet'),
        ('Red', 'Beam'),
        ('Purple', 'Beam'),
        ('Grey', 'Reverse Bullet'),
        ('White', 'Reverse Bullet'),
        ('Rainbow', 'Multi bullet')
    ]
    TEXTS1 = public.FONT_BIG.render('Choose Your Character', True, public.WHITE)
    TEXTS2 = public.FONT_BIG.render('Space To Continue', True, public.WHITE)
    TEXTS3 = public.FONT_BOLD_ITALIC.render('VS.', True, public.WHITE)

    # Character value used when starting the game 
    playero_int = 0
    playert_int = 1

    # Get the image, character text, and ability text by using get()
    # Return distributes the values of the function to the variables here in their exact order
    playero_image, chartxto, abiltxto = get(color_choices[playero_int])
    playert_image, chartxtt, abiltxtt = get(color_choices[playert_int])

    # Selectors for both characters
    selector_a = sprites.Selector((30, 188))
    selector_b = sprites.Selector((85, 388))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(selector_a, selector_b)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # AD for player 1
            # Arrows for player 2
            # Space to confirm
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    playero_int += 1
                    selector_a.pos[0] += 55
                elif event.key == pygame.K_a:
                    playero_int -= 1
                    selector_a.pos[0] -= 55
                if event.key == pygame.K_RIGHT:
                    playert_int += 1
                    selector_b.pos[0] += 55
                elif event.key == pygame.K_LEFT:
                    playert_int -= 1
                    selector_b.pos[0] -= 55
                if event.key == pygame.K_SPACE:
                    # Loads character values based on Player 1 and Player 2's choices.
                    public.playero_charvalue = color_choices[playero_int][0]
                    public.playert_charvalue = color_choices[playert_int][0]

                    if public.playero_charvalue == 'Grey' and public.playert_charvalue == 'White': # Easter egg activation
                        public.mem_activate = True
                    loop = False
                if event.key in (pygame.K_d, pygame.K_a, pygame.K_RIGHT, pygame.K_LEFT):
                    # When key changes, load new information based on changed index
                    playero_int %= len(color_choices)
                    playert_int %= len(color_choices)
                    playero_image, chartxto, abiltxto = get(color_choices[playero_int])
                    playert_image, chartxtt, abiltxtt = get(color_choices[playert_int])
                    dictionaries.MEDIA['select_sound'].play()
        all_sprites.update(470, 30)

        # Draw everything
        # Guidance Text, Selectors, Character/Ability Text, and the character selection bar
        public.screen.fill(public.BLACK)
        public.screen.blit(TEXTS1, (90, 50))
        public.screen.blit(TEXTS2, (120, 500))
        public.screen.blit(TEXTS3, (230, 275))
        public.screen.blit(chartxto, (dictionaries.PLAYER_MEDIA[color_choices[playero_int][0]]['Location'][0], 218))
        public.screen.blit(chartxtt, (dictionaries.PLAYER_MEDIA[color_choices[playert_int][0]]['Location'][0], 300))
        public.screen.blit(abiltxto, (dictionaries.PLAYER_MEDIA[color_choices[playero_int][0]]['Location'][1], 248))
        public.screen.blit(abiltxtt, (dictionaries.PLAYER_MEDIA[color_choices[playert_int][0]]['Location'][1], 330))
        public.screen.blit(dictionaries.MEDIA['charsel_bar'], (0, 158))
        public.screen.blit(dictionaries.MEDIA['charsel_bar'], (0, 358))
        all_sprites.draw(public.screen)

        pygame.display.flip()
        clock.tick(60)


def main():
    # Main game loop/Fight Sequence

    ABIL = { # Ability functions for each character
        'Blue': functions.big_bullet,
        'Orange': functions.big_bullet,

        'Green': functions.split_bullet,
        'Yellow': functions.split_bullet,

        'Red': functions.beam,
        'Purple': functions.beam,

        'Grey': functions.reverse_bullet,
        'White': functions.reverse_bullet,

        'Rainbow': functions.multi_bullet

    }

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    bullets_o = pygame.sprite.Group() # Player one bullets
    bullets_t = pygame.sprite.Group() # Player 2 bullets

    clock = pygame.time.Clock()

    # Guidance Texts [3 and 4 only show themselves when game has ended]
    TEXTS1 = public.FONT_SMALL.render('Player 1', True, dictionaries.PLAYER_MEDIA[public.playero_charvalue]['Color'])
    TEXTS2 = public.FONT_SMALL.render('Player 2', True, dictionaries.PLAYER_MEDIA[public.playert_charvalue]['Color'])
    TEXTS3 = public.FONT_SMALL.render('Escape to leave', True, public.WHITE)
    TEXTS4 = public.FONT_SMALL.render('Enter to restart', True, public.WHITE)

    # Using modevalue, selects attributes to use for game
    game_music = dictionaries.MODE_VALUES[public.game_modevalue]['Music'] # Music thats playing
    timer = dictionaries.MODE_VALUES[public.game_modevalue]['Timer'] # Timer
    player_velocity = dictionaries.MODE_VALUES[public.game_modevalue]['Player_Velocity'] # Movement speed of player
    bullet_velocity = dictionaries.MODE_VALUES[public.game_modevalue]['Bullet_Velocity'] # Bullet speed of player
    player_o = sprites.RectPlayer((35, 35), bullets_t, (bullet_velocity, 0), public.playero_charvalue, ABIL[public.playero_charvalue],  all_sprites) # Player 1's Character
    player_t = sprites.RectPlayer((465, 465), bullets_o, (-bullet_velocity, 0), public.playert_charvalue, ABIL[public.playert_charvalue], all_sprites) # Player 2's Character
    player_o.health = dictionaries.MODE_VALUES[public.game_modevalue]['Health'] # Player 1 Health
    player_t.health = dictionaries.MODE_VALUES[public.game_modevalue]['Health'] # Player 2 Health
    cooldown_o = dictionaries.MODE_VALUES[public.game_modevalue]['Cooldown'] # Player 1 Ability Cooldown
    cooldown_t = dictionaries.MODE_VALUES[public.game_modevalue]['Cooldown'] # Player 2 Ability Cooldown

    # Bools
    loop = True # Main game loop
    time = True # Timer still running
    ability_o = False # If ability is active
    ability_t = False
    time_o = True # If ability has activated
    time_t = True
    on_start = True # Initializer Variable [So that certain things can play first but never again]
    on_end = False # Ending variable that enables exit/retry options
    confirm = False # Variable that makes sure that you havent just paused the game
    draw = False # Draw Determiner

    # Integers
    velocity_reset = 0 # Base speed [To stop players when no key is pressed]

    # Timer stuff
    dt = clock.tick(60) / 1000
    text_location = (222, 520)

    while loop:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                public.superloop = False
                loop = False
            # Keymap
            # WASD for player 1
            # Arrows for player 2
            # F for player 1 bullets
            # SPACE for player 2 bullets
            # E for player 1 ability
            # RCTRL for player 2 ability
            #
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and not player_o.toggle: # If key pressed and player not dead
                    BULLET = sprites.Bullet(player_o.rect.center, (player_o.fire_direction), player_o.bullet_image, 'Bullet') # Fire bullet
                    bullets_o.add(BULLET)
                    all_sprites.add(BULLET)
                    dictionaries.MEDIA['shoot_sound'].play()
                if event.key == pygame.K_SPACE and not player_t.toggle:
                    BULLET = sprites.Bullet(player_t.rect.center, (player_t.fire_direction), player_t.bullet_image, 'Bullet')
                    bullets_t.add(BULLET)
                    all_sprites.add(BULLET)
                    dictionaries.MEDIA['shoot_sound'].play()
                if event.key == pygame.K_e and not player_o.toggle and ability_o: # If ability cooldown at 1, and player not dead and key is pressed
                    player_o.ability(bullets_o, all_sprites, player_o.rect.center, (player_o.fire_direction), *player_o.params) # Activate ability using params
                    time_o = True # Reset cooldown
                    ability_o = False # Disable ability
                    cooldown_o = dictionaries.MODE_VALUES[public.game_modevalue]['Cooldown']
                if event.key == pygame.K_RCTRL and not player_t.toggle and ability_t:
                    player_t.ability(bullets_t, all_sprites, player_t.rect.center, (player_t.fire_direction), *player_t.params)
                    time_t = True
                    ability_t = False
                    cooldown_t = dictionaries.MODE_VALUES[public.game_modevalue]['Cooldown']

                # Movement changes
                if event.key == pygame.K_d and not player_o.toggle and player_o.vel.x == 0: # If not dead, moving in that direction, and if key is pressed
                    player_o.vel.x = player_velocity # Change player velocity to the one determined by move value
                    player_o.fire_direction = (bullet_velocity, 0) # Change fire direction to that velocity
                if event.key == pygame.K_a and not player_o.toggle and player_o.vel.x == 0:
                    player_o.vel.x = -player_velocity
                    player_o.fire_direction = (-bullet_velocity, 0)
                if event.key == pygame.K_s and not player_o.toggle and player_o.vel.y == 0:
                    player_o.vel.y = player_velocity
                    player_o.fire_direction = (0, bullet_velocity)
                if event.key == pygame.K_w and not player_o.toggle and player_o.vel.y == 0:
                    player_o.vel.y = -player_velocity
                    player_o.fire_direction = (0, -bullet_velocity)
                if event.key == pygame.K_RIGHT and not player_t.toggle and player_t.vel.x == 0:
                    player_t.vel.x = player_velocity
                    player_t.fire_direction = (bullet_velocity, 0)
                if event.key == pygame.K_LEFT and not player_t.toggle and player_t.vel.x == 0:
                    player_t.vel.x = -player_velocity
                    player_t.fire_direction = (-bullet_velocity, 0)
                if event.key == pygame.K_DOWN and not player_t.toggle and player_t.vel.y == 0:
                    player_t.vel.y = player_velocity
                    player_t.fire_direction = (0, bullet_velocity)
                if event.key == pygame.K_UP and not player_t.toggle and player_t.vel.y == 0:
                    player_t.vel.y = -player_velocity
                    player_t.fire_direction = (0, -bullet_velocity)

            # Stopping
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d: # If keyup was specific key
                    player_o.vel.x = velocity_reset # Zero the velocity in that direction
                if event.key == pygame.K_a:
                    player_o.vel.x = velocity_reset
                if event.key == pygame.K_s:
                    player_o.vel.y = velocity_reset
                if event.key == pygame.K_w:
                    player_o.vel.y = velocity_reset
                if event.key == pygame.K_RIGHT:
                    player_t.vel.x = velocity_reset
                if event.key == pygame.K_LEFT:
                    player_t.vel.x = velocity_reset
                if event.key == pygame.K_DOWN:
                    player_t.vel.y = velocity_reset
                if event.key == pygame.K_UP:
                    player_t.vel.y = velocity_reset

        # Code that runs on first iteration, runs music and the "FIGHT!" announcer but only once
        if on_start:
            dictionaries.MEDIA['fight_sound'].play()
            game_music.play()
            on_start = False

        # On TAB keypress, all game functions cease and pause screen appears until LSHIFT/ESC/ENTER is pressed
        # ESC: Game leaves, both superloop and loop are declared false as the game ends
        # ENTER: Restarts, only loop ends, restarting the game
        # LSHIFT: Continues operation of game
        if keys[pygame.K_TAB] and not confirm and not on_end:
            confirm = True
            time = False
            time_o = False
            time_t = False
            for sprite in all_sprites:
                sprite.toggle = True
            pygame.mixer.pause()
            dictionaries.MEDIA['pause_sound'].play()

        elif keys[pygame.K_LSHIFT] and confirm:
            confirm = False
            time = True
            time_o = True
            time_t = True
            for sprite in all_sprites:
                sprite.toggle = False
            pygame.mixer.unpause()
            dictionaries.MEDIA['pause_sound'].play()

        elif keys[pygame.K_ESCAPE] and confirm:
            public.superloop = False
            loop = False

        elif keys[pygame.K_RETURN] and confirm:
            game_music.stop()
            loop = False

        # Time code, subtracts timer and cooldown, detects when time is @0 and does according actions, and contains more action code
        if time:
            timer -= dt
            txt = dictionaries.TIMER_DICT[timer < 10][1].render(str(round(timer, 1)), True, dictionaries.TIMER_DICT[timer < 10][0]) # Very long tring that basically determines if the timer needs to be red or not.
            if timer <= 0:
                # If time ends, game ends with effective draw

                for sprite in all_sprites:
                    sprite.toggle = True
                game_music.stop()
                time = False
                time_o = False
                time_t = False
                on_end = True
                text_location = (190, 530)
                txt = public.FONT_BIG.render('Times Up!', True, public.GREY)
                dictionaries.MEDIA['die_sound'].play()

        if not time and keys[pygame.K_ESCAPE]:
            # If escape, end game

            public.superloop = False
            loop = False

        elif not time and keys[pygame.K_RETURN] and not confirm:
            # If enterm restart game

            game_music.stop()
            loop = False

        # Player cooldown abilities
        if time_o:
            cooldown_o -= dt
            if cooldown_o <= 0:
                time_o = False
                ability_o = True
        if time_t:
            cooldown_t -= dt
            if cooldown_t <= 0:
                time_t = False
                ability_t = True

        # Outcome code, when health of a player(s) is at 0, code is run that shows outcome on timer area, stops time, and also contains key actions
        # Very repetetive, should have been consolidated into one block of code to be honest.
        if player_o.health <= 0 and not draw:
            # Player 1 case

            txt = public.FONT_BIG.render('Player 2 Wins!', True, player_t.color) # Render the winners name
            text_location = (155, 530)
            time = False
            time_o = False
            time_t = False
            on_end = True # Flag game as ended
            game_music.stop()
            if keys[pygame.K_ESCAPE] and not confirm:
                public.superloop = False
                loop = False
            elif keys[pygame.K_RETURN] and not confirm:
                # Easter egg check
                loop = False
                if public.mem_activate:
                    public.mem.append(1)
                    if public.mem == public.mem_ideal:
                        pygame.display.set_caption('Regg fitte') # What joke was I trying to make? I have no idea.

        if player_t.health <= 0 and not draw:
            # Player 2 Case

            txt = public.FONT_BIG.render('Player 1 Wins!', True, player_o.color)
            text_location = (155, 530)
            time = False
            time_o = False
            time_t = False
            on_end = True
            game_music.stop()
            if keys[pygame.K_ESCAPE] and not confirm:
                public.superloop = False
                loop = False
            elif keys[pygame.K_RETURN] and not confirm:
                loop = False
                if public.mem_activate:
                    public.mem.append(0)
                    if public.mem == public.mem_ideal:
                        pygame.display.set_caption('Regg fitte')

        if player_o.health <= 0 and player_t.health <= 0:
            # Draw case [Both players dead]

            txt = public.FONT_BIG.render('Draw!', True, public.GREY)
            text_location = (210, 530)
            time = False
            time_o = False
            time_t = False
            on_end = True
            draw = True
            game_music.stop()

            if keys[pygame.K_ESCAPE] and not confirm:
                public.superloop = False
                loop = False
            elif keys[pygame.K_RETURN] and not confirm:
                loop = False
                if public.mem_activate:
                    public.mem.append(' ')
                    if public.mem == public.mem_ideal:
                        pygame.display.set_caption('Regg fitte')

        all_sprites.update()

        # Drawing code, draws media, hp bars, text, sprites, etc.
        public.screen.fill(public.BLACK)
        public.screen.blit(dictionaries.MEDIA['wall'], (0, 0))
        public.screen.blit(pygame.transform.flip(dictionaries.HP_MEDIA[player_o.health], True, False), (20, 530)) # Draw HP bar based on data from dictionary
        public.screen.blit(dictionaries.HP_MEDIA[player_t.health], (380, 530))
        public.screen.blit(txt, text_location)
        public.screen.blit(TEXTS1, (19, 515))
        public.screen.blit(TEXTS2, (429, 515))
        DRAWPARAMS1 = [functions.get_cooldown_img(public.game_modevalue, cooldown_o), (100, 515)] # Set variables to the cooldown values retrieved from dictionary
        DRAWPARAMS2 = [functions.get_cooldown_img(public.game_modevalue, cooldown_t), (380, 515)]
        public.screen.blit(*DRAWPARAMS1) # Draw those values
        public.screen.blit(*DRAWPARAMS2)

        all_sprites.draw(public.screen)

        if on_end:
            # Draw game over guidance texts if game ended

            public.screen.blit(TEXTS3, (395, 10))
            public.screen.blit(TEXTS4, (10, 10))
        if confirm:
            # Draw pause screen if paused.

            public.screen.blit(dictionaries.MEDIA['paused'], (154, 165))

        pygame.display.flip()
        clock.tick(60)

# OxygenCobalt