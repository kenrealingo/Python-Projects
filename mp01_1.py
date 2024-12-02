#Franciesca dela Cruz & Ken Realingo
#ES26 Machine Problem 1 - Mastermind

# Import necessary libraries
import random
import tkinter as tk
from tkinter import messagebox

# Function to create a random code
def make_secret_code(colors, length):
    """
    Creat a random secret code.
    
    Args:
    colors (int): Number of possible color
    length (int): Lenght of the code
    
    Returns:
    list: A list of random number represent the secret code
    """
    secret_code = []
    for i in range(length):
        secret_code.append(str(random.randint(1, colors)))
    return secret_code

# Function to check the guess and give feedback
def check_guess(player_guess, secret_code):
    """
    Compare the player guess with the secret code and provide feedback.
    
    Args:
    player_guess (list): The player gues
    secret_code (list): The secret code to be guess
    
    Returns:
    tuple: number of corect colors in correct position (black_pegs) and
           number of correct colors in worng position (white_pegs)
    """
    black_pegs = 0
    white_pegs = 0
    
    code_copy = secret_code.copy()
    guess_copy = player_guess.copy()
    
    # Check for correct colors in correct positions
    for i in range(len(guess_copy)):
        if guess_copy[i] == code_copy[i]:
            black_pegs += 1
            guess_copy[i] = 'X'
            code_copy[i] = 'O'
    
    # Check for correct colors in wrong positions
    for i in range(len(guess_copy)):
        if guess_copy[i] != 'X' and guess_copy[i] in code_copy:
            white_pegs += 1
            code_copy[code_copy.index(guess_copy[i])] = 'O'
    
    return black_pegs, white_pegs

def start_game(difficulty):
    if difficulty == "Easy":
        num_colors = 6
        code_length = 4
    elif difficulty == "Medium":
        num_colors = 7
        code_length = 5
    else:  # Hard
        num_colors = 8
        code_length = 6

    max_attempts = 12
    code = make_secret_code(num_colors, code_length)
    game_window(difficulty, code, max_attempts, num_colors, code_length)

def game_window(difficulty, code, max_attempts, num_colors, code_length):
    attempts = 0
    previous_attempts = []

    def check_guess_action(event=None):
        nonlocal attempts
        guess = entry.get()

        if len(guess) != code_length or not guess.isdigit() or not all('1' <= digit <= str(num_colors) for digit in guess):
            messagebox.showerror("Invalid Input!", f"Enter {code_length} digits from 1 to {num_colors}.")
            return

        attempts += 1
        guess_list = list(guess)
        black_pegs, white_pegs = check_guess(guess_list, code.copy())

        feedback.set(f"Feedback: {black_pegs}B - {white_pegs}W")
        attempts_label.set(f"Attempts: {attempts}/{max_attempts}")
        
        previous_attempts.append(f"{guess} => {black_pegs}B - {white_pegs}W")
        previous_guesses.set("\n".join(previous_attempts))
        
        entry.delete(0, tk.END)

        if black_pegs == code_length:
            messagebox.showinfo("Congrats!", f"You guessed it in {attempts} attempts!")
            window.destroy()  # Close the game window
            difficulty_selection()  # Show difficulty selection again
        elif attempts >= max_attempts:
            messagebox.showinfo("Game Over", f"Out of guesses! The code was {''.join(code)}.")
            window.destroy()  # Close the game window
            difficulty_selection()  # Show difficulty selection again

    window = tk.Tk()
    window.title("Mastermind")

    tk.Label(window, text=f"Difficulty: {difficulty}").pack()
    tk.Label(window, text=f"Guess the {code_length}-digit code using numbers 1 to {num_colors}.").pack()

    entry = tk.Entry(window)
    entry.pack()
    entry.focus()  # Set focus to the entry widget
    entry.bind('<Return>', check_guess_action)  # Bind Enter key to check_guess_action

    feedback = tk.StringVar()
    tk.Label(window, textvariable=feedback).pack()

    attempts_label = tk.StringVar(value=f"Attempts: {attempts}/{max_attempts}")
    tk.Label(window, textvariable=attempts_label).pack()

    previous_guesses = tk.StringVar()
    tk.Label(window, text="Previous Attempts:").pack()
    tk.Label(window, textvariable=previous_guesses).pack()

    tk.Button(window, text="Submit", command=check_guess_action).pack()
    window.mainloop()

def difficulty_selection():
    diff_window = tk.Tk()
    diff_window.title("Select Difficulty")

    tk.Label(diff_window, text="Choose difficulty:").pack()
    tk.Button(diff_window, text="Easy", command=lambda: [diff_window.destroy(), start_game("Easy")]).pack()
    tk.Button(diff_window, text="Medium", command=lambda: [diff_window.destroy(), start_game("Medium")]).pack()
    tk.Button(diff_window, text="Hard", command=lambda: [diff_window.destroy(), start_game("Hard")]).pack()

    diff_window.mainloop()

# Main game function
def mastermind():
    """
    Main funcion to start the Mastermind game.
    """
    difficulty_selection()

# Start the game if this script is run directly
if __name__ == "__main__":
    mastermind()
