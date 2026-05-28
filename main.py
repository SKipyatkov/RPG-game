"""
Основной файл Telegram-бота «Кузница Персонажей».
"""

import telebot
from telebot import types
import time
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
from generator import create_character, get_effective_stats
from data import (save_character, get_character, update_stats, add_item, remove_item,
                  get_inventory, has_item, set_location, get_location, equip_item, unequip_item)
from rules import RACE_BONUSES, CLASS_BONUSES, CLASS_WEAPONS, CLASS_ARMORS
from world import WORLD
from bestiary import MONSTERS
from items import ITEMS, WEAPONS, ARMORS
from battle import calculate_damage, is_alive, get_defense, get_attack_bonus

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

user_states = {}
battle_states = {}

STAT_EMOJIS = {
    "сила": "💪",
    "ловкость": "🏃",
    "выносливость": "❤️",
    "интеллект": "🧠",
    "мудрость": "🦉",
    "восприятие": "👁️"
}

TRAIN_COOLDOWN_MIN = 10

LOCATION_TRAINING = {
    "стартовая_деревня": ["сила", "выносливость"],
    "тёмный_лес": ["ловкость", "восприятие"],
    "старая_мельница": ["интеллект", "мудрость"],
    "горный_перевал": ["сила", "выносливость"],
    "заброшенный_замок": ["интеллект", "восприятие"]
}

TRAIN_EVENTS = {
    "сила": {
        1: {"change": -1, "msg": "Ты поскользнулся на турнике и ушибся. {emoji} {stat} -1"},
        2: {"change": 1, "msg": "Неплохая тренировка! {emoji} {stat} +1"},
        3: {"change": 1, "msg": "Мышцы приятно напряглись. {emoji} {stat} +1"},
        4: {"change": 3, "msg": "Отличная работа! {emoji} {stat} +3"},
        5: {"change": 3, "msg": "Ты чувствуешь прилив сил! {emoji} {stat} +3"},
        6: {"change": 5, "msg": "🔥 НЕВЕРОЯТНО! Ты побил рекорд! {emoji} {stat} +5",
            "crit_fail_chance": 0.25,
            "crit_fail": {"change": -2, "msg": "💥 Штанга упала на тебя! {emoji} {stat} -2"}},
    },
    "ловкость": {
        1: {"change": -1, "msg": "Нога подвернулась на полосе препятствий. {emoji} {stat} -1"},
        2: {"change": 1, "msg": "Неплохо! Реакция улучшается. {emoji} {stat} +1"},
        3: {"change": 1, "msg": "Ты стал чуть проворнее. {emoji} {stat} +1"},
        4: {"change": 3, "msg": "Грациозно, как кошка! {emoji} {stat} +3"},
        5: {"change": 3, "msg": "Твои движения стали молниеносными. {emoji} {stat} +3"},
        6: {"change": 5, "msg": "⚡ Ты уклонился от невидимой атаки! {emoji} {stat} +5",
            "crit_fail_chance": 0.25,
            "crit_fail": {"change": -2, "msg": "🤕 Ты запнулся о свои ноги. {emoji} {stat} -2"}},
    },
    "выносливость": {
        1: {"change": -1, "msg": "Слишком быстро выдохся. {emoji} {stat} -1"},
        2: {"change": 1, "msg": "Дыхание стало ровнее. {emoji} {stat} +1"},
        3: {"change": 1, "msg": "Ты пробежал ещё круг. {emoji} {stat} +1"},
        4: {"change": 3, "msg": "Ты как скала — усталости нет! {emoji} {stat} +3"},
        5: {"change": 3, "msg": "Твоё тело становится выносливее. {emoji} {stat} +3"},
        6: {"change": 5, "msg": "🏔️ Ты готов взойти на Эверест! {emoji} {stat} +5",
            "crit_fail_chance": 0.25,
            "crit_fail": {"change": -2, "msg": "😵 Ты упал в обморок от перенапряжения. {emoji} {stat} -2"}},
    },
    "интеллект": {
        1: {"change": -1, "msg": "Голова болит от перенапряжения. {emoji} {stat} -1"},
        2: {"change": 1, "msg": "Ты запомнил новый факт. {emoji} {stat} +1"},
        3: {"change": 1, "msg": "Логика стала острее. {emoji} {stat} +1"},
        4: {"change": 3, "msg": "Ты решил сложную задачу! {emoji} {stat} +3"},
        5: {"change": 3, "msg": "Твой ум работает как швейцарские часы. {emoji} {stat} +3"},
        6: {"change": 5, "msg": "🧠 ЭВРИКА! Ты совершил открытие! {emoji} {stat} +5",
            "crit_fail_chance": 0.25,
            "crit_fail": {"change": -2, "msg": "📚 Ты так увлёкся чтением, что забыл всё остальное. {emoji} {stat} -2"}},
    },
    "мудрость": {
        1: {"change": -1, "msg": "Ты запутался в своих мыслях. {emoji} {stat} -1"},
        2: {"change": 1, "msg": "Ты обрёл немного ясности. {emoji} {stat} +1"},
        3: {"change": 1, "msg": "Жизненный опыт прибавляется. {emoji} {stat} +1"},
        4: {"change": 3, "msg": "Ты видишь суть вещей. {emoji} {stat} +3"},
        5: {"change": 3, "msg": "Твоё понимание мира углубилось. {emoji} {stat} +3"},
        6: {"change": 5, "msg": "🕯️ Ты постиг древнюю истину. {emoji} {stat} +5",
            "crit_fail_chance": 0.25,
            "crit_fail": {"change": -2,
                          "msg": "🌀 Ты ушёл в глубокую медитацию и потерял связь с реальностью. {emoji} {stat} -2"}},
    },
    "восприятие": {
        1: {"change": -1, "msg": "Ты упустил важную деталь. {emoji} {stat} -1"},
        2: {"change": 1, "msg": "Ты стал чуть внимательнее. {emoji} {stat} +1"},
        3: {"change": 1, "msg": "Твои чувства обострились. {emoji} {stat} +1"},
        4: {"change": 3, "msg": "Ты замечаешь то, что скрыто от других. {emoji} {stat} +3"},
        5: {"change": 3, "msg": "Твоё зрение стало орлиным. {emoji} {stat} +3"},
        6: {"change": 5, "msg": "🔍 Ты видишь сквозь ложь! {emoji} {stat} +5",
            "crit_fail_chance": 0.25,
            "crit_fail": {"change": -2, "msg": "👁️ Ты так всматривался, что устал. {emoji} {stat} -2"}},
    },
}

