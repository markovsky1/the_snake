"""Привет Данила!
Меня зовут Игорь, а я сейчас работаю инженером конструктором.
Очень приятно  познакомиться!
Я поправил все критичные ошибки на которые ты указал
и "Можно исправить" на которые хватило времени.
"""
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Координаты центра:
CENTER_COORDINATES = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """The base class for all game objects.

    Attributes:
        position (tuple): The current position of the object on the playing
        field.
        body_color (purple): The color of the object.
    """

    def __init__(self, body_color=None):
        """Initializing an object with basic attributes."""
        self.position = (CENTER_COORDINATES)
        self.body_color = body_color

    def draw(self):
        """Method for drawing an object. Redefined in child classes."""
        raise NotImplementedError(
            f'Method draw must be implemented '
            f'in subclass {self.__class__.__name__}.'
        )

    def drawing_a_rect(self, position=None):
        """Drawing a rectangle."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """A class representing an apple on the playing field."""

    def __init__(self, occupied_cells=None):
        """Initializing an apple with a given color and a random position."""
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied_cells=None)

    def draw(self):
        """Draws an apple on the screen."""
        self.drawing_a_rect(self.position)

    def randomize_position(self, occupied_cells=None):
        """Generating a random apple position on the playing field."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if occupied_cells is None or self.position not in occupied_cells:
                break


class Snake(GameObject):
    """A class representing a snake on the playing field."""

    def __init__(self):
        """Initializing a snake with the original length,
        position, color and direction.
        """
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.positions = [CENTER_COORDINATES]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Drawing a snake on the screen."""
        for position in self.positions[:-1]:
            self.drawing_a_rect(position)
        # Отрисовка головы змейки
        self.drawing_a_rect(self.get_head_position())
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Updates the direction of travel to a new one, if it is set."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Returns the current position of the snake's head."""
        return self.positions[0]

    def move(self):
        """Moves the snake in the current direction, updating its position."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        self.positions.insert(
            0,
            (
                (x + dx * GRID_SIZE) % SCREEN_WIDTH,
                (y + dy * GRID_SIZE) % SCREEN_HEIGHT
            )
        )
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Resets the state of the snake to the initial parameters."""
        self.length = 1
        self.positions = [CENTER_COORDINATES]
        self.direction = choice(DIRECTIONS)
        self.next_direction = None


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Processes the input for controlling the snake."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """The main game function that starts the game."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_cells=snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
