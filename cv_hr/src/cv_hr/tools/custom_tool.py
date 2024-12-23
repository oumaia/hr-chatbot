def format_suggestions(suggestions):
    """Format suggestions as a bullet-point list."""
    return "\n".join(f"- {suggestion}" for suggestion in suggestions)
