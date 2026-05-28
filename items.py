"""
Модуль предметов: расходуемые предметы, оружие и доспехи.
"""

ITEMS = {
    "healing_potion": {
        "name": "Зелье лечения",
        "description": "Восстанавливает 5 HP",
        "type": "расходуемое",
        "effect": {"hp": 5},
        "price": 10
    },
    "torch": {
        "name": "Факел",
        "description": "Освещает тёмные локации",
        "type": "расходуемое",
        "effect": {"свет": "освещает тёмные локации"},
        "price": 5
    },
    "gold": {
        "name": "Золото",
        "description": "Основная валюта королевства",
        "type": "валюта",
        "effect": {},
        "price": 0
    },
    "mana_potion": {
        "name": "Зелье маны",
        "description": "Восстанавливает 5 MP",
        "type": "расходуемое",
        "effect": {"mp": 5},
        "price": 12
    },
    "lockpick": {
        "name": "Отмычка",
        "description": "Открывает запертые двери",
        "type": "расходуемое",
        "effect": {"открыть_замок": "открывает запертые двери"},
        "price": 8
    },
    "rations": {
        "name": "Сухпаёк",
        "description": "Восстанавливает 2 HP",
        "type": "расходуемое",
        "effect": {"hp": 2},
        "price": 3
    },
    "scroll_of_wisdom": {
        "name": "Свиток мудрости",
        "description": "Временно увеличивает мудрость на 2",
        "type": "расходуемое",
        "effect": {"мудрость": 2},
        "price": 20
    }
}

WEAPONS = {
    "dagger": {
        "name": "Кинжал",
        "description": "Лёгкий и быстрый клинок",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"ловкость": 1},
        "attack_bonus": 0,
        "damage_bonus": 1,
        "price": 15,
        "required_level": 1
    },
    "short_sword": {
        "name": "Короткий меч",
        "description": "Универсальное оружие ближнего боя",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"сила": 1, "ловкость": 1},
        "attack_bonus": 1,
        "damage_bonus": 2,
        "price": 25,
        "required_level": 1
    },
    "iron_sword": {
        "name": "Железный меч",
        "description": "Надёжный меч из добротного железа",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"сила": 2},
        "attack_bonus": 1,
        "damage_bonus": 3,
        "price": 40,
        "required_level": 1
    },
    "wooden_staff": {
        "name": "Деревянный посох",
        "description": "Простой посох для начинающих магов",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"интеллект": 2},
        "attack_bonus": 0,
        "damage_bonus": 1,
        "price": 15,
        "required_level": 1
    },
    "magic_wand": {
        "name": "Волшебная палочка",
        "description": "Усиливает магические способности",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"интеллект": 3},
        "attack_bonus": 2,
        "damage_bonus": 2,
        "price": 35,
        "required_level": 1
    },
    "short_bow": {
        "name": "Короткий лук",
        "description": "Лёгкий лук для быстрой стрельбы",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"ловкость": 2},
        "attack_bonus": 1,
        "damage_bonus": 2,
        "price": 30,
        "required_level": 1
    },
    "throwing_knives": {
        "name": "Метательные ножи",
        "description": "Набор сбалансированных ножей",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"ловкость": 3},
        "attack_bonus": 2,
        "damage_bonus": 1,
        "price": 30,
        "required_level": 1
    },
    "mace": {
        "name": "Булава",
        "description": "Тяжёлое дробящее оружие",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"сила": 2},
        "attack_bonus": 1,
        "damage_bonus": 3,
        "price": 35,
        "required_level": 1
    },
    "holy_staff": {
        "name": "Святой посох",
        "description": "Посох, благословлённый высшими силами",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"мудрость": 3},
        "attack_bonus": 2,
        "damage_bonus": 2,
        "price": 40,
        "required_level": 1
    },
    "steel_axe": {
        "name": "Стальной топор",
        "description": "Тяжёлый топор из закалённой стали",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"сила": 3},
        "attack_bonus": 1,
        "damage_bonus": 5,
        "price": 60,
        "required_level": 2
    },
    "war_hammer": {
        "name": "Боевой молот",
        "description": "Сокрушительный молот для тяжёлой пехоты",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"сила": 4},
        "attack_bonus": 0,
        "damage_bonus": 6,
        "price": 70,
        "required_level": 2
    },
    "longsword": {
        "name": "Длинный меч",
        "description": "Элегантный меч для опытных воинов",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"сила": 2, "ловкость": 2},
        "attack_bonus": 2,
        "damage_bonus": 4,
        "price": 65,
        "required_level": 2
    },
    "crystal_staff": {
        "name": "Хрустальный посох",
        "description": "Посох с кристаллом чистой магии",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"интеллект": 5},
        "attack_bonus": 3,
        "damage_bonus": 3,
        "price": 70,
        "required_level": 2
    },
    "long_bow": {
        "name": "Длинный лук",
        "description": "Мощный лук для дальней стрельбы",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"ловкость": 4},
        "attack_bonus": 2,
        "damage_bonus": 3,
        "price": 60,
        "required_level": 2
    },
    "crossbow": {
        "name": "Арбалет",
        "description": "Точный и смертоносный арбалет",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"ловкость": 2, "восприятие": 2},
        "attack_bonus": 3,
        "damage_bonus": 4,
        "price": 75,
        "required_level": 2
    },
    "blessed_hammer": {
        "name": "Благословенный молот",
        "description": "Молот, наполненный святой силой",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"сила": 3, "мудрость": 2},
        "attack_bonus": 2,
        "damage_bonus": 4,
        "price": 70,
        "required_level": 2
    },
    "holy_sword": {
        "name": "Святой меч",
        "description": "Легендарный меч паладинов",
        "type": "оружие",
        "slot": "weapon",
        "stats": {"сила": 3, "мудрость": 2},
        "attack_bonus": 3,
        "damage_bonus": 5,
        "price": 80,
        "required_level": 3
    }
}

