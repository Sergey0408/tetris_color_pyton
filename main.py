
import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
GAME_WIDTH = 250
INFO_WIDTH = 50
SQUARE_SIZE = 60
SECTORS = 4
SECTOR_WIDTH = GAME_WIDTH // SECTORS
CLICK_SENSITIVITY = 20  # Increased click area

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = WHITE
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
          (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0),
          (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
          (192, 192, 192), (128, 128, 128), (128, 0, 0)]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Color Squares")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.dragging = False
        self.elapsed_time = 0
        self.start_time = time.time()
        self.show_time = True
        self.drag_offset = 0
        self.color_count = 4
        self.speed_level = 1
        self.total_squares = 10
        self.remaining_squares = self.total_squares
        self.squares = []
        self.current_square = self.create_square()
        self.fall_speed = 30  # mm per second
        self.time_blinking = False
        self.last_blink = 0
        self.show_time = True
        self.delay_start = None
        self.is_delayed = True

    def create_square(self):
        sector = random.randint(0, SECTORS - 1)
        x = sector * SECTOR_WIDTH
        color = random.choice(COLORS[:self.color_count])
        self.remaining_squares -= 1
        self.is_delayed = True
        self.delay_start = None
        return {'x': x, 'y': 0, 'color': color, 'sector': sector}

    def update(self):
        if self.game_over:
            current_time = time.time()
            if current_time - self.last_blink >= 0.5:
                self.show_time = not self.show_time
                self.last_blink = current_time
            return

        if self.current_square:
            if self.is_delayed:
                if self.delay_start is None:
                    self.delay_start = time.time()
                elif time.time() - self.delay_start >= 2:
                    self.is_delayed = False
            else:
                move_distance = (self.fall_speed * (1.3 ** (self.speed_level - 1))) / 60
                self.current_square['y'] += move_distance

            # Check collision with bottom or other squares
            if self.current_square['y'] + SQUARE_SIZE >= WINDOW_HEIGHT:
                self.squares.append(self.current_square)
                self.current_square = self.create_square()
            else:
                for square in self.squares:
                    if (self.current_square['y'] + SQUARE_SIZE >= square['y'] and
                        self.current_square['x'] == square['x']):
                        if self.current_square['color'] == square['color']:
                            self.squares.remove(square)
                        else:
                            self.squares.append(self.current_square)
                        self.current_square = self.create_square()
                        break

        # Check game end conditions
        if not self.current_square and self.remaining_squares <= 0:
            self.game_over = True
        
        # Check vertical stack in each sector
        sector_counts = [0] * SECTORS
        for square in self.squares:
            sector = square['x'] // SECTOR_WIDTH
            sector_counts[sector] += 1
            if sector_counts[sector] >= 9:
                self.game_over = True
                break

        self.elapsed_time = int(time.time() - self.start_time)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, WHITE, (0, 0, GAME_WIDTH, WINDOW_HEIGHT), 1)
        
        
        
        # Draw squares
        for square in self.squares:
            pygame.draw.rect(self.screen, square['color'],
                           (square['x'], square['y'], SQUARE_SIZE, SQUARE_SIZE))

        if self.current_square:
            pygame.draw.rect(self.screen, self.current_square['color'],
                           (self.current_square['x'], self.current_square['y'],
                            SQUARE_SIZE, SQUARE_SIZE))

        # Draw info panel
        info_x = GAME_WIDTH
        LIGHT_BLUE = (173, 216, 230)
        pygame.draw.rect(self.screen, LIGHT_BLUE, (info_x, 0, INFO_WIDTH, WINDOW_HEIGHT))
        BLUE = (0, 0, 255)

        # Draw buttons and info
        font = pygame.font.Font(None, 20)
        
        button_width = 40
        
        # Start button
        pygame.draw.rect(self.screen, BLUE, (info_x + 5, 10, button_width, 30), 1)
        start_text = font.render("Start", True, BLUE)
        text_x = info_x + 5 + (button_width - start_text.get_width()) // 2
        self.screen.blit(start_text, (text_x, 20))

        # Time display
        if not self.game_over or self.show_time:
            time_text = font.render(str(self.elapsed_time), True, BLUE)
            text_x = info_x + 5 + (button_width - time_text.get_width()) // 2
            self.screen.blit(time_text, (text_x, 60))

        # Color count button
        pygame.draw.rect(self.screen, BLUE, (info_x + 5, 100, button_width, 30), 1)
        color_text = font.render(str(self.color_count), True, BLUE)
        text_x = info_x + 5 + (button_width - color_text.get_width()) // 2
        self.screen.blit(color_text, (text_x, 110))

        # Speed button
        pygame.draw.rect(self.screen, BLUE, (info_x + 5, 150, button_width, 30), 1)
        speed_text = font.render(str(self.speed_level), True, BLUE)
        text_x = info_x + 5 + (button_width - speed_text.get_width()) // 2
        self.screen.blit(speed_text, (text_x, 160))

        # # Square count button
        # pygame.draw.rect(self.screen, BLUE, (info_x + 5, 200, button_width, 30), 1)
        # count_text = font.render(str(self.total_squares), True, BLUE)
        # text_x = info_x + 5 + (button_width - count_text.get_width()) // 2
        # self.screen.blit(count_text, (text_x, 210))

        # # Remaining squares
        # remain_text = font.render(str(self.remaining_squares), True, BLUE)
        # text_x = info_x + 5 + (button_width - remain_text.get_width()) // 2
        # self.screen.blit(remain_text, (text_x, 260))

        # Stop button at bottom
        pygame.draw.rect(self.screen, BLUE, (info_x + 5, WINDOW_HEIGHT - 40, button_width, 30), 1)
        stop_text = font.render("Stop", True, BLUE)
        text_x = info_x + 5 + (button_width - stop_text.get_width()) // 2
        self.screen.blit(stop_text, (text_x, WINDOW_HEIGHT - 30))

        pygame.display.flip()

    def handle_click(self, pos):
        info_x = GAME_WIDTH
        x, y = pos

        if info_x + 5 <= x <= info_x + 45:
            if 10 <= y <= 40:  # Start button
                self.reset_game()
            elif 100 <= y <= 130:  # Color count button
                color_counts = [4, 5, 7, 10, 15]
                current_index = color_counts.index(self.color_count)
                self.color_count = color_counts[(current_index + 1) % len(color_counts)]
                self.time_blinking = False
            elif 150 <= y <= 180:  # Speed button
                self.speed_level = self.speed_level % 10 + 1
                self.time_blinking = False
            elif 200 <= y <= 230:  # Square count button
                square_counts = [10, 20, 30, 40, 50]
                current_index = square_counts.index(self.total_squares)
                self.total_squares = square_counts[(current_index + 1) % len(square_counts)]
                self.remaining_squares = self.total_squares
                self.time_blinking = False
            elif WINDOW_HEIGHT - 40 <= y <= WINDOW_HEIGHT - 10:  # Stop button
                self.squares = []
                self.current_square = None
                self.game_over = False
                self.elapsed_time = 0
                self.remaining_squares = self.total_squares

