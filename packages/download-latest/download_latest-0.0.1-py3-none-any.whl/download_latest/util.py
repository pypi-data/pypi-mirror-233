"""
Standalone utility methods.
"""

import base64
from datetime import datetime, timezone
from email.message import Message
import hashlib
import locale
import logging
import os
from pathlib import Path
import re
from typing import Optional, Union
from urllib.parse import urlparse

from .meta import __program__


__all__ = [
    "COLORS",
    "DEFAULT_LOGGER",
    "MD5_BUFFER_SIZE",
    "deduce_filename_from_url",
    "get_file_md5",
    "get_file_modified",
    "get_file_size",
    "get_human_file_size",
    "get_human_time",
    "get_user_cache_dir",
    "parse_header_accept_ranges",
    "parse_header_content_length",
    "parse_header_content_md5",
    "parse_header_etag",
    "parse_header_last_modified",
    "rm_f",
    "sanitize_filename",
    "truncate",
]

DEFAULT_LOGGER = logging.getLogger(__name__.split(".")[0])

MD5_BUFFER_SIZE = 32768


class COLORS:
    # https://stackoverflow.com/a/33206814
    GREY243 = "\x1b[38;5;243m"
    ORANGE214 = "\x1b[38;5;214m"
    RED160 = "\x1b[38;5;160m"
    GREEN = "\x1b[0;32m"
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"


def deduce_filename_from_url(url: str, os_name: str = "auto") -> Optional[str]:
    """
    Deduces and returns a filename from url. Returns None if not possible.

    If os_name is 'auto', then uses the system os.name.
    """
    purl = urlparse(url)
    if not purl.scheme:
        purl = urlparse(f"http://{url}")
    path = purl._replace(scheme="", netloc="").geturl()
    parts = path.split("/")
    while parts:
        if parts[-1] in ("", "."):
            parts.pop()
        elif parts[-1] == "..":
            parts.pop()
            if parts:
                parts.pop()
        else:
            break
    if parts:
        return sanitize_filename(parts[-1], os_name=os_name)
    else:
        return None


def get_file_md5(path: Union[os.PathLike, str]) -> Optional[str]:
    """Returns the MD5 hexdigest of path."""
    hash = hashlib.md5()
    try:
        with Path(path).open("rb") as f:
            while True:
                buffer = f.read(MD5_BUFFER_SIZE)
                if buffer:
                    hash.update(buffer)
                else:
                    break
            return hash.hexdigest()
    except FileNotFoundError:
        return None


def get_file_modified(path: Union[os.PathLike, str]) -> Optional[int]:
    """Returns the modified time as epoch time of path."""
    try:
        return round(Path(path).stat().st_mtime)
    except FileNotFoundError:
        return None


def get_file_size(path: Union[os.PathLike, str]) -> Optional[int]:
    """Returns the size of path."""
    try:
        return Path(path).stat().st_size
    except FileNotFoundError:
        return None


def get_human_file_size(size: int) -> str:
    """Returns the file size as a friendlier string."""
    KB = 2**10
    MB = 2**20
    GB = 2**30
    if size < KB:
        return f"{size}B"
    elif size < MB:
        return f"{(size / KB):.1f}K ({size})"
    elif size < GB * 10:  # Prefer showing MB over GB
        return f"{(size / MB):.1f}M ({size})"
    else:
        return f"{(size / GB):.1f}G ({size})"


def get_human_time(timestamp: int) -> str:
    """Returns the time epoch as a friendlier string."""
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    except Exception:
        return f"XXXX-XX-XXTXX:XX:XXZ ({timestamp})"
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ") + f" ({timestamp})"


def get_user_cache_dir() -> Path:
    """
    Return the (hopefully platform-independent) cache directory for the
    current user.
    """

    if os.name == "nt":
        return (
            Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
            / __program__
            / "Cache"
        )
    else:  # posix
        return (
            Path(os.environ.get("XDG_CACHE_HOME") or (Path.home() / ".cache"))
            / __program__
        )


def parse_header_accept_ranges(headers: Message) -> bool:
    """Parse and return the Accept-Ranges header to determine server resume
    support."""
    return headers.get("accept-ranges") == "bytes"


def parse_header_content_length(headers: Message) -> Optional[int]:
    """Parse and return the Content-Length header."""
    value = headers.get("content-length")
    if not isinstance(value, str):
        return None
    match = re.match(r"^\s*([0-9]+)\s*$", value)
    if match:
        return int(match[1])
    else:
        return None


def parse_header_content_md5(headers: Message) -> Optional[str]:
    """Parse and return the Content-MD5 header as a hexdigest."""
    value = headers.get("content-md5")
    if not isinstance(value, str):
        return None
    try:
        raw = base64.b64decode(value)
    except ValueError:
        return None
    hex = raw.hex()
    return hex if len(hex) == 32 else None


def parse_header_etag(headers: Message) -> Optional[str]:
    """Parse and return the ETag header."""
    value = headers.get("etag")
    if isinstance(value, str) and value:
        return value
    else:
        return None


def parse_header_last_modified(headers: Message) -> Optional[int]:
    """Parse and return the Last-Modified header as epoch time."""
    value = headers.get("last-modified")
    if not isinstance(value, str):
        return None
    old_locale = locale.getlocale(locale.LC_TIME)
    locale.setlocale(locale.LC_TIME, "C")
    try:
        dt = datetime.strptime(value, "%a, %d %b %Y %H:%M:%S GMT")
    except ValueError:
        return None
    finally:
        locale.setlocale(locale.LC_TIME, old_locale)
    dt = dt.replace(tzinfo=timezone.utc)
    return round(dt.timestamp())


def rm_f(path: Union[os.PathLike, str]) -> None:
    """Robust unlink."""
    try:
        Path(path).unlink()
    except OSError:
        pass


def sanitize_filename(filename: str, os_name: str = "auto") -> Optional[str]:
    """
    Returns a filename that is likely sanitized for most operating systems.
    Returns None if not possible.

    If os_name is 'auto', then uses the system os.name.

    - Removes control-characters and /
    - Replaces < > : " | ? * \\ with _      (Windows-only)
    - Removes trailing . and spaces         (Windows-only)
    - Truncates filenames to 240 bytes in UTF-8

    https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names
    """
    if os_name == "auto":
        os_name = os.name
    filename = re.sub(r"[\x00-\x1F/]", "", filename)
    if os_name == "nt":
        filename = re.sub(r'[<>:"|?*\\]', "_", filename)
        filename = re.sub(r"[ .]+$", "", filename)
    truncated = filename.encode("utf-8", errors="ignore")[:240]
    filename = truncated.decode("utf-8", errors="ignore")
    filename = "" if filename in (".", "..") else filename
    return filename if filename else None


def truncate(text: str, max: int = 80, ellipses: str = "...") -> str:
    """Truncates the text to max characters."""
    if len(text) > max and max >= 0:
        if len(ellipses) > max:
            text = ellipses[:max]
        else:
            text = text[: max - len(ellipses)] + ellipses
    return text
