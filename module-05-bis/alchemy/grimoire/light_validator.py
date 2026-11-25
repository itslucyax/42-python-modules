def validate_ingredients(ingredients: str) -> str:
    # Late import: resolved when the function runs, not when the module
    # loads, so the spellbook <-> validator cycle never exists at import.
    from .light_spellbook import light_spell_allowed_ingredients

    cleaned = "".join(c if c.isalnum() else " " for c in ingredients.lower())
    words = cleaned.split()
    allowed = light_spell_allowed_ingredients()
    if any(word in allowed for word in words):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
