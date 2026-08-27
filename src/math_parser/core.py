from typing import cast

import sympy as sp
from lark import Lark, UnexpectedToken, UnexpectedCharacters, UnexpectedEOF

from .exceptions import *
from .transformer import ExpressionTransformer

_parser = Lark.open(
    "grammar.lark",
    rel_to=__file__,
    parser="lalr",
    transformer=ExpressionTransformer(),
)


def parse_math(expression: str) -> sp.Expr:
    """
    Parses a string and returns a SymPy expression, or raises an `MathParserError`.

    Args:
         expression (str): The string to parse.

    Returns:
        sp.Expr: The parsed expression.

    Raises:
        MultipleVariablesDefinedError: If more than one variable is defined.
        MathSyntaxError: If an invalid operator is encountered, e.g. "@".
        MathSemanticError: MathSemanticError
    """
    try:
        parser_result = _parser.parse(expression)

        expression: sp.Expr = cast(sp.Expr, cast(object, parser_result))

        variables: set[sp.Basic] = expression.free_symbols

        if len(variables) > 1:
            raise MultipleVariablesDefinedError(
                f"[Multiple Variables Error] There are more than one variable defined, which is not "
                "allowed since the integrals must be evaluated in "
                f"one dimension. Variables used: {expression.free_symbols}")

        return expression

    except UnexpectedCharacters as e:
        raise MathSyntaxError(
            "[Syntax Error] There is an invalid operator or function:",
            e.get_context(str(expression)))

    except UnexpectedToken as e:
        raise MathSemanticError(
            f"[Semantic Error] There is an incorrect math order, "
            f"like missing operators between values or incomplete functions:",
            e.get_context(str(expression)))

    except UnexpectedEOF as e:
        raise IncompleteExpressionError(
            f"[Incomplete Expression Error] There is an incomplete expression, "
            f"probably missing opening or closing parenthesis:",
            e.get_context(str(expression))
        )

    except ValueError as e:
        raise MathParserError(f"[Generic Error]: {e}")
