# 🐔 Chicken Coop Tycoon

A pygame-based farm tycoon game where you build and manage chicken coops, care for chickens, and sell eggs to grow your farm empire!

## Game Overview

Build your chicken farm from the ground up! Purchase land, build coops, buy chickens, and manage egg production to maximize profits. Similar to FarmVille, this idle/management game rewards strategic planning and resource management.

## Features

- **Land Management**: Buy land plots to expand your farm
- **Coop Building**: Construct chicken coops on your land
- **Chicken Care**: Purchase chickens to populate your coops
- **Egg Production**: Coops and chickens automatically produce eggs over time
- **Economy System**: Sell eggs for money to invest in more structures
- **Real-time Production**: Watch your farm generate income while you play
- **Pause Mechanism**: Press SPACE to pause/resume the game

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

### Game Controls

| Control | Action |
|---------|--------|
| **Click "Buy Land"** | Purchase a new land plot |
| **Click "Buy Coop"** | Place a chicken coop on empty land |
| **Click "Buy Chicken"** | Add a chicken to an existing coop |
| **Click "Sell All Eggs"** | Sell all eggs for money |
| **SPACE** | Pause/Resume the game |

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

### Strategy Tips

- **Early Game**: Buy a coop first to house chickens
- **Scaling**: Add chickens to increase production rate
- **Investment**: Balance between buying new land and stocking existing coops
- **Passive Income**: Let your farm produce eggs while you wait
- **Planning**: Think ahead about which coops to expand

## Game Elements

### Visual Components

- **Green Squares**: Empty land plots
- **Brown Buildings with Red Roofs**: Chicken coops
- **Orange Circles**: Chickens
- **Gray Panel (right side)**: UI with buttons and status

### Displayed Information

- Current money balance
- Total eggs collected
- Game time elapsed
- Pause state

## Example Progression

1. Start with $500
2. Buy a coop ($100) → Now have $400 and 1 coop producing eggs
3. Buy 2 chickens ($60) → Now have $340 and 2.1 eggs/second production
4. After ~30 seconds: Collect ~60 eggs = $300 in sales
5. Use profits to expand: Buy more land, more coops, more chickens

## Technical Details

### Classes

- **Game**: Main game loop and state management
- **Button**: UI button with hover and click detection
- **Land**: Land plot that can contain a coop
- **Coop**: Chicken coop that houses chickens and produces eggs
- **Chicken**: Individual chicken entity

### Game Constants

```python
COOP_COST = 100
CHICKEN_COST = 30
LAND_COST = 150
EGG_SELL_PRICE = 5

COOP_PRODUCTION_RATE = 0.5 eggs/second
CHICKEN_PRODUCTION_RATE = 0.3 eggs/second
```

## Troubleshooting

**Issue**: "ModuleNotFoundError: No module named 'pygame'"
- **Solution**: Run `pip install pygame`

**Issue**: Game runs but displays are small
- **Solution**: Screen is 1200x800. Adjust SCREEN_WIDTH and SCREEN_HEIGHT in main.py if needed

**Issue**: Game is running slow
- **Solution**: Close other applications, ensure your system meets minimum requirements

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
