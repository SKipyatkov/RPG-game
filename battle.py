"""
Модуль боевой системы.
"""

import random
from items import WEAPONS, ARMORS
from generator import get_effective_stats


def calculate_damage(attacker_attack: int, attacker_bonus: int, defender_defense: int, damage_bonus: int = 0) -> int:
    """
    Рассчитывает урон от атаки.

    Args:
        attacker_attack: сила атаки атакующего
        attacker_bonus: бонус к атаке
        defender_defense: защита защищающегося
        damage_bonus: бонус к урону

    Returns:
        Количество урона (минимум 1)
    """
    d6_roll = random.randint(1, 6)
    damage = d6_roll + attacker_attack + attacker_bonus - defender_defense + damage_bonus
    return max(1, damage)


def is_alive(entity: dict) -> bool:
    """
    Проверяет, жив ли персонаж или монстр.

    Args:
        entity: словарь с данными существа

    Returns:
        True если HP > 0
    """
    return entity.get("hp", 0) > 0


def get_defense(character: dict) -> int:
    """
    Возвращает защиту персонажа с учётом экипировки.

    Args:
        character: словарь с данными персонажа

    Returns:
        Значение защиты
    """
    effective_stats = get_effective_stats(character)
    defense = effective_stats.get("выносливость", 0)

    # Добавляем бонус защиты от доспеха
    armor_id = character.get("equipment", {}).get("armor")
    if armor_id and armor_id in ARMORS:
        defense += ARMORS[armor_id].get("defense_bonus", 0)

    return defense


def get_attack_bonus(character: dict) -> tuple:
    """
    Возвращает бонусы к атаке и урону от оружия.

    Args:
        character: словарь с данными персонажа

    Returns:
        Кортеж (attack_bonus, damage_bonus)
    """
    weapon_id = character.get("equipment", {}).get("weapon")
    if weapon_id and weapon_id in WEAPONS:
        weapon = WEAPONS[weapon_id]
        return (weapon.get("attack_bonus", 0), weapon.get("damage_bonus", 0))

    return (0, 0)