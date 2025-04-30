## Summary of changes: load-env

- Created `src/load_env.py` module with `load_env()` function to locate and load `.env` files.
- Updated `src/app.py` to import and call `load_env()` instead of inline dotenv-loading logic.
