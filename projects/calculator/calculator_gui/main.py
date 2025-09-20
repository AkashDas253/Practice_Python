import tkinter as tk
from tkinter import messagebox

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("340x420")
        self.resizable(False, False)
        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        self.display = tk.Entry(self, font=("Arial", 20), bd=10, relief=tk.RIDGE, justify='right', state='readonly')
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        buttons = [
            ('C', 1, 0), ('(', 1, 1), (')', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('⌫', 5, 3)
        ]
        for (text, row, col) in buttons:
            if text == 'C':
                btn = tk.Button(self, text=text, font=("Arial", 16), command=self.clear)
            elif text == '=':
                btn = tk.Button(self, text=text, font=("Arial", 16), command=self.calculate)
            elif text == '⌫':
                btn = tk.Button(self, text=text, font=("Arial", 16), command=self.backspace)
            else:
                btn = tk.Button(self, text=text, font=("Arial", 16), command=lambda t=text: self.on_click(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1, minsize=60)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1, minsize=80)

    def backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)
        self.display.config(state='readonly')

    def on_click(self, char):
        brackets = {'(': ')'}
        closing = {')'}
        opening = {'('}
        if char in '+-*/.':
            # Prevent consecutive operators or decimals
            if not self.expression:
                if char == '-':
                    self.expression += char
                else:
                    return
            elif self.expression[-1] in '+-*/.':
                return
            elif char == '.' and any(op in self.expression.split('+')[-1].split('-')[-1].split('*')[-1].split('/')[-1] for op in ['.']):
                return
            else:
                self.expression += char
        elif char in opening:
            if not self.expression or self.expression[-1] in '+-*/(' or self.expression[-1] in opening:
                self.expression += char
            else:
                return
        elif char in closing:
            # Only add if there is an unmatched opening bracket
            if self.expression.count('(') > self.expression.count(')') and (self.expression and self.expression[-1] not in '+-*/(' and self.expression[-1] not in opening):
                self.expression += char
            else:
                return
        else:
            self.expression += str(char)
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)
        self.display.config(state='readonly')

    def clear(self):
        self.expression = ""
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.config(state='readonly')

    def calculate(self):
        # Safeguard: prevent evaluation if brackets are not balanced
        if self.expression.count('(') != self.expression.count(')'):
            messagebox.showerror("Error", "Unbalanced brackets")
            return
        # Safeguard: prevent ending with operator
        if self.expression and self.expression[-1] in '+-*/.':
            messagebox.showerror("Error", "Expression cannot end with operator or decimal")
            return
        try:
            result = str(eval(self.expression))
            self.display.config(state='normal')
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
            self.display.config(state='readonly')
            self.expression = result
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.clear()

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
