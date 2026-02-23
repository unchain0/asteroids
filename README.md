# Asteroids

A modern Python implementation of the classic Asteroids arcade game using Pygame.

## Features

- **Classic Gameplay**: Pilot a spaceship and destroy asteroids
- **Scoring System**: Earn points for destroying asteroids (20/50/100 based on size)
- **Multiple Lives**: 3 lives with respawn invulnerability
- **Explosion Effects**: Particle effects when asteroids are destroyed
- **Screen Wrapping**: Objects wrap around screen edges
- **Acceleration-based Movement**: Realistic thrust physics with momentum
- **Lumpy Asteroids**: Irregular polygon shapes instead of perfect circles
- **Triangular Ship Hitbox**: Accurate collision detection
- **Weapon Types**: Switch between Normal, Spread, and Rapid fire modes
- **Power-ups**: Shield (green) and Speed boost (blue) power-ups
- **Bombs**: Drop area-damage bombs
- **Background Image**: Custom space background support

## Controls

| Key   | Action          |
| ----- | --------------- |
| W     | Thrust forward  |
| S     | Thrust backward |
| A     | Rotate left     |
| D     | Rotate right    |
| SPACE | Shoot           |

## Installation

```bash
# Clone the repository
git clone https://github.com/unchain0/asteroids.git
cd asteroids

# Install dependencies
uv sync

# Run the game
uv run main.py
```

## Optional: Background Image

Place a `background.png` file in an `assets/` directory to use a custom background:

```
asteroids/
├── assets/
│   └── background.png
├── main.py
└── ...
```

## Development

The codebase follows a clean architecture with separated concerns:

- `main.py` - Game loop and orchestration
- `player.py` - Player ship logic
- `asteroid.py` - Asteroid entities with polygon generation
- `circleshape.py` - Base sprite class with collision
- `particles.py` - Explosion particle effects
- `bomb.py` - Bomb weapon implementation
- `powerups.py` - Power-up entities
- `constants.py` - Game configuration

## License

MIT License
