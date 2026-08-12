# Linux/macOS compatibility matrix

Target upstream: `adnanh/webhook` commit
`2548ffb800e0db0fc779acfc64fe624cee107af6`.

This matrix is the release contract. A row becomes supported only when a
black-box fixture exercises the matching upstream configuration and observable
HTTP/process behavior on both Linux and macOS.

| Area | Status | Notes |
| --- | --- | --- |
| JSON hooks file | partial | `id`, `execute-command`, literal `pass-arguments-to-command`, `response-message`, command-output flags, `incoming-payload-content-type`, and value/header or payload-HMAC `trigger-rule.match` work. |
| YAML and template hooks files | planned | Requires parser/template compatibility corpus. |
| Request references | partial | Command environment/argv support `string`, header, URL/query, JSON payload dotted paths (including top-level arrays under upstream-compatible `root`), URL-encoded and multipart text-form fields, bounded XML dotted element paths, raw body, `request.method`, IPv4 `request.remote-addr` (`address:port`), `entire-payload`, `entire-query`, and JSON `entire-headers`; multipart files, XML attributes/entities, and IPv6 remain. |
| Rule composition | partial | Nested `and`, `or`, `not`, header value, POSIX ERE regex (Linux/macOS), HMAC-SHA1/SHA256/SHA512 (including deprecated `payload-hash-*` aliases), and IPv4 `ip-whitelist` CIDR/single-address matches work; IPv6 and Scalr signatures remain. |
| Command arguments | partial | Literal and request-reference objects work through structured argv, never a shell; payload/complete-source forms remain. |
| Child cwd/environment/files | partial | `command-working-directory` and per-child environment (`string`, header, raw body, method) work; query/payload/complete sources and temporary-file policy remain. |
| Command output response | partial | Successful stdout can be returned; stderr/error and status compatibility remain. |
| Hook response policy | partial | `response-message`, response headers, success status, mismatch status, hook `http-methods` (including PATCH), and CLI default `--http-methods` work. |
| HTTP server behavior | partial | One request per connection, serial acceptance, IPv4/hostname `--ip` binding, configurable `--urlprefix` (default `hooks`), and repeatable global `--header name=value` response headers (including CORS). |
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
