# Lab 1 — Set Up a Reproducible Python Project with uv

**Topic 1** · Create and run a Python project using uv

The learner installs uv, creates a project, adds locked dependencies, and runs code through uv so the environment is identical on every machine. This is the foundation every later lab builds on.

- **You will build:** A uv project with pyproject.toml, uv.lock and a working entry point
- **Tools:** uv, Python 3.12, pyproject.toml, uv.lock

## Steps

1. Confirm uv is installed and check the version

   ```bash
   uv --version
   ```

2. Create a new project folder and initialise it

   ```bash
   uv init cardguard
   cd cardguard
   ```

3. Inspect what uv generated — note pyproject.toml is the project manifest

   ```bash
   ls -a
   cat pyproject.toml
   ```

4. Pin the Python version so every learner runs the same interpreter

   ```bash
   uv python pin 3.12
   ```

5. Add a dependency — uv resolves, installs and writes uv.lock in one step

   ```bash
   uv add pandas
   ```

6. Open uv.lock and observe the exact pinned versions

   ```python
   head -30 uv.lock
   ```

7. Write a first script that proves the dependency is importable

   ```python
   # main.py
   import pandas as pd
   
   def main() -> None:
       df = pd.DataFrame({"card": ["4111...1111", "5500...0004", "4111...1111"],
                          "merchant": ["SG Grocer", "Overseas ATM", "SG Grocer"],
                          "amount": [42.90, 800.00, 15.50]})
       print(df)
       print(f"Total screened: ${df['amount'].sum():,.2f}")
   
   if __name__ == "__main__":
       main()
   ```

8. Run it through uv — no venv activation needed

   ```bash
   uv run python main.py
   ```

9. Prove reproducibility: delete the venv and restore it from the lockfile

   ```bash
   rm -rf .venv
   uv sync
   uv run python main.py
   ```


## Verify

uv run python main.py prints the transaction DataFrame and the screened total. After deleting .venv, uv sync restores it and the script produces identical output.
