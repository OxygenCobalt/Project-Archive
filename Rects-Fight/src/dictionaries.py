# Dictionaries.py
# Instead of refactoring my unruly dictionaries when I split them up, I put them in this file instead so I didnt have to think about them, apparently.

import public
import pygame
import random
import os
import glob

pygame.init()

# Media Dictionary
# Loads sounds/images into dictionary based on filename
MEDIA = {}
image_files = glob.glob(os.path.join(os.path.dirname(__file__), 'res', 'image', '*.png')) # Images
audio_files = glob.glob(os.path.join(os.path.dirname(__file__), 'res', 'audio', '*.wav')) # Audio

for file in image_files:
    obj = pygame.image.load(file).convert_alpha()
    MEDIA[os.path.split(file)[-1][:-4]] = obj # Load in media as its filename [Excluding Extension]

for file in audio_files:
    obj = pygame.mixer.Sound(file)
    MEDIA[os.path.split(file)[-1][:-4]] = obj

PLAYER_MEDIA = {
    # This was where I stored the images for special moves/character looks/text colors
    # The entry names are pretty verbose [I hope]

    'Blue': {
        'Color': public.BLUE,
        'Image': MEDIA['blue_face'],
        'Bullet_Image': MEDIA['blue_bullet'],
        'Location': (220, 145),
        'Parameters': [MEDIA['blue_big_bullet'], 'Big_Bullet']
    },
    'Orange': {
        'Color': public.ORANGE,
        'Image': MEDIA['orange_face'],
        'Bullet_Image': MEDIA['orange_bullet'],
        'Location': (208, 145),
        'Parameters': [MEDIA['orange_big_bullet'], 'Big_Bullet']
    },
    'Green': {
        'Color': public.GREEN,
        'Image': MEDIA['green_face'],
        'Bullet_Image': MEDIA['green_bullet'],
        'Split_Bullet_Image': MEDIA['green_split_bullet'],
        'Location': (210, 135),
        'Parameters': [MEDIA['green_split_bullet'], 'Green']
    },
    'Yellow': {
        'Color': public.YELLOW,
        'Image': MEDIA['yellow_face'],
        'Bullet_Image': MEDIA['yellow_bullet'],
        'Split_Bullet_Image': MEDIA['yellow_split_bullet'],
        'Location': (209, 135),
        'Parameters': [MEDIA['yellow_split_bullet'], 'Yellow']
    },
    'Red': {
        'Color': public.RED,
        'Image': MEDIA['red_face'],
        'Bullet_Image': MEDIA['red_bullet'],
        'Location': (224, 160),
        'Parameters': ['Red']
    },
    'Purple': {
        'Color': public.PURPLE,
        'Image': MEDIA['purple_face'],
        'Bullet_Image': MEDIA['purple_bullet'],
        'Location': (211, 160),
        'Parameters': ['Purple']
    },
    'Grey': {
        'Color': public.GREY,
        'Image': MEDIA['grey_face'],
        'Bullet_Image': MEDIA['grey_bullet'],
        'Location': (220, 115),
        'Parameters': [MEDIA['grey_boomerang_bullet'], 'Grey']
    },
    'White': {
        'Color': public.WHITE,
        'Image': MEDIA['white_face'],
        'Bullet_Image': MEDIA['white_bullet'],
        'Location': (210, 115),
        'Parameters': [MEDIA['white_boomerang_bullet'], 'White']
    },
    'Rainbow': {
        # Rainbow randomly picks a text color, as I didnt want to somehow make the letters in text different colors.
        'Color': random.choice((
            public.RED, public.ORANGE, public.YELLOW, public.GREEN, public.BLUE, public.PURPLE 
        )),
        'Image': MEDIA['rainbow_face'],
        'Bullet_Image': MEDIA['rainbow_bullet'],
        'Location': (200, 135),
    }
}