SPECIAL_EVENTS = {
    ("Вор", "интеллект"): {"change": -2, "msg": "🗡️ Пока ты читал, другой вор украл твою книгу! {emoji} {stat} -2"},
    ("Вор", "восприятие"): {"change": -1,
                            "msg": "👀 Ты так смотрел по сторонам, что не заметил, как украли твой кошелёк. {emoji} {stat} -1"},
    ("Маг", "сила"): {"change": -1,
                      "msg": "🪄 Ты попытался поднять штангу заклинанием, но она упала. {emoji} {stat} -1"},
    ("Воин", "интеллект"): {"change": -1, "msg": "⚔️ Книга оказалась тяжелее меча. Голова болит. {emoji} {stat} -1"},
}


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def format_character_card(char_data: dict) -> str:
    """Форматирует карточку персонажа для отображения."""
    name = char_data['name']
    race = char_data['race']
    char_class = char_data['class']
    level = char_data['level']
    xp = char_data.get('xp', 0)
    hp = char_data.get('hp', 0)
    max_hp = char_data.get('max_hp', 0)

    # Эффективные статы с учётом экипировки
    stats = get_effective_stats(char_data)

    card = f"🧝 {race}-{char_class} «{name}»\n"
    card += f"⭐ Уровень: {level} | ✨ Опыт: {xp}\n"
    card += f"❤️ HP: {hp}/{max_hp}\n\n"
    card += "📊 Характеристики:\n"
    for stat_name, emoji in STAT_EMOJIS.items():
        value = stats.get(stat_name, 0)
        card += f"{emoji} {stat_name.capitalize()}: {value}\n"

    # Экипировка
    equipment = char_data.get("equipment", {})
    card += "\n⚔️ Экипировка:\n"
    if equipment.get("weapon"):
        weapon = WEAPONS.get(equipment["weapon"], {})
        card += f"  🗡️ Оружие: {weapon.get('name', 'Нет')}\n"
    else:
        card += "  🗡️ Оружие: Нет\n"
    if equipment.get("armor"):
        armor = ARMORS.get(equipment["armor"], {})
        card += f"  🛡️ Доспех: {armor.get('name', 'Нет')}\n"
    else:
        card += "  🛡️ Доспех: Нет\n"

    return card


