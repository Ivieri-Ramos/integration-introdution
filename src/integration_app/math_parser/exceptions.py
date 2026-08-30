class MathParserError(Exception):
    """
    Base exception from which all math parser errors inherit.
    """
    pass


class MathSyntaxError(MathParserError):
    """
    Raised when a syntax error is encountered in the expression.

    Examples of syntax error:
    - "x + 1 @ 3" (The '@' is not a valid operator)
    - "coss(x)" (The 'coss' is not a valid function)

    Example of valid syntax:
    - "x + 1 * 3" (All operators are valid).

    Args:
        message (str): The error message.
        context (str): The string context surrounding the error.
    """

    def __init__(self, message: str, context: str):
        super().__init__(message)

        self.message = message
        self.context = context

    def __str__(self):
        return (f"{self.message}\n"
                f"{self.context}\n")


class IncompleteExpressionError(MathParserError):
    """
    Raised when an expression is incomplete, such as having unclosed parentheses.

    Example of an incomplete expression:
    - "1 + 3 * (x * 1" (Missing a closing parenthesis ')' at the end)

    Example of a complete expression:
    - "1 + 3 * (x * 1)" (The parentheses are properly closed).

    Args:
        message (str): The error message.
        context (str): The string context surrounding the error.
    """

    def __init__(self, message: str, context: str):
        super().__init__(message)

        self.message = message
        self.context = context

    def __str__(self):
        return (f"{self.message}\n"
                f"{self.context}\n")


class MathSemanticError(MathParserError):
    """
    Raised when a semantic error is encountered.

    Examples of semantics errors:
    - "1 2 + 3" (Missing an operator between '1 2')
    - "x3" (For implicit multiplication, the variable must come after the number, e.g., '3x')

    Example of valid semantic:
    - "1 + 3 * 2" (Operators correctly separate distinct constants)

    Args:
        message (str): The error message.
        context (str): The string context surrounding the error.
    """

    def __init__(self, message: str, context: str):
        super().__init__(message)

        self.message = message
        self.context = context

    def __str__(self):
        return (f"{self.message}\n"
                f"{self.context}\n")


class MultipleVariablesDefinedError(MathParserError):
    """
    Raised when the expression contains two or more distinct variables.

    Example:
    - "x * y" (Contains both 'x' and 'y', which is not allowed since the integrals are one-dimensional).
    """
    pass
