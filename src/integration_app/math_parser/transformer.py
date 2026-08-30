from typing import Callable

import sympy as sp
from lark import Transformer, v_args, Token

_ALIAS_FUNCTION_MAP: dict[tuple[str, ...], Callable[[sp.Expr], sp.Expr]] = {
    ("sin", "sen"): sp.sin,
    ("asin", "asen", "arcsin", "arcsen"): sp.asin,
    ("sec",): sp.sec,

    ("cos",): sp.cos,
    ("acos", "arccos"): sp.acos,
    ("csc",): sp.csc,

    ("tan",): sp.tan,
    ("atan",): sp.atan,
    ("cot",): sp.cot,

    ("log", "ln"): sp.log,
    ("exp",): sp.exp,
    ("sqrt", "raiz"): sp.sqrt,

    ("abs",): sp.Abs,
}
""" Contains all the mathematical functions that can be evaluated. """

functions_dict: dict[str, Callable[[sp.Expr], sp.Expr]] = {
    alias: func
    for aliases, func in _ALIAS_FUNCTION_MAP.items()
    for alias in aliases
}
""" Verify if the input is in `_ALIAS_FUNCTION_MAP`. """

_ALIAS_CONSTANT_MAP: dict[tuple[str, ...], sp.Expr] = {
    ("pi", "PI", "Pi", "pI"): sp.pi,
    ("e", "E"): sp.E,
}
""" Contains all the mathematical constants that can be evaluated. """

constants_dict: dict[str, sp.Expr] = {
    alias: expression
    for aliases, expression in _ALIAS_CONSTANT_MAP.items()
    for alias in aliases
}
""" Verify if the input is in `_ALIAS_CONSTANT_MAP`. """


@v_args(inline=True)
class ExpressionTransformer(Transformer):
    def addition(self, a: sp.Expr, b: sp.Expr) -> sp.Expr:
        """
        Returns the addition between two expressions preserving the symbolic form.

        Args:
            a (sp.Expr): First expression.
            b (sp.Expr): Second expression.

        Returns:
            sp.Expr: The result of the addition.
        """
        return a + b

    def subtraction(self, a: sp.Expr, b: sp.Expr) -> sp.Expr:
        """
        Returns the subtraction between two expressions preserving the symbolic form.

        Args:
            a (sp.Expr): First expression.
            b (sp.Expr): Second expression.

        Returns:
            sp.Expr: The result of the subtraction.
        """
        return a - b

    def multiplication(self, a: sp.Expr, b: sp.Expr) -> sp.Expr:
        """
        Returns the multiplication between two expressions preserving the symbolic form.

        Args:
            a (sp.Expr): First expression.
            b (sp.Expr): Second expression.

        Returns:
            sp.Expr: The result of the multiplication.
        """
        return a * b

    def division(self, a: sp.Expr, b: sp.Expr) -> sp.Expr:
        """
        Returns the division between two expressions preserving the symbolic form.

        Args:
            a (sp.Expr): First expression.
            b (sp.Expr): Second expression.

        Returns:
            sp.Expr: The result of the division.
        """
        return a / b

    def positive(self, a: sp.Expr) -> sp.Expr:
        """
        Preserves the sign of the expression itself, in cases like "+x" == "x"

        Args:
            a (sp.Expr): The expression.

        Returns:
            sp.Expr: The expression itself.
        """
        return a

    def negative(self, a: sp.Expr) -> sp.Expr:
        """
        Inverts the sign of the expression.

        Args:
            a (sp.Expr): The expression.

        Returns:
            sp.Expr: The expression with inverted sign.
        """
        return -a

    def power(self, a: sp.Expr, b: sp.Expr) -> sp.Expr:
        """
        Return the power between `a` and `b`, i.e. "a ^ b".

        Args:
            a (sp.Expr): The basis expression
            b (sp.Expr): The exponent.

        Returns:
            sp.Expr: The expression powered "a ^ b".
        """
        return a ** b

    def function_call(self, token: Token, value: sp.Expr) -> sp.Expr:
        """
        Verify if the `token.value` is a function presents in `_ALIAS_FUNCTION_MAP`,
        if so, returns the correspondent function. Otherwise, verify if
        the `token.value` is an implicit multiplication, like "ex(x - 1)", which
        returns "e * x * (x - 1)".

        Args:
            token (Token): The token to verify.
            value (sp.Expr): The expression inside the parentheses.

        Returns:
            sp.Expr: The expression which can be a function or an implicit multiplication expression.
        """
        function_name: str = token.value

        if function_name in functions_dict:
            return functions_dict[function_name](value)

        implicit_expr: sp.Expr = self.identifier(token)
        return implicit_expr * value

    def function_power_call(self, token: Token, power: sp.Expr, value: sp.Expr) -> sp.Expr:
        """
        Verify if the `token.value` is a function presents in `_ALIAS_FUNCTION_MAP`,
        if so, returns the correspondent function powered by `power`. Otherwise, verify if
        the `token.value` is an implicit multiplication, like "sen**2(x)", which
        returns "(sen ** 2) * (x)", the same as "sen^2(x)".

        Args:
            token (Token): The token to verify.
            power (sp.Expr): The value to power the function or expression.
            value (sp.Expr): The expression inside the parentheses.

        Returns:
            sp.Expr: The expression which can be a function or an implicit multiplication expression,
                powered by `power`.
        """
        function_name: str = token.value

        if function_name in functions_dict:
            return functions_dict[function_name](value) ** power

        implicit_expr: sp.Expr = self.identifier(token)
        return (implicit_expr ** power) * value

    def identifier(self, token: Token) -> sp.Expr:
        """
        Verify if the `token.value` is a constant presents in `_ALIAS_CONSTANT_MAP`,
        if so, returns the correspondent constant. Otherwise, verify if it has the
        length of a valid variable, which is one. If not of these statements occurs,
        this function verifies if the `token.value` is an expression with implicit
        multiplication, like "expi", which corresponds to "e * x * pi".

        Args:
            token (Token): The token to verify.

        Returns:
            sp.Expr: The expression which can be a constant, a variable, or an implicit expression.
        """
        name: str = token.value

        if name in constants_dict:
            return constants_dict[name]

        if len(name) == 1:
            return sp.Symbol(name)

        # Below this line, the code only will happen in cases like x(x - 1) or ex(x - 1)
        result: sp.Expr = sp.Rational(1)
        i: int = 0

        while i < len(name):
            if name[i: i + 2].lower() == "pi":
                result *= sp.pi
                i += 2
            else:
                char: str = name[i]

                if char in constants_dict:
                    result *= constants_dict[char]
                else:
                    result *= sp.Symbol(char)

                i += 1

        return result

    def number(self, token: Token) -> sp.Expr:
        """
        Returns any number preserving its symbolic form, e.g., "0.5" corresponds
        to "1/2", and not `0.500000000...`, the `float` which not guarantees mathematical
        precision.

        Args:
            token (Token): The token to cast.

        Returns:
            sp.Expr: The symbolic form of the number.
        """
        return sp.Rational(token.value)
