import localeet


def get_version() -> str:
    """Print and return local version of localeet"""
    print(localeet.__version__)
    return localeet.__version__
