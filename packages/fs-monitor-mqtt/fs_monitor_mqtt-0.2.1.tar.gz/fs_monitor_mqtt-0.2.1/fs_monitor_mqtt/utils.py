import os


def resolve_absolute_path(path: str) -> str:
    """Resolves the given path to an absolute path.

    Args:
        path (str): The path to resolve.

    Returns:
        str: The absolute path if it exists and is accessible.

    Raises:
        FileNotFoundError: If the path does not exist.
        PermissionError: If there is no permission to access the path.
    """
    abs_path = os.path.abspath(path)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"The path {abs_path} does not exist.")

    if not os.access(abs_path, os.R_OK):
        raise PermissionError(f"No permission to access {abs_path}.")

    return abs_path
