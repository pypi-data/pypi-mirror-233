from contextlib import contextmanager
import json
import logging
import os
from pathlib import Path
import time
from typing import Generator, IO, Union

from .util import DEFAULT_LOGGER, get_user_cache_dir, rm_f

__all__ = [
    "Cache",
    "DEFAULT_LOCK_TIMEOUT",
    "LOCK_SLEEP_INTERVAL",
    "MAIN_CACHE_KEYS",
]

DEFAULT_LOCK_TIMEOUT = 0.5  # seconds
LOCK_SLEEP_INTERVAL = 0.01  # seconds
MAIN_CACHE_KEYS = {"download", "output"}


class Cache:
    """A cache class to store persistent data."""

    cache_dir: Path
    data: dict

    def __init__(
        self,
        cache_dir: Union[str, os.PathLike, None] = None,
        logger: logging.Logger = DEFAULT_LOGGER,
        lock_timeout: Union[int, float] = DEFAULT_LOCK_TIMEOUT,
    ) -> None:
        if cache_dir is None:
            self.cache_dir = get_user_cache_dir()
        else:
            self.cache_dir = Path(cache_dir)
        self.logger = logger
        self.lock_timeout = lock_timeout
        self.data = self._normalize(self._read())

    @property
    def cache_path(self) -> Path:
        """Returns the path to the cache file."""
        return self.cache_dir / "cache.json"

    @property
    def lock_path(self) -> Path:
        """Returns the path to the lock file."""
        return self.cache_dir / "cache.lock"

    def load(self) -> dict:
        """Loads the cache and returns it."""
        with self.lock():
            new_data = self._read()
            if isinstance(new_data, dict):
                self.data = self._normalize(new_data)
            return self.data

    @contextmanager
    def lock(self) -> Generator:
        """
        Wait / block until lock_path is available. This will also release when
        lock_timeout is reached, logging a warning.
        """
        self._ensure_cache_dir()
        start = None
        while True:
            try:
                self._open_exclusive(self.lock_path)
                break
            except FileExistsError:
                pass
            except OSError as e:
                self.logger.warning(f"cache lock error: {str(e)}")
            if start is None:
                self.logger.debug("cache lock detected")
                start = time.time()
            elapsed = time.time() - start
            if elapsed > self.lock_timeout:
                self.logger.warning("cache lock timeout")
                break
            time.sleep(LOCK_SLEEP_INTERVAL)
        try:
            yield
        finally:
            rm_f(self.lock_path)

    @contextmanager
    def update(self) -> Generator:
        """
        Returns the cache from the filesystem to a yield context and then saves
        the result back to the filesystem.

            with Cache().update() as data:
                data['foo'] = bar
        """
        with self.lock():
            new_data = self._read()
            if isinstance(new_data, dict):
                self.data = self._normalize(new_data)
            yield self.data
            self._write(self.data)

    # Private

    def _ensure_cache_dir(self) -> None:
        """Makes the cache directory if it does not exist."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _open_exclusive(self, path: Path, **kwargs) -> IO:
        """Opens path exclusively, i.e., it most not exist."""
        return path.open(mode="x", **kwargs)

    def _normalize(self, data: object) -> dict:
        """Normalizes the cache data."""
        if not isinstance(data, dict):
            data = {}
        for key in MAIN_CACHE_KEYS:
            value = data.get(key)
            if not isinstance(value, dict):
                data[key] = {}
        return data

    def _read(self) -> object:
        """Reads the parses JSON from the filesystem cache and returns it."""
        try:
            return self._read_json(self.cache_path)
        except (FileNotFoundError, ValueError):
            pass
        except OSError as e:
            self.logger.warning(f"cache read error: {str(e)}")
        return None

    def _read_json(self, path: Path) -> object:
        """Reads and parses JSON data from path."""
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        """Writes a dictionary to the filesystem cache as JSON."""
        try:
            self._write_json(self.cache_path, data)
        except OSError as e:
            self.logger.warning(f"cache write error: {str(e)}")

    def _write_json(self, path: Path, data: object) -> None:
        """Writes data to path as JSON."""
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
