import pygame
import sys
import random
import pygame_menu

pygame.init()
bg_image = pygame.image.load("logo.jpg")
SIZE_BLOCK = 20
# bg color
############################
bg_color = (200, 230, 200)
WHITE = (255, 255, 255)
BLUE = (180, 255, 255)
# food color
RED = (250, 50, 50)
############################
# snake color
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 104, 0)
############################
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")
# скорость змейки
timer = pygame.time.Clock()
# pygame ссылка на шрифт
courier = pygame.font.SysFont("courier", 36)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # пределы стенки
    def inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    # сравнение apple and head
    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK, SIZE_BLOCK])


def start_the_game():
    def get_random_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        food_block = SnakeBlock(x, y)
        # баг появление блока в змейке
        while food_block in snake_blocks:
            food_block.x = random.randint(0, COUNT_BLOCKS - 1)
            food_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return food_block

    snake_blocks = [SnakeBlock(10, 8), SnakeBlock(10, 9), SnakeBlock(10, 10)]
    apple = get_random_block()

    # dx , dy
    d_row = buf_row = 0
    d_col = buf_col = 1
    # счет
    total = 0
    # скорость
    speed = 1

    while True:

        # цикл обработки событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(bg_color)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f"Total: {total}", 0, WHITE)
        text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 230, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.inside():
            print("crash game")
            break


        draw_block(RED, apple.x, apple.y)

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()

        if apple == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_random_block()

        d_row = buf_row
        d_col = buf_col

        # голова
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print("crash game")
            break
            # pygame.quit()
            # sys.exit()

        snake_blocks.append(new_head)
        # хвост()
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


main_theme = pygame_menu.themes.THEME_DARK.copy()  # цвет menu
main_theme.set_background_color_opacity(0.7)  # прозрачность

menu = pygame_menu.Menu(300, 400, 'Snake Game',
                        theme=main_theme)

menu.add_text_input('Name :', default='Player 1')
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

while True:

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
