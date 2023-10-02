class AmbiguityError(Exception):
    """Raised when multiple files match a key."""


class InvalidSelfError(Exception):
    """Raised when the contents of `__self__.*` is invalid."""


class MultipleSelfError(Exception):
    """Raised when multiple `__self__.*` files exist."""
