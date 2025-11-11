# Chicken Coop Tycoon 🐔 

A pygame-based farm tycoon game where you build and manage chicken coops, care for chickens, and sell eggs to grow your farm empire!

## Game Overview

Build your chicken farm from the ground up! Purchase land, build coops, buy chickens, and manage egg production to maximize profits. Similar to FarmVille, this idle/management game rewards strategic planning and resource management.

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. Navigate to the project directory:
```bash
cd ChickenCoop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

### Running the Game
```bash
python main.py
```

### Gameplay Mechanics

1. **Starting Capital**: You begin with $500
2. **Buying Land**: Land costs $150 and is required to place structures
3. **Building Coops**: Coops cost $100 and can hold multiple chickens
4. **Adding Chickens**: Chickens cost $30 each and increase egg production
5. **Egg Production**: 
   - Coops produce 0.5 eggs per second (even empty)
   - Each chicken adds 0.3 eggs per second to their coop
6. **Selling Eggs**: Each egg sells for $5
7. **Beware the Blight!!**: Too many chickens in a coop may trigger a plague, watch out for coop population

### Game Controls

| Control | Action |
|---------|--------|
| **Click "Buy Land"** | Purchase a new land plot |
| **Click "Buy Coop"** | Place a chicken coop on empty land |
| **Click "Buy Chicken"** | Add a chicken to an existing coop |
| **Click "Sell All Eggs"** | Sell all eggs for money |
| **SPACE** | Pause/Resume the game |

## Future Enhancement Ideas

- Save/load game progress
- Upgrades for coops (better production)
- Different chicken types with varied production rates
- Weather effects (storms, sunny days)
- NPC traders
- Achievements and leaderboards
- Sound effects and music
- Animations for egg laying
- Market prices that fluctuate
- Farm aesthetics/customization

## License

This is a free, open-source project. Feel free to modify and distribute!

---

Happy farming! 🐓🐓🐓