def format_inventory(user_id: int) -> str:
    """Форматирует инвентарь для отображения."""
    inv = get_inventory(user_id)
    if not inv:
        return "🎒 Рюкзак пуст"

    lines = ["🎒 Рюкзак:"]
    for item_id, amount in inv.items():
        name = None
        emoji = "📦"

        if item_id in ITEMS:
            name = ITEMS[item_id]["name"]
            if ITEMS[item_id]["type"] == "валюта":
                emoji = "🪙"
                lines.append(f"{emoji} {name}: {amount}")
                continue
            elif ITEMS[item_id]["type"] == "расходуемое":
                emoji = "🧪"
        elif item_id in WEAPONS:
            name = WEAPONS[item_id]["name"]
            emoji = "🗡️"
        elif item_id in ARMORS:
            name = ARMORS[item_id]["name"]
            emoji = "🛡️"

        if name:
            lines.append(f"{emoji} {name}: {amount} шт.")
        else:
            lines.append(f"📦 {item_id}: {amount}")

    return "\n".join(lines)


def check_training_cooldown(character: dict) -> tuple:
    """Проверяет кулдаун тренировки."""
    last = character.get("last_training")
    if not last:
        return True, ""

    try:
        last_dt = datetime.fromisoformat(last)
        diff = datetime.now() - last_dt
        if diff < timedelta(minutes=TRAIN_COOLDOWN_MIN):
            remaining = int((timedelta(minutes=TRAIN_COOLDOWN_MIN) - diff).total_seconds() // 60) + 1
            return False, f"⏳ Ты ещё устал. Подожди {remaining} мин."
    except:
        pass

    return True, ""


def get_training_outcome(stat: str, char_class: str, roll: int) -> dict:
    """Определяет результат тренировки."""
    events = TRAIN_EVENTS.get(stat, {})
    outcome = events.get(roll)
    if not outcome:
        return {"change": 0, "msg": "Что-то пошло не так..."}

    if roll == 6 and outcome.get("crit_fail_chance") and random.random() < outcome["crit_fail_chance"]:
        crit = outcome["crit_fail"]
        return {"change": crit["change"],
                "msg": crit["msg"].format(emoji=STAT_EMOJIS.get(stat, ""), stat=stat.capitalize())}

    special_key = (char_class, stat)
    if special_key in SPECIAL_EVENTS and random.random() < 0.25:
        spec = SPECIAL_EVENTS[special_key]
        return {"change": spec["change"],
                "msg": spec["msg"].format(emoji=STAT_EMOJIS.get(stat, ""), stat=stat.capitalize())}

    msg = outcome["msg"].format(emoji=STAT_EMOJIS.get(stat, ""), stat=stat.capitalize())
    return {"change": outcome["change"], "msg": msg}


# ========== МЕНЮ ==========

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Отправляет приветственное сообщение с меню."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("⚔️ Создать персонажа"),
        types.KeyboardButton("📜 Мой персонаж"),
        types.KeyboardButton("🎒 Инвентарь"),
        types.KeyboardButton("🏋️ Тренировать"),
        types.KeyboardButton("🗺️ Карта"),
        types.KeyboardButton("🏕️ Лагерь")
    )
    bot.send_message(
        message.chat.id,
        "🏰 Добро пожаловать в Кузницу Персонажей!\n\n"
        "Создай героя и отправляйся в приключение!",
        reply_markup=markup
    )


