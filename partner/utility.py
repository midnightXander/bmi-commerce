def generate_slug(text:str):
    """Generate a slug from the given text."""
    # Remove special characters and replace spaces with hyphens
    return text.strip().lower().replace(' ', '-').replace("'", '')