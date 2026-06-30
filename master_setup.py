"""
master_setup.py — Cross-platform onboarding. Works on Linux, macOS, Windows.
Prerequisites: Python 3.12+, Docker running.
Usage: python master_setup.py
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
_USE_SUDO_FOR_DOCKER = False


def _run(
    cmd: list[str], *, check: bool = True, **kw
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True, **kw)  # noqa: S603


def _info(msg: str) -> None:
    print(f"\033[92m[setup]\033[0m {msg}")


def _warn(msg: str) -> None:
    print(f"\033[93m[warn]\033[0m  {msg}", file=sys.stderr)


def _abort(msg: str) -> None:
    print(f"\033[91m[error]\033[0m {msg}", file=sys.stderr)
    sys.exit(1)


def _needs_sudo() -> bool:
    if platform.system() == "Linux":
        sock = Path("/var/run/docker.sock")
        if sock.exists() and not os.access(sock, os.W_OK):
            return True
    return False


def _check_docker() -> None:
    global _USE_SUDO_FOR_DOCKER
    if not shutil.which("docker"):
        _abort(
            "Docker not found. Install Docker Desktop (Win/Mac) "
            "or Docker Engine (Linux)."
        )
    _USE_SUDO_FOR_DOCKER = _needs_sudo()
    if _USE_SUDO_FOR_DOCKER:
        _info("Using sudo for Docker commands (permission required).")

    cmd = ["sudo", "docker", "info"] if _USE_SUDO_FOR_DOCKER else ["docker", "info"]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, check=False)
    if result.returncode != 0:
        _abort("Docker daemon is not running. Start Docker and retry.")


def _install_uv() -> None:
    if shutil.which("uv"):
        return
    _warn("uv not found — installing...")
    if platform.system() == "Windows":
        _run(
            [
                "powershell",
                "-ExecutionPolicy",
                "ByPass",
                "-c",
                "irm https://astral.sh/uv/install.ps1 | iex",
            ]
        )
    else:
        _run(["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"])
    _add_uv_to_path()
    if not shutil.which("uv"):
        _abort(
            "uv install failed. See: https://docs.astral.sh/uv/getting-started/installation/"
        )


def _add_uv_to_path() -> None:
    local_bin = Path.home() / ".local" / "bin"
    os.environ["PATH"] = str(local_bin) + os.pathsep + os.environ.get("PATH", "")


def _copy_env() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        shutil.copy(ROOT / ".env.example", env_file)
        _info(".env created from .env.example — edit credentials if needed.")


def _start_infra() -> None:
    _info("Starting Postgres + Redis via Docker Compose...")
    cmd = ["docker", "compose", "up", "-d", "--wait"]
    if _USE_SUDO_FOR_DOCKER:
        cmd = ["sudo"] + cmd
    _run(cmd)
    _info("Infrastructure is healthy.")


def _install_deps() -> None:
    _info("Installing Python dependencies...")
    _run(["uv", "sync", "--all-extras", "--dev"])


def _read_env_var(key: str) -> str:
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1]
    return ""


def _run_migrations() -> None:
    _info("Running migrations (main DB)...")
    _run(["uv", "run", "alembic", "upgrade", "head"])
    _info("Running migrations (test DB)...")
    env = {**os.environ, "DATABASE_URL": _read_env_var("DATABASE_TEST_URL")}
    _run(["uv", "run", "alembic", "upgrade", "head"], env=env)


def _init_secrets() -> None:
    baseline = ROOT / ".secrets.baseline"
    if not baseline.exists():
        result = _run(["uv", "run", "detect-secrets", "scan"], capture_output=True)
        baseline.write_text(result.stdout)
        _info(".secrets.baseline created.")


def _print_summary() -> None:
    _info("✅  Setup complete!")
    print()
    services = [
        ("control_mapping", "10001"),
        ("evidence_aggregator", "10002"),
        ("gap_analyzer", "10003"),
        ("resilience_scorer", "10004"),
        ("report_generator", "10005"),
        ("framework_registry", "10006"),
        ("report_publisher", "10007"),
        ("postgres", "5432"),
        ("redis", "6379"),
    ]
    print("  Service               Port")
    print("  ─────────────────     ──────")
    for name, port in services:
        print(f"  {name:<22}{port}")
    print()
    print("  Run tests : python guard-my-code.py")
    print("  Start svc : uv run uvicorn apps.<svc>.main:app --port <port> --reload")
    print()


def main() -> None:
    _check_docker()
    _install_uv()
    _copy_env()
    _start_infra()
    _install_deps()
    _run_migrations()
    _init_secrets()
    _print_summary()


if __name__ == "__main__":
    main()
