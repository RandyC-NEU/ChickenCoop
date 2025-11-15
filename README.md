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
3. **Building Coops**: Coops cost $100 (Classic) or $200 (Deluxe). Deluxe coops occupy two adjacent land plots and have higher capacity.
4. **Adding Chickens**: Chickens cost $30 each and increase egg production
5. **Egg Production**: 
   - Coops produce 0.5 eggs per second (even empty)
   - Each chicken adds 0.3 eggs per second to their coop
6. **Selling Eggs**: Each egg sells for $5
7. **Blight**: Too many chickens in a coop may trigger a plague, reducing production. Blight can be cured or blighted chickens culled.
8. **Feed System**: Each coop has a feed level. Chickens require feed to produce eggs. Buy feed to keep production up; starvation stops egg production.
9. **Lighting & Shadows**: The game features a day/night cycle, dynamic lighting, and shadows for visual depth.
10. **Panels & UI**: Use retractable info and selector panels to view coop stats and select coop types. Improved UI feedback and controls.

### Game Controls

| Control | Action |
|---------|--------|
| **Click "Buy Land"** | Purchase a new land plot |
| **Click "Select Coop" panel** | Open the retractable menu to choose Classic or Deluxe coop |
| **Click on land plot** | Select a plot (Deluxe coops can be selected from either occupied plot) |
| **Click "Buy Chicken"** | Add a chicken to an existing coop |
| **Click "Buy Feed"** | Buy feed for the selected coop |
| **Click "Sell All Eggs"** | Sell all eggs for money |
| **Click "Buy Blight Cure"** | Cure blight in all coops |
| **Click "Cull Blighted Chickens"** | Remove all blighted chickens |
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
