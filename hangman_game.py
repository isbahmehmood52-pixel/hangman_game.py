import random
import tkinter as tk
from tkinter import messagebox

# Word list categories
WORDS = ["PYTHON", "DEVELOPER", "ALGORITHM", "VARIABLE", "FUNCTION", "SYNTAX", "DEBUGGING", "FRAMEWORK"]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game - Desktop App")
        self.root.geometry("600x650")
        self.root.config(bg="#1e1e2f")
        self.root.resizable(False, False)

        self.secret_word = ""
        self.guessed_letters = set()
        self.lives = 6

        # Title Label
        self.title_label = tk.Label(root, text="HANGMAN GAME", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="#00ffcc")
        self.title_label.pack(pady=15)

        # Canvas for Hangman Drawing
        self.canvas = tk.Canvas(root, width=200, height=200, bg="#2d2d44", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.draw_gallows()

        # Word Display Label
        self.word_label = tk.Label(root, text="", font=("Courier New", 28, "bold"), bg="#1e1e2f", fg="#ffffff")
        self.word_label.pack(pady=20)

        # Lives Status Label
        self.lives_label = tk.Label(root, text="", font=("Arial", 14), bg="#1e1e2f", fg="#ff5555")
        self.lives_label.pack(pady=5)

        # Keyboard Buttons Frame
        self.btn_frame = tk.Frame(root, bg="#1e1e2f")
        self.btn_frame.pack(pady=15)

        self.letter_buttons = {}
        self.create_keyboard()

        # Restart / Play Again Button
        self.restart_btn = tk.Button(root, text="New Game", font=("Arial", 12, "bold"), bg="#00ffcc", fg="#1e1e2f", 
                                     activebackground="#00cca3", relief="flat", padx=15, pady=5, command=self.reset_game)
        self.restart_btn.pack(pady=15)

        # Start the first game
        self.reset_game()

    def draw_gallows(self):
        self.canvas.delete("drawing")
        # Base and pole
        self.canvas.create_line(40, 180, 160, 180, width=4, fill="#ffffff", tags="drawing")
        self.canvas.create_line(70, 20, 70, 180, width=4, fill="#ffffff", tags="drawing")
        self.canvas.create_line(70, 20, 130, 20, width=4, fill="#ffffff", tags="drawing")
        self.canvas.create_line(130, 20, 130, 50, width=4, fill="#ffffff", tags="drawing")

    def draw_hangman(self, lives_left):
        # Depending on lives left (6 down to 0), draw parts
        if lives_left == 5:
            # Head
            self.canvas.create_oval(115, 50, 145, 80, width=3, outline="#ff5555", tags="drawing")
        elif lives_left == 4:
            # Torso
            self.canvas.create_line(130, 80, 130, 130, width=3, fill="#ff5555", tags="drawing")
        elif lives_left == 3:
            # Left Arm
            self.canvas.create_line(130, 95, 105, 115, width=3, fill="#ff5555", tags="drawing")
        elif lives_left == 2:
            # Right Arm
            self.canvas.create_line(130, 95, 155, 115, width=3, fill="#ff5555", tags="drawing")
        elif lives_left == 1:
            # Left Leg
            self.canvas.create_line(130, 130, 110, 165, width=3, fill="#ff5555", tags="drawing")
        elif lives_left == 0:
            # Right Leg (Game Over)
            self.canvas.create_line(130, 130, 150, 165, width=3, fill="#ff5555", tags="drawing")

    def create_keyboard(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        row, col = 0, 0
        for letter in alphabet:
            btn = tk.Button(self.btn_frame, text=letter, font=("Arial", 11, "bold"), width=3, height=1,
                            bg="#3d3d5c", fg="#ffffff", activebackground="#5c5c8a", activeforeground="#ffffff",
                            relief="flat", command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.letter_buttons[letter] = btn
            col += 1
            if col > 6:  # 7 buttons per row
                col = 0
                row += 1

    def guess_letter(self, letter):
        self.guessed_letters.add(letter)
        self.letter_buttons[letter].config(state="disabled", bg="#2a2a3d", fg="#666666")

        if letter in self.secret_word:
            # Correct guess
            self.update_word_display()
            if all(l in self.guessed_letters for l in self.secret_word):
                self.end_game(won=True)
        else:
            # Incorrect guess
            self.lives -= 1
            self.draw_hangman(self.lives)
            self.update_lives_display()
            if self.lives == 0:
                self.end_game(won=False)

    def update_word_display(self):
        display_text = " ".join([l if l in self.guessed_letters else "_" for l in self.secret_word])
        self.word_label.config(text=display_text)

    def update_lives_display(self):
        self.lives_label.config(text=f"Lives Remaining: {'❤️ ' * self.lives}")

    def reset_game(self):
        self.secret_word = random.choice(WORDS)
        self.guessed_letters = set()
        self.lives = 6

        self.draw_gallows()
        self.update_word_display()
        self.update_lives_display()

        # Re-enable all keyboard buttons
        for btn in self.letter_buttons.values():
            btn.config(state="normal", bg="#3d3d5c", fg="#ffffff")

    def end_game(self, won):
        # Disable all buttons
        for btn in self.letter_buttons.values():
            btn.config(state="disabled")

        if won:
            messagebox.showinfo("You Win! 🎉", f"Awesome! You guessed the word: {self.secret_word}")
        else:
            messagebox.showerror("Game Over 😢", f"You ran out of lives! The word was: {self.secret_word}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()