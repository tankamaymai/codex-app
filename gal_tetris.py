# Gal-style Tetris using pygame
# Run this script with: python3 gal_tetris.py
import pygame
import random

# Game configuration
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS

# Gal-style colors
BACKGROUND_COLOR = (255, 182, 193)  # light pink
GRID_COLOR = (255, 105, 180)        # hot pink
COLORS = [
    (255, 20, 147),  # deep pink
    (255, 192, 203), # pink
    (255, 105, 180), # hot pink
    (238, 130, 238), # violet
    (221, 160, 221), # plum
    (255, 182, 193), # light pink
    (255, 99, 71),   # tomato
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],               # I
    [[1, 1, 0], [0, 1, 1]],       # Z
    [[0, 1, 1], [1, 1, 0]],       # S
    [[1, 1, 1], [0, 1, 0]],       # T
    [[1, 1, 1], [1, 0, 0]],       # L
    [[1, 1, 1], [0, 0, 1]],       # J
    [[1, 1], [1, 1]],             # O
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.board = [[(0, None) for _ in range(COLS)] for _ in range(ROWS)]
        self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        self.piece = Piece(COLS // 2 - 1, 0, random.choice(SHAPES))

    def valid(self, offset_x=0, offset_y=0, shape=None):
        if shape is None:
            shape = self.piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if not cell:
                    continue
                new_x = self.piece.x + x + offset_x
                new_y = self.piece.y + y + offset_y
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return False
                if new_y >= 0 and self.board[new_y][new_x][0]:
                    return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell and self.piece.y + y >= 0:
                    self.board[self.piece.y + y][self.piece.x + x] = (1, self.piece.color)
        self.clear_lines()
        self.new_piece()
        if not self.valid():
            self.game_over = True

    def clear_lines(self):
        new_board = []
        cleared = 0
        for row in self.board:
            if all(cell[0] for cell in row):
                cleared += 1
            else:
                new_board.append(row)
        for _ in range(cleared):
            new_board.insert(0, [(0, None) for _ in range(COLS)])
        self.board = new_board
        self.score += cleared

    def move(self, dx):
        if self.valid(offset_x=dx):
            self.piece.x += dx

    def drop(self):
        if self.valid(offset_y=1):
            self.piece.y += 1
        else:
            self.lock_piece()

    def rotate(self):
        new_shape = [list(row) for row in zip(*self.piece.shape[::-1])]
        if self.valid(shape=new_shape):
            self.piece.shape = new_shape

    def hard_drop(self):
        while self.valid(offset_y=1):
            self.piece.y += 1
        self.lock_piece()


def draw_board(screen, game):
    screen.fill(BACKGROUND_COLOR)
    for y in range(ROWS):
        for x in range(COLS):
            cell, color = game.board[y][x]
            if cell:
                pygame.draw.rect(screen, color,
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_COLOR,
                             (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    for y, row in enumerate(game.piece.shape):
        for x, cell in enumerate(row):
            if cell:
                px = (game.piece.x + x) * CELL_SIZE
                py = (game.piece.y + y) * CELL_SIZE
                pygame.draw.rect(screen, game.piece.color,
                                 (px, py, CELL_SIZE, CELL_SIZE))
    pygame.display.set_caption(f"Gal Tetris - Score: {game.score}")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0
    fall_speed = 500  # milliseconds

    running = True
    while running:
        delta = clock.tick()
        fall_time += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_DOWN:
                    game.drop()
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()

        if fall_time >= fall_speed:
            fall_time = 0
            game.drop()

        draw_board(screen, game)
        pygame.display.flip()

        if game.game_over:
            print("Game Over! Score:", game.score)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
