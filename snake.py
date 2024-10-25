import pygame
import sys
import random
import heapq

# Initialize Pygame
pygame.init()

# Screen dimensions
CELL_SIZE = 20
GRID_WIDTH = 30  # Number of cells horizontally
GRID_HEIGHT = 20  # Number of cells vertically
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Automated Snake Game with Dijkstra's Algorithm")

clock = pygame.time.Clock()

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def main():
    while True:
        # Initial snake position (center of the screen)
        snake = [(GRID_HEIGHT // 2, GRID_WIDTH // 2)]
        snake_set = set(snake)
        score = 0  # Initialize score

        # Place initial food
        food = place_food(snake_set)

        # Wait for user to start the game
        font = pygame.font.SysFont(None, 55)
        start_text = font.render("Press any key to start", True, WHITE)
        screen.fill(BLACK)
        screen.blit(
            start_text,
            (
                SCREEN_WIDTH // 2 - start_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - start_text.get_height() // 2,
            ),
        )
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        running = True
        while running:
            screen.fill(BLACK)

            # Display score
            score_font = pygame.font.SysFont(None, 35)
            score_text = score_font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (5, 5))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Compute the next move using Dijkstra's algorithm
            path = dijkstra(snake[0], food, snake_set)
            if not path or len(path) < 2:
                # No path to food (snake is trapped) or already at food
                running = False
                continue

            next_move = path[1]  # The first element is the current head

            # Move the snake
            snake.insert(0, next_move)
            snake_set.add(next_move)

            if next_move == food:
                # Snake eats the food; place new food
                score += 1
                food = place_food(snake_set)
            else:
                # Remove the tail segment
                tail = snake.pop()
                snake_set.remove(tail)

            # Check for collision with self
            if snake.count(next_move) > 1:
                running = False
                continue

            # Draw food
            draw_cell(food, RED)

            # Draw snake
            for segment in snake:
                draw_cell(segment, GREEN)

            pygame.display.flip()
            clock.tick(10)  # Control the speed of the game (10 frames per second)

        # Game over, ask user to restart or quit
        screen.fill(BLACK)
        game_over_font = pygame.font.SysFont(None, 55)
        game_over_text1 = game_over_font.render("Game Over", True, RED)
        game_over_text2 = game_over_font.render(
            "Press R to Restart or Q to Quit", True, WHITE
        )
        screen.blit(
            game_over_text1,
            (
                SCREEN_WIDTH // 2 - game_over_text1.get_width() // 2,
                SCREEN_HEIGHT // 2 - game_over_text1.get_height(),
            ),
        )
        screen.blit(
            game_over_text2,
            (
                SCREEN_WIDTH // 2 - game_over_text2.get_width() // 2,
                SCREEN_HEIGHT // 2 + game_over_text2.get_height(),
            ),
        )
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False  # Restart the game
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


def dijkstra(start, goal, snake_set):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while queue:
        current_cost, current = heapq.heappop(queue)

        if current == goal:
            # Reconstruct path
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in get_neighbors(current, snake_set):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(queue, (priority, neighbor))
                came_from[neighbor] = current

    return None  # No path found


def get_neighbors(pos, snake_set):
    neighbors = []
    y, x = pos
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx

        # Allow wrapping around edges
        ny %= GRID_HEIGHT
        nx %= GRID_WIDTH

        if (ny, nx) not in snake_set:
            neighbors.append((ny, nx))
    return neighbors


def place_food(snake_set):
    while True:
        y = random.randint(0, GRID_HEIGHT - 1)
        x = random.randint(0, GRID_WIDTH - 1)
        if (y, x) not in snake_set:
            return (y, x)


def draw_cell(pos, color):
    y, x = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


if __name__ == "__main__":
    main()
