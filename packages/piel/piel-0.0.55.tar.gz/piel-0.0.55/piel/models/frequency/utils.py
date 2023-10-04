from .defaults import get_default_models

__all__ = [
    "compose_custom_model_library_from_defaults",
]


def compose_custom_model_library_from_defaults(custom_models: dict) -> dict:
    """
    Compose the default models with the custom models.

    Args:
        custom_models (dict): Custom models dictionary.

    Returns:
        dict: Composed models dictionary.
    """
    return {**get_default_models(), **custom_models}


def check_is_unitary(model: dict) -> bool:
    """
    Check if the model is unitary.

    Args:
        model (dict): Model dictionary.

    Returns:
        bool: True if unitary, False if not.
    """
    # TODO
    pass
