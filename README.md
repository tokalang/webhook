# Toka webhook

An independent, bounded Toka implementation of the core workflow of
[`adnanh/webhook`](https://github.com/adnanh/webhook): receive a webhook,
check a rule, and run a configured program. It is not an upstream release or
an affiliation with that project. See [UPSTREAM.md](UPSTREAM.md) for the fixed
source version, license notice, and compatibility boundary.

## Safety boundary

This program invokes commands only through Toka's structured
`std/process::Command` argv API. Request data is not interpolated into a shell
command. The first version runs only literal, configuration-owned arguments.

## Run

```sh
webhook --hooks hooks.json --port 9000 --header 'Access-Control-Allow-Origin=*'
```

The configuration is a JSON array using upstream's `id`, `execute-command`,
`pass-arguments-to-command`, and value/header `trigger-rule.match` keys.
The optional repeatable `--header name=value` flag adds a response header to
every result (including CORS headers). The server handles one request per
connection and one connection at a time in this initial implementation.

## Current scope

The in-repository vertical slice implements a `POST /hooks/:id` endpoint,
header equality authorization, JSON configuration loading, and command
execution with a completed exit status. The known standard-library blocker for
per-child cwd/environment is in [docs/toka-gaps.md](docs/toka-gaps.md).
The complete Linux/macOS compatibility contract is in
[docs/compatibility-matrix.md](docs/compatibility-matrix.md).

## Qualification

With a Toka checkout at `../toka`:

```sh
python3 tests/qualify.py
```

The qualification compiles and runs both direct dispatch and loopback HTTP
tests against the local Toka compiler and runtime.
