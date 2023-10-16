import pygame
from pygame.locals import *
import random
from pygame import mixer

# Pygame setup
pygame.init()
dis_width = 1100
dis_height = 800
screen = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("2D Football by ShervinMoh")
clock = pygame.time.Clock()
running = True

# Load and set the volume for sound effects
game_sound = pygame.mixer.Sound("musics\game.mp3")
game_sound.set_volume(0.2)

# Create Circle and Movement
class Circle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = 30
        self.speed = 5
        self.color = color

    def move(self, dx, dy):
        # Check if the new position will overlap with the red rectangle
        if not self.is_blocking(self.x + dx * self.speed, self.y + dy * self.speed):
            self.x += dx * self.speed
            self.y += dy * self.speed

    # Set area limit for gate
    def is_blocking(self, x, y):
        # Red gate position for set blocking method
        red_rect_pos = (972, 270)
        red_rect_width = 57
        red_rect_height = 266

        if x > red_rect_pos[0] and x < red_rect_pos[0] + red_rect_width and y > red_rect_pos[1] and y < red_rect_pos[1] + red_rect_height:
            return True
        else:
            # Blue gate position for set blocking method
            blue_rect_pos = (70, 270)
            blue_rect_width = 57
            blue_rect_height = 266

            if x > blue_rect_pos[0] and x < blue_rect_pos[0] + blue_rect_width and y > blue_rect_pos[1] and y < blue_rect_pos[1] + blue_rect_height:
                return True
            else:
                return False

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Create Ball
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 18
        self.speed = 5
        self.color = (255, 255, 0)
        self.target = random.choice([circle1, circle2])
        self.in_gate = False
        self.score1 = 0
        self.score2 = 0
        self.just_scored = False
        self.time_elapsed = None  # New attribute to keep track of time elapsed since entering a gate

    def move(self):
        if self.target is not None:
            dx = (self.target.x - self.x) / ((self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2) ** 0.5
            dy = (self.target.y - self.y) / ((self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2) ** 0.5
            self.x += dx * self.speed
            self.y += dy * self.speed
        else:
            # Check if the circle is hitting the border of the screen
            if self.x - self.radius <= 50:
                self.move_dx = abs(self.move_dx)
            elif self.x + self.radius >= 1050:
                self.move_dx = -abs(self.move_dx)
            if self.y - self.radius <= 24:
                self.move_dy = abs(self.move_dy)
            elif self.y + self.radius >= 770:
                self.move_dy = -abs(self.move_dy)

            # Check if the circle is hitting the poles
            if (70 < self.x < 127 and 298 - self.radius < self.y < 308) or \
               (70 < self.x < 127 and 500 - self.radius < self.y < 510 + self.radius) or \
               (972 < self.x < 1027 and 298 - self.radius < self.y < 308) or \
               (972 < self.x < 1027 and 500 - self.radius < self.y < 510 + self.radius):
                self.move_dy = -self.move_dy

            # Check if the white circle is inside one of the gates
            if (70 <= self.x <= 127 and 308 < self.y < 500) or \
               (972 <= self.x <= 1027 and 308 < self.y < 500):
                self.in_gate = True
                if self.time_elapsed is None:
                    self.time_elapsed = pygame.time.get_ticks()  # Set the time elapsed since entering the gate
            else:
                self.in_gate = False
                self.time_elapsed = None  # Reset the time elapsed if the ball is not inside a gate

            # Gradually decrease the speed of the white circle if it's inside a gate
            if self.in_gate:
                self.speed -= 1
                
            # If 5 seconds have elapsed since entering the gate, reset the ball's position to the center of the field
            if self.time_elapsed is not None and pygame.time.get_ticks() - self.time_elapsed >= 5000:
                self.x = dis_width / 2
                self.y = dis_height / 2
                self.speed = 5
                self.target = random.choice([circle1, circle2])
                self.in_gate = False
                self.time_elapsed = None
                self.just_scored = False
                circle1.x = 946
                circle1.y = 399
                circle2.x = 160
                circle2.y = 399

            self.x += self.move_dx * self.speed
            self.y += self.move_dy * self.speed
            self.speed *= 1
            if self.speed < 1:
                self.speed = 1

            if (70 <= self.x <= 127 and 308 < self.y < 500):
                if not self.just_scored: # Only update score when not just scored
                    self.score2 += 1  # Increase player 2 score
                    self.just_scored = True
            elif (972 <= self.x <= 1027 and 308 < self.y < 500):
                if not self.just_scored: # Only update score when not just scored
                    self.score1 += 1  # Increase player 1 score
                    self.just_scored = True        

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, other):
        if ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5 <= self.radius + other.radius:
            collision_dx = (self.x - other.x) / ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
            collision_dy = (self.y - other.y) / ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
            self.speed = 10
            self.target = None
            self.move_dx = collision_dx
            self.move_dy = collision_dy

class Score:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.purple_color = (204, 153, 255)
        self.blue_color = (0, 128, 255)
        self.white_color = (255, 255, 255)
        self.score_font = pygame.font.SysFont("impact", 25)  # Font for displaying scores

    def draw(self):
        value1 = self.score_font.render("Player Score: " + str(self.score1), True, self.purple_color)
        value2 = self.score_font.render("Player Score: " + str(self.score2), True, self.blue_color)
        rotated_value1 = pygame.transform.rotate(value1, 90)
        rotated_value2 = pygame.transform.rotate(value2, 270)

        pygame.draw.rect(screen, self.white_color, pygame.Rect(9, 581, 33, 190))
        pygame.draw.rect(screen, self.white_color, pygame.Rect(1058, 28, 33, 190))

        screen.blit(rotated_value1, [9, 600])
        screen.blit(rotated_value2, [1060, 45])
    
    def update_scores(self, score1, score2):
        self.score1 = score1
        self.score2 = score2

class Field:
    def field(screen):
         
        dark_blue_color = (32, 42, 68)
        orange_color = (255, 128, 0)
        yellow_color = (255, 255, 0)

        # Background
        screen.fill(dark_blue_color)
            
        # Around the football field
        pygame.draw.rect(screen, orange_color, pygame.Rect(47, 22, 1007, 2)) #Up
        pygame.draw.rect(screen, orange_color, pygame.Rect(47, 777, 1007, 2)) #Down
        pygame.draw.rect(screen, orange_color, pygame.Rect(47, 22, 2, 755)) #Left
        pygame.draw.rect(screen, orange_color, pygame.Rect(1052, 24, 2, 755)) #Right
            
        # The area on the left side of the field
        pygame.draw.rect(screen, orange_color, pygame.Rect(47, 177, 160, 2)) #Up
        pygame.draw.rect(screen, orange_color, pygame.Rect(47, 623, 160, 2)) #Down
        pygame.draw.rect(screen, orange_color, pygame.Rect(205, 179, 2, 446)) #Left

        # The area on the right side of the field
        pygame.draw.rect(screen, orange_color, pygame.Rect(894, 177, 160, 2)) #Up
        pygame.draw.rect(screen, orange_color, pygame.Rect(894, 623, 160, 2)) #Down
        pygame.draw.rect(screen, orange_color, pygame.Rect(894, 179, 2, 446)) #Left 

        # Draw the oval on the screen
        ellipse1 = pygame.Rect(466, 300, 170, 200)
        ellipse2 = pygame.Rect(480, 314, 140, 170)
        pygame.draw.ellipse(screen, orange_color, ellipse1)
        pygame.draw.ellipse(screen, dark_blue_color, ellipse2)
        pygame.draw.circle(screen, orange_color, (551, 397), 5)

        # The middle line of the football field
        pygame.draw.rect(screen, orange_color, pygame.Rect(550, 22, 2, 755))

        # Left side gate
        pygame.draw.rect(screen, orange_color, pygame.Rect(100, 298, 2, 202)) #Goal line
        pygame.draw.rect(screen, yellow_color, pygame.Rect(46, 500, 57, 10)) #Down
        pygame.draw.rect(screen, yellow_color, pygame.Rect(46, 298, 57, 10)) #Up
        pygame.draw.rect(screen, yellow_color, pygame.Rect(46, 298, 10, 210)) #Left

        # right side gate 
        pygame.draw.rect(screen, orange_color, pygame.Rect(999, 298, 2, 202)) #Goal line
        pygame.draw.rect(screen, yellow_color, pygame.Rect(998, 500, 57, 10)) #Up
        pygame.draw.rect(screen, yellow_color, pygame.Rect(998, 298, 57, 10)) #Down
        pygame.draw.rect(screen, yellow_color, pygame.Rect(1045, 298, 10, 210)) #Right

class Keys:
    def __init__(self):
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        # Circle radius
        circle_radius = 30
        # Set Movement keys and some area limits
        if not ball.in_gate:  # Only allow movement if the ball is not inside a gate
            if keys[K_UP] and circle1.y > 24 + circle_radius:
                circle1.move(0, -1)
            if keys[K_DOWN] and circle1.y < 715 + circle_radius:
                circle1.move(0, 1)
            if keys[K_LEFT] and not circle1.x < 553 + circle_radius:
                circle1.move(-1, 0)
            if keys[K_RIGHT] and not circle1.x > 1050 - circle_radius:
                circle1.move(1, 0)
            if keys[K_w] and circle2.y > 24 + circle_radius:
                circle2.move(0, -1)
            if keys[K_s] and circle2.y < 715 + circle_radius:
                circle2.move(0, 1)
            if keys[K_a] and not circle2.x < 50 + circle_radius:
                circle2.move(-1, 0)
            if keys[K_d] and not circle2.x > 547 - circle_radius:
                circle2.move(1, 0)

if __name__ == '__main__':
    
    game_sound.play()
    
    # Circles
    circle1 = Circle(946, 399, (0, 128, 255))  # Blue Circle
    circle2 = Circle(160, 399, (204, 153, 255))  # Purple Circle

    # White Circle
    ball = Ball(dis_width / 2, dis_height / 2)

    score = Score()

    while running:

        # Game field
        Field.field(screen)

        # Defiend keys
        Keys()

        # Draw the red and blue circles
        circle1.draw()
        circle2.draw()
        
        # Move and draw the white circle
        ball.move()
        ball.draw()

        # Check for collisions between the white circle and the red and blue circles
        ball.collide(circle1)
        ball.collide(circle2)

        # Update score
        score.draw()
        score.update_scores(ball.score1, ball.score2)

        # Update the display
        pygame.display.update()

        # Set the game's frame rate
        clock.tick(70)

    # Quit Pygame
    pygame.quit()