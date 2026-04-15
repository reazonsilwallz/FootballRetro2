# footballRetro

A 2-player retro-style football game made with Python and Pygame.

## Project Overview

`footballRetro` is a simple local multiplayer game where two players compete to score goals before the timer runs out.

- Blue player uses the **Spacebar**
- Red player uses the **Enter key**
- Each player rotates automatically
- Holding the control key makes the player move forward
- Touching the ball while moving kicks it
- The game keeps score and declares a winner at the end

## Features

- Main menu with Start and Exit
- 2-player gameplay
- Ball movement with friction
- Goal detection and score system
- 2-minute match timer
- Game over screen
- Sound effects for kicks and goals
- Visual effects such as goal flash
- Custom player shapes and field design

## Controls

### Blue Player
- **Spacebar** → move forward

### Red Player
- **Enter** → move forward

### Menu / Game Over
- **Mouse click** → Start or Exit from menu
- **Enter** → return to menu after game over

## Technologies Used

- **Python**
- **Pygame**

## Files Used

- `main.py` — main game code
- `kick.wav` — kick sound effect
- `cheer.mp3` — goal cheer sound

## How to Run

1. Make sure Python is installed
2. Install Pygame:
   ```bash
   pip install pygame
