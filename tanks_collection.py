from missiles_collection import check_missiles_collection
from random import randint
from units import Tank
import world
from tkinter import NW

_tanks = []
_canvas = None
id_screen_text = 0
_kills_count = 0  # Счетчик убитых врагов
_spawn_timer = 0  # Таймер для спавна врагов
_SPAWN_DELAY = 60  # Задержка между спавнами (в кадрах, ~1 секунда при 60 FPS)
_MAX_ENEMIES = 3  # Максимальное количество врагов на карте


def initialize(canv):
    global _canvas, id_screen_text
    _canvas = canv
    player = spawn(False)
    # Создаем 3 врагов изначально
    for _ in range(3):
        enemy = spawn(True)
        if enemy:
            enemy.set_target(player)
    id_screen_text = _canvas.create_text(10, 10, text=_get_screen_text(),
                                         font=('TkDefaultFont', 20, 'bold'),
                                         fill='white', anchor=NW)


def _get_screen_text():
    player = get_player()
    if player.is_destroyed():
        return 'Wasted'
    enemies_count = get_enemies_count()
    if enemies_count == 0:
        return f'Kills: {_kills_count} - WIN!'
    return f'Enemies: {enemies_count} | Kills: {_kills_count}'


def _update_screen_text():
    _canvas.itemconfig(id_screen_text, text=_get_screen_text())


def get_player():
    return _tanks[0] if _tanks else None


def get_enemies_count():
    """Возвращает количество живых врагов"""
    return len([t for t in _tanks if t.is_bot() and not t.is_destroyed()])


def get_kills_count():
    return _kills_count


def update():
    global _spawn_timer, _kills_count

    player = get_player()
    if not player or player.is_destroyed():
        # Если игрок мертв, просто обновляем экран
        for tank in _tanks:
            if not tank.is_destroyed():
                tank.update()
                check_collision(tank)
                check_missiles_collection(tank)
        _update_screen_text()
        return

    # Подсчет врагов ДО обновления, чтобы поймать момент когда враг умер
    enemies_before = get_enemies_count()

    # Обновляем всех
    start = len(_tanks) - 1
    enemies_destroyed = 0

    for i in range(start, -1, -1):
        tank = _tanks[i]
        if tank.is_destroyed():
            if tank.is_bot():  # Если уничтожен враг
                enemies_destroyed += 1
            del _tanks[i]
        else:
            tank.update()
            check_collision(tank)
            check_missiles_collection(tank)

    # Увеличиваем счетчик убийств
    _kills_count += enemies_destroyed

    # Спавн новых врагов
    current_enemies = get_enemies_count()

    if current_enemies < _MAX_ENEMIES:
        _spawn_timer += 1
        if _spawn_timer >= _SPAWN_DELAY:
            # Спавним врага до максимального количества
            enemies_to_spawn = _MAX_ENEMIES - current_enemies
            for _ in range(enemies_to_spawn):
                enemy = spawn(True)
                if enemy:
                    enemy.set_target(player)
            _spawn_timer = 0

    _update_screen_text()


def check_collision(tank):
    for other_tank in _tanks:
        if tank == other_tank:
            continue
        if tank.intersects(other_tank):
            return True
    return False


def spawn(is_bot=True):
    cols = world.get_cols()
    rows = world.get_rows()
    max_attempts = 50  # Максимальное количество попыток спавна

    for _ in range(max_attempts):
        col = randint(1, cols - 2)
        row = randint(1, rows - 2)

        if world.get_block(row, col) != world.GROUND:
            continue

        # Преобразуем координаты клетки в пиксельные координаты
        x = col * world.BLOCK_SIZE
        y = row * world.BLOCK_SIZE

        # Создаем временный танк для проверки коллизий
        temp_tank = Tank(_canvas, x, y, bot=is_bot)
        collision = check_collision(temp_tank)

        # Удаляем временный объект (не через __del__, а явно)
        try:
            temp_tank._canvas.delete(temp_tank._id)
            if hasattr(temp_tank, '_hp_indicator') and temp_tank._hp_indicator:
                temp_tank._hp_indicator.hide()
        except:
            pass

        if not collision:
            # Создаем настоящий танк
            tank = Tank(_canvas, x, y, bot=is_bot)
            _tanks.append(tank)
            return tank

    return None


def reset_game():
    """Сброс игры (можно использовать для перезапуска)"""
    global _tanks, _kills_count, _spawn_timer
    # Очищаем все танки
    for tank in _tanks:
        try:
            tank.destroy()
        except:
            pass
    _tanks = []
    _kills_count = 0
    _spawn_timer = 0