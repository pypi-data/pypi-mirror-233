# Download Latest

Download a file only if the remote file has changed.

## Example

```sh
URL='https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US'
ARCHIVE="firefox.tar.bz2"

dl "$URL" "$ARCHIVE"

if [ -f "$ARCHIVE.new" ]; then
  echo "New version detected"
  tar -xjf "$ARCHIVE"
fi
```

## Install

Make sure [cURL](https://curl.se/) and [Python 3](https://www.python.org/) are
installed. Then:

```sh
pip install download-latest
```

[See the install guide](INSTALL.md) for more information.

## Usage

```
usage: download-latest [ -h | --help ] [OPTIONS] URL [FILE]

Download URL to FILE only if remote file has changed.

positional arguments:
  URL              url to download
  FILE             path to output (deduced if not specified, see below)

optional arguments:
  -h, --help       show this help message and exit
  -V, --version    show program's version number and exit
  -n, --dry-run    do not download (default: false)
  -f, --force      do not check for changes (default: false)
  -q, --quiet      suppress output (default: false)
  -v, --verbose    increase output (default: false)
  --color WHEN     colorize output (default: auto)
  --progress WHEN  show a progress meter (default: auto)

WHEN must be one of 'always', 'never' or 'auto', where 'auto' will be
detected from the TTY.

If FILE is not specified, it will be deduced by the filename part of the
URL. If no filename can be deduce, e.g., https://example.com/, then the
program will exit with an error.

Additional files may be generated:

FILE.new       present when download occured, otherwise absent
FILE.download  in-progress download
```
