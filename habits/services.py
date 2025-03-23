def make_replacements(text: str, replacements: dict) -> str:
    """Replaces vars in text with correct values."""
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text
