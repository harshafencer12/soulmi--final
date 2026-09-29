# Architecture SOP: Python Tool Scripts

## Constraints & Environment
- **OS Encoding Constraints:** All scripts run in environments (like Windows PowerShell) must avoid using unsupported Unicode characters (such as emojis like ✅ or ❌) in `print()` statements to prevent `UnicodeEncodeError`. Use text-based markers like `[SUCCESS]` or `[FAILED]` instead.

## Standards
- Use `.env` for all secrets.
- Deterministic logic only.
