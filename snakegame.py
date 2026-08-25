import pygame
import random

pygame.init()

# Create the game window
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Game speed
clock = pygame.time.Clock()
simple_speed = 8
hard_speed = 15

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Snake settings
snake_size = 20

# Fonts
font = pygame.font.SysFont("Arial", 30)


def create_food(snake_body):
    """Return a grid position that is not already used by the snake."""
    while True:
        food_x = random.randrange(0, WIDTH, snake_size)
        food_y = random.randrange(0, HEIGHT, snake_size)

        if [food_x, food_y] not in snake_body:
            return food_x, food_y


def reset_game():
    """Set all game values back to their starting state."""
    snake_x = 300
    snake_y = 200
    x_change = 0
    y_change = 0
    snake_body = []
    snake_length = 1
    score = 0
    food_x, food_y = create_food(snake_body)

    return (snake_x, snake_y, x_change, y_change, snake_body,
            snake_length, score, food_x, food_y)


def show_score(score):
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, [10, 10])


def show_game_over(score):
    game_over_text = font.render("GAME OVER", True, red)
    screen.blit(game_over_text, [220, 130])

    final_score_text = font.render("Final Score: " + str(score), True, white)
    screen.blit(final_score_text, [200, 175])

    restart_text = font.render("Press C to Play Again or Q to Quit", True, white)
    screen.blit(restart_text, [80, 220])


def show_difficulty_screen():
    """Display the screen where the player chooses the snake speed."""
    title_text = font.render("SNAKE GAME", True, white)
    choose_text = font.render("Choose Difficulty", True, white)
    simple_text = font.render("Press 1 - SIMPLE", True, white)
    hard_text = font.render("Press 2 - HARD", True, white)

    screen.blit(title_text, [220, 80])
    screen.blit(choose_text, [190, 130])
    screen.blit(simple_text, [195, 190])
    screen.blit(hard_text, [200, 235])


# The game waits here until the player chooses a difficulty.
game_state = "difficulty"
game_running = True
snake_speed = simple_speed

while game_running:
    if game_state == "difficulty":
        screen.fill(black)
        show_difficulty_screen()
        pygame.display.update()
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    snake_speed = simple_speed
                    game_state = "playing"
                elif event.key == pygame.K_2:
                    snake_speed = hard_speed
                    game_state = "playing"

                if game_state == "playing":
                    (snake_x, snake_y, x_change, y_change, snake_body,
                     snake_length, score, food_x, food_y) = reset_game()

    elif game_state == "game_over":
        screen.fill(black)
        show_game_over(score)
        pygame.display.update()
        clock.tick(snake_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_running = False

                elif event.key == pygame.K_c:
                    # Choose a new difficulty before resetting the game.
                    game_state = "difficulty"

    elif game_state == "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            elif event.type == pygame.KEYDOWN:
                # Do not allow an immediate turn back into the snake's body.
                if event.key == pygame.K_LEFT and x_change != snake_size:
                    x_change = -snake_size
                    y_change = 0

                elif event.key == pygame.K_RIGHT and x_change != -snake_size:
                    x_change = snake_size
                    y_change = 0

                elif event.key == pygame.K_UP and y_change != snake_size:
                    y_change = -snake_size
                    x_change = 0

                elif event.key == pygame.K_DOWN and y_change != -snake_size:
                    y_change = snake_size
                    x_change = 0

        # Keep moving in the currently chosen direction.
        snake_x = snake_x + x_change
        snake_y = snake_y + y_change

        # Check whether the snake has hit a wall.
        if snake_x < 0 or snake_x >= WIDTH or snake_y < 0 or snake_y >= HEIGHT:
            game_state = "game_over"

        screen.fill(black)
        pygame.draw.rect(screen, red, [food_x, food_y, snake_size, snake_size])

        # Add the head, then remove the oldest segment unless food was eaten.
        snake_head = [snake_x, snake_y]
        snake_body.append(snake_head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check whether the head ran into any other snake segment.
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_state = "game_over"

        for block in snake_body:
            pygame.draw.rect(screen, green, [block[0], block[1], snake_size, snake_size])

        # Food adds one segment and one point to the score.
        if snake_x == food_x and snake_y == food_y:
            snake_length = snake_length + 1
            score = score + 1
            food_x, food_y = create_food(snake_body)

        show_score(score)
        pygame.display.update()
        clock.tick(snake_speed)

pygame.quit()
