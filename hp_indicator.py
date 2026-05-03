import world
import texture as skin


class HPIndicator:

    def __init__(self, canvas, owner):
        self._canvas = canvas
        self._owner = owner
        self._image_id = None
        self._offset_y = -15  # БЫЛО -20, СТАЛО -40 (сильнее вверх)
        self._create()  # ОТЛАДКА

    def update(self):
        """Обновляет позицию и текстуру индикатора"""
        if self._image_id is None:
            return

        # Новая позиция на основе текущего положения танка
        x = self._owner.get_x() + self._owner.get_size() // 2
        y = self._owner.get_y() + self._offset_y

        screen_x = world.get_screen_x(x)
        screen_y = world.get_screen_y(y)

        # Перемещаем индикатор
        self._canvas.coords(self._image_id, screen_x, screen_y)

        # Обновляем текстуру если изменилось HP
        hp = self._owner.get_hp()
        texture_name = self._get_texture_by_hp(hp)
        self._canvas.itemconfig(self._image_id, image=skin.get(texture_name))

    def _get_texture_by_hp(self, hp):
        if hp > 75:
            return '100_hp'
        elif hp > 50:
            return '75_hp'
        elif hp > 25:
            return '50_hp'
        else:
            return '25_hp'

    def _create(self):
        hp = self._owner.get_hp()
        texture_name = self._get_texture_by_hp(hp)
        # Позиция над танком (центр танка + смещение вверх)
        tank_center_x = self._owner.get_x() + self._owner.get_size() // 2
        tank_center_y = self._owner.get_y()
        x = tank_center_x
        y = tank_center_y - 20  # Смещение вверх на 20 пикселей

        screen_x = world.get_screen_x(x)
        screen_y = world.get_screen_y(y)

        self._image_id = self._canvas.create_image(
            screen_x, screen_y,
            image=skin.get(texture_name),
            anchor='center'
        )
    def hide(self):
        if self._image_id is not None:
            self._canvas.delete(self._image_id)
            self._image_id = None