VELOCITY_VALUES = {
    # Velocity Values in this game work on a per-frame method
    # Frame 1: (0, 0) -> Frame 2 (8, 0)

    # This dictionary stores the entires [Albeit completely unreadably] in order to be pulled later by sprites
    'Convert': {
        'Big_Bullet': {
            # Normal Mode Values
            (8, 0): (4, 0), # Values are based on built-in bullet velocity, deterined by mode-select. This one is UP
            (-8, 0): (-4, 0), # DOWN
            (0, 8): (0, 4), # RIGHT
            (0, -8): (0, -4), # LEFT

            # Tense Values
            (12, 0): (6, 0),
            (-12, 0): (-6, 0),
            (0, 12): (0, 6),
            (0, -12): (0, -6),

            # Chaos Values
            (16, 0): (8, 0),
            (-16, 0): (-8, 0),
            (0, 16): (0, 8),
            (0, -16): (0, -8),
        },
        'Laser': {
            # A Function is used here that increased the bullet velocity [Slightly] over time, still the same corresponding usages

            (8, 0): lambda bullet: -(bullet.vel[0] + 10),
            (-8, 0): lambda bullet: -(bullet.vel[0] - 10),
            (0, 8): lambda bullet: -(bullet.vel[1] + 10),
            (0, -8): lambda bullet: -(bullet.vel[1] - 10),

            (12, 0): lambda bullet: -(bullet.vel[0] + 15),
            (-12, 0): lambda bullet: -(bullet.vel[0] - 15),
            (0, 12): lambda bullet: -(bullet.vel[1] + 15),
            (0, -12): lambda bullet: -(bullet.vel[1] - 15),

            (16, 0): lambda bullet: -(bullet.vel[0] + 20),
            (-16, 0): lambda bullet: -(bullet.vel[0] - 20),
            (0, 16): lambda bullet: -(bullet.vel[1] + 20),
            (0, -16): lambda bullet: -(bullet.vel[1] - 20)
        },
        'Split_Bullet': {
            # One bullets velocity is converted into three bullet's velocity.
            # The initial/middle bullet have the same velocity, while the top/bottom bullets go in different directions

            (8, 0): [(-8, 0), (-8, -5), (-8, 5)],
            (-8, 0): [(8, 0), (8, -5), (8, 5)],
            (0, 8): [(0, -8), (5, -8), (-5, -8)],
            (0, -8): [(0, 8), (5, 8), (-5, 8)],

            (12, 0): [(-12, 0), (-12, -8), (-12, 8)],
            (-12, 0): [(12, 0), (12, -8), (12, 8)],
            (0, 12): [(0, -12), (8, -12), (-8, -12)],
            (0, -12): [(0, 12), (8, 12), (-8, 12)],

            (16, 0): [(-16, 0), (-16, -10), (-16, 10)],
            (-16, 0): [(16, 0), (16, -10), (16, 10)],
            (0, 16): [(0, -16), (10, -16), (-10, -16)],
            (0, -16): [(0, 16), (10, 16), (-10, 16)]
        },
        'Reverse_Bullet': {
            # Due to the nature of this ability it was split up into multiple subdictionaries

            'Velocity': {
                # The starting direction determined by the mode

                (8, 0): (8, 0),
                (-8, 0): (-8, 0),
                (0, 8): (0, 8),
                (0, -8): (0, -8),
                (12, 0): (10, 0),
                (-12, 0): (-10, 0),
                (0, 12): (0, 10),
                (0, -12): (0, -10),
                (16, 0): (12, 0),
                (-16, 0): (-12, 0),
                (0, 16): (0, 12),
                (0, -16): (0, -12)
            },
            'Direction': {
                # Direction dermined by the Velocity entry [This comes in handy later]

                (8, 0): 'Right',
                (-8, 0): 'Left',
                (0, 8): 'Down',
                (0, -8): 'Up',
                (10, 0): 'Medium_Right',
                (-10, 0): 'Medium_Left',
                (0, 10): 'Medium_Down',
                (0, -10): 'Medium_Up',
                (12, 0): 'Fast_Right',
                (-12, 0): 'Fast_Left',
                (0, 12): 'Fast_Down',
                (0, -12): 'Fast_Up'
            },
            'White': {
                # Bullet curve determined by Direction entry
                # Whites curved bullets move to the left

                'Right': lambda self: (self.vel[0] - 0.2, self.vel[1] + 0.02),
                'Left': lambda self: (self.vel[0] + 0.2, self.vel[1] + 0.02),
                'Up': lambda self: (self.vel[0] - 0.02, self.vel[1] + 0.2),
                'Down': lambda self: (self.vel[0] -   0.02, self.vel[1] - 0.2),

                'Medium_Right': lambda self: (self.vel[0] - 0.4, self.vel[1] + 0.1),
                'Medium_Left': lambda self: (self.vel[0] + 0.4, self.vel[1] + 0.1),
                'Medium_Up': lambda self: (self.vel[0] - 0.1, self.vel[1] + 0.4),
                'Medium_Down': lambda self: (self.vel[0] - 0.1, self.vel[1] - 0.4),

                'Fast_Right': lambda self: (self.vel[0] - 0.6, self.vel[1] + 0.2),
                'Fast_Left': lambda self: (self.vel[0] + 0.6, self.vel[1] + 0.2),
                'Fast_Up': lambda self: (self.vel[0] - 0.2, self.vel[1] + 0.6),
                'Fast_Down': lambda self: (self.vel[0] - 0.2, self.vel[1] - 0.6)},
            'Grey': {
                # Greys curved bullets move to the right

                'Right': lambda self: (self.vel[0] - 0.2, self.vel[1] - 0.02),
                'Left': lambda self: (self.vel[0] + 0.2, self.vel[1] - 0.02),
                'Up': lambda self: (self.vel[0] + 0.02, self.vel[1] + 0.2),
                'Down': lambda self: (self.vel[0] + 0.02, self.vel[1] - 0.2),

                'Medium_Right': lambda self: (self.vel[0] - 0.4, self.vel[1] - 0.1),
                'Medium_Left': lambda self: (self.vel[0] + 0.4, self.vel[1] - 0.1),
                'Medium_Up': lambda self: (self.vel[0] + 0.1, self.vel[1] + 0.4),
                'Medium_Down': lambda self: (self.vel[0] + 0.1, self.vel[1] - 0.4),

                'Fast_Right': lambda self: (self.vel[0] - 0.6, self.vel[1] - 0.2),
                'Fast_Left': lambda self: (self.vel[0] + 0.6, self.vel[1] - 0.2),
                'Fast_Up': lambda self: (self.vel[0] + 0.2, self.vel[1] + 0.6),
                'Fast_Down': lambda self: (self.vel[0] + 0.2, self.vel[1] - 0.6)
                }
        },
        'Multi_Bullet': {
            # Rainbows multi-bullet ability, which is the most OP in the game.
            # Here I actually split them up by mode, which is weird.
            # The numbers represent which bullet [In clockwise order] goes in what direction

            'Classic': {
                1: (5, 0),
                2: (5, -5),
                3: (0, -5),
                4: (-5, -5),
                5: (-5, 0),
                6: (-5, 5),
                7: (0, 5),
                8: (5, 5)
            },
            'Tense': {
                1: (7, 0),
                2: (7, -7),
                3: (0, -7),
                4: (-7, -7),
                5: (-7, 0),
                6: (-7, 7),
                7: (0, 7),
                8: (7, 7)
            },
            'Chaos': {
                1: (9, 0),
                2: (9, -9),
                3: (0, -9),
                4: (-9, -9),
                5: (-9, 0),
                6: (-9, 9),
                7: (0, 9),
                8: (9, 9)
                }
        }
    },
    'Compare': {
        # The Comparison dictionary is used to determine the image used when the laser is fired
        # Why is this in the velocity dictionary? I dont know.
        # Everything else still applies though, at least 13-yo me had consistant organization [Even if he didnt comment very often]

        'Laser_Image': {
            'Purple': {
                (8, 0): MEDIA['purple_laser'],
                (-8, 0): MEDIA['purple_laser'],
                (0, 8): pygame.transform.rotate(MEDIA['purple_laser'], -90),
                (0, -8): pygame.transform.rotate(MEDIA['purple_laser'], 90),

                (12, 0): MEDIA['purple_laser'],
                (-12, 0): MEDIA['purple_laser'],
                (0, 12): pygame.transform.rotate(MEDIA['purple_laser'], -90),
                (0, -12): pygame.transform.rotate(MEDIA['purple_laser'], 90),

                (16, 0): MEDIA['purple_laser'],
                (-16, 0): MEDIA['purple_laser'],
                (0, 16): pygame.transform.rotate(MEDIA['purple_laser'], -90),
                (0, -16): pygame.transform.rotate(MEDIA['purple_laser'], 90)
            },
            'Red': {
                (8, 0): MEDIA['red_laser'],
                (-8, 0): MEDIA['red_laser'],
                (0, 8): pygame.transform.rotate(MEDIA['red_laser'], -90),
                (0, -8): pygame.transform.rotate(MEDIA['red_laser'], 90),

                (12, 0): MEDIA['red_laser'],
                (-12, 0): MEDIA['red_laser'],
                (0, 12): pygame.transform.rotate(MEDIA['red_laser'], -90),
                (0, -12): pygame.transform.rotate(MEDIA['red_laser'], 90),

                (16, 0): MEDIA['red_laser'],
                (-16, 0): MEDIA['red_laser'],
                (0, 16): pygame.transform.rotate(MEDIA['red_laser'], -90),
                (0, -16): pygame.transform.rotate(MEDIA['red_laser'], 90)
                    }
                }
            }
        }



