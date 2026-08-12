# Toka capability gaps found by this port

The original port identified a per-child process-configuration gap. That gap
is now closed by Toka's `std/process::Command`: `current_dir`, `env`, stdio
policy, cancel policy, `request_cancel`, and configured `output` run below the
POSIX child boundary. This application must use those APIs rather than
process-global `std/env::set_var` or `set_current_dir`.

The historic note remains so the port's safety decision is auditable: shell
concatenation and unsafe mutable process-global state were never acceptable
workarounds.
