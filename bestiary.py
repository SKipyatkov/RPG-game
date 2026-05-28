"""
Модуль бестиария: монстры и их характеристики.
"""

MONSTERS = {
    "wolf": {
        "name": "Волк",
        "description": "Серый хищник с горящими глазами. Охотится стаей, но этот — одиночка.",
        "hp": 15,
        "attack": 3,
        "defense": 1,
        "xp": 15,
        "loot": {"gold": 5, "rations": 1}
    },
    "ghost_miller": {
        "name": "Призрак мельника",
        "description": "Прозрачная фигура с мешком муки. Бормочет о несправедливости.",
        "hp": 20,
        "attack": 4,
        "defense": 2,
        "xp": 25,
        "loot": {"gold": 15, "scroll_of_wisdom": 1}
    },
    "mountain_troll": {
        "name": "Горный тролль",
        "description": "Огромное существо с каменной кожей. Медленное, но сокрушительное.",
        "hp": 35,
        "attack": 6,
        "defense": 3,
        "xp": 40,
        "loot": {"gold": 25, "healing_potion": 2, "steel_axe": 1}
    },
    "ancient_spirit": {
        "name": "Древний дух",
        "description": "Хранитель замка. Тысячи лет ждал достойного противника.",
        "hp": 50,
        "attack": 8,
        "defense": 4,
        "xp": 100,
        "loot": {"gold": 100, "mana_potion": 3, "crystal_staff": 1}
    }
}