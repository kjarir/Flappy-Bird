import pygame
import random
import sys
import os
import math
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_GAP = 200
PIPE_FREQUENCY = 1500  # milliseconds
CLOUD_SPEED = 1
GROUND_SPEED = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Load images
try:
    background_img = pygame.image.load('assets/background.png')
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bird_img = pygame.image.load('assets/bird.png')
    bird_img = pygame.transform.scale(bird_img, (40, 40))
    pipe_img = pygame.image.load('assets/pipe.png')
    pipe_img = pygame.transform.scale(pipe_img, (50, 400))
    ground_img = pygame.image.load('assets/ground.png')
    ground_img = pygame.transform.scale(ground_img, (SCREEN_WIDTH, 50))
    cloud_img = pygame.image.load('assets/cloud.png')
    cloud_img = pygame.transform.scale(cloud_img, (100, 50))
except:
    print("Image files not found. Using default graphics.")
    background_img = None
    bird_img = None
    pipe_img = None
    ground_img = None
    cloud_img = None

# Load sounds
try:
    flap_sound = mixer.Sound('assets/flap.wav')
    hit_sound = mixer.Sound('assets/hit.wav')
    point_sound = mixer.Sound('assets/point.wav')
    background_music = mixer.Sound('assets/background.wav')
    background_music.play(-1)  # -1 means loop indefinitely
