# spelling-test AGENTS.md

## Your role

## Documentation

- Lint markdown files with markdownlint-cli2 (npm package).
- Markdown line length should wrap at 120 characters.

## Python projects

### Python command naming

- Scripts use **kebab-case**
- Scripts use **verb-noun** naming, e.g `get-pdf`
- The verb MUST be a valid verb from the PowerShell `Get-Verb` list, e.g. `Get-Verb "split"` returns output.
- The noun SHOULD be a short simple high-level object
- Sub-commands in the CLI arguments can specify components of that high-level object, e.g `get-pdf bookmarks`,
  `get-pdf images`, `get-pdf toc`, etc.

### Python tooling

- Use `uv`.

## Python coding guidelines

### Code quality

- Use `ruff` with repo-wide settings in the root `pyproject.toml` file.
- Use `pyright`.
- When encountering `pyright` warnings on code written in another session, fix problems opportunistically UNLESS there
are a large number of them (e.g. 10+)

### Input and output

- Use `FastAPI` for API creation. The FastAPI object should be named `api()`.
- Use `FastMCP` for MCP creation. The FastMCP object should be named `mcp()`.
- Use `typer` for command-line argument handling. The Typer object should be named `cli()`.
- Use `rich` for human-readable output.
- Apps scripts, etc. should support a `--json` switch to enable machine-readable output instead of `rich` output.

#### Logging

- Use `loguru` for logging; write logs to `stderr`.
- Default logging level is `SUCCESS` (25).
- To show `INFO` level logs in the terminal needs use of a `--verbose` CLI switch.
- To show `DEBUG` level logs in the terminal needs use of a `--debug` CLI switch.
- Never use `print()` or `console.print()` for logging/debugging output.