# ========== СОЗДАНИЕ ПЕРСОНАЖА ==========

@bot.message_handler(func=lambda m: m.text == "⚔️ Создать персонажа")
def start_creation(message):
    """Начинает процесс создания персонажа."""
    user_id = message.from_user.id
    user_states[user_id] = {"step": "выбор_расы"}

    markup = types.InlineKeyboardMarkup()
    for race_name in RACE_BONUSES.keys():
        markup.add(types.InlineKeyboardButton(text=race_name, callback_data=f"race:{race_name}"))

    bot.send_message(message.chat.id, "Выбери расу:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("race:"))
def handle_race_selection(call):
    """Обрабатывает выбор расы."""
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    _, race_name = call.data.split(":", 1)

    if user_id not in user_states:
        return

    user_states[user_id] = {"race": race_name, "step": "выбор_класса"}

    markup = types.InlineKeyboardMarkup()
    for class_name in CLASS_BONUSES.keys():
        markup.add(types.InlineKeyboardButton(text=class_name, callback_data=f"class:{class_name}"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Раса: {race_name}. Выбери класс:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("class:"))
def handle_class_selection(call):
    """Обрабатывает выбор класса."""
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    _, class_name = call.data.split(":", 1)

    if user_id not in user_states:
        return

    user_states[user_id]["class"] = class_name
    user_states[user_id]["step"] = "ввод_имени"

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Введи имя персонажа:"
    )


@bot.message_handler(func=lambda m: user_states.get(m.from_user.id, {}).get("step") == "ввод_имени")
def handle_name_input(message):
    """Обрабатывает ввод имени и создаёт персонажа."""
    user_id = message.from_user.id
    state = user_states[user_id]
    name = message.text.strip()
    race = state["race"]
    char_class = state["class"]

    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)

    character = create_character(name, race, char_class)
    save_character(user_id, character)
    del user_states[user_id]

    card_text = format_character_card(character)
    equip_info = (
        f"\n\n🎁 Стартовое снаряжение:\n"
        f"• {WEAPONS[character['equipment']['weapon']]['name']}\n"
        f"• {ARMORS[character['equipment']['armor']]['name']}"
    )
    bot.send_message(message.chat.id, "✅ Персонаж создан!\n\n" + card_text + equip_info)


# ========== ПРОСМОТР ПЕРСОНАЖА ==========

@bot.message_handler(func=lambda m: m.text == "📜 Мой персонаж")
def view_character(message):
    """Показывает карточку персонажа."""
    user_id = message.from_user.id
    character = get_character(user_id)

    if not character:
        bot.send_message(message.chat.id, "У тебя ещё нет персонажа. Нажми «⚔️ Создать персонажа»!")
    else:
        bot.send_message(message.chat.id, format_character_card(character))


# ========== ИНВЕНТАРЬ ==========

@bot.message_handler(func=lambda m: m.text == "🎒 Инвентарь")
def view_inventory(message):
    """Показывает инвентарь персонажа."""
    user_id = message.from_user.id
    character = get_character(user_id)

    if not character:
        bot.send_message(message.chat.id, "Сначала создай персонажа!")
        return

    bot.send_message(message.chat.id, format_inventory(user_id))


# ========== ТРЕНИРОВКА ==========

@bot.message_handler(func=lambda m: m.text == "🏋️ Тренировать")
def start_training(message):
    """Начинает процесс тренировки."""
    user_id = message.from_user.id
    character = get_character(user_id)

    if not character:
        bot.send_message(message.chat.id, "Сначала создай персонажа!")
        return

    location = get_location(user_id)
    available_stats = LOCATION_TRAINING.get(location, [])

    if not available_stats:
        bot.send_message(message.chat.id, "Здесь негде тренироваться.")
        return

    markup = types.InlineKeyboardMarkup()
    for stat_name in available_stats:
        emoji = STAT_EMOJIS[stat_name]
        markup.add(types.InlineKeyboardButton(
            text=f"{emoji} {stat_name.capitalize()}",
            callback_data=f"train:{stat_name}"
        ))

    bot.send_message(
        message.chat.id,
        f"📍 {WORLD[location]['name']}\nКакую характеристику тренируем?",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("train:"))
