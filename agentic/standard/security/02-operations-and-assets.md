# Operations & Asset Management

## Asset Centralization
- **Repository**: All static assets must live under `/assets`.
- **Pathing**: Resolve locations via `PROJECT_ROOT` helpers (e.g., `get_resource`).
- **README**: Every subfolder MUST have a `README.md` explaining purpose and structure.

## Configuration Externalization
- **Zero-Secret Codebase**: No credentials in code.
- **Master Registry**: `config.ini` is the master registry.
- **Exclusive Broker**: `config.py` is the only module permitted to read `config.ini`.

## SSL/TLS Management
- **Storage**: Certificates in `src/config/ssl/`.
- **Permissions**: `600` for keys, `644` for certs.
- **Prohibition**: Never commit private keys to version control.

## 12-Factor App Methodology
Torro adheres to the 12-Factor methodology for production-grade systems (Statelessness, Port Binding, Concurrency, etc.).
