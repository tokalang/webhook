# Upstream and compatibility policy

This is an independent Toka implementation inspired by
[`adnanh/webhook`](https://github.com/adnanh/webhook), fixed at commit
`2548ffb800e0db0fc779acfc64fe624cee107af6` (retrieved 2026-08-12).

The upstream project is MIT licensed, copyright (c) 2015 Adnan Hajdarevic.
Its complete copyright and license notice is retained in
[`LICENSES/adnanh-webhook-MIT.txt`](LICENSES/adnanh-webhook-MIT.txt). Toka webhook
does not claim to be affiliated with, endorsed by, or a drop-in release of the
upstream project.

## Initial compatibility target

The initial release must accept a JSON hook configuration and provide
`POST /hooks/:id`. A hook has an id, an executable, literal argument list, and
one header-equality trigger rule. Matching requests launch the configured
program using a direct argv vector; no input is ever passed to a shell.

The following upstream features are intentionally not claimed until separately
implemented and qualified: YAML and template configuration, multipart/XML
payloads, nested rule trees, request data interpolation, environment passing,
working-directory selection, hot reload, TLS server configuration, Unix socket
activation, CORS, and platform daemon integration.

The initial restriction is not an equivalence claim. In particular, Toka's
current `std/process::Command` has a direct argv API but no per-child
environment or working-directory API; that gap is recorded in
[`docs/toka-gaps.md`](docs/toka-gaps.md).

The current Linux/macOS release contract and every remaining upstream feature
are tracked in [`docs/compatibility-matrix.md`](docs/compatibility-matrix.md).