def handle_training(call):
    """Обрабатывает тренировку характеристики."""
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    _, stat_name = call.data.split(":", 1)

    character = get_character(user_id)
    if not character:
        bot.send_message(call.message.chat.id, "❌ Персонаж не найден.")
        return

    can_train, cooldown_msg = check_training_cooldown(character)
    if not can_train:
        bot.send_message(call.message.chat.id, cooldown_msg)
        return

    roll = random.randint(1, 6)
    char_class = character.get("class", "")
    result = get_training_outcome(stat_name, char_class, roll)
    change = result["change"]
    msg = result["msg"]

    updated_char = update_stats(user_id, stat_name, change)

    if updated_char:
        character["last_training"] = datetime.now().isoformat()
        save_character(user_id, character)

        emoji = STAT_EMOJIS.get(stat_name, "")
        new_value = updated_char["stats"][stat_name]
        sign = "+" if change >= 0 else ""
        response = f"🎲 Выпало: {roll}\n{msg}\n📊 {emoji} {stat_name.capitalize()}: {new_value}"
        bot.send_message(call.message.chat.id, response)
    else:
        bot.send_message(call.message.chat.id, "❌ Ошибка при обновлении.")


# ========== КАРТА И ПЕРЕМЕЩЕНИЕ ==========

@bot.message_handler(func=lambda m: m.text == "🗺️ Карта")
def show_map(message):
    """Показывает карту с доступными направлениями."""
    user_id = message.from_user.id
    character = get_character(user_id)

    if not character:
        bot.send_message(message.chat.id, "Сначала создай персонажа!")
        return

    location_id = get_location(user_id)
    location = WORLD[location_id]

    text = f"📍 {location['name']}\n{location['description']}\n\n🚪 Выходы:"

    markup = types.InlineKeyboardMarkup()
    direction_emojis = {
        "север": "⬆️ Север",
        "юг": "⬇️ Юг",
        "запад": "⬅️ Запад",
        "восток": "➡️ Восток"
    }

    for direction, target_id in location["connections"].items():
        text += f"\n{direction_emojis[direction]} → {WORLD[target_id]['name']}"
        markup.add(types.InlineKeyboardButton(
            text=direction_emojis[direction],
            callback_data=f"move:{direction}"
        ))

    if not location["connections"]:
        text += "\n🚪 Выходов нет"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("move:"))
