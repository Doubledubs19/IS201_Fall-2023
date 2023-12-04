import os

# This function uses the os python module to clear the console screen depending on OS
# os.system is used to execute a command inside of the parentheses
# the command () inside os.system is os.name, which is a built-in function that returns the operating system being used
# nt = windows so the command "cls" is given. anything else and the command "clear" is given
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# responsibile for dynamically displaying the board. it invokes the clear_screen function at the beginning to "start fresh"
# the for loop then iterates over the 0-9 range in steps of 3 to create the game board
# by using list comprehension, you can generate a list of elements that form the rows of a tic-tac-toe board dynamically
# the first part of the .join statement checks the value of the current position against any choices and if it's not empty, then it retains the value
# the enumerate portion iterates through a portion of the board list and returns the index and value of each element
# the join method concats the elements of the generated rows together using the pipe '|' as a seperator
# the row is then printed and another check is done if i is less than 6, it will build a separator using dashes
def display_board(board):
    clear_screen()
    for i in range(0, 9, 3):
        row = " | ".join([str(idx + 1 + i) if val == ' ' else val for idx, val in enumerate(board[i:i+3])])
        print(row)
        if i < 6:
            print("-" * 9)

# this function is used to constantly check if the current player has won based on the game boards' state.
# by using the all() python function, you can iterate across all of the winning combos to see if the player
# occupies the correct number of combinations
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

# just a quick check to see if the board has any empty spaces or not
def is_board_full(board):
    return " " not in board

# gets the input from the current player and will error if it's not a valid move
# the "or board[move] != " "" is meant as a check against choosing an already taken spot
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

# min_value and max_value are meant to calculate the best move achievable by the player
# the "AI" will switch between min_value and max_value based on the player's choice of X or O
# they were built as recursive functions so that they can handle the recursive depth approach
# to determining the optimal move for the computer opponent. it checks for different terminal states
# based off the empty spaces and which moves it can theoretically make and then returns the the best_score
# to the function. the find_best_move function then iterates through the empty spaces and simulates
# placing the human player's symbol at that position. it calls min_value or max_value depending on symbols assigned
# the algorithm evaluates each possible move and returns the best possible score.
# the best_score is initialized as pos or neg infinity to ensure the function correctly selects the best move
# whether it's min/max'ing the scores
# after each simulated move, it updates best_score and best_move if a better "move" is found
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

def find_best_move(board, player):
    best_score = -float("inf") if player == "O" else float("inf")
    best_move = -1

    for i in range(9):
        if board[i] == " ":
            board[i] = player
            if player == "O":
                score = min_value(board, 0)
            else:
                score = max_value(board, 0)
            board[i] = " "

            if (player == "O" and score > best_score) or (player == "X" and score < best_score):
                best_score = score
                best_move = i
    return best_move

# simple input to determine whether the human player wants the X or O symbol
# errors if the input from the choice variable does not equal X or O
def get_player_choice():
    while True:
        choice = input("Choose 'X' or 'O' to play: ").upper()
        if choice in ['X', 'O']:
            return choice
        else:
            print("Invalid choice. Please enter 'X' or 'O.'")

# uses all of the built functions to run the actual game, handle player choices, turns, move validation, and
# determines the game outcome by invoking the check_winner or is_board_full functions
# creates the board variable that will get used by the display_board function to generate the playing board based
# off the computer and player's choices
# creates the player variable where it runs the get_player_choice function
# sets the computer's symbol to whatever wasn't chosen by the player
# initializes the current_player to the player unless the while loop below states differently
# implements a while True loop if the player wants to go first or not

# while True loops were used so that you can keep looping until the break statements occur
# goes back and forth between player and computer until a break statement occurs

def play_tic_tac_toe():
    board = [" " for _ in range(9)]
    player = get_player_choice()
    computer = "O" if player == "X" else "X"
    current_player = player
    
    print(f"You are playing as {player}. Computer is {computer}.")
    
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
            move = find_best_move(board,computer)
            board[move] = computer
        else:
            display_board(board)
            move = get_valid_input(board, current_player)
            board[move] = current_player
            clear_screen()

        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_board_full(board):
            display_board(board)
            print("It's a draw!")
            break

        current_player = player if current_player == computer else computer

# allows the user to play multiple times
if __name__ == "__main__":
    while True:
        clear_screen()
        play_tic_tac_toe()
        play_again = input("Play again? (y/n): ").lower()
        if play_again != "y":
            break
