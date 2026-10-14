from __future__ import annotations

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "check_markdown_links.py"
SPEC = spec_from_file_location("check_markdown_links", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_generated_directories_are_pruned_without_reading_them(tmp_path: Path) -> None:
    for directory in (".git", ".venv", "node_modules", "var", "apps/example/node_modules"):
        ignored = tmp_path / directory / "broken.md"
        ignored.parent.mkdir(parents=True, exist_ok=True)
        ignored.write_bytes(b"\xff")

    assert MODULE.check_markdown_links(tmp_path) == []


def test_authored_boundaries_and_similar_directory_names_are_checked(tmp_path: Path) -> None:
    for relative in (
        "apps/example/docs/broken.md",
        ".agent/broken.md",
        ".codex/broken.md",
        "variables/broken.md",
        "various/broken.md",
        "node_modules-guide/broken.md",
    ):
        write(tmp_path / relative, "[missing](missing.md)\n")

    assert MODULE.check_markdown_links(tmp_path) == [
        ".agent/broken.md -> missing.md",
        ".codex/broken.md -> missing.md",
        "apps/example/docs/broken.md -> missing.md",
        "node_modules-guide/broken.md -> missing.md",
        "variables/broken.md -> missing.md",
        "various/broken.md -> missing.md",
    ]


def test_valid_relative_fragment_and_external_links_pass(tmp_path: Path) -> None:
    write(tmp_path / "docs/target.md", "# Target\n")
    write(
        tmp_path / "docs/source.md",
        "[relative](target.md) [fragment](#target) [web](https://example.com) "
        "[mail](mailto:a@example.com)\n",
    )

    assert MODULE.check_markdown_links(tmp_path) == []


def test_root_beneath_var_parent_is_still_checked(tmp_path: Path) -> None:
    root = tmp_path / "var" / "checkout"
    write(root / "docs/broken.md", "[missing](missing.md)\n")

    assert MODULE.check_markdown_links(root) == ["docs/broken.md -> missing.md"]


def test_main_reports_success_and_failure(tmp_path: Path, capsys) -> None:
    write(tmp_path / "node_modules/package/broken.md", "[missing](missing.md)\n")
    assert MODULE.main(tmp_path) == 0
    assert capsys.readouterr().out == "Markdown links: passed\n"

    write(tmp_path / "docs/broken.md", "[missing](missing.md)\n")
    assert MODULE.main(tmp_path) == 1
    assert capsys.readouterr().out == "Broken Markdown links:\ndocs/broken.md -> missing.md\n"
