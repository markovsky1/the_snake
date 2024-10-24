from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """The base class for all game objects.

    Attributes:
        position (tuple): The current position of the object on the playing
        field.
        body_color (purple): The color of the object.
    """

    def __init__(self):
        """Initializing an object with basic attributes."""
        self.position = (CENTER_COORDINATES)
        self.body_color = None

    def draw(self):
        """Method for drawing an object. Redefined in child classes."""
        pass


class Apple(GameObject):
    """A class representing an apple on the playing field."""

    def __init__(self):
        """Initializing an apple with a given color and a random position."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def draw(self):
        """Draws an apple on the screen."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Generating a random apple position on the playing field."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)


class Snake(GameObject):
    """A class representing a snake on the playing field."""

    def __init__(self):
        """ Initializing a snake with the original length,
        position, color and direction.
        """
        super().__init__()
        self.length = 1
        self.positions = [CENTER_COORDINATES]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def draw(self):
        """Drawing a snake on the screen."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # if self.last:
        #     last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
        #     pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
            self.positions.pop()

    def reset(self):
        """Resets the state of the snake to the initial parameters."""
        self.length = 1
        self.positions = [CENTER_COORDINATES]
        self.direction = choice(DIRECTIONS)
        self.next_direction = None

    def check_self_collision(self):
        """Checks if the snake has collided with itself.
        True if the snake collided with itself, otherwise False.
        """
        if self.positions[0] in self.positions[1:]:
            return True
        else:
            return False


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Processes the input for controlling the snake."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """The main game function that starts the game."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # print(f'{snake.positions} l={snake.length}')
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.check_self_collision():
            snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
