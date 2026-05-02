def greet(name: str) -> str:
    """Return a greeting message.
    
    Args:
        name: Name to greet
        
    Returns:
        Greeting message
    """
    return f"Hello, {name}! Welcome to Torro Agent Framework!"


if __name__ == "__main__":
    print(greet("World"))