except:
    print("Sound files not found. Game will run without sound.")

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 30
        self.color = (255, 255, 255, 255)
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.color = (255, 255, 255, int(self.life * 8.5))

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(50, 200)
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        self.x -= self.speed
        if self.x < -100:
            self.x = SCREEN_WIDTH
            self.y = random.randint(50, 200)

    def draw(self):
        if cloud_img:
            screen.blit(cloud_img, (int(self.x), int(self.y)))
        else:
            pygame.draw.ellipse(screen, WHITE, (self.x, self.y, 100, 50))

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 20
        self.color = YELLOW
        self.rotation = 0
        self.particles = []
        self.wing_angle = 0
        self.wing_direction = 1

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.rotation = 30
        self.wing_angle = 30
        self.wing_direction = 1
        
        # Create particles
        for _ in range(5):
            self.particles.append(Particle(self.x, self.y))
        
        try:
            flap_sound.play()
        except:
            pass

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rotation = max(-90, self.rotation - 5)
        
        # Update wing animation
        self.wing_angle += self.wing_direction * 5
        if self.wing_angle > 30:
            self.wing_direction = -1
        elif self.wing_angle < -30:
            self.wing_direction = 1

        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

        # Keep bird within screen bounds
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius
            self.velocity = 0

    def draw(self):
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)

        if bird_img:
            # Rotate the bird image
            rotated_bird = pygame.transform.rotate(bird_img, self.rotation)
            bird_rect = rotated_bird.get_rect(center=(self.x, int(self.y)))
            screen.blit(rotated_bird, bird_rect)
        else:
            # Draw body
            pygame.draw.circle(screen, self.color, (self.x, int(self.y)), self.radius)
            
            # Draw eye
            pygame.draw.circle(screen, BLACK, (self.x + 8, int(self.y) - 5), 5)
            
            # Draw beak
            pygame.draw.polygon(screen, (255, 165, 0), 
                              [(self.x + self.radius, int(self.y)), 
                               (self.x + self.radius + 15, int(self.y)), 
                               (self.x + self.radius, int(self.y) - 5)])
            
            # Draw wings
            wing_length = 20
            wing_x = self.x - 10
            wing_y = self.y
            wing_end_x = wing_x - wing_length * math.cos(math.radians(self.wing_angle))
            wing_end_y = wing_y - wing_length * math.sin(math.radians(self.wing_angle))
            pygame.draw.line(screen, self.color, (wing_x, wing_y), 
                           (wing_end_x, wing_end_y), 3)

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(100, SCREEN_HEIGHT - 100)
        self.x = SCREEN_WIDTH
        self.width = 50
        self.passed = False
        self.particles = []

    def update(self):
        self.x -= PIPE_SPEED
        
        # Create particles at the bottom of the pipe
        if random.random() < 0.1:
            self.particles.append(Particle(self.x + self.width // 2, 
                                         self.gap_y + PIPE_GAP // 2))

        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self):
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)

        if pipe_img:
            # Draw top pipe (flipped)
            top_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(top_pipe, (self.x, self.gap_y - PIPE_GAP // 2 - 400))
            # Draw bottom pipe
            screen.blit(pipe_img, (self.x, self.gap_y + PIPE_GAP // 2))
        else:
            # Draw top pipe
            pygame.draw.rect(screen, GREEN, 
                           (self.x, 0, self.width, self.gap_y - PIPE_GAP // 2))
            # Draw bottom pipe
            pygame.draw.rect(screen, GREEN, 
                           (self.x, self.gap_y + PIPE_GAP // 2, 
                            self.width, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2)))

    def collide(self, bird):
        # Check collision with top pipe
        if (bird.x + bird.radius > self.x and 
            bird.x - bird.radius < self.x + self.width and 
            bird.y - bird.radius < self.gap_y - PIPE_GAP // 2):
            return True
        # Check collision with bottom pipe
        if (bird.x + bird.radius > self.x and 
            bird.x - bird.radius < self.x + self.width and 
            bird.y + bird.radius > self.gap_y + PIPE_GAP // 2):
            return True
        return False

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.clouds = [Cloud() for _ in range(3)]
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.last_pipe = pygame.time.get_ticks()
        self.font = pygame.font.SysFont('Arial', 36)
        self.title_font = pygame.font.SysFont('Arial', 72, bold=True)
        self.ground_offset = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started:
                        self.game_started = True
                    elif self.game_over:
                        self.__init__()  # Reset game
                    else:
                        self.bird.flap()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_started:
                    self.game_started = True
                elif self.game_over:
                    self.__init__()  # Reset game
                else:
                    self.bird.flap()

    def update(self):
        if self.game_started and not self.game_over:
            self.bird.update()
            self.ground_offset = (self.ground_offset + GROUND_SPEED) % SCREEN_WIDTH

            # Update clouds
            for cloud in self.clouds:
                cloud.update()

            # Generate new pipes
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe > PIPE_FREQUENCY:
                self.pipes.append(Pipe())
                self.last_pipe = current_time

            # Update pipes
            for pipe in self.pipes[:]:
                pipe.update()
                if pipe.x + pipe.width < 0:
                    self.pipes.remove(pipe)
                elif not pipe.passed and pipe.x + pipe.width < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                    try:
                        point_sound.play()
                    except:
                        pass

            # Check collisions
            for pipe in self.pipes:
                if pipe.collide(self.bird):
                    self.game_over = True
                    try:
                        hit_sound.play()
                    except:
                        pass

            # Check if bird hits the ground or ceiling
            if (self.bird.y + self.bird.radius >= SCREEN_HEIGHT or 
                self.bird.y - self.bird.radius <= 0):
                self.game_over = True
                try:
                    hit_sound.play()
                except:
                    pass

    def draw(self):
        # Draw background
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(SKY_BLUE)

        # Draw clouds
        for cloud in self.clouds:
            cloud.draw()

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw()

        # Draw bird
        self.bird.draw()

        # Draw ground
        if ground_img:
            screen.blit(ground_img, (self.ground_offset, SCREEN_HEIGHT - 50))
            screen.blit(ground_img, (self.ground_offset - SCREEN_WIDTH, SCREEN_HEIGHT - 50))
        else:
            pygame.draw.rect(screen, GREEN, 
                           (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        if not self.game_started:
            # Draw start screen
            title_text = self.title_font.render('Flappy Bird', True, WHITE)
            start_text = self.font.render('Press SPACE or Click to Start', True, WHITE)
            screen.blit(title_text, 
                       (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 
                        SCREEN_HEIGHT // 3))
            screen.blit(start_text, 
                       (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2))

        if self.game_over:
            # Draw game over screen
            game_over_text = self.title_font.render('Game Over!', True, WHITE)
            restart_text = self.font.render('Press SPACE or Click to Restart', True, WHITE)
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                        SCREEN_HEIGHT // 3))
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2))

        pygame.display.flip()

def main():
    game = Game()
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)

if __name__ == "__main__":
    main() 