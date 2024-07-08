import tkinter as tk
import random

def display_board(board):
    """Updates the button grid to reflect the current board state."""
    for i in range(9):
        buttons[i].config(text=board[i])

def player_move(position):
    """Handles the player's move."""
    if board[position - 1] == ' ':  # Check if position is empty
        board[position - 1] = player_marker
        display_board(board)
        if win_check(board, player_marker):
            show_result("You won!")
        elif full_board_check(board):
            show_result("It's a tie!")
        else:
            computer_move()

def computer_move():
    """Handles the computer's move."""
    position = computer_choice(board)
    board[position - 1] = computer_marker
    display_board(board)
    if win_check(board, computer_marker):
        show_result("Computer won!")
    elif full_board_check(board):
        show_result("It's a tie!")

def show_result(message):
    """Displays a message box with the game result."""
    global game_on
    game_on = False  # Stop the game loop
    tk.messagebox.showinfo("Game Over", message)

# ... (Other functions: win_check, choose_first, space_check, full_board_check, computer_choice remain the same)
def win_check(board, mark):
    """Checks if the given mark has won the game."""
    return ((board[0] == mark and board[1] == mark and board[2] == mark) or  # across the top
            (board[3] == mark and board[4] == mark and board[5] == mark) or  # across the middle
            (board[6] == mark and board[7] == mark and board[8] == mark) or  # across the bottom
            (board[0] == mark and board[3] == mark and board[6] == mark) or  # down the left side
            (board[1] == mark and board[4] == mark and board[7] == mark) or  # down the middle
            (board[2] == mark and board[5] == mark and board[8] == mark) or  # down the right side
            (board[0] == mark and board[4] == mark and board[8] == mark) or  # diagonal
            (board[2] == mark and board[4] == mark and board[6] == mark))   # diagonal

def choose_first():
    """Randomly determines who goes first."""
    if random.randint(0, 1) == 0:
        return 'Player'
    else:
        return 'Computer'

def space_check(board, position):
    """Checks if a position on the board is empty."""
    return board[position - 1] == ' '

def full_board_check(board):
    """Checks if the board is full."""
    for i in range(9):
        if space_check(board, i + 1):
            return False
    return True

def player_input():
    """Gets the player's marker choice ('X' or 'O')."""
    marker = ''
    while not (marker == 'X' or marker == 'O'):
        marker = input('Player, choose X or O: ').upper()
    return ('X', 'O') if marker == 'X' else ('O', 'X')

def computer_choice(board):
    """Randomly chooses a position for the computer's move."""
    position = random.randint(1, 9)
    while not space_check(board, position):
        position = random.randint(1, 9)
    return position
# Tkinter setup
window = tk.Tk()
window.title("Tic-Tac-Toe")

board = [' '] * 9
player_marker, computer_marker = player_input()  # Get marker choices upfront

# Create button grid
buttons = []
for i in range(9):
    button = tk.Button(window, text=" ", font=('Arial', 20), width=3, height=1,
                       command=lambda pos=i+1: player_move(pos))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

game_on = True
turn = choose_first()
if turn == 'Computer':
    computer_move()  # Computer goes first if it won the toss

window.mainloop()