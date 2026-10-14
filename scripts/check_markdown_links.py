"""Fail when a repository-relative Markdown file link does not resolve."""

from __future__ import annotations

import os
import re
from pathlib import Path

LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
EXCLUDED_DIR_NAMES = frozenset({".git", ".venv", "node_modules", "var"})


def iter_markdown_files(root: Path):
    """Yield authored Markdown files below ``root`` in deterministic order."""

    for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        dirnames[:] = sorted(dirname for dirname in dirnames if dirname not in EXCLUDED_DIR_NAMES)
        for filename in sorted(filenames):
            if filename.endswith(".md"):
                yield Path(directory, filename)


def check_markdown_links(root: Path) -> list[str]:
    failures: list[str] = []
    for markdown in iter_markdown_files(root):
        for target in LINK.findall(markdown.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            file_target = target.split("#", 1)[0]
            if file_target and not (markdown.parent / file_target).resolve().is_file():
                failures.append(f"{markdown.relative_to(root)} -> {target}")
    return failures


def main(root: Path | None = None) -> int:
    root = root or Path(__file__).resolve().parents[1]
    failures = check_markdown_links(root)
    if failures:
        print("Broken Markdown links:\n" + "\n".join(failures))
        return 1
    print("Markdown links: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