def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < GAME_WIDTH and game.current_square:  # Only in game field
                    if x < game.current_square['x']:
                        sector = max(0, game.current_square['sector'] - 1)
                        game.current_square['sector'] = sector
                        game.current_square['x'] = sector * SECTOR_WIDTH
                    elif x > game.current_square['x'] + SQUARE_SIZE:
                        sector = min(SECTORS - 1, game.current_square['sector'] + 1)
                        game.current_square['sector'] = sector
                        game.current_square['x'] = sector * SECTOR_WIDTH
                    elif (x >= game.current_square['x'] and 
                          x < game.current_square['x'] + SQUARE_SIZE):
                        game.dragging = True
                        game.drag_offset = x - game.current_square['x']
                elif x >= GAME_WIDTH:  # Info panel clicks
                    game.handle_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if game.dragging:
                    game.dragging = False
                    # Snap to nearest sector
                    sector = round(game.current_square['x'] / SECTOR_WIDTH)
                    sector = max(0, min(sector, SECTORS - 1))
                    game.current_square['sector'] = sector
                    game.current_square['x'] = sector * SECTOR_WIDTH
            elif event.type == pygame.MOUSEMOTION:
                if game.dragging and game.current_square:
                    x = event.pos[0] - game.drag_offset
                    x = max(0, min(x, GAME_WIDTH - SQUARE_SIZE))
                    game.current_square['x'] = x

        game.update()
        game.draw()
        game.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
