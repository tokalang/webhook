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
| Child cwd/environment/files | partial | `command-working-directory` now maps to Toka's per-child cwd; environment references and temporary-file policy remain. |
| Command output response | planned | Must preserve stdout/stderr and non-zero status behavior. |
| Hook response policy | planned | Response message, headers, status codes, allowed methods, mismatch code. |
| HTTP server behavior | partial | One request per connection, serial acceptance, fixed `/hooks` prefix. |
| TLS, ciphers, Unix socket | planned | TLS can use existing Toka TLS layer; Unix socket needs a platform adapter. |
| Configuration reload and signals | planned | HUP/USR1 on Linux/macOS. |
| systemd activation | Linux-only planned | Not applicable to macOS. |
| PID file, uid/gid drop, logs | planned | Linux/macOS semantics only. |

## Toka capability history

The two initial candidates are now available in Toka: `std/process` has an
owned per-child specification for environment, working directory, stdio, and
cancellation; `stdx/crypto` has HMAC-SHA1, HMAC-SHA256, and HMAC-SHA512.

No application-local process or cryptographic workaround is needed for these
features. Any future native adapter remains private to this repository and
requires dedicated Linux/macOS lifecycle tests.
