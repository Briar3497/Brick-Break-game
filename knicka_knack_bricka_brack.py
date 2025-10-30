
import pygame
import random

pygame.init()
timer = pygame.time.Clock()
fps = 60
white = (255, 255, 255)
black = (0, 0, 0)
grey = (180, 180, 180)
dark_grey = (60, 60, 60)
red = (200, 0, 0)
orange = (255, 150, 30)
green = (50, 255, 50)
blue = (80, 80, 255)
purple = (120, 80, 200)
colors = [red, orange, green, blue, purple]

WIDTH = 500
HEIGHT = 850

player_x = 190
player_speed = 8
player_direction = 0

ball_x_direction = 0
ball_y_direction = 0
ball_x_speed = 5
ball_y_speed = 5

ball_x = WIDTH / 2
ball_y = HEIGHT - 30

board = []
create_new = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
active = False
score = 0
font = pygame.font.SysFont("Arial", 30)
large_font = pygame.font.SysFont("Arial", 40)


def create_new_board():
    new_board = []
    rows = random.randint(4, 9)
    for index in range(rows):
        row = []
        for j in range(5):
            row.append(random.randint(1, 5))
        new_board.append(row)
    return new_board


def draw_board(board_bricks):
    board_squares = []
    for i in range(len(board_bricks)):
        for j in range(len(board_bricks[i])):
            if board_bricks[i][j] > 0:
                rect = pygame.Rect(j * 100, i * 40, 98, 38)
                pygame.draw.rect(screen, colors[(board_bricks[i][j]) - 1], rect, 0, 5)
                pygame.draw.rect(screen, black, rect, 1, 5)
                board_squares.append((rect, (i, j)))
    return board_squares


run = True
while run:
    screen.fill(grey)
    timer.tick(fps)

    if create_new:
        board = create_new_board()
        create_new = False

    board_rects_and_pos = draw_board(board)

    player = pygame.draw.rect(screen, dark_grey, [player_x, HEIGHT - 20, 120, 15], 0, 3)
    pygame.draw.rect(screen, white, [player_x + 5, HEIGHT - 18, 110, 11], 0, 3)
    ball = pygame.draw.circle(screen, white, (ball_x, ball_y), 10)
    pygame.draw.circle(screen, black, (ball_x, ball_y), 10, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not active:
                active = True
                ball_y_direction = -1
                ball_x_direction = random.choice([-1, 1])
                score = 0
                create_new = True
            if event.key == pygame.K_RIGHT and active:
                player_direction = 1
            if event.key == pygame.K_LEFT and active:
                player_direction = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and player_direction == 1:
                player_direction = 0
            if event.key == pygame.K_LEFT and player_direction == -1:
                player_direction = 0

    # Game logic
    if active:
        player_x += player_direction * player_speed
        if player_x < 0:
            player_x = 0
        if player_x > WIDTH - 120:
            player_x = WIDTH - 120

        # Ball movement
        ball_y += ball_y_direction * ball_y_speed
        ball_x += ball_x_direction * ball_x_speed

        # Ball wall collision
        if ball_x <= 10 or ball_x >= WIDTH - 10:
            ball_x_direction *= -1
        if ball_y <= 10:
            ball_y_direction *= -1

        # Ball-brick collision
        for brick_rect, (row_index, col_index) in board_rects_and_pos[:]:
            if ball.colliderect(brick_rect):
                # Check for top/bottom collision
                if brick_rect.collidepoint(ball_x, ball_y - ball_y_speed) or brick_rect.collidepoint(ball_x,
                                                                                                     ball_y + ball_y_speed):
                    ball_y_direction *= -1
                # Check for side collision
                elif brick_rect.collidepoint(ball_x - ball_x_speed, ball_y) or brick_rect.collidepoint(
                        ball_x + ball_x_speed, ball_y):
                    ball_x_direction *= -1

                # Deduct brick health and update score
                board[row_index][col_index] -= 1
                score += 1

                # Prevent ball from getting stuck
                if ball.colliderect(brick_rect):
                    ball_y += ball_y_direction * ball_y_speed

        # Ball-paddle collision
        if ball.colliderect(player) and ball_y_direction == 1:
            ball_y_direction *= -1
            # Increase ball speed slightly when it hits a moving paddle
            if player_direction != 0 and ball_x_speed < 15:
                ball_x_speed += 1

    # Game restart conditions
    is_board_empty = all(brick_val < 1 for row in board for brick_val in row) if board else False
    if ball_y >= HEIGHT - 10 or is_board_empty:
        active = False
        player_x = 190
        player_direction = 0
        ball_x_direction = 0
        ball_y_direction = 0
        ball_x_speed = 5
        ball_y_speed = 5
        ball_x = WIDTH / 2
        ball_y = HEIGHT - 30
        if is_board_empty:
            create_new = True

    # Display UI
    if not active:
        if is_board_empty and len(board) > 0:
            win_text = large_font.render('You win!', True, black)
            screen.blit(win_text, (WIDTH / 2 - win_text.get_width() / 2, HEIGHT / 2 - 50))
            start_text = large_font.render('Spacebar for new game', True, black)
            screen.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2 + 10))
        else:
            start_text = large_font.render('Spacebar to start', True, black)
            screen.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2 - 50))


    score_text = font.render(f'Score: {score}', True, black)
    screen.blit(score_text, (10, 5))


    pygame.display.flip()

pygame.quit()