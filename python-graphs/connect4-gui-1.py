import tkinter as tk
from tkinter import messagebox
import random

class Connect4:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect 4")
        self.window.geometry("600x400")
        self.player_turn = 'X'
        self.buttons = []
        for i in range(6):
            row = []
            for j in range(7):
                button = tk.Button(self.window, command=lambda row=i, column=j: self.click(row, column), height=3, width=6)
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset)
        self.reset_button.grid(row=6, column=0, columnspan=7)
        self.num_players = None
        self.ask_num_players()

    def ask_num_players(self):
        self.num_players = messagebox.askquestion("Number of Players", "Do you want to play against the computer?")

    def click(self, row, column):
        try:
            if self.buttons[0][column]['text'] == "":
                for i in range(5, -1, -1):
                    if self.buttons[i][column]['text'] == "":
                        self.buttons[i][column]['text'] = self.player_turn
                        if self.check_win():
                            self.highlight_winning_buttons()
                            self.window.after(1000, lambda: messagebox.showinfo("Game Over", f"Player {self.player_turn} wins!"))
                            self.window.after(2000, self.window.quit)
                        self.player_turn = 'O' if self.player_turn == 'X' else 'X'
                        break
                if self.num_players == 'yes':
                    self.computer_move()
            else:
                messagebox.showerror("Error", "Column is full. Please choose another column.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_win(self):
        try:
            for i in range(6):
                for j in range(7):
                    if self.buttons[i][j]['text'] != "":
                        if self.check_line(i, j, 1, 0) or self.check_line(i, j, 0, 1) or self.check_line(i, j, 1, 1) or self.check_line(i, j, 1, -1):
                            return True
            return False
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_line(self, row, column, row_dir, col_dir):
        try:
            player = self.buttons[row][column]['text']
            for i in range(1, 4):
                r = row + row_dir * i
                c = column + col_dir * i
                if r < 0 or r >= 6 or c < 0 or c >= 7 or self.buttons[r][c]['text'] != player:
                    return False
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset(self):
        try:
            self.player_turn = 'X'
            for row in self.buttons:
                for button in row:
                    button['text'] = ""
                    button['bg'] = 'SystemButtonFace'
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def computer_move(self):
        try:
            column = random.randint(0, 6)
            while self.buttons[0][column]['text'] != "":
                column = random.randint(0, 6)
            for i in range(5, -1, -1):
                if self.buttons[i][column]['text'] == "":
                    self.buttons[i][column]['text'] = 'O'
                    break
            self.player_turn = 'X'
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def highlight_winning_buttons(self):
        for i in range(6):
            for j in range(7):
                if self.buttons[i][j]['text'] != "":
                    if self.check_line(i, j, 1, 0) or self.check_line(i, j, 0, 1) or self.check_line(i, j, 1, 1) or self.check_line(i, j, 1, -1):
                        for k in range(4):
                            if self.check_line(i, j, 1, 0):
                                self.buttons[i+k][j]['bg'] = 'red'
                            elif self.check_line(i, j, 0, 1):
                                self.buttons[i][j+k]['bg'] = 'red'
                            elif self.check_line(i, j, 1, 1):
                                self.buttons[i+k][j+k]['bg'] = 'red'
                            elif self.check_line(i, j, 1, -1):
                                self.buttons[i+k][j-k]['bg'] = 'red'

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    game = Connect4()
    game.run()