ARMORS = {
    "cloth_robe": {
        "name": "Тканевая роба",
        "description": "Простая роба из ткани",
        "type": "доспех",
        "slot": "armor",
        "stats": {"интеллект": 1},
        "defense_bonus": 0,
        "hp_bonus": 2,
        "price": 15,
        "required_level": 1
    },
    "padded_armor": {
        "name": "Стёганый доспех",
        "description": "Лёгкая защита из простеганной ткани",
        "type": "доспех",
        "slot": "armor",
        "stats": {},
        "defense_bonus": 1,
        "hp_bonus": 3,
        "price": 20,
        "required_level": 1
    },
    "leather_armor": {
        "name": "Кожаный доспех",
        "description": "Доспех из выделанной кожи",
        "type": "доспех",
        "slot": "armor",
        "stats": {"ловкость": 1},
        "defense_bonus": 1,
        "hp_bonus": 4,
        "price": 25,
        "required_level": 1
    },
    "iron_armor": {
        "name": "Железный доспех",
        "description": "Тяжёлый доспех из железных пластин",
        "type": "доспех",
        "slot": "armor",
        "stats": {"сила": 1},
        "defense_bonus": 2,
        "hp_bonus": 5,
        "price": 40,
        "required_level": 1
    },
    "mage_robe": {
        "name": "Роба мага",
        "description": "Роба, усиленная магическими нитями",
        "type": "доспех",
        "slot": "armor",
        "stats": {"интеллект": 2, "мудрость": 1},
        "defense_bonus": 0,
        "hp_bonus": 3,
        "price": 35,
        "required_level": 1
    },
    "chainmail": {
        "name": "Кольчуга",
        "description": "Гибкая защита из металлических колец",
        "type": "доспех",
        "slot": "armor",
        "stats": {},
        "defense_bonus": 3,
        "hp_bonus": 6,
        "price": 50,
        "required_level": 2
    },
    "studded_leather": {
        "name": "Шипастая кожа",
        "description": "Кожаный доспех с металлическими шипами",
        "type": "доспех",
        "slot": "armor",
        "stats": {"ловкость": 2},
        "defense_bonus": 2,
        "hp_bonus": 5,
        "price": 45,
        "required_level": 2
    },
    "steel_armor": {
        "name": "Стальной доспех",
        "description": "Доспех из закалённой стали",
        "type": "доспех",
        "slot": "armor",
        "stats": {"сила": 2},
        "defense_bonus": 3,
        "hp_bonus": 8,
        "price": 65,
        "required_level": 2
    },
    "enchanted_robe": {
        "name": "Зачарованная роба",
        "description": "Роба, пропитанная мощными чарами",
        "type": "доспех",
        "slot": "armor",
        "stats": {"интеллект": 3, "мудрость": 2},
        "defense_bonus": 1,
        "hp_bonus": 5,
        "price": 70,
        "required_level": 2
    },
    "holy_robe": {
        "name": "Священная роба",
        "description": "Роба, благословлённая высшими силами",
        "type": "доспех",
        "slot": "armor",
        "stats": {"мудрость": 3},
        "defense_bonus": 1,
        "hp_bonus": 6,
        "price": 65,
        "required_level": 2
    },
    "shadow_cloak": {
        "name": "Теневой плащ",
        "description": "Плащ, скрывающий в тенях",
        "type": "доспех",
        "slot": "armor",
        "stats": {"ловкость": 3, "восприятие": 2},
        "defense_bonus": 1,
        "hp_bonus": 4,
        "price": 75,
        "required_level": 2
    },
    "ranger_vest": {
        "name": "Жилет следопыта",
        "description": "Лёгкий жилет для охотников",
        "type": "доспех",
        "slot": "armor",
        "stats": {"ловкость": 2, "восприятие": 2},
        "defense_bonus": 2,
        "hp_bonus": 6,
        "price": 70,
        "required_level": 2
    },
    "plate_armor": {
        "name": "Латный доспех",
        "description": "Полный латный доспех рыцаря",
        "type": "доспех",
        "slot": "armor",
        "stats": {"сила": 3},
        "defense_bonus": 4,
        "hp_bonus": 12,
        "price": 100,
        "required_level": 3
    },
    "blessed_armor": {
        "name": "Благословенный доспех",
        "description": "Доспех, освящённый древними ритуалами",
        "type": "доспех",
        "slot": "armor",
        "stats": {"мудрость": 3},
        "defense_bonus": 3,
        "hp_bonus": 10,
        "price": 100,
        "required_level": 3
    },
    "holy_armor": {
        "name": "Святой доспех",
        "description": "Легендарный доспех паладинов",
        "type": "доспех",
        "slot": "armor",
        "stats": {"сила": 2, "мудрость": 3},
        "defense_bonus": 4,
        "hp_bonus": 12,
        "price": 120,
        "required_level": 3
    }
}

# Стартовое снаряжение
STARTING_EQUIPMENT = {
    "Воин": {"weapon": "iron_sword", "armor": "iron_armor"},
    "Маг": {"weapon": "wooden_staff", "armor": "cloth_robe"},
    "Лучник": {"weapon": "short_bow", "armor": "leather_armor"},
    "Вор": {"weapon": "dagger", "armor": "padded_armor"},
    "Жрец": {"weapon": "mace", "armor": "chainmail"},
    "Паладин": {"weapon": "longsword", "armor": "steel_armor"}
}