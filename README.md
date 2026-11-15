# Tic-Tac-Toe with AI

A console Tic-Tac-Toe game where you play against the computer.

## How to run (VS Code)
1. Open the folder in VS Code.
2. Open the terminal (Ctrl + `) and run:
   ```
   python tictactoe.py
   ```
   (Python 3.8+ required, no extra packages.)

## Features
- Board is displayed after **every** move (empty cells show their number 1-9).
- **Easy AI** - simple rules: win if possible -> block the opponent -> take center -> take a corner -> take any side.
- **Hard AI** - **Minimax** algorithm with alpha-beta pruning; it never loses.
- Correct detection of **win**, **loss** and **draw** (8 winning lines + full-board check).
- Input validation (non-numbers, out-of-range, occupied cells).
- Choose X or O, play again, running score.

## How Minimax works (short)
The AI tries every possible future move, assuming you also play your best.
Each end position is scored: AI win = `10 - depth`, your win = `depth - 10`, draw = `0`.
The AI picks the move with the highest score. Alpha-beta pruning skips branches
that cannot change the result, making it faster.

## Files
- `tictactoe.py` - the complete game
