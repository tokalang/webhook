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

## Current scope

The in-repository vertical slice implements a `POST /hooks/:id` endpoint,
header equality authorization, and command execution with a completed exit
status. JSON configuration and a long-running CLI are the next executable
slice; they are not represented as complete until their compatibility fixtures
pass. The known standard-library blocker for per-child cwd/environment is in
[docs/toka-gaps.md](docs/toka-gaps.md).

## Qualification

With a Toka checkout at `../toka`:

```sh
python3 tests/qualify.py
```

The qualification compiles and runs both direct dispatch and loopback HTTP
tests against the local Toka compiler and runtime.
