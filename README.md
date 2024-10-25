# 🐍 Automated Snake Game with Pathfinding

An advanced implementation of the classic Snake game featuring automated pathfinding algorithms and customizable gameplay options.

## Features

### Game Modes

- **Dijkstra's Algorithm Mode**: Snake automatically finds the shortest path to food
- **Survival Mode**: Snake uses A\* pathfinding with tail-proximity heuristics

### Wall Settings

- **Go Through Walls**: Snake can wrap around screen edges
- **Solid Walls**: Classic boundary collision mechanics

### Technical Features

- Real-time pathfinding visualization
- Score tracking system
- Dynamic food placement
- Collision detection
- Interactive game mode selection
- Restart/Quit options

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Install Pygame:

## Usage

Run the game:

## Controls

- Press 'M' to toggle between game modes during selection
- Press 'W' to toggle wall settings during selection
- Press 'Enter' to start the game
- Press 'R' to restart after game over
- Press 'Q' to quit after game over

## Game Mechanics

- The snake automatically moves towards food using selected pathfinding algorithm
- Score increases when food is consumed
- Game ends on collision with walls (in solid wall mode) or snake body
- Snake grows longer with each food item consumed

## Technical Implementation

- Uses Dijkstra's algorithm for shortest path finding
- Implements A\* algorithm with custom heuristics for survival mode
- Efficient collision detection using set data structure
- Grid-based movement system
- Frame-rate controlled game loop

## Development

The game is built using:

- Python for core logic
- Pygame for graphics and event handling
- Priority queues for pathfinding algorithms
- Custom path reconstruction methods

## Performance

- 10 FPS game loop for smooth visualization
- Efficient pathfinding with heap-based priority queue
- Optimized collision detection using set lookups
