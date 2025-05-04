def generate_slug(text:str):
    """Generate a slug from the given text."""
    return text.lower().replace(' ', '-').replace("'", '')