MODE_VALUES = {
    # Values that corellate to the difficulty selected in mode select
    # Elements like time, velocity, health, ability cooldowns, etc
    'Classic': {
        'Timer': 30,
        'Player_Velocity': 6,
        'Bullet_Velocity': 8, # Bullet velocities determines alot of the velocity dictionary.
        'Health': 3,
        'Sound': MEDIA['classic_sound'],
        'Music': MEDIA['classic_music'],
        'Cooldown': 3,
        'Color': public.GREEN, # Text color used in the mode select screen
        'Location': (220, 190) # Entry position
    },
    'Tense': {
        'Timer': 20,
        'Player_Velocity': 7,
        'Bullet_Velocity': 12,
        'Health': 2,
        'Sound': MEDIA['tense_sound'],
        'Music': MEDIA['tense_music'],
        'Cooldown': 1,
        'Color': public.YELLOW,
        'Location': (220, 290)
    },
    'Chaos': {
        'Timer': 10,
        'Player_Velocity': 8,
        'Bullet_Velocity': 16,
        'Health': 1,
        'Sound': MEDIA['chaos_sound'],
        'Music': MEDIA['chaos_music'],
        'Cooldown': 0.3,
        'Color': public.RED,
        'Location': (220, 390)
    }
}

HP_MEDIA = {
    # HP bars pulled by main game loop based on player health

    0: MEDIA['hp_dead'],
    1: MEDIA['hp_low'],
    2: MEDIA['hp_decayed'],
    3: MEDIA['hp_full'],
    # Added to prevent an exception where the game cannot find the correct dictionary entry
    -1: MEDIA['hp_dead'],
    -2: MEDIA['hp_dead'],
    -3: MEDIA['hp_dead'],
    -4: MEDIA['hp_dead'],
    -5: MEDIA['hp_dead'],   
}

TIMER_DICT = {
    # If time is <10, change to red, otherwise white
    # Why is this a dictionary?

    True: [public.RED, public.FONT_BOLD],
    False: [public.WHITE, public.FONT_BIG]
}

# OxygenCobalt