@echo off
REM Windows CMD / PowerShell entry point for the quality gate.
REM Logic lives in guard-my-code.py.
uv run python guard-my-code.py %*
