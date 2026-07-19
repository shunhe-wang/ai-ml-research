from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceSnapshot:
    sha256: str
    paths: tuple[str, ...]


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def directory_file_hashes(root: Path) -> dict[str, str]:
    """Hash every file in an external artifact directory by relative path."""
    if not root.is_dir():
        raise ValueError(f"artifact directory does not exist: {root}")
    files = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    return {
        path.relative_to(root).as_posix(): _file_sha256(path)
        for path in files
    }


def source_snapshot(root: Path) -> SourceSnapshot:
    """Hash the exact executable project inputs independently of Git state."""
    candidates = [root / "pyproject.toml", root / "uv.lock"]
    source_root = root / "src"
    if source_root.is_dir():
        candidates.extend(path for path in source_root.rglob("*") if path.is_file())
    files = sorted(
        (path for path in candidates if path.is_file() and "__pycache__" not in path.parts),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    digest = hashlib.sha256()
    relative_paths = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        relative_paths.append(relative)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return SourceSnapshot(sha256=digest.hexdigest(), paths=tuple(relative_paths))


def git_source_snapshot(root: Path, commit: str, paths: tuple[str, ...]) -> SourceSnapshot:
    """Reconstruct a source snapshot from the immutable Git objects named by a run."""
    digest = hashlib.sha256()
    for relative in paths:
        content = subprocess.check_output(
            ["git", "show", f"{commit}:{relative}"],
            cwd=root,
        )
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return SourceSnapshot(sha256=digest.hexdigest(), paths=paths)


def git_is_dirty(root: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout)


def git_paths_are_dirty(root: Path, paths: tuple[str, ...]) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "--", *paths],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout)
