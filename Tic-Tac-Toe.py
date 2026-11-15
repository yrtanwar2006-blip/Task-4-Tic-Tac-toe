Tic-Tac-Toe
"""
Tic-Tac-Toe: Human vs Computer
==============================- Console game, board is printed after every move.- Two AI levels:
    1) Easy  - simple rule-based AI (win > block > center > corner > side)
    2) Hard  - Minimax algorithm with alpha-beta pruning (unbeatable)- Detects win, loss and draw correctly.
Run:  python tictactoe.py
"""
import random
EMPTY = " "
# All 8 ways to win (indices into the 9-cell board list)
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]
# -------------------------------------------------------------------------
# Board helpers
# -------------------------------------------------------------------------
def new_board():
    return [EMPTY] * 9
def display_board(board):
    """Print the board; empty cells show their number (1-9) as a hint."""
    print()
    for r in range(3):
        cells = []
        for c in range(3):
            i = r * 3 + c
            cells.append(board[i] if board[i] != EMPTY else str(i + 1))
        print(" " + " | ".join(cells))
        if r < 2:
            print("---+---+---")
    print()
def get_winner(board):
    """Return 'X' or 'O' if someone has won, otherwise None."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None
def is_full(board):
    return EMPTY not in board
def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]
def game_over(board):
    return get_winner(board) is not None or is_full(board)
# -------------------------------------------------------------------------
# AI 1: simple rule-based opponent
# -------------------------------------------------------------------------
def find_winning_move(board, mark):
    """Return a move that lets `mark` win immediately, else None."""
    for move in available_moves(board):
        board[move] = mark
        won = get_winner(board) == mark
        board[move] = EMPTY
        if won:
            return move
    return None
def rule_based_move(board, ai, human):
    """Priority: win -> block -> center -> corner -> side."""
    move = find_winning_move(board, ai)
    if move is not None:
        return move
    move = find_winning_move(board, human)      # block the opponent
    if move is not None:
        return move
    if board[4] == EMPTY:
        return 4
    corners = [i for i in (0, 2, 6, 8) if board[i] == EMPTY]
    if corners:
        return random.choice(corners)
    return random.choice(available_moves(board))
# -------------------------------------------------------------------------
# AI 2: Minimax with alpha-beta pruning
# -------------------------------------------------------------------------
def minimax(board, depth, is_maximizing, ai, human, alpha, beta):
    """
    Score a position from the AI's point of view.
    +10 - depth : AI wins (faster wins score higher)
    depth - 10  : human wins (slower losses score higher)
    0           : draw
    """
    winner = get_winner(board)
    if winner == ai:
        return 10 - depth
    if winner == human:
        return depth - 10
    if is_full(board):
        return 0
    if is_maximizing:
        best = float("-inf")
        for move in available_moves(board):
            board[move] = ai
            score = minimax(board, depth + 1, False, ai, human, alpha, beta)
            board[move] = EMPTY
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float("inf")
        for move in available_moves(board):
            board[move] = human
            score = minimax(board, depth + 1, True, ai, human, alpha, beta)
            board[move] = EMPTY
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best
def minimax_move(board, ai, human):
    """Pick the move with the best minimax score (random among ties)."""
    best_score = float("-inf")
    best_moves = []
    for move in available_moves(board):
        board[move] = ai
        score = minimax(board, 1, False, ai, human,
                        float("-inf"), float("inf"))
        board[move] = EMPTY
        if score > best_score:
            best_score, best_moves = score, [move]
        elif score == best_score:
            best_moves.append(move)
    return random.choice(best_moves)
# -------------------------------------------------------------------------
# User input
# -------------------------------------------------------------------------
def ask_choice(prompt, valid):
    while True:
        answer = input(prompt).strip().upper()
        if answer in valid:
            return answer
        print(f"  Please enter one of: {', '.join(sorted(valid))}")
def get_human_move(board):
    while True:
        raw = input("Your move (1-9): ").strip()
        if not raw.isdigit() or not 1 <= int(raw) <= 9:
            print("  Invalid input. Enter a number from 1 to 9.")
            continue
        move = int(raw) - 1
        if board[move] != EMPTY:
            print("  That cell is already taken. Try another.")
            continue
        return move
# -------------------------------------------------------------------------
# Game loop
# -------------------------------------------------------------------------
def play_game(level, human, ai):
    board = new_board()
    turn = "X"                       # X always goes first
    display_board(board)
    while not game_over(board):
        if turn == human:
            move = get_human_move(board)
            board[move] = human
            print(f"You placed {human} at position {move + 1}.")
        else:
            print("Computer is thinking...")
            if level == "1":
                move = rule_based_move(board, ai, human)
            else:
                move = minimax_move(board, ai, human)
            board[move] = ai
            print(f"Computer placed {ai} at position {move + 1}.")
        display_board(board)         # show board after EVERY move
        turn = "O" if turn == "X" else "X"
    winner = get_winner(board)
    if winner == human:
        print("*** You WIN! Congratulations! ***")
        return "win"
    if winner == ai:
        print("*** You LOSE. The computer wins! ***")
        return "loss"
    print("*** It's a DRAW! ***")
    return "draw"
def main():
    print("=" * 36)
    print("   TIC-TAC-TOE : You vs Computer")
    print("=" * 36)
    print("Cells are numbered 1-9 like this:")
    display_board([str(i) for i in range(1, 10)])
    print("Choose difficulty:")
    print("  1) Easy - simple rules (win, block, center, corner)")
    print("  2) Hard - Minimax algorithm (unbeatable)")
    level = ask_choice("Enter 1 or 2: ", {"1", "2"})
    human = ask_choice("Play as X (goes first) or O? ", {"X", "O"})
    ai = "O" if human == "X" else "X"
    score = {"win": 0, "loss": 0, "draw": 0}
    while True:
        result = play_game(level, human, ai)
        score[result] += 1
        print(f"\nScore -> Wins: {score['win']} | "
              f"Losses: {score['loss']} | Draws: {score['draw']}")
        again = ask_choice("\nPlay again? (Y/N): ", {"Y", "N"})
        if again == "N":
            print("Thanks for playing!")
            break
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame ended. Goodbye!")