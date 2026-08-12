# Toka capability gaps found by this port

`std/process::Command` safely starts a process from a program plus an argv
vector, which is sufficient for the first webhook execution boundary. It does
not currently provide a per-child environment map or working directory. Using
process-global `std/env::set_var` or `set_current_dir` would be unsafe for a
concurrent HTTP server, so this project deliberately does not emulate those
upstream options through global mutation.

This repository treats the missing APIs as a Toka standard-library gap, not as
permission to use shell concatenation or unsafe mutable process-global state.
