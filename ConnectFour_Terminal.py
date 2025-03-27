import numpy as np
import random
import math
import time
import threading
from queue import Queue

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

# Add difficulty levels
EASY = {
    'depth': 2,    # Looks 2 moves ahead
    'multiplier': 0.5 , # Reduces AI's scoring
    'time_limit': None
}
MEDIUM = {
    'depth': 4,    # Looks 4 moves ahead
    'multiplier': 1.0,# Normal scoring
    'time_limit': 15     
}
HARD = {
    'depth': 6,    # Looks 6 moves ahead
    'multiplier': 1.5 ,# Increases AI's scoring
    'time_limit': 10   
}

def timed_input(prompt, time_limit):
    q = Queue()
    
    def get_input():
        try:
            user_input = input(prompt)
            q.put(user_input)
        except:
            q.put(None)
    
    # Create and start input thread
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()
    
    # Wait for input or timeout
    try:
        user_input = q.get(timeout=time_limit)
        return user_input
    except:
        print(f"\nTime's up! You took longer than {time_limit} seconds!")
        return None
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Kiểm tra chiến thắng theo các hướng (ngang, dọc, chéo)
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece, difficulty_multiplier):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    # Scoring based on piece configurations
    if window.count(piece) == 4:
        score += 100 * difficulty_multiplier
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5 * difficulty_multiplier
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2 * difficulty_multiplier

    # Defensive scoring
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4 * (2 - difficulty_multiplier)  # Less defensive in hard mode

    return score
def score_position(board, piece, difficulty_multiplier):
    score = 0
    # Center column control is more important in harder difficulties
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3 * difficulty_multiplier


    for r in range(ROW_COUNT): #horizontal scoring
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece, difficulty_multiplier)

    for c in range(COLUMN_COUNT): #vertical scoring
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece, difficulty_multiplier)

    for r in range(ROW_COUNT-3): # Positive Diagonal Scoring (bottom-left to top-right)

        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece, difficulty_multiplier)

    for r in range(ROW_COUNT-3): # Negative Diagonal Scoring (top-left to bottom-right)
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece, difficulty_multiplier)

    return score

def is_terminal_node(board):    
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer, difficulty_multiplier):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: 
                return (None, 0)
        else: 
            return (None, score_position(board, AI_PIECE, difficulty_multiplier))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False, difficulty_multiplier)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: 
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True, difficulty_multiplier)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def play_game():
    board = create_board()
    game_over = False

    # Add difficulty selection
    while True:
        try:
            print("\nSelect difficulty level:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            difficulty = int(input("Enter your choice (1-3): "))
            if difficulty in [1, 2, 3]:
                difficulty_settings = {
                    1: EASY,
                    2: MEDIUM,
                    3: HARD
                }[difficulty]
                depth = difficulty_settings['depth']
                multiplier = difficulty_settings['multiplier']
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")


    while True:
        try:
            choice = int(input("Who goes first?\n1. Player\n2. AI\nEnter your choice (1-2): "))
            if choice in [1, 2]:
                turn = PLAYER if choice == 1 else AI
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number (1-2).")

    print("\nGame starting...")
    print("Player is RED, AI is YELLOW")
    print_board(board)

    while not game_over:
        if turn == PLAYER:
            try:
                if difficulty_settings['time_limit']:
                    print(f"\nYou have {difficulty_settings['time_limit']} seconds to move!")
                    user_input = timed_input("Player 1 (RED), choose a column (1-7): ", 
                                          difficulty_settings['time_limit'])
                    if user_input is None:
                        print("Time's up! Turn forfeited to AI!")
                        turn += 1
                        turn = turn % 2
                        continue
                    col = int(user_input) - 1
                else:
                    # Easy mode - no time limit
                    col = int(input("Player 1 (RED), choose a column (1-7): ")) - 1
                if col < 0 or col >= COLUMN_COUNT:
                    print("Invalid column. Please choose a column between 1 and 7.")
                    continue
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        print_board(board)
                        print("Player 1 (RED) wins!!")
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                else:
                    print("Column full, try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")

        if turn == AI and not game_over:
            print("AI is making its move...")
            start_time = time.time()
            col, _ = minimax(board, depth, -math.inf, math.inf, True, multiplier)
            thinking_time = time.time() - start_time
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                print(f"AI moved in {thinking_time:.1f} seconds")

                if winning_move(board, AI_PIECE):
                    print_board(board)
                    print("AI (YELLOW) wins!!")
                    game_over = True
                turn += 1
                turn = turn % 2
                print_board(board)

    print("Game Over!")

if __name__ == "__main__":
    play_game()
