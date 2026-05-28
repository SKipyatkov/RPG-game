"""
Модуль генерации персонажа.
"""

import random
from datetime import date
from rules import RACE_BONUSES, CLASS_BONUSES
from items import WEAPONS, ARMORS, STARTING_EQUIPMENT

BASE_STATS = 10
DICE_SIDES = 6
STATS_NAMES = ["сила", "ловкость", "выносливость", "интеллект", "мудрость", "восприятие"]


def generate_stats(race: str, character_class: str) -> dict:
    """
    Генерирует базовые характеристики персонажа.

    Args:
        race: раса персонажа
        character_class: класс персонажа

    Returns:
        Словарь с характеристиками
    """
    stats = {}
    race_bonus = RACE_BONUSES.get(race, {})
    class_bonus = CLASS_BONUSES.get(character_class, {})

    for stat in STATS_NAMES:
        base = BASE_STATS
        race_mod = race_bonus.get(stat, 0)
        class_mod = class_bonus.get(stat, 0)
        dice_roll = random.randint(1, DICE_SIDES)
        stats[stat] = base + race_mod + class_mod + dice_roll

    return stats


def get_effective_stats(character: dict) -> dict:
    """
    Возвращает характеристики персонажа с учётом экипировки.

    Args:
        character: словарь с данными персонажа

    Returns:
        Словарь эффективных характеристик
    """
    stats = character.get("stats", {}).copy()
    equipment = character.get("equipment", {})

    # Добавляем бонусы от оружия
    weapon_id = equipment.get("weapon")
    if weapon_id and weapon_id in WEAPONS:
        weapon_stats = WEAPONS[weapon_id].get("stats", {})
        for stat, bonus in weapon_stats.items():
            stats[stat] = stats.get(stat, 0) + bonus

    # Добавляем бонусы от доспеха
    armor_id = equipment.get("armor")
    if armor_id and armor_id in ARMORS:
        armor_stats = ARMORS[armor_id].get("stats", {})
        for stat, bonus in armor_stats.items():
            stats[stat] = stats.get(stat, 0) + bonus

    return stats


def create_character(name: str, race: str, character_class: str) -> dict:
    """
    Создаёт нового персонажа.

    Args:
        name: имя персонажа
        race: раса
        character_class: класс

    Returns:
        Словарь с данными персонажа
    """
    stats = generate_stats(race, character_class)
    max_hp = 20 + stats["выносливость"]

    # Получаем стартовое снаряжение
    starting_equip = STARTING_EQUIPMENT.get(character_class, {"weapon": None, "armor": None})

    character = {
        "name": name,
        "race": race,
        "class": character_class,
        "level": 1,
        "xp": 0,
        "stats": stats,
        "hp": max_hp,
        "max_hp": max_hp,
        "inventory": {"torch": 1, "healing_potion": 1, "gold": 10},
        "equipment": {
            "weapon": starting_equip["weapon"],
            "armor": starting_equip["armor"]
        },
        "current_location": "стартовая_деревня",
        "visited_locations": ["стартовая_деревня"],
        "created": date.today().isoformat()
    }

    return character