"""Hook PostToolUse: aplica Ruff (lint + format) al archivo Python que editó el agente."""

import json
import subprocess
import sys
from pathlib import Path

RUFF_STEPS = (["check", "--fix"], ["format"])


def run_ruff(path: Path, root: Path) -> None:
    for step in RUFF_STEPS:
        cmd = ["uv", "run", "ruff", *step, "--force-exclude", str(path)]
        try:
            result = subprocess.run(
                cmd,
                cwd=root,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            sys.stderr.write(f"No se pudo ejecutar uv: {error}\n")
            return
        if result.returncode != 0:
            sys.stderr.write(f"ruff {step[0]}:\n{result.stdout}{result.stderr}")


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        event = {}

    if not event.get("error"):
        args = (event.get("toolCall") or {}).get("args") or {}
        raw = args.get("TargetFile")
        workspaces = [Path(p).resolve() for p in event.get("workspacePaths", [])]

        if raw and workspaces:
            path = (workspaces[0] / raw).resolve()  # si raw es absoluto, se respeta
            root = next(
                (w for w in workspaces if path.is_relative_to(w)), workspaces[0]
            )
            if path.suffix in {".py", ".pyi"} and path.is_file():
                run_ruff(path, root)

    print("{}")  # PostToolUse debe devolver un objeto JSON vacío


if __name__ == "__main__":
    main()
