# Golden test input: complexity scoring
# Range of function complexities from trivial to deeply nested.


def trivial(x):
    """Complexity 1 — should NOT trigger (below threshold)."""
    return x + 1


def moderate(items, threshold):
    """Complexity 4 — if/for/if — should NOT trigger (below 5)."""
    result = []
    if items:
        for item in items:
            if item > threshold:
                result.append(item)
    return result


def complex_handler(request, db, cache):
    """Complexity 8+ — should trigger refactor suggestion."""
    if not request:
        return None
    if request.method == "GET":
        for key in request.params:
            if key in cache:
                return cache[key]
            else:
                try:
                    result = db.query(key)
                except Exception:
                    return None
    elif request.method == "POST":
        for field in request.body:
            if not field:
                raise ValueError("empty field")
    return "ok"


def deeply_nested(matrix, filters, validators):
    """Complexity 10+ — heavy nesting, comprehensions, boolean ops."""
    results = []
    if matrix and filters:
        for row in matrix:
            for col in row:
                if col > 0 and col < 100:
                    for f in filters:
                        if f(col):
                            try:
                                validated = [v(col) for v in validators]
                                results.extend(validated)
                            except ValueError:
                                pass
    return results
