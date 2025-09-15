from __future__ import annotations

import argparse
import shutil
import sysconfig
from pathlib import Path
from typing import Iterable, Sequence

_NOTEBOOK_SHARE_SUBDIR: Sequence[str] = ("share", "ccf_map", "notebooks")


def _notebook_source_dir() -> Path:
    """Return the path where the wheel installs bundled notebooks."""
    base = Path(sysconfig.get_path("data"))
    src = base.joinpath(*_NOTEBOOK_SHARE_SUBDIR)
    if not src.exists():
        raise FileNotFoundError(
            f"No notebooks found at {src}. Did you install the package with the 'notebooks' extra?"
        )
    return src


def copy_notebooks(destination: str | Path = ".", *, overwrite: bool = False) -> list[Path]:
    """Copy packaged notebooks into *destination* and return the written paths."""
    src = _notebook_source_dir()
    target_dir = Path(destination).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    for notebook in sorted(src.glob("*.ipynb")):
        target = target_dir / notebook.name
        if target.exists() and not overwrite:
            continue
        shutil.copy2(notebook, target)
        copied.append(target)
    if not copied:
        pattern = "overwrote" if overwrite else "copied"
        raise FileExistsError(
            f"No notebooks {pattern}. Files already exist in {target_dir}. "
            "Use --overwrite to replace them."
        )
    return copied


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Copy bundled CCF MAP notebooks into your working directory."
    )
    parser.add_argument(
        "destination",
        nargs="?",
        default=".",
        help="Folder to place the notebooks (defaults to current directory).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite files if they already exist in the destination.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        copied = copy_notebooks(args.destination, overwrite=args.overwrite)
    except FileNotFoundError as exc:
        parser.exit(status=1, message=f"error: {exc}\n")
    except FileExistsError as exc:
        parser.exit(status=1, message=f"error: {exc}\n")

    dest = copied[0].parent if copied else Path(args.destination)
    parser.exit(message=f"Copied {len(copied)} notebooks to {dest}\n")


if __name__ == "__main__":
    main()
