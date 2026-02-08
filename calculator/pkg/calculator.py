import math
import re


class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "log": math.log,
            "exp": math.exp,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "log": 3,
            "exp": 3,
            "(": 0,
        }

    def _tokenize(self, expression):
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            if char in "()+-*/":
                tokens.append(char)
                i += 1
            elif char.isalpha():
                j = i
                while j < len(expression) and expression[j].isalpha():
                    j += 1
                word = expression[i:j]
                if word in ["log", "exp"]:
                    tokens.append(word)
                    i = j
                else:
                    raise ValueError(f"Unknown function or variable: {word}")
            elif char.isdigit() or (
                char == "." and i + 1 < len(expression) and expression[i + 1].isdigit()
            ):  # Handle leading '.'
                j = i
                while j < len(expression) and (
                    expression[j].isdigit() or expression[j] == "."
                ):
                    j += 1
                tokens.append(expression[i:j])
                i = j
            else:
                raise ValueError(f"Invalid character: {char}")
        return tokens

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if not operators:
                    raise ValueError("Mismatched parentheses")
                operators.pop()  # Pop the '('
            elif token in self.operators:
                while (
                    operators
                    and operators[-1] != "("
                    and self.precedence.get(operators[-1], 0) >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:  # Must be a number
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")

        while operators:
            if operators[-1] == "(":
                raise ValueError("Mismatched parentheses")
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()

        if operator in ["log", "exp"]:
            if len(values) < 1:
                raise ValueError(f"Not enough operands for unary operator {operator}")
            a = values.pop()
            values.append(self.operators[operator](a))
        else:  # Binary operators
            if len(values) < 2:
                raise ValueError(f"Not enough operands for operator {operator}")
            b = values.pop()
            a = values.pop()
            values.append(self.operators[operator](a, b))
