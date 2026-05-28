"""
Модуль работы с JSON-хранилищем персонажей.
"""

import json
import os
from items import WEAPONS, ARMORS
from rules import CLASS_WEAPONS, CLASS_ARMORS

FILENAME = "characters.json"


def load_characters() -> dict:
    """
    Загружает всех персонажей из файла.

    Returns:
        Словарь с персонажами или пустой словарь
    """
    if not os.path.exists(FILENAME):
        _save_raw_data({"characters": {}})
        return {}

    try:
        with open(FILENAME, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get("characters", {})
    except (json.JSONDecodeError, FileNotFoundError):
        _save_raw_data({"characters": {}})
        return {}


def _save_raw_data(data: dict):
    """
    Сохраняет данные в JSON-файл.

    Args:
        data: данные для сохранения
    """
    with open(FILENAME, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def save_character(user_id: int, character: dict):
    """
    Сохраняет персонажа пользователя.

    Args:
        user_id: ID пользователя
        character: данные персонажа
    """
    data = {"characters": load_characters()}
    data["characters"][str(user_id)] = character
    _save_raw_data(data)


def get_character(user_id: int) -> dict or None:
    """
    Получает персонажа пользователя.

    Args:
        user_id: ID пользователя

    Returns:
        Словарь с данными персонажа или None
    """
    characters = load_characters()
    return characters.get(str(user_id))


def update_stats(user_id: int, stat: str, amount: int):
    """
    Обновляет конкретную характеристику персонажа.

    Args:
        user_id: ID пользователя
        stat: название характеристики
        amount: величина изменения

    Returns:
        Обновлённый персонаж или None
    """
    character = get_character(user_id)
    if not character:
        return None

    if stat in character.get("stats", {}):
        character["stats"][stat] += amount
        # Обновляем max_hp если изменилась выносливость
        if stat == "выносливость":
            new_max_hp = 20 + character["stats"]["выносливость"]
            diff = new_max_hp - character.get("max_hp", 20)
            character["max_hp"] = new_max_hp
            if character.get("hp", 0) > 0:
                character["hp"] = min(character["hp"] + diff, new_max_hp)
        save_character(user_id, character)
        return character
    return None


def add_item(user_id: int, item: str, amount: int = 1):
    """
    Добавляет предмет в инвентарь персонажа.

    Args:
        user_id: ID пользователя
        item: ID предмета
        amount: количество
    """
    character = get_character(user_id)
    if not character:
        return

    if "inventory" not in character:
        character["inventory"] = {}

    character["inventory"][item] = character["inventory"].get(item, 0) + amount
    save_character(user_id, character)


def remove_item(user_id: int, item: str, amount: int = 1) -> bool:
    """
    Убирает предмет из инвентаря.

    Args:
        user_id: ID пользователя
        item: ID предмета
        amount: количество

    Returns:
        True если успешно, False если предмета нет
    """
    character = get_character(user_id)
    if not character:
        return False

    inventory = character.get("inventory", {})
    if item not in inventory or inventory[item] < amount:
        return False

    inventory[item] -= amount
    if inventory[item] <= 0:
        del inventory[item]

    save_character(user_id, character)
    return True


def get_inventory(user_id: int) -> dict:
    """
    Возвращает инвентарь персонажа.

    Args:
        user_id: ID пользователя

    Returns:
        Словарь инвентаря
    """
    character = get_character(user_id)
    if not character:
        return {}
    return character.get("inventory", {})


def has_item(user_id: int, item: str, amount: int = 1) -> bool:
    """
    Проверяет наличие предмета в инвентаре.

    Args:
        user_id: ID пользователя
        item: ID предмета
        amount: необходимое количество

    Returns:
        True если предмет есть в нужном количестве
    """
    inventory = get_inventory(user_id)
    return inventory.get(item, 0) >= amount


def set_location(user_id: int, location_id: str):
    """
    Устанавливает текущую локацию персонажа.

    Args:
        user_id: ID пользователя
        location_id: ID локации
    """
    character = get_character(user_id)
    if not character:
        return

    character["current_location"] = location_id

    if "visited_locations" not in character:
        character["visited_locations"] = []

    if location_id not in character["visited_locations"]:
        character["visited_locations"].append(location_id)

    save_character(user_id, character)


def get_location(user_id: int) -> str:
    """
    Возвращает текущую локацию персонажа.

    Args:
        user_id: ID пользователя

    Returns:
        ID локации
    """
    character = get_character(user_id)
    if not character:
        return "стартовая_деревня"
    return character.get("current_location", "стартовая_деревня")


def equip_item(user_id: int, item_id: str) -> bool:
    """
    Экипирует предмет на персонажа.

    Args:
        user_id: ID пользователя
        item_id: ID предмета

    Returns:
        True если успешно
    """
    character = get_character(user_id)
    if not character:
        return False

    # Проверяем наличие предмета
    if not has_item(user_id, item_id):
        return False

    # Определяем тип предмета
    if item_id in WEAPONS:
        item_type = "weapon"
        item_data = WEAPONS[item_id]
        class_list = CLASS_WEAPONS
    elif item_id in ARMORS:
        item_type = "armor"
        item_data = ARMORS[item_id]
        class_list = CLASS_ARMORS
    else:
        return False

    # Проверяем доступность предмета классу
    char_class = character.get("class")
    available_items = class_list.get(char_class, [])
    if item_id not in available_items:
        return False

    # Проверяем уровень
    if item_data.get("required_level", 1) > character.get("level", 0):
        return False

    # Снимаем старый предмет если есть
    old_item = character.get("equipment", {}).get(item_type)
    if old_item:
        # Возвращаем старый предмет в инвентарь
        add_item(user_id, old_item, 1)

    # Надеваем новый предмет
    if "equipment" not in character:
        character["equipment"] = {}
    character["equipment"][item_type] = item_id

    # Убираем из инвентаря
    remove_item(user_id, item_id, 1)

    save_character(user_id, character)
    return True


def unequip_item(user_id: int, slot: str) -> bool:
    """
    Снимает предмет из указанного слота.

    Args:
        user_id: ID пользователя
        slot: слот (weapon или armor)

    Returns:
        True если успешно
    """
    character = get_character(user_id)
    if not character:
        return False

    if slot not in ["weapon", "armor"]:
        return False

    equipment = character.get("equipment", {})
    item_id = equipment.get(slot)

    if not item_id:
        return False

    # Возвращаем предмет в инвентарь
    add_item(user_id, item_id, 1)

    # Убираем из слота
    equipment[slot] = None
    character["equipment"] = equipment

    save_character(user_id, character)
    return True