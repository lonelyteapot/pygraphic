import inflection


def default_alias_generator(name: str) -> str:
    return inflection.camelize(name, False)
