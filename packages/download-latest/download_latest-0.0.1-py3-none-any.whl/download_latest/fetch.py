from __future__ import annotations

from http.client import HTTPException, HTTPResponse
import io
import os
import logging
from pathlib import Path
import shlex
from socket import socket
import subprocess
import time
from typing import List, Optional, Union
from urllib.parse import urljoin

from .util import DEFAULT_LOGGER, truncate

__all__ = [
    "DEFAULT_CURL_PATH",
    "Fetch",
    "FetchException",
    "FetchResponse",
    "FetchResponseList",
    "FetchRunError",
]

DEFAULT_CURL_PATH = "curl"


class FetchException(HTTPException):
    """Exceptions raised by Fetch."""

    pass


class FetchParseException(FetchException):
    """HTTP parse exception."""

    pass


class FetchRunError(FetchException):
    """Subprocess (cURL) error."""

    def __init__(self, msg: str, code):
        super().__init__(msg)
        self.code = code


class FetchResponse(HTTPResponse):
    """An HTTPResponse wrapper supporting static, raw bytes."""

    def __init__(
        self,
        raw: bytes,
        url: str,
        debuglevel: int = 0,
        method: Optional[str] = None,
    ):
        """
        Patches HTTPResponse initializer to support bytes instead of a socket
        argument.
        """

        class FakeSocket(socket):
            def __init__(self, fp: io.IOBase) -> None:
                self.fp = fp

            def makefile(self, *args, **kwargs) -> io.IOBase:  # type: ignore
                return self.fp

        raw = self._patch_raw(raw)
        raw_stream = io.BytesIO(raw)
        sock = FakeSocket(raw_stream)
        super().__init__(sock, debuglevel=debuglevel, method=method, url=url)

        self.url = url  # assign url due to a bug in HTTPResponse
        self.begin()

    def begin(self) -> None:
        """Raises a FetchException when unable to parse the raw response."""
        try:
            super().begin()
        except HTTPException:
            raise FetchParseException("cannot parse response")

    @staticmethod
    def _patch_raw(raw: bytes) -> bytes:
        """
        Replaces HTTP/x with HTTP/1.1 in a raw response so HTTPResponse.begin()
        doesn't throw an exception. Also, adds a fake HTTP status line if we
        don't find one to handle non-HTTP protocols.
        """
        raw_lines = raw.strip().split(b"\r\n")
        parts = raw_lines[0].split(None, 1) if raw_lines else []
        if parts and parts[0].startswith(b"HTTP"):
            raw_lines[0] = b" ".join([b"HTTP/1.1"] + parts[1:])
        else:
            raw_lines.insert(0, b"HTTP/1.1 200 OK")
        return b"\r\n".join(raw_lines + [])


class FetchResponseList(List):
    """A list of FetchResponses."""

    @classmethod
    def make_from_raw(cls, raw_list: bytes, url: str) -> FetchResponseList:
        """
        Returns a FetchResponseList from the raw bytes of one or more HEAD
        requests.
        """
        responses = cls()
        for raw in raw_list.strip().split(b"\r\n\r\n"):
            response = FetchResponse(raw=raw, url=url)
            responses.append(response)
            location = response.headers["location"]
            if location:
                url = urljoin(url, location)
        return responses


class Fetch:
    """Simplified request/response methods using the cURL CLI."""

    curl_path: Path
    spinner_index: int

    def __init__(
        self,
        logger: logging.Logger = DEFAULT_LOGGER,
        curl_path: Union[os.PathLike, str] = DEFAULT_CURL_PATH,
    ):
        self.logger = logger
        self.curl_path = Path(curl_path)
        self.spinner_index = 0

    def head(self, url: str, progress: bool = False) -> FetchResponseList:
        """
        Make one or more HEAD requests to url, following redirects, and returns
        a corresponding FetchResponseList.
        """
        code, stdout, stderr = self._run_silent_curl(
            "--location", "--head", "--", url, progress=progress
        )
        if code != 0:
            raise self._make_curl_run_error(stderr, code)
        return FetchResponseList.make_from_raw(stdout, url=url)

    def download(
        self,
        url: str,
        path: Union[os.PathLike, str],
        resume: bool = False,
        progress: bool = False,
    ) -> None:
        """Download url to path."""
        path = str(path)
        resume_args = ("--continue-at", "-") if resume else ()
        code, stdout, stderr = self._run_silent_curl(
            "--fail",
            "--location",
            "--output",
            path,
            *resume_args,
            "--",
            url,
            progress=progress,
        )
        if code != 0:
            raise self._make_curl_run_error(stderr, code)

    def run(self, *args: str, progress: bool = False) -> tuple:
        """
        Run a subprocess and return a tuple with its return code, stdout and
        stderr.
        """
        cmd = " ".join(shlex.quote(arg) for arg in args)
        self.logger.debug(f">>> {cmd}")

        if progress:
            p1 = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
            )
            self._spinner(p1)
            stdout = p1.stdout.read() if p1.stdout else b""  # TODO
            stderr = p1.stderr.read() if p1.stderr else b""  # TODO
            code = p1.returncode
        else:
            p2 = subprocess.run(args, capture_output=True)
            stdout, stderr = p2.stdout, p2.stderr
            code = p2.returncode

        self.logger.debug(
            truncate(f"<<< code={code} out={stdout!r} err={stderr!r}", 120)
        )
        return (code, stdout, stderr)

    # Private

    def _make_curl_run_error(self, stderr: bytes, code: int) -> FetchRunError:
        """Return a FetchRunError in response to a cURL error."""
        msg = stderr.strip().decode("utf-8", errors="ignore")
        if msg == "":
            msg = f"curl ({code})"
        return FetchRunError(msg, code)

    def _run_silent_curl(self, *args: str, progress: bool = False) -> tuple:
        """Run cURL with silent options."""
        return self.run(
            str(self.curl_path), "--silent", "--show-error", *args, progress=progress
        )

    def _spinner(self, p: subprocess.Popen) -> None:
        width = 23
        wave = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
        wave = wave * (1 + int(width / len(wave)))
        i = self.spinner_index
        print(" " * width, end="", flush=True)
        try:
            while p.poll() is None:
                subspin = (wave[i:] + wave[:i])[: (width - 1)]
                print("\b" * width + subspin + " ", end="", flush=True)
                i = (i + 1) % len(wave)
                time.sleep(0.07)
        finally:
            self.spinner_index = i
            print("\r\x1b[K", end="", flush=True)
