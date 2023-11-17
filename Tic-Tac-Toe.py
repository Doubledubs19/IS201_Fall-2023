import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_board(board):
    clear_screen()
    for i in range(0, 9, 3):
        row = " | ".join([str(idx + 1 + i) if val == ' ' else val for idx, val in enumerate(board[i:i+3])])
        print(row)
        if i < 6:
            print("-" * 9)
# i want to dynamically keep the board on the screen and then remove the position number when a choice occurs

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_board_full(board):
    return " " not in board

def get_valid_input(board, player):
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if move < 0 or move > 8 or board[move] != " ":
                print("Invalid move. Try again.")
            else:
                return move
        except ValueError:
            print("Invalid input. Enter a number between 1 and 9.")

def min_value(board, depth):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_board_full(board):
        return 0

    best_score = float("inf")
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = max_value(board, depth + 1)
            board[i] = " "
            best_score = min(score, best_score)
    return best_score

def max_value(board, depth):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_board_full(board):
        return 0

    best_score = -float("inf")
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = min_value(board, depth + 1)
            board[i] = " "
            best_score = max(score, best_score)
    return best_score

def find_best_move(board):
    best_score = -float("inf")
    best_move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = min_value(board, 0)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def get_player_choice():
    while True:
        choice = input("Choose 'X' or 'O' to play: ").upper()
        if choice in ['X', 'O']:
            return choice
        else:
            print("Invalid choice. Please enter 'X' or 'O.'")

def play_tic_tac_toe():
    board = [" " for _ in range(9)]
    player = get_player_choice()
    computer = "O" if player == "X" else "X"
    current_player = player
    
    print(f"You are playing as {player}. Computer is {computer}.")
    
    # Ask the user if they want to play first
    while True:
        user_choice = input("Do you want to play first? (y/n): ").lower()
        if user_choice == 'y':
            current_player = player
            break
        elif user_choice == 'n':
            current_player = computer
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

    while True:
        display_board(board)

        if current_player == computer:
            move = find_best_move(board)
            board[move] = computer
        else:
            display_board(board)
            move = get_valid_input(board, current_player)
            board[move] = current_player
            clear_screen()  # clear screen after player's move to hide positions

        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_board_full(board):
            display_board(board)
            print("It's a draw!")
            break

        current_player = player if current_player == computer else computer

if __name__ == "__main__":
    while True:
        clear_screen()
        play_tic_tac_toe()
        play_again = input("Play again? (y/n): ").lower()
        if play_again != "y":
            break
