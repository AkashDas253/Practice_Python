import tkinter as tk
from tkinter import messagebox
import math

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("400x520")
        self.resizable(False, False)
        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        self.display = tk.Entry(self, font=("Arial", 20), bd=10, relief=tk.RIDGE, justify='right', state='readonly')
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")
        buttons = [
            ('C', 1, 0), ('(', 1, 1), (')', 1, 2), ('/', 1, 3), ('⌫', 1, 4),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3), ('^', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3), ('√', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3), ('log', 4, 4),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('sin', 5, 3), ('cos', 5, 4),
            ('tan', 6, 0), ('exp', 6, 1), ('π', 6, 2), ('e', 6, 3), ('abs', 6, 4)
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
        for i in range(7):
            self.grid_rowconfigure(i, weight=1, minsize=60)
        for i in range(5):
            self.grid_columnconfigure(i, weight=1, minsize=80)

    def on_click(self, char):
        sci_funcs = {
            '√': 'math.sqrt(',
            'log': 'math.log10(',
            'sin': 'math.sin(',
            'cos': 'math.cos(',
            'tan': 'math.tan(',
            'exp': 'math.exp(',
            'abs': 'abs(',
            'π': 'math.pi',
            'e': 'math.e',
            '^': '**'
        }
        if char in sci_funcs:
            if char in ['π', 'e', '^']:
                self.expression += sci_funcs[char]
            else:
                self.expression += sci_funcs[char]
        elif char in '+-*/.':
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
        elif char == '(':  # Opening bracket
            if not self.expression or self.expression[-1] in '+-*/(':
                self.expression += char
            else:
                return
        elif char == ')':  # Closing bracket
            if self.expression.count('(') > self.expression.count(')') and (self.expression and self.expression[-1] not in '+-*/('):
                self.expression += char
            else:
                return
        else:
            self.expression += str(char)
        # Display-friendly expression
        display_expr = self.expression.replace('math.sqrt(', '√(')
        display_expr = display_expr.replace('math.log10(', 'log(')
        display_expr = display_expr.replace('math.sin(', 'sin(')
        display_expr = display_expr.replace('math.cos(', 'cos(')
        display_expr = display_expr.replace('math.tan(', 'tan(')
        display_expr = display_expr.replace('math.exp(', 'exp(')
        display_expr = display_expr.replace('math.pi', 'π')
        display_expr = display_expr.replace('math.e', 'e')
        # Show abs(x) as abs(x) in display
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, display_expr)
        self.display.config(state='readonly')

    def clear(self):
        self.expression = ""
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.config(state='readonly')

    def backspace(self):
        if self.expression:
            # Remove function and opening parenthesis together if present at the end
            func_starts = [
                'math.sqrt(',
                'math.log10(',
                'math.sin(',
                'math.cos(',
                'math.tan(',
                'math.exp(',
                'abs('
            ]
            for start in func_starts:
                if self.expression.endswith(start):
                    self.expression = self.expression[:-len(start)]
                    break
            else:
                self.expression = self.expression[:-1]
        display_expr = self.expression.replace('math.sqrt(', '√(')
        display_expr = display_expr.replace('math.log10(', 'log(')
        display_expr = display_expr.replace('math.sin(', 'sin(')
        display_expr = display_expr.replace('math.cos(', 'cos(')
        display_expr = display_expr.replace('math.tan(', 'tan(')
        display_expr = display_expr.replace('math.exp(', 'exp(')
        display_expr = display_expr.replace('math.pi', 'π')
        display_expr = display_expr.replace('math.e', 'e')
        # Show abs(x) as abs(x) in display
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, display_expr)
        self.display.config(state='readonly')

    def calculate(self):
        if self.expression.count('(') != self.expression.count(')'):
            messagebox.showerror("Error", "Unbalanced brackets")
            return
        if self.expression and self.expression[-1] in '+-*/.':
            messagebox.showerror("Error", "Expression cannot end with operator or decimal")
            return
        try:
            result = str(eval(self.expression, {"math": math, "abs": abs}))
            # Display-friendly result
            display_result = result.replace('math.sqrt(', '√(')
            display_result = display_result.replace('math.log10(', 'log(')
            display_result = display_result.replace('math.sin(', 'sin(')
            display_result = display_result.replace('math.cos(', 'cos(')
            display_result = display_result.replace('math.tan(', 'tan(')
            display_result = display_result.replace('math.exp(', 'exp(')
            display_result = display_result.replace('math.pi', 'π')
            display_result = display_result.replace('math.e', 'e')
            # Show abs(x) as abs(x) in display
            self.display.config(state='normal')
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, display_result)
            self.display.config(state='readonly')
            self.expression = result
        except Exception:
            messagebox.showerror("Error", "Invalid Expression\n(try using parentheses for function arguments)")
            self.clear()

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
