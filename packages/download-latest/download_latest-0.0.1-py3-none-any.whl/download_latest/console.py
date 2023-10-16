import argparse
import logging
import sys
import textwrap
from typing import Optional

from .cls import DownloadLatest, DownloadLatestException
from .fetch import FetchRunError
from .meta import __program__, __version__
from .util import COLORS


__all__ = [
    "ConsoleFormatter",
    "get_logger",
    "get_args",
    "main",
]


class ConsoleFormatter(logging.Formatter):
    """A simple logging formatter supporting colors."""

    def __init__(self, *args, color=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color = color

    def format(self, record: logging.LogRecord) -> str:
        """Format the record using colors if requested."""
        formatted = super().format(record)
        if self.color:
            if formatted.startswith("success"):
                msg_color = COLORS.GREEN + COLORS.BOLD
            elif record.levelno <= logging.DEBUG:
                msg_color = COLORS.GREY243
            elif record.levelno <= logging.INFO:
                msg_color = ""
            elif record.levelno <= logging.WARNING:
                msg_color = COLORS.ORANGE214 + COLORS.BOLD
            else:
                msg_color = COLORS.RED160 + COLORS.BOLD
            prog_color = COLORS.GREY243
            reset = COLORS.RESET
        else:
            prog_color = msg_color = reset = ""
        return f"{prog_color}{__program__}: {reset}{msg_color}{formatted}{reset}"


def get_logger(
    quiet: bool = False,
    verbose: bool = False,
    color: bool = True,
    name: str = __name__,
) -> logging.Logger:
    """
    Returns the logger for the CLI.

    If quiet is set, then the logger has no handler. Otherwise, two handlers are
    added such that:

    - Messages of WARNING, ERROR and CRITICAL levels are sent to stderr.
    - Messages of INFO (and DEBUG if verbose) levels are sent to stdout.
    """

    logger = logging.getLogger(name)

    if quiet:
        logger.setLevel(logging.CRITICAL + 1)
        logger.addHandler(logging.NullHandler())
        return logger

    if verbose:
        min_level = logging.DEBUG
    else:
        min_level = logging.INFO

    class StdOutFilter(logging.Filter):
        def filter(self, record):
            return min_level <= record.levelno and record.levelno < logging.WARNING

    formatter = ConsoleFormatter(color=color)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)
    stdout_handler.addFilter(StdOutFilter())
    stderr_handler.setLevel(logging.WARNING)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)
    logger.setLevel(logging.DEBUG)
    return logger


def get_args(
    args: Optional[list] = None, isatty: Optional[bool] = None
) -> argparse.Namespace:
    """Returns the parsed arguments for the CLI."""

    USAGE = "%(prog)s [ -h | --help ] [OPTIONS] URL [FILE]"
    DESCRIPTION = "Download URL to FILE only if remote file has changed."
    EPILOG = textwrap.dedent(
        """\
        WHEN must be one of 'always', 'never' or 'auto', where 'auto' will be
        detected from the TTY.

        If FILE is not specified, it will be deduced by the filename part of the
        URL. If no filename can be deduce, e.g., https://example.com/, then the
        program will exit with an error.

        Additional files may be generated:

        FILE.new       present when download occured, otherwise absent
        FILE.download  in-progress download
        """
    )

    parser = argparse.ArgumentParser(
        prog=__program__,
        usage=USAGE,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "url",
        help="url to download",
        metavar="URL",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="path to output (deduced if not specified, see below)",
        metavar="FILE",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{__program__} {__version__}",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="do not download (default: false)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="do not check for changes (default: false)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="suppress output (default: false)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output (default: false)",
    )
    parser.add_argument(
        "--color",
        choices=("always", "never", "auto"),
        default="auto",
        help="colorize output (default: auto)",
        metavar="WHEN",
    )
    parser.add_argument(
        "--progress",
        choices=("always", "never", "auto"),
        default="auto",
        help="show a progress meter (default: auto)",
        metavar="WHEN",
    )

    # https://docs.python.org/3/library/argparse.html#intermixed-parsing
    parsed_args = parser.parse_intermixed_args(args)

    for key in ("color", "progress"):
        when = getattr(parsed_args, key)
        if when is None or when == "always":
            value = True
        elif when == "never":
            value = False
        else:
            value = sys.stdin.isatty() if isatty is None else isatty
        setattr(parsed_args, key, value)

    return parsed_args


def main(args: Optional[list] = None, isatty: Optional[bool] = None) -> bool:
    """The main function called from the CLI."""
    a = get_args(args=args, isatty=isatty)
    logger = get_logger(quiet=a.quiet, verbose=a.verbose, color=a.color)
    try:
        return DownloadLatest.run(
            url=a.url,
            file=a.file,
            dry_run=a.dry_run,
            force=a.force,
            progress=a.progress,
            logger=logger,
        )
    except DownloadLatestException as e:
        logger.error(str(e))
        sys.exit(32)
    except FetchRunError as e:
        logger.error(str(e))
        sys.exit(e.code)
    except KeyboardInterrupt:
        logger.warning("keyboard interrupt")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"exception: {str(e)}")
        raise e
