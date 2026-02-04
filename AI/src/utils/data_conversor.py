def to_python_type(x):
    if hasattr(x, "item"):
        return x.item()
    return x