# Mathematical Expression Calculator AI Agent

This AI agent functions as a mathematical expression calculator. It is designed to parse, evaluate, and return the results of mathematical expressions.I can also enable to write ,update operations in the calculator file.This was done as part of my learning of AI agent course on boot.dev

AI model provider: Gemini
Model used: Gemini-2.5 Flash

## Features:
- **Expression Evaluation**: Capable of evaluating standard mathematical expressions.
- **Operator Precedence Handling**: Correctly processes expressions based on operator precedence (e.g., multiplication before addition).
- **Parentheses Support**: Handles nested parentheses for complex expressions.
- **Supported Operations**:
    - Addition (`+`)
    - Subtraction (`-`)
    - Multiplication (`*`)
    - Division (`/`)
    - Logarithm (`log`)
    - Exponential (`exp`)
- **JSON Output**: Provides results in a structured JSON format, including the original expression and the calculated result.

## How to Use:
The agent can be invoked with a mathematical expression as a command-line argument.
Example: `python main.py "3 + 5 * (10 - 2)"`
