_mapping: dict[type, str] = {
    int: "Int",
    float: "Float",
    str: "String",
    bool: "Boolean",
}


def register_graphql_type(graphql_type: str, python_class: type) -> None:
    _mapping[python_class] = graphql_type


def class_to_graphql_type(python_class: type, allow_none: bool) -> str:
    try:
        type_ = _mapping[python_class]
        if allow_none:
            return type_
        else:
            return type_ + "!"
    except KeyError:
        raise KeyError(
            f"Type '{python_class.__name__}' could not be converted to a GraphQL type."
            "See pygraphic.types.register_graphql_type"
        )
