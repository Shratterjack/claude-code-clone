import unittest
import math

from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_logarithm(self):
        result = self.calculator.evaluate("log(2.718281828459045)") # close to math.e
        self.assertAlmostEqual(result, 1.0)
        result = self.calculator.evaluate("log(1)")
        self.assertAlmostEqual(result, 0.0)

    def test_exponential(self):
        result = self.calculator.evaluate("exp(0)")
        self.assertAlmostEqual(result, 1.0)
        result = self.calculator.evaluate("exp(1)")
        self.assertAlmostEqual(result, math.e)

    def test_parentheses(self):
        result = self.calculator.evaluate("(3 + 5) * 2")
        self.assertEqual(result, 16)
        result = self.calculator.evaluate("10 / (2 + 3)")
        self.assertEqual(result, 2)

    def test_combined_functions_and_operators(self):
        result = self.calculator.evaluate("log(exp(2)) + 3")
        self.assertAlmostEqual(result, 5.0)
        result = self.calculator.evaluate("exp(log(4)) * 2")
        self.assertAlmostEqual(result, 8.0)
        result = self.calculator.evaluate("1 + exp(0) * log(1)") # 1 + 1 * 0 = 1
        self.assertAlmostEqual(result, 1.0)


if __name__ == "__main__":
    unittest.main()
