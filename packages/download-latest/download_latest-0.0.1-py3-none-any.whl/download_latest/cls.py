from dataclasses import dataclass
import logging
import os
from pathlib import Path
import time
from typing import Optional, Union

from .cache import Cache
from .fetch import Fetch, FetchResponse, FetchResponseList
from .util import (
    COLORS,
    DEFAULT_LOGGER,
    deduce_filename_from_url,
    get_file_md5,
    get_file_modified,
    get_file_size,
    get_human_file_size,
    get_human_time,
    parse_header_accept_ranges,
    parse_header_content_length,
    parse_header_content_md5,
    parse_header_etag,
    parse_header_last_modified,
    rm_f,
)


__all__ = [
    "Decision",
    "DownloadLatest",
    "DownloadLatestException",
    "FileData",
]


class DownloadLatestException(Exception):
    """Exceptions raised by DownloadLatest."""

    pass


@dataclass
class FileData:
    """Local or Remote attributes for DownloadLatest."""

    etag: Optional[str]
    md5: Optional[str]
    modified: Optional[int]
    resumable: bool
    size: Optional[int]


@dataclass
class Decision:
    """Decision parameters for DownloadLatest."""

    download: bool
    download_reason: str
    dry_run: bool
    force: bool
    local: FileData
    remote: FileData
    restart: bool
    resume: bool
    resume_restart_reason: Optional[str]
    resume_start_at: Optional[int]


