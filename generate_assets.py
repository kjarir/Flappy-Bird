import os
import pygame
import math
import random

def create_assets():
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Initialize Pygame for image generation
    pygame.init()
    
    # Create a surface for drawing
    surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    
    # Generate background
    print("Generating background...")
    # Simple blue background
    surface.fill((135, 206, 235))  # Sky blue
    
    # Draw simple clouds
    for _ in range(5):
        x = random.randint(0, 700)
        y = random.randint(50, 200)
        # Simple white cloud
        pygame.draw.ellipse(surface, (255, 255, 255), (x, y, 100, 40))
    
    pygame.image.save(surface, 'assets/background.png')
    
    # Generate bird
    print("Generating bird...")
    bird_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Simple round yellow bird
    pygame.draw.circle(bird_surface, (255, 255, 0), (20, 20), 15)  # Main body
    pygame.draw.circle(bird_surface, (255, 255, 255), (25, 15), 6)  # Eye white
    pygame.draw.circle(bird_surface, (0, 0, 0), (25, 15), 3)  # Eye black
    # Orange triangle beak
    pygame.draw.polygon(bird_surface, (255, 165, 0), [(30, 20), (40, 20), (30, 15)])
    # Simple wing
    pygame.draw.ellipse(bird_surface, (255, 220, 0), (8, 15, 15, 10))
    
    pygame.image.save(bird_surface, 'assets/bird.png')
    
    # Generate pipe
    print("Generating pipe...")
    pipe_surface = pygame.Surface((52, 500), pygame.SRCALPHA)
    
    # Simple green pipe
    pygame.draw.rect(pipe_surface, (40, 180, 40), (0, 0, 52, 500))  # Main body
    pygame.draw.rect(pipe_surface, (34, 150, 34), (0, 0, 52, 30))   # Top cap
    pygame.draw.rect(pipe_surface, (34, 150, 34), (0, 470, 52, 30)) # Bottom cap
    
    pygame.image.save(pipe_surface, 'assets/pipe.png')
    
    # Generate ground
    print("Generating ground...")
    ground_surface = pygame.Surface((800, 100), pygame.SRCALPHA)
    
    # Simple brown ground
    pygame.draw.rect(ground_surface, (210, 180, 140), (0, 0, 800, 100))  # Tan color
    # Add some simple grass
    for x in range(0, 800, 30):
        pygame.draw.rect(ground_surface, (34, 139, 34), (x, 0, 20, 10))
    
    pygame.image.save(ground_surface, 'assets/ground.png')
    
    # Generate simple cloud sprite
    print("Generating cloud...")
    cloud_surface = pygame.Surface((100, 50), pygame.SRCALPHA)
    pygame.draw.ellipse(cloud_surface, (255, 255, 255), (0, 10, 70, 30))
    pygame.draw.ellipse(cloud_surface, (255, 255, 255), (30, 0, 70, 40))
    
    pygame.image.save(cloud_surface, 'assets/cloud.png')
    
    # Generate simple sound effects
    print("Generating sound effects...")
    sample_rate = 44100
    duration = 0.1
    
    # Simple beep sounds
    def generate_beep(frequency):
        return pygame.mixer.Sound(buffer=bytearray(
            [int(127 + 127 * math.sin(2 * math.pi * frequency * t / sample_rate)) 
             for t in range(int(sample_rate * duration))]))
    
    # Generate and save sounds
    generate_beep(440).save('assets/flap.wav')  # Higher pitch for flap
    generate_beep(220).save('assets/hit.wav')   # Lower pitch for hit
    generate_beep(880).save('assets/point.wav') # Highest pitch for point
    
    # Simple background music
    background_music = pygame.mixer.Sound(buffer=bytearray(
        [int(127 + 127 * math.sin(2 * math.pi * 440 * t / sample_rate)) 
         for t in range(int(sample_rate * 1))]))
    pygame.mixer.Sound.save(background_music, 'assets/background.wav')
    
    print("\nAll assets generated successfully!")
    print("The game now includes:")
    print("- Simple blue background")
    print("- Classic yellow bird")
    print("- Simple green pipes")
    print("- Basic ground with grass")
    print("- White clouds")
    print("- Basic sound effects")

if __name__ == "__main__":
    create_assets() 