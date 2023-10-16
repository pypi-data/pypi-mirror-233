try:
    from importlib.metadata import metadata  # type: ignore
except ModuleNotFoundError:
    from importlib_metadata import metadata  # type: ignore

__all__ = ["__program__", "__version__", "__description__"]

__metadata = metadata(__name__.split(".")[0])

__program__ = __metadata["Name"]
__version__ = __metadata["Version"]
__description__ = __metadata["Summary"]
