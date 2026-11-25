from .dark_spellbook import dark_spell_allowed_ingredients


def dark_validate_ingredients(ingredients: str) -> str:
    cleaned = "".join(c if c.isalnum() else " " for c in ingredients.lower())
    allowed = dark_spell_allowed_ingredients()
    if any(word in allowed for word in cleaned.split()):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
