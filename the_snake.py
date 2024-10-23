import pygame
import random

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # черный цвет фона
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Глобальные переменные для экрана и часов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake pwnz edition')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=None):
        """Инициализирует базовые атрибуты объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Абстрактный метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__()
        self.image = self.load_image('apple.png')
        self.randomize_position()

    def load_image(self, name):
        """Загрузка изображения и обработка ошибок."""
        try:
            image = pygame.image.load(name)
            return pygame.transform.scale(image, (20, 20))
        except pygame.error as e:
            print(f"Не удалось загрузить изображение {name}: {e}")
            raise SystemExit

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, screen):
        """Отрисовывает яблоко на игровой поверхности."""
        screen.blit(self.image, self.position)


class Poison(GameObject):
    """Класс для яда."""

    def __init__(self):
        """Инициализирует яд."""
        super().__init__()
        self.image = self.load_image('poison.png')
        self.randomize_position()

    def load_image(self, name):
        """Загрузка изображения и обработка ошибок."""
        try:
            image = pygame.image.load(name)
            return pygame.transform.scale(image, (20, 20))
        except pygame.error as e:
            print(f"Не удалось загрузить изображение {name}: {e}")
            raise SystemExit

    def randomize_position(self):
        """Устанавливает случайное положение яда на игровом поле."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, screen):
        """Отрисовывает яд на игровой поверхности."""
        screen.blit(self.image, self.position)


class Rock(GameObject):
    """Класс для камня."""

    def __init__(self):
        """Инициализирует камень."""
        super().__init__()
        self.image = self.load_image('rock.png')
        self.randomize_position()

    def load_image(self, name):
        """Загрузка изображения и обработка ошибок."""
        try:
            image = pygame.image.load(name)
            return pygame.transform.scale(image, (20, 20))
        except pygame.error as e:
            print(f"Не удалось загрузить изображение {name}: {e}")
            raise SystemExit

    def randomize_position(self):
        """Устанавливает случайное положение камня на игровом поле."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, screen):
        """Отрисовывает камень на игровой поверхности."""
        screen.blit(self.image, self.position)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__((320, 240), None)
        self.length = 1
        self.positions = [self.position]
        self.direction = 'right'
        self.next_direction = None
        self.head_image = self.load_image('snake_head.png')
        self.body_image = self.load_image('snake_body.png')
        self.lives = 3

    def load_image(self, name):
        """Загрузка изображения и обработка ошибок."""
        try:
            image = pygame.image.load(name)
            return pygame.transform.scale(image, (20, 20))
        except pygame.error as e:
            print(f"Не удалось загрузить изображение {name}: {e}")
            raise SystemExit

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_position = self.get_head_position()
        if self.direction == 'right':
            new_head_position = (head_position[0] + GRID_SIZE,
                                 head_position[1])
        elif self.direction == 'left':
            new_head_position = (head_position[0] - GRID_SIZE,
                                 head_position[1])
        elif self.direction == 'up':
            new_head_position = (head_position[0],
                                 head_position[1] - GRID_SIZE)
        elif self.direction == 'down':
            new_head_position = (head_position[0],
                                 head_position[1] + GRID_SIZE)

        # Проверка выхода за границы игрового поля
        new_head_position = (
            new_head_position[0] % SCREEN_WIDTH,
            new_head_position[1] % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, screen):
        """Отрисовывает змейку на игровой поверхности."""
        screen.blit(self.head_image, self.get_head_position())
        for position in self.positions[1:self.length]:
            screen.blit(self.body_image, position)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = 'right'
        self.next_direction = None
        self.lives = 3


def display_game_over(screen):
    """Отображает заставку GAME OVER."""
    font = pygame.font.SysFont('Arial', 50)
    game_over_surface = font.render('GAME OVER', True, (255, 0, 0))
    text_rect = game_over_surface.get_rect(center=(
        screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(game_over_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)


def draw_text_with_outline(screen, text, font, color, outline_color, position):
    """Отрисовывает текст с обводкой."""
    text_surface = font.render(text, True, color)
    outline_surface = font.render(text, True, outline_color)

    # Рисуем обводку (сначала)
    screen.blit(outline_surface, (position[0] - 2, position[1] - 2))
    screen.blit(outline_surface, (position[0] + 2, position[1] - 2))
    screen.blit(outline_surface, (position[0] - 2, position[1] + 2))
    screen.blit(outline_surface, (position[0] + 2, position[1] + 2))

    # Рисуем основной текст
    screen.blit(text_surface, position)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake.direction != 'right':
        snake.next_direction = 'left'
    elif keys[pygame.K_RIGHT] and snake.direction != 'left':
        snake.next_direction = 'right'
    elif keys[pygame.K_UP] and snake.direction != 'down':
        snake.next_direction = 'up'
    elif keys[pygame.K_DOWN] and snake.direction != 'up':
        snake.next_direction = 'down'


def handle_menu_selection(event, selected_option, options):
    """Обрабатывает выбор в меню."""
    if event.key == pygame.K_UP:
        selected_option = (selected_option - 1) % len(options)
    elif event.key == pygame.K_DOWN:
        selected_option = (selected_option + 1) % len(options)
    return selected_option


def display_menu(screen):
    """Отображает главное меню."""
    font = pygame.font.SysFont('Arial', 36)
    options = ["Новая игра", "Выйти из игры"]
    selected_option = 0
    background_image = pygame.image.load('background.png')
    background_image = pygame.transform.scale(background_image,
                                              (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        screen.blit(background_image, (0, 0))

        draw_text_with_outline(
            screen, "Snake X pwnz", font, (255, 255, 255),
            (0, 0, 0), (screen.get_width() // 2 - 100, 20)
        )

        total_height = len(options) * 40

        for index, option in enumerate(options):
            color = (255, 255, 255) if index == selected_option else (100,
                                                                      100, 100)
            menu_surface = font.render(option, True, color)

            menu_x = (screen.get_width() // 2 - menu_surface.get_width() // 2)
            menu_y = screen.get_height() // 2 - total_height // 2 + index * 40

            screen.blit(menu_surface, (menu_x, menu_y))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                selected_option = handle_menu_selection(event,
                                                        selected_option,
                                                        options)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return "new_game"
                    elif selected_option == 1:
                        pygame.quit()
                        return


def display_difficulty_menu(screen):
    """Отображает меню выбора сложности."""
    font = pygame.font.SysFont('Arial', 36)
    options = ["Легко", "Нормально", "Сложно"]
    selected_option = 0
    background_image = pygame.image.load('background.png')
    background_image = pygame.transform.scale(background_image,
                                              (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        screen.blit(background_image, (0, 0))

        draw_text_with_outline(
            screen, "Snake X pwnz", font, (255, 255, 255),
            (0, 0, 0), (screen.get_width() // 2 - 100, 20)
        )

        total_height = len(options) * 40

        for index, option in enumerate(options):
            color = (255, 255, 255) if index == selected_option else (100,
                                                                      100, 100)
            menu_surface = font.render(option, True, color)

            menu_x = (screen.get_width() // 2 - menu_surface.get_width() // 2)
            menu_y = (screen.get_height() // 2 - total_height // 2)
            menu_y += index * 40

            screen.blit(menu_surface, (menu_x, menu_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected_option


def handle_game_events(snake):
    """Обрабатывает события игры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.direction != 'right':
                snake.next_direction = 'left'
            elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                snake.next_direction = 'right'
            elif event.key == pygame.K_UP and snake.direction != 'down':
                snake.next_direction = 'up'
            elif event.key == pygame.K_DOWN and snake.direction != 'up':
                snake.next_direction = 'down'
    return True


