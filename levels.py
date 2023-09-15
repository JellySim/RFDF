from sprite_classes import *


def return_level(x, x_res=1920, y_res=1080):
    # TO DO - This is currently very inefficient. It loads all the stuff then returns a single level
    # could definitely fix this

    fp = getcwd() + "\\Assets\\"
    levels = [

        # LEVEL ONE
        {
            "player": Player((269, 866)),
            "player_omni": Omni((269, 866)),
            "islands": [
                Island((1451, 371))
            ],

            "emitters": [
                EmittingSprite(fp + "Models/cow.png", fp + "Sounds/cow_sounds.mp3", (1449, 374)),

                EmittingSprite(fp + "Models/seagull_sprite.png", fp + "Sounds/seagull_sound.mp3",
                               (1875, 430), [(1654, 915), (1317, 596), (828, 293), (474, 172), (84, 346)]),
            ],
            "enemy_territory": None,
            "overlay": None
            },

        # LEVEL TWO
        {
            "player": Player((159, 906)),
            "player_omni": Omni((159, 906)),
            "islands": [
                Island((1701, 908))
            ],

            "emitters": [
                EmittingSprite(fp + "Models/cow.png", fp + "Sounds/cow_sounds.mp3", (1701, 908)),

                EmittingSprite(fp + "Models/jellyfish.png", fp + "Sounds/jellyfish.mp3",
                               (1875, 430),
                               [(915, 541), (1604, 968), (1625, 751), (1575, 266), (1320, 154),
                                (824, 139), (533, 189), (387, 387), (370, 674), (406, 932)],
                               scale=(50, 50), speed=0.5),
                EmittingSprite(fp + "Models/seagull_sprite.png", fp + "Sounds/seagull_sound.mp3",
                               (1654, 915), [(1654, 915), (1654, 200), (200, 293), (450, 550), (230, 990)]),
            ],
            "enemy_territory": EnemyTerritory(x_res, y_res, fp + "/Models/et_level2.png"),
            "overlay": None
        },

        # LEVEL THREE
        {
            "player": Player((175, 500)),
            "player_omni": Omni((175, 500)),
            "islands": [
                Island((164, 145)),
                Island((47, 1016)),
                Island((1615, 604))
            ],

            "emitters": [
                EmittingSprite(fp + "Models/cow.png", fp + "Sounds/cow_sounds.mp3", (1615, 604)),
                EmittingSprite(fp + "Models/seagull_sprite.png", fp + "Sounds/seagull_sound.mp3",
                               (720, 999), [(720, 999), (1191, 106), (810, 1045), (92, 994), (146, 120)]),
                EmittingSprite(fp + "Models/mushroom.png", fp + "Sounds/whale.mp3",
                               (647, 487))
                # EmittingSprite(fp + "Models/jellyfish.png", fp + "Sounds/jellyfish.mp3",
                #                (1875, 430),
                #                [(915, 541), (1604, 968), (1625, 751), (1575, 266), (1320, 154),
                #                 (824, 139), (533, 189), (387, 387), (370, 674), (406, 932)],
                #                scale=(50, 50), speed=0.5)
           ],

            "enemy_territory": EnemyTerritory(x_res, y_res, fp + "/Models/et_level3.png"),
            "overlay": Overlay(1, x_res, y_res)
        },

        # LEVEL Four
        {
            "player": Player((438, 948)),
            "player_omni": Omni((438, 948)),
            "islands": [
                Island((1780, 1002)),
                Island((47, 1016)),
                Island((950, 1021)),
                Island((682, 57)) # emitter
            ],

            "emitters": [
                EmittingSprite(fp + "Models/cow.png", fp + "Sounds/cow_sounds.mp3", (682, 57)),
                EmittingSprite(fp + "Models/seagull_sprite.png", fp + "Sounds/seagull_sound.mp3",
                               (1840, 312), [(1840, 312), (1592, 451), (127, 450), (66, 227)]),
                EmittingSprite(fp + "Models/mushroom.png", fp + "Sounds/whale.mp3",
                               (784, 539), [(784, 539), (10, 472), (257, 0), (1919, 328)])
            ],

            "enemy_territory": EnemyTerritory(x_res, y_res, fp +"/Models/et_level4.png"),
            "overlay": Overlay(2, x_res, y_res)
        }
    ]

    return levels[x-1]



