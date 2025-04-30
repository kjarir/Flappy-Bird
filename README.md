# Flappy Bird Game

A modern and realistic implementation of the classic Flappy Bird game using Python and Pygame.

## Features

- Realistic bird physics with wing animations
- Particle effects for flapping and pipe movement
- Parallax scrolling background with moving clouds
- Animated ground texture
- Randomly generated pipes with realistic textures
- Score tracking
- Collision detection
- Game over screen with restart option
- High-quality sound effects and background music
- Start screen with instructions

## Requirements

- Python 3.x
- Pygame 2.5.2

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate the game assets:
   ```bash
   python generate_assets.py
   ```

## Running the Game

Run the game using Python:
```bash
python flappy_bird.py
```

## Controls

- Space bar or Mouse click: Make the bird flap
- Click anywhere to restart after game over

## Game Rules

1. Control the bird by tapping/clicking to make it flap
2. Navigate through the gaps between pipes
3. Each successful pass through a pipe pair earns one point
4. Game ends if the bird hits a pipe or the ground/ceiling

## Realistic Features

The game includes several realistic elements:

### Visual Effects
- Animated bird with flapping wings
- Particle effects when the bird flaps
- Moving clouds in the background
- Parallax scrolling ground
- Realistic pipe textures
- Smooth animations and transitions

### Physics
- Realistic gravity and momentum
- Bird rotation based on movement
- Smooth acceleration and deceleration
- Natural-looking pipe movement

### Sound Effects
- Generated background music
- Realistic flap sound
- Impact sound when hitting obstacles
- Point scoring sound effect

## Assets

The game generates all assets programmatically:
- Background with procedurally generated clouds
- Animated bird sprite with wing movements
- Pipe textures with realistic details
- Animated ground texture with grass details
- Cloud sprites
- Generated sound effects and music

All assets are automatically generated when you run `generate_assets.py`. 