class DownloadLatest:
    """Download a file only if the remote file has changed."""

    url: str
    file: Path
    local_output_path: Path
    local_download_path: Path
    local_new_path: Path
    logger: logging.Logger
    responses: Optional[FetchResponseList]
    decision: Optional[Decision]
    cache: Cache
    fetch: Fetch

    def __init__(
        self,
        url: str,
        file: Union[os.PathLike, str, None] = None,
        logger: logging.Logger = DEFAULT_LOGGER,
    ):
        """
        Initialize the instance with the parameters. Deduces file if not
        specified.

        Raises a DownloadLatestException if it could not deduce file, or one of
        the paths is not writeable.
        """
        self.url = url
        if file is None:
            self.file = self._deduce_file(url)
        else:
            self.file = self._check_file(file)
        self.logger = logger
        self.responses = None
        self.decision = None
        self.cache = Cache(logger=logger)
        self.fetch = Fetch(logger=logger)

        local_output_path = self.file.resolve()
        name = local_output_path.name
        self.local_output_path = local_output_path
        self.local_download_path = local_output_path.with_name(f"{name}.download")
        self.local_new_path = local_output_path.with_name(f"{name}.new")

        self._require_writeable(self.local_output_path)
        self._require_writeable(self.local_download_path)
        self._require_writeable(self.local_new_path)

    def main(
        self, dry_run: bool = False, force: bool = False, progress: bool = False
    ) -> bool:
        """
        Runs the main download tasks and returns whether or not there was a new
        download.

        Raises a DownloadLatestException or FetchError on problems.
        """
        self.log_basics()
        self.prefetch(progress=progress)
        self.decide(dry_run=dry_run, force=force)
        self.log_decision()
        return self.download(progress=progress)

    def log_basics(self) -> None:
        """Log the url, file and local paths."""
        self.logger.info(f" url: {self.url}")
        self.logger.info(f"file: {self.file}")

        def debug_path(name, path):
            suffix = " (exists)" if path.exists() else ""
            self.logger.debug(f"{name}: {path}{suffix}")

        debug_path(" out", self.local_output_path)
        debug_path("down", self.local_download_path)
        debug_path(" new", self.local_new_path)

    def prefetch(self, progress: bool = False) -> FetchResponseList:
        """
        Makes one or more HEAD requests to url, following redirects, and sets
        the responses.

        Raises a FetchError if there was a request/response problem, or a
        DownloadLatestException if the server returned an error or no response
        was received.
        """
        self.responses = self.fetch.head(self.url, progress=progress)
        status = self._require_response().status
        for i, response in enumerate(self.responses):
            self.logger.debug(f"req{i + 1}: [{response.status}] {response.url}")
        if status < 200 or 299 < status:
            raise DownloadLatestException(f"server returned error: {status}")
        return self.responses

    def decide(self, force: bool = False, dry_run: bool = False) -> Decision:
        """
        Make a decision to download the remote file.
        """
        self._require_response()
        self.cache.load()

        d = Decision(
            download=True,
            download_reason="ready",
            dry_run=dry_run,
            force=force,
            local=self._get_local_data(),
            remote=self._get_remote_data(),
            restart=False,
            resume=False,
            resume_restart_reason=None,
            resume_start_at=None,
        )

        if not force and self.local_download_path.exists():
            dc = self.cache.data["download"].get(str(self.local_download_path))
            if not d.remote.resumable:
                d.restart = True
                d.resume_restart_reason = "resume unsupported"
            elif (
                isinstance(dc, dict)
                and self.url == dc.get("url")
                and (
                    d.remote.md5 is not None
                    or d.remote.etag is not None
                    or (d.remote.size is not None and d.remote.modified is not None)
                )
                and d.remote.etag == dc.get("etag")
                and d.remote.md5 == dc.get("md5")
                and d.remote.modified == dc.get("modified")
                and d.remote.size == dc.get("size")
            ):
                d.resume = True
                size = get_file_size(self.local_download_path) or 0
                d.resume_start_at = size
                d.resume_restart_reason = "cache match"
            else:
                d.restart = True
                d.resume_restart_reason = "cache mismatch"

        if force:
            d.download_reason = "force enabled"
        elif d.restart:
            d.download_reason = "restarting"
        elif d.resume:
            d.download_reason = (
                f"resuming from {get_human_file_size(d.resume_start_at or 0)}"
            )
        elif not self.local_output_path.exists():
            d.download_reason = "first time"
        elif d.remote.md5 is not None and d.local.md5 is not None:
            if d.remote.md5 == d.local.md5:
                d.download = False
                d.download_reason = "md5s match"
            else:
                d.download_reason = "md5 mismatch"
        elif d.remote.etag is not None and d.local.etag is not None:
            if d.remote.etag == d.local.etag:
                d.download = False
                d.download_reason = "etags match"
            else:
                d.download_reason = "etag mismatch"
        elif (
            d.remote.size is not None
            and d.local.size is not None
            and d.remote.modified is not None
            and d.local.modified is not None
            and d.remote.size == d.local.size
            and d.remote.modified == d.local.modified
        ):
            d.download = False
            d.download_reason = "size and modified match"
        else:
            d.download_reason = "local / remote mismatch"

        self.decision = d
        return d

    def log_decision(self) -> None:
        """Log details about the decision."""
        d = self._require_decision()

        def v(where, key):
            value = getattr(getattr(d, where), key)
            if value is None:
                value = "-"
            else:
                if key == "size":
                    value = get_human_file_size(value)
                elif key == "modified":
                    value = get_human_time(value)
            return value

        self.logger.debug(f"{'':>8} | {'local file':<34} | remote server")
        for key in ("md5", "etag", "size", "modified"):
            self.logger.debug(f"{key:>8} | {v('local', key):<34} | {v('remote',key)}")
        self.logger.debug(
            f"  resume | {'supported':<34} | "
            + ("" if d.remote.resumable else "un")
            + "supported"
        )
        if d.resume_restart_reason:
            self.logger.info(f"stopped download detected: {d.resume_restart_reason}")
        if d.download:
            self.logger.info(f"downloading: {d.download_reason}")
        else:
            self.logger.info(f"not downloading: {d.download_reason}")

    def download(self, progress: bool = False) -> bool:
        """
        Performs the download, if possible, and returns whether or not there was
        a new downloaded file.
        """

        decision = self._require_decision()
        response = self._require_response()

        if decision.dry_run:
            self.logger.debug("dry-run enabled, aborting...")
            return False

        rm_f(self.local_new_path)
        if not decision.download:
            rm_f(self.local_download_path)
            self.logger.debug("not downloading, aborting...")
            return False

        if decision.resume:
            start_size = decision.resume_start_at or 0
        else:
            start_size = 0

        with self.cache.update() as data:
            data["download"][str(self.local_download_path)] = {
                "url": self.url,
                "md5": decision.remote.md5,
                "etag": decision.remote.etag,
                "size": decision.remote.size,
                "modified": decision.remote.modified,
            }

        start = time.time()
        self.fetch.download(
            url=response.url,
            path=self.local_download_path,
            resume=decision.resume,
            progress=progress,
        )
        elapsed = time.time() - start

        download_md5 = get_file_md5(self.local_download_path)
        download_size = get_file_size(self.local_download_path) or 0
        transfered = download_size - start_size

        if decision.remote.md5 is not None and download_md5 != decision.remote.md5:
            self.logger.error(f"md5 mismatch: {self.local_download_path}")
            self.logger.error("md5 mismatch: aborting...")
            return False
        if decision.remote.size is not None and download_size != decision.remote.size:
            self.logger.warning("size mismatch")

        with self.cache.update() as data:
            data["download"].pop(str(self.local_download_path), None)
            if decision.remote.etag:
                data["output"][str(self.local_output_path)] = {
                    "md5": download_md5,
                    "etag": decision.remote.etag,
                }
            else:
                data["output"].pop(str(self.local_output_path), None)

        rm_f(self.local_output_path)
        self.local_download_path.rename(self.local_output_path)
        modified = decision.remote.modified
        if modified is not None:
            self.logger.debug(f"set modified: {get_human_time(modified)}")
            os.utime(self.local_output_path, (modified, modified))
        self.local_new_path.open("a+")

        # HACK: the green color is determined by the first word being 'success'
        self.logger.info(
            f"success: transferred {get_human_file_size(transfered)}"
            + f" in {elapsed:.1f}s{COLORS.RESET}"
        )
        return True

    # Private Methods

    def _check_file(self, file: Union[os.PathLike, str]) -> Path:
        """
        Checks the file to make sure it's not empty and returns it.

        Raises a DownloadLatestException otherwise.
        """
        file = Path(file)
        resolved_name = file.resolve().name
        if resolved_name == "" or resolved_name == "..":
            raise DownloadLatestException(f"filename is empty: {str(file)!r}")
        return file

    def _deduce_file(self, url: str) -> Path:
        """
        Deduce a file from url.

        Raises DownloadLatestException if not possible.
        """
        filename = deduce_filename_from_url(url)
        if filename:
            return self._check_file(filename)
        else:
            raise DownloadLatestException("cannot deduce filename from url")

    def _get_local_data(self) -> FileData:
        """Returns the local output file data."""
        md5 = self._get_local_md5()
        return FileData(
            etag=self._get_local_etag_from_cache(check_md5=md5),
            md5=md5,
            modified=self._get_local_modified(),
            resumable=False,
            size=self._get_local_size(),
        )

    def _get_local_etag_from_cache(
        self, check_md5: Optional[str] = None
    ) -> Optional[str]:
        """Returns the local output etag stored in the cache."""
        info = self.cache.data["output"].get(str(self.local_output_path))
        if isinstance(info, dict) and check_md5 is not None:
            etag = info.get("etag")
            md5 = info.get("md5")
            if check_md5 == md5:
                return etag
            else:
                self.logger.warning("cached local etag: md5 mismatch")
        return None

    def _get_local_md5(self) -> Optional[str]:
        """Returns the local output md5."""
        return get_file_md5(self.local_output_path)

    def _get_local_modified(self) -> Optional[int]:
        """Returns the local output modified time."""
        return get_file_modified(self.local_output_path)

    def _get_local_size(self) -> Optional[int]:
        """Returns the local output file size."""
        return get_file_size(self.local_output_path)

    def _get_remote_data(self) -> FileData:
        """Returns the remote file data."""
        return FileData(
            etag=self._get_remote_etag(),
            md5=self._get_remote_md5(),
            modified=self._get_remote_modified(),
            resumable=self._get_remote_resumable(),
            size=self._get_remote_size(),
        )

    def _get_remote_etag(self) -> Optional[str]:
        """Returns the remote etag."""
        headers = self._require_response().headers
        return parse_header_etag(headers)

    def _get_remote_md5(self) -> Optional[str]:
        """Returns the remote md5."""
        headers = self._require_response().headers
        return parse_header_content_md5(headers)

    def _get_remote_modified(self) -> Optional[int]:
        """Returns the remote modified time."""
        headers = self._require_response().headers
        return parse_header_last_modified(headers)

    def _get_remote_resumable(self) -> bool:
        """Returns whether the server supports resuming downloads."""
        headers = self._require_response().headers
        return parse_header_accept_ranges(headers)

    def _get_remote_size(self) -> Optional[int]:
        """Returns the remote file size."""
        headers = self._require_response().headers
        return parse_header_content_length(headers)

    def _require_decision(self) -> Decision:
        """Raises DownloadLatestException if no decision was made."""
        if self.decision:
            return self.decision
        else:
            raise DownloadLatestException("no decision made")

    def _require_response(self) -> FetchResponse:
        """Raises DownloadLatestException if no response was received."""
        if self.responses:
            return self.responses[-1]
        else:
            raise DownloadLatestException("no response received")

    def _require_writeable(self, path: Path) -> Path:
        """Raises DownloadLatestException if path is not writeable."""
        if not path.exists() or path.is_file():
            return path
        else:
            raise DownloadLatestException(f"file exists: {path}")

    @classmethod
    def run(
        cls,
        url: str,
        file: Union[os.PathLike, str, None] = None,
        dry_run: bool = False,
        force: bool = False,
        progress: bool = False,
        logger: logging.Logger = DEFAULT_LOGGER,
    ) -> bool:
        """
        Runs the main download tasks and returns whether or not there was a new
        download.

        Raises a DownloadLatestException or FetchError on problems.

        Example usage:

            from download_latest import DownloadLatest
            downloaded = DownloadLatest.run(...)
            if downloaded:
                # ...
        """
        dl = cls(url=url, file=file, logger=logger)
        return dl.main(dry_run=dry_run, force=force, progress=progress)
