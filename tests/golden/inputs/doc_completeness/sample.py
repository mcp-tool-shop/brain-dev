# Golden test input: documentation completeness
# Mix of missing, incomplete, and complete docstrings.


def no_docs(x, y):
    return x + y


def short_doc(items):
    """Process items."""
    return [i * 2 for i in items]


def complete_doc(name, age):
    """Create a user profile.

    Args:
        name: The user's full name.
        age: The user's age in years.

    Returns:
        A dictionary containing the user profile.
    """
    return {"name": name, "age": age}


class UndocumentedClass:
    def __init__(self, value):
        self.value = value

    def transform(self, factor):
        return self.value * factor


def _private_helper(data):
    return sorted(data)
