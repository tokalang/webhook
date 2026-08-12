# Linux/macOS compatibility matrix

Target upstream: `adnanh/webhook` commit
`2548ffb800e0db0fc779acfc64fe624cee107af6`.

This matrix is the release contract. A row becomes supported only when a
black-box fixture exercises the matching upstream configuration and observable
HTTP/process behavior on both Linux and macOS.

| Area | Status | Notes |
| --- | --- | --- |
| JSON hooks file | partial | `id`, `execute-command`, literal `pass-arguments-to-command`, and value/header `trigger-rule.match` work. |
| YAML and template hooks files | planned | Requires parser/template compatibility corpus. |
| Request references | planned | Header, query, request, JSON/form/XML payload, and complete-source forms. |
| Rule composition | planned | `and`, `or`, `not`, value, regex, IP, HMAC, Scalr signatures. |
| Command arguments | partial | Literal arguments only; execution uses structured argv, never a shell. |
| Child cwd/environment/files | blocked by adapter | Requires per-child process setup, not process-global mutation. |
| Command output response | planned | Must preserve stdout/stderr and non-zero status behavior. |
| Hook response policy | planned | Response message, headers, status codes, allowed methods, mismatch code. |
| HTTP server behavior | partial | One request per connection, serial acceptance, fixed `/hooks` prefix. |
| TLS, ciphers, Unix socket | planned | TLS can use existing Toka TLS layer; Unix socket needs a platform adapter. |
| Configuration reload and signals | planned | HUP/USR1 on Linux/macOS. |
| systemd activation | Linux-only planned | Not applicable to macOS. |
| PID file, uid/gid drop, logs | planned | Linux/macOS semantics only. |

## Toka candidates identified during porting

1. `std/process` needs an owned, per-child specification for environment,
   working directory, stdin/stdout/stderr policy, and cancellation. Global
   `setenv`/`chdir` is not safe for concurrent webhook requests.
2. `stdx/crypto` has SHA-1 and HMAC-SHA256 but no HMAC-SHA1 or HMAC-SHA512;
   upstream signature rules require all three.

Until those standard APIs exist, any application-local native adapter stays
private to this repository and receives dedicated Linux/macOS lifecycle tests.