def handle_move(call):
    """Обрабатывает перемещение между локациями."""
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    _, direction = call.data.split(":", 1)

    character = get_character(user_id)
    if not character:
        bot.send_message(call.message.chat.id, "Сначала создай персонажа!")
        return

    current_location = get_location(user_id)
    target_id = WORLD[current_location]["connections"].get(direction)

    if not target_id:
        bot.send_message(call.message.chat.id, "Туда нельзя идти.")
        return

    target = WORLD[target_id]

    # Проверка требований
    for item, amount in target["requirements"].items():
        if not has_item(user_id, item, amount):
            item_name = ITEMS.get(item, {}).get("name", item)
            bot.send_message(
                call.message.chat.id,
                f"❌ Чтобы войти в «{target['name']}», нужно: {item_name} ×{amount}"
            )
            return

    # Перемещение
    set_location(user_id, target_id)

    # Проверка первого входа
    character = get_character(user_id)
    text = f"📍 {target['name']}\n{target['description']}"

    if target_id not in character.get("visited_locations", []):
        character["visited_locations"] = character.get("visited_locations", []) + [target_id]

        # Бонус первого входа
        if target_id == "старая_мельница":
            add_item(user_id, "lockpick", 1)
            text += "\n\n🔍 Ты нашёл отмычку среди хлама!"
        elif target_id == "заброшенный_замок":
            add_item(user_id, "gold", 50)
            text += "\n\n🪙 Ты нашёл сундук с золотом! +50 золота"

        save_character(user_id, character)

    bot.send_message(call.message.chat.id, text)

    # Проверка встречи с монстром
    encounter_chance = target.get("encounter_chance", 0)
    monsters = target.get("monsters", [])

    if monsters and random.random() < encounter_chance:
        monster_id = random.choice(monsters)
        monster_data = MONSTERS[monster_id]
        monster_copy = {"id": monster_id, **monster_data, "hp": monster_data["hp"]}

        battle_states[user_id] = {
            "monster": monster_copy,
            "monster_hp": monster_data["hp"],
            "character_hp": character["hp"],
            "defending": False
        }

        battle_text = (
            f"⚔️ Ты встретил {monster_data['name']}!\n"
            f"{monster_data['description']}\n\n"
            f"❤️ Твоё HP: {character['hp']}/{character['max_hp']}\n"
            f"❤️ HP {monster_data['name']}: {monster_data['hp']}/{monster_data['hp']}\n\n"
            f"Что делаешь?"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⚔️ Атаковать", callback_data="battle:attack"))
        markup.add(types.InlineKeyboardButton("🛡️ Защищаться", callback_data="battle:defend"))
        if has_item(user_id, "healing_potion"):
            markup.add(types.InlineKeyboardButton("🧪 Зелье лечения", callback_data="battle:use_potion"))
        markup.add(types.InlineKeyboardButton("🏃 Сбежать", callback_data="battle:flee"))

        bot.send_message(call.message.chat.id, battle_text, reply_markup=markup)


# ========== БОЕВАЯ СИСТЕМА ==========

@bot.callback_query_handler(func=lambda call: call.data.startswith("battle:"))
def handle_battle(call):
    """Обрабатывает действия в бою."""
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if user_id not in battle_states:
        bot.send_message(chat_id, "Бой уже закончен.")
        return

    _, action = call.data.split(":", 1)
    battle = battle_states[user_id]
    character = get_character(user_id)

    if not character:
        bot.send_message(chat_id, "Персонаж не найден.")
        return

    monster = battle["monster"]
    effective_stats = get_effective_stats(character)
    attack_bonus, damage_bonus = get_attack_bonus(character)

    if action == "attack":
        battle["defending"] = False
        # Герой атакует
        hero_dmg = calculate_damage(0, effective_stats["сила"], monster["defense"], damage_bonus)
        battle["monster_hp"] -= hero_dmg
        msg = f"⚔️ Ты атакуешь! Наносишь {hero_dmg} урона.\n"

        if battle["monster_hp"] <= 0:
            # Победа
            msg += f"\n🎉 Ты победил {monster['name']}!\n"
            msg += "📦 Добыча:\n"
            for item_id, amount in monster["loot"].items():
                add_item(user_id, item_id, amount)
                name = item_id
                if item_id in ITEMS:
                    name = ITEMS[item_id]["name"]
                elif item_id in WEAPONS:
                    name = WEAPONS[item_id]["name"]
                elif item_id in ARMORS:
                    name = ARMORS[item_id]["name"]
                msg += f"  • {name} ×{amount}\n"

            # Добавляем опыт
            xp_gained = monster.get("xp", 0)
            character["xp"] = character.get("xp", 0) + xp_gained
            msg += f"\n✨ Получено опыта: {xp_gained}"

            # Проверка повышения уровня
            xp_needed = character["level"] * 100
            if character["xp"] >= xp_needed:
                character["level"] += 1
                character["xp"] -= xp_needed
                msg += f"\n⭐ Уровень повышен! Теперь ты {character['level']} уровня!"

            save_character(user_id, character)
            del battle_states[user_id]
            bot.send_message(chat_id, msg)
            return
        else:
            msg += f"❤️ HP {monster['name']}: {battle['monster_hp']}/{monster['hp']}\n"

    elif action == "defend":
        battle["defending"] = True
        msg = "🛡️ Ты встал в защитную стойку! Урон будет снижен вдвое.\n"

    elif action == "use_potion":
        if has_item(user_id, "healing_potion"):
            remove_item(user_id, "healing_potion", 1)
            heal = 5
            battle["character_hp"] = min(battle["character_hp"] + heal, character["max_hp"])
            msg = f"🧪 Ты выпил зелье лечения! +{heal} HP\n"
        else:
            msg = "❌ У тебя нет зелья лечения!\n"

    elif action == "flee":
        if random.random() < 0.5:
            del battle_states[user_id]
            bot.send_message(chat_id, "🏃 Ты сбежал! Монстр потерял твой след.")
            return
        else:
            msg = "❌ Не получилось сбежать!\n"

    # Монстр атакует (если не умер)
    if battle["monster_hp"] > 0:
        hero_defense = get_defense(character)

        monster_dmg = calculate_damage(monster["attack"], 0, hero_defense)
        if battle["defending"]:
            monster_dmg = max(1, monster_dmg // 2)
            battle["defending"] = False

        battle["character_hp"] -= monster_dmg
        msg += f"💥 {monster['name']} атакует! Наносит {monster_dmg} урона.\n"

        if battle["character_hp"] <= 0:
            # Поражение
            del battle_states[user_id]
            gold_lost = character.get("inventory", {}).get("gold", 0) // 5
            if gold_lost > 0:
                remove_item(user_id, "gold", gold_lost)
            character["hp"] = character["max_hp"]
            set_location(user_id, "стартовая_деревня")
            save_character(user_id, character)

            msg += (
                f"\n💀 Ты пал в бою...\n"
                f"Потеряно золота: {gold_lost}\n"
                f"Ты очнулся в Стартовой деревне."
            )
            bot.send_message(chat_id, msg)
            return

    # Обновление HP персонажа
    character["hp"] = battle["character_hp"]
    save_character(user_id, character)

    # Обновление состояния боя
    msg += f"\n❤️ Твоё HP: {battle['character_hp']}/{character['max_hp']}"
    if battle["monster_hp"] > 0:
        msg += f"\n❤️ HP {monster['name']}: {battle['monster_hp']}/{monster['hp']}"

    msg += "\n\nЧто делаешь?"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⚔️ Атаковать", callback_data="battle:attack"))
    markup.add(types.InlineKeyboardButton("🛡️ Защищаться", callback_data="battle:defend"))
    if has_item(user_id, "healing_potion"):
        markup.add(types.InlineKeyboardButton("🧪 Зелье лечения", callback_data="battle:use_potion"))
    markup.add(types.InlineKeyboardButton("🏃 Сбежать", callback_data="battle:flee"))

    bot.send_message(chat_id, msg, reply_markup=markup)


# ========== ЛАГЕРЬ ==========

@bot.message_handler(func=lambda m: m.text == "🏕️ Лагерь")
def show_camp(message):
    """Показывает полную информацию о персонаже в лагере."""
    user_id = message.from_user.id
    character = get_character(user_id)

    if not character:
        bot.send_message(message.chat.id, "Сначала создай персонажа!")
        return

    location_id = get_location(user_id)
    location = WORLD[location_id]

    card = format_character_card(character)
    camp_text = f"{card}\n\n📍 Локация: {location['name']}\n\n{format_inventory(user_id)}"
    bot.send_message(message.chat.id, camp_text)


# ========== ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ ==========

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    """Обрабатывает все остальные текстовые сообщения."""
    if message.text in ["⚔️ Создать персонажа", "📜 Мой персонаж", "🎒 Инвентарь",
                        "🏋️ Тренировать", "🗺️ Карта", "🏕️ Лагерь"]:
        return  # Уже обработано другими хендлерами

    bot.send_message(
        message.chat.id,
        "Используй кнопки меню для навигации.\n"
        "Доступные команды:\n"
        "• ⚔️ Создать персонажа\n"
        "• 📜 Мой персонаж\n"
        "• 🎒 Инвентарь\n"
        "• 🏋️ Тренировать\n"
        "• 🗺️ Карта\n"
        "• 🏕️ Лагерь"
    )


if __name__ == "__main__":
    print("🤖 Бот «Кузница Персонажей» запущен...")
    bot.infinity_polling()