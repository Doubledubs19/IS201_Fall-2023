import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_board(board):
    clear_screen()
    print("1" + " | " + "2" + " | " + "3")
    print("--+---+--")
    print("4" + " | " + "5" + " | " + "6")
    print("--+---+--")
    print("7" + " | " + "8" + " | " +"9")

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals REWRITE for scalability
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
#split into 2 functions
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
#think about constructor instead of new finction
def play_tic_tac_toe():
    board = [" " for _ in range(9)]
    player = get_player_choice()  # Get player's choice
    computer = "O" if player == "X" else "X"  # Set the other value for the computer
    current_player = player  # Initialize current_player

    print(f"You are playing as {player}. Computer is {computer}.")

    while True:
        display_board(board)

        if current_player == computer:
            # Computer's move using minimax
            move = find_best_move(board)
            board[move] = computer  # Set computer's choice

            display_board(board)
        else:
            # Human's move
            move = get_valid_input(board, current_player)

        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_board_full(board):
            display_board(board)
            print("It's a draw!")
            break

        current_player = player if current_player == computer else computer
# define a "main function" instead
if __name__ == "__main__":
    while True:
        clear_screen()
        play_tic_tac_toe()
        play_again = input("Play again? (y/n): ").lower()
        if play_again != "y":
            break
        
