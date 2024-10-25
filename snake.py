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
pygame.display.set_caption("Automated Snake Game with Options")

clock = pygame.time.Clock()

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def main():
    # Ask user for game mode
    game_mode, wall_setting = get_user_options()

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

            # Compute the next move based on the selected game mode
            if game_mode == "Dijkstra":
                path = find_path_dijkstra(snake, food, wall_setting)
            else:
                path = find_path_survival(snake, food, wall_setting)

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

            # Check for collision with wall when walls are solid
            if not wall_setting and (
                next_move[0] < 0
                or next_move[0] >= GRID_HEIGHT
                or next_move[1] < 0
                or next_move[1] >= GRID_WIDTH
            ):
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


def get_user_options():
    # Display options to the user
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 35)
    mode_text = font.render("Select Game Mode:", True, WHITE)
    mode_option1 = font.render("1. Dijkstra's Algorithm", True, WHITE)
    mode_option2 = font.render("2. Survival Mode", True, WHITE)

    wall_text = font.render("Wall Setting:", True, WHITE)
    wall_option1 = font.render("1. Go Through Walls", True, WHITE)
    wall_option2 = font.render("2. Solid Walls", True, WHITE)

    screen.blit(mode_text, (50, 50))
    screen.blit(mode_option1, (70, 90))
    screen.blit(mode_option2, (70, 130))

    screen.blit(wall_text, (50, 190))
    screen.blit(wall_option1, (70, 230))
    screen.blit(wall_option2, (70, 270))

    prompt_text = font.render(
        "Press M for Mode, W for Wall, Enter to Start", True, WHITE
    )
    screen.blit(prompt_text, (50, 330))

    pygame.display.flip()

    game_mode = "Dijkstra"
    wall_setting = True  # True for Go Through Walls, False for Solid Walls

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    # Toggle game mode
                    if game_mode == "Dijkstra":
                        game_mode = "Survival"
                    else:
                        game_mode = "Dijkstra"
                elif event.key == pygame.K_w:
                    # Toggle wall setting
                    wall_setting = not wall_setting
                elif event.key == pygame.K_RETURN:
                    selecting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update display with current selections
        if game_mode == "Dijkstra":
            mode_option1 = font.render(
                "1. Dijkstra's Algorithm [Selected]", True, GREEN
            )
            mode_option2 = font.render("2. Survival Mode", True, WHITE)
        else:
            mode_option1 = font.render("1. Dijkstra's Algorithm", True, WHITE)
            mode_option2 = font.render("2. Survival Mode [Selected]", True, GREEN)

        if wall_setting:
            wall_option1 = font.render("1. Go Through Walls [Selected]", True, GREEN)
            wall_option2 = font.render("2. Solid Walls", True, WHITE)
        else:
            wall_option1 = font.render("1. Go Through Walls", True, WHITE)
            wall_option2 = font.render("2. Solid Walls [Selected]", True, GREEN)

        screen.fill(BLACK)
        screen.blit(mode_text, (50, 50))
        screen.blit(mode_option1, (70, 90))
        screen.blit(mode_option2, (70, 130))

        screen.blit(wall_text, (50, 190))
        screen.blit(wall_option1, (70, 230))
        screen.blit(wall_option2, (70, 270))

        screen.blit(prompt_text, (50, 330))

        pygame.display.flip()

    return game_mode, wall_setting


def find_path_dijkstra(snake, food, wall_setting):
    # Generate the shortest path to the food using Dijkstra's algorithm
    path = dijkstra(snake[0], food, set(snake), wall_setting)
    return path


def find_path_survival(snake, food, wall_setting):
    # In Survival Mode, the snake takes paths closer to its body and tail
    path = a_star(snake, food, wall_setting)
    return path


def a_star(snake, food, wall_setting):
    # A* algorithm with heuristic that prefers positions closer to the snake's tail
    snake_set = set(snake)
    start = snake[0]
    tail = snake[-1]

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        current_f_score, current = heapq.heappop(open_set)

        if current == food:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor in get_neighbors(current, snake_set, wall_setting):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                # Heuristic: prefer positions closer to the tail
                h_score = manhattan_distance(neighbor, tail)
                f_score = tentative_g_score + h_score
                heapq.heappush(open_set, (f_score, neighbor))
                came_from[neighbor] = current

        # Temporarily add current to snake_set to prevent revisiting
        snake_set.add(current)

    return None  # No path found


def dijkstra(start, goal, snake_set, wall_setting):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while queue:
        current_cost, current = heapq.heappop(queue)

        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor in get_neighbors(current, snake_set, wall_setting):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(queue, (priority, neighbor))
                came_from[neighbor] = current

    return None  # No path found


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos, snake_set, wall_setting):
    neighbors = []
    y, x = pos
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx

        if wall_setting:
            # Allow wrapping around edges
            ny %= GRID_HEIGHT
            nx %= GRID_WIDTH
        else:
            # Solid walls; check boundaries
            if ny < 0 or ny >= GRID_HEIGHT or nx < 0 or nx >= GRID_WIDTH:
                continue  # Skip positions outside the grid

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
