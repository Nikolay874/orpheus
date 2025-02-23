from pygments.util import ClassNotFound
from pygments.lexers import guess_lexer


def get_code_language(text: str) -> str | None:
    try:
        lexer = guess_lexer(text)
        return lexer.name
    except ClassNotFound:
        return None
