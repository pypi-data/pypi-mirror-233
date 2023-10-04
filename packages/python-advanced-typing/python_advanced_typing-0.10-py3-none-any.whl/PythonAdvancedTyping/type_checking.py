def check_individual_type(variable: any, variable_name: str, expected_type_or_types: type | tuple[type]) -> None:
    """
        Check the type of a given variable against the expected type or types.

        Parameters:
        - variable (any): The variable to be checked.
        - variable_name (str): The name of the variable (for error messaging purposes).
        - expected_type_or_types (type or tuple of types): The expected type or a tuple of expected types for the
        variable.

        Raises:
        - TypeError: If the variable type does not match the expected type or types.
        """
    if not isinstance(variable_name, str):
        raise TypeError(f"Expected type str for variable_name. Instead got {type(variable_name)}.")
    if isinstance(expected_type_or_types, type):
        pass
    elif isinstance(expected_type_or_types, tuple):
        for item in expected_type_or_types:
            check_individual_type(item, "expected_type_or_types_item", type)
    else:
        raise TypeError(
            f"Expected type str or tuple for expected_type_or_types. Instead got {type(expected_type_or_types)}."
        )
    if not isinstance(variable, expected_type_or_types):
        raise TypeError(f"Expected type {expected_type_or_types} for {variable_name}. Instead got {type(variable)}.")


def check_type(*args) -> None:
    """
    Check the type of a variable against the expected type or types, or perform multiple checks in a list.

    Usage:
    - check_type(variable, variable_name, expected_type_or_types)
    - check_type((variable1, variable_name1, expected_type_or_types1),
    (variable2, variable_name2, expected_type_or_types2), ...)

    Raises:
    - ValueError: If improper inputs are provided.
    - TypeError: If the variable type does not match the expected type or types.
    """

    if not args:
        raise ValueError("No arguments provided to check_type.")

    if len(args) == 3 and isinstance(args[1], str) and (isinstance(args[2], type) or isinstance(args[2], tuple)):
        var, var_name, expected = args
        check_individual_type(var, var_name, expected)
        return

    for arg in args:
        if not isinstance(arg, tuple) or len(arg) != 3:
            raise ValueError("Invalid input format for check_type.")
        var, var_name, expected = arg
        if not (isinstance(var_name, str) and (isinstance(expected, type) or isinstance(expected, tuple))):
            raise ValueError("Invalid input format for check_type.")
        check_individual_type(var, var_name, expected)
