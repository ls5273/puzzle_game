# 🧩 TERMINAL BLOCK PUZZLE GAME

## 📌 Overview:
- Terminal Block Puzzle is an interactive, command-line puzzle game built entirely in Python. Players are challenged to fit a variety of uniquely colored shapes onto a 6x6 grid. The objective is to maximize your score by filling as many open tiles as possible while navigating around randomized obstacle blocks.

## ✨ Key Features:
- **Vibrant Terminal Graphics:** Utilizes ANSI escape codes to render brightly colored, solid-block puzzle pieces directly in the console.
- **Dynamic Shape Manipulation:** Players can rotate pieces in precise 90-degree increments.
- **Axis Flipping:** Pieces can be flipped over their horizontal (y) or vertical (x) axis to fit into tricky spaces.
- **Interactive Game Loop:** Features a robust CLI loop allowing users to continuously preview, place, move, and remove pieces on the board.
- **Randomized Obstacles:** Each game initializes with one of several predefined configurations of "blocker" spots on the board, ensuring every playthrough requires a unique strategy.
- **Collision Detection:** Includes built-in error handling that prevents players from placing pieces out of bounds or overlapping with existing shapes and blockers.

## 🛠️ Tech Stack:
- **Language:** Pure Python (No external dependencies required).
- **Concepts Demonstrated:** Object-Oriented Programming (OOP), matrix manipulation using 2D arrays, standard input/output parsing, and exception management.

## 🎮 How to Play:
1. Run python main.py in your terminal to initialize the game board.
2. Choose a puzzle piece from the available character options (L, l, T, t, z, c, f).
3. Preview your piece in the console and choose an action to Rotate, Flip, or Place it.
4. Input the top-left 2D coordinates for placement (e.g., (0, 1)).
5. Continue placing pieces to fill the board and achieve the highest score possible!