def update_game_state(snake, apple, poisons, rocks, score):
    """Обновляет состояние игры."""
    snake.update_direction()
    snake.move()

    # Проверка столкновения с яблоком
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position()
        score += 1

    # Проверка столкновения с ядами
    for poison in poisons:
        if snake.get_head_position() == poison.position:
            snake.lives -= 1
            poison.randomize_position()
            if snake.lives == 0:
                return False, score

    # Проверка столкновения с камнями
    for rock in rocks:
        if snake.get_head_position() == rock.position:
            snake.length = 0
            rock.randomize_position()
            snake.lives -= 1
            if snake.lives == 0:
                return False, score

    # Проверка столкновения со своим телом
    if snake.get_head_position() in snake.positions[1:]:
        snake.lives -= 1
        if snake.lives == 0:
            return False, score

    return True, score


def draw_game_objects(screen, snake, apple, poisons, rocks):
    """Отрисовывает игровые объекты."""
    snake.draw(screen)
    apple.draw(screen)
    for poison in poisons:
        poison.draw(screen)
    for rock in rocks:
        rock.draw(screen)


def display_game(screen, difficulty):
    """Основная игровая логика."""
    apple = Apple()
    snake = Snake()

    # Уровень сложности определяет количество ядов и камней
    if difficulty == 0:  # Легко
        poisons = [Poison() for _ in range(1)]
        rocks = [Rock() for _ in range(1)]
    elif difficulty == 1:  # Нормально
        poisons = [Poison() for _ in range(3)]
        rocks = [Rock() for _ in range(3)]
    elif difficulty == 2:  # Сложно
        poisons = [Poison() for _ in range(6)]
        rocks = [Rock() for _ in range(6)]

    score = 0
    font = pygame.font.SysFont('Arial', 24)

    # Загрузка фона для игры
    try:
        background_image = pygame.image.load('background.png')
        background_image = pygame.transform.scale(background_image,
                                                  (SCREEN_WIDTH,
                                                   SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Не удалось загрузить фоновое изображение: {e}")
        raise SystemExit

    running = True
    while running:
        handle_keys(snake)  # Вызов функции обработки клавиш
        running = handle_game_events(snake)
        if not running:
            break

        running, score = update_game_state(snake, apple, poisons, rocks, score)
        if not running:
            display_game_over(screen)
            break

        screen.blit(background_image, (0, 0))  # Отображаем фон
        draw_game_objects(screen, snake, apple, poisons, rocks)

        # Отрисовка текста с количеством очков и жизней
        score_text = font.render(f'Счет: {score}', True, (255, 255, 255))
        lives_text = font.render(f'Жизни: {snake.lives}', True,
                                 (255, 255, 255))

        score_text_x = (screen.get_width() // 2 - score_text.get_width() // 2)
        score_text_y = 10
        screen.blit(score_text, (score_text_x, score_text_y))

        lives_text_x = screen.get_width() - 100
        lives_text_y = 10
        screen.blit(lives_text, (lives_text_x, lives_text_y))

        pygame.display.flip()
        clock.tick(10)


def main():
    """Основная функция."""
    while True:
        clock.tick(10)
        menu_choice = display_menu(screen)
        if menu_choice == "new_game":
            difficulty = display_difficulty_menu(screen)
            if difficulty is not None:
                display_game(screen, difficulty)
        elif menu_choice is None:
            break
    clock.tick(10)
    pygame.quit()


if __name__ == "__main__":
    main()
