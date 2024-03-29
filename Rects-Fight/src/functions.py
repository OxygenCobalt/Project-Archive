# Functions.py
# Self-Explanatory, alot of these functions should have gone into sprite classes but oh well.
import pygame
import public as public
import dictionaries as dictionaries
import sprites as sprites

pygame.init()

# Abilities
# Most of the time it converts velocities, creates bullet instances, and adds them.
def big_bullet(group_a, group_b, pos, vel, img, type_of):
    vel = dictionaries.VELOCITY_VALUES['Convert']['Big_Bullet'][vel] # Get Velocity Information
    _big_bullet = sprites.Bullet(pos, vel, img, type_of)  # Create sprite with position, velocity, color, and type
    group_a.add(_big_bullet) # Add bullets to both sprite groups [all_sprites and bullets]
    group_b.add(_big_bullet)
    dictionaries.MEDIA['big_shoot_sound'].play()

# These functions all basically make a bullet and add it to the groups
def split_bullet(group_a, group_b, pos, vel, img, color):
    _split_bullet = sprites.SplitBullet(pos, vel, img, group_a, group_b, color)
    group_a.add(_split_bullet)
    group_b.add(_split_bullet)
    dictionaries.MEDIA['split_shoot_sound'].play()


def beam(group_a, group_b, pos, vel, color):
    beam = sprites.Beam(pos, vel, color)
    group_a.add(beam)
    group_b.add(beam)
    dictionaries.MEDIA['laser_shoot_sound'].play()


def reverse_bullet(group_a, group_b, pos, vel, img, color):
    vel = dictionaries.VELOCITY_VALUES['Convert']['Reverse_Bullet']['Velocity'][vel] # Get Velocity
    _reverse_bullet = sprites.ReverseBullet(pos, vel, img, color)
    group_a.add(_reverse_bullet)
    group_b.add(_reverse_bullet)
    dictionaries.MEDIA['reverse_shoot_sound'].play()


def multi_bullet(group_a, group_b, pos, fire_direction, game_modevalue):
    # Spawn 9 bullets with their own color arguments and velocities

    bullet_1 = sprites.Bullet(
        pos,
        dictionaries.VELOCITY_VALUES['Convert']['Multi_Bullet'][game_modevalue][1], # Index at correct bullet number
        dictionaries.MEDIA['red_bullet'], 'Bullet')
    bullet_2 = sprites.Bullet(
        pos,
        dictionaries.VELOCITY_VALUES['Convert']['Multi_Bullet'][game_modevalue][2],
        dictionaries.MEDIA['orange_bullet'], 'Bullet'
    )
    bullet_3 = sprites.Bullet(
        pos,
        dictionaries.VELOCITY_VALUES['Convert']['Multi_Bullet'][game_modevalue][3],
        dictionaries.MEDIA['yellow_bullet'], 'Bullet'
    )
    bullet_4 = sprites.Bullet(
        pos,
        dictionaries.VELOCITY_VALUES['Convert']['Multi_Bullet'][game_modevalue][4],
        dictionaries.MEDIA['green_bullet'], 'Bullet'
    )
    bullet_5 = sprites.Bullet(
        pos,
        dictionaries.VELOCITY_VALUES['Convert']['Multi_Bullet'][game_modevalue][5],
        dictionaries.MEDIA['blue_bullet'], 'Bullet'
    )
    bullet_6 = sprites.Bullet(
        pos,
        dictionaries.VELOCITY_VALUES['Convert']['Multi_Bullet'][game_modevalue][6],
        dictionaries.MEDIA['purple_bullet'], 'Bullet'
    )
    bullet_7 = sprites.Bullet(
        pos,
        dictionaries.VELOCITY_VALUES['Convert']['Multi_Bullet'][game_modevalue][7],
        dictionaries.MEDIA['white_bullet'], 'Bullet'
    )
    bullet_8 = sprites.Bullet(
        pos,
        dictionaries.VELOCITY_VALUES['Convert']['Multi_Bullet'][game_modevalue][8],
        dictionaries.MEDIA['grey_bullet'], 'Bullet'
    )
    group_a.add(bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, bullet_6, bullet_7, bullet_8) # Add all bullets to both groups
    group_b.add(bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, bullet_6, bullet_7, bullet_8)
    dictionaries.MEDIA['multi_shoot_sound'].play()


def get_cooldown_img(mode, cooldown):
    # Checks mode and timer, returns images
    if mode == 'Classic':
        if 3 >= cooldown >= 2: # If time given is at 4, use the lowest cooldown image
            return dictionaries.MEDIA['cooldown4']
        elif 2 >= cooldown >= 1:
            return dictionaries.MEDIA['cooldown3']
        elif 1 >= cooldown >= 0:
            return dictionaries.MEDIA['cooldown2']
        elif cooldown <= 0: # If time given is at 0, use highest cooldown image
            return dictionaries.MEDIA['cooldown1']

    # Tense mode variants
    elif mode == 'Tense':
        if 1 >= cooldown >= 0.6:
            return dictionaries.MEDIA['cooldown4']
        elif 0.6 >= cooldown >= 0.3:
            return dictionaries.MEDIA['cooldown3']
        elif 0.3 >= cooldown >= 0:
            return dictionaries.MEDIA['cooldown2']
        elif cooldown <= 0:
            return dictionaries.MEDIA['cooldown1']

    # Chaos mode variants
    elif mode == 'Chaos':
        if 0.3 >= cooldown >= 0.2:
            return dictionaries.MEDIA['cooldown4']
        elif 0.2 >= cooldown >= 0.1:
            return dictionaries.MEDIA['cooldown3']
        elif 0.1 >= cooldown >= 0:
            return dictionaries.MEDIA['cooldown2']
        elif cooldown <= 0:
            return dictionaries.MEDIA['cooldown1']

# OxygenCobalt