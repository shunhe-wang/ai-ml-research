from pathlib import Path

from rule_carryover.provenance import directory_file_hashes, source_snapshot


def test_source_snapshot_changes_when_executable_source_changes(tmp_path: Path) -> None:
    (tmp_path / "src" / "package").mkdir(parents=True)
    (tmp_path / "src" / "package" / "module.py").write_text("VALUE = 1\n")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='example'\n")
    (tmp_path / "uv.lock").write_text("version = 1\n")
    (tmp_path / "unrelated.txt").write_text("not executable provenance\n")

    first = source_snapshot(tmp_path)
    (tmp_path / "unrelated.txt").write_text("changed but still unrelated\n")
    unrelated_change = source_snapshot(tmp_path)
    (tmp_path / "src" / "package" / "module.py").write_text("VALUE = 2\n")
    source_change = source_snapshot(tmp_path)

    assert first.sha256 == unrelated_change.sha256
    assert first.paths == ("pyproject.toml", "src/package/module.py", "uv.lock")
    assert source_change.sha256 != first.sha256


def test_directory_file_hashes_cover_weights_tokenizer_config_and_template(
    tmp_path: Path,
) -> None:
    (tmp_path / "model.safetensors").write_bytes(b"weights")
    (tmp_path / "tokenizer.json").write_text('{"tokenizer":1}\n')
    (tmp_path / "config.json").write_text('{"model":1}\n')
    (tmp_path / "chat_template.jinja").write_text("{{ messages }}\n")

    first = directory_file_hashes(tmp_path)
    (tmp_path / "tokenizer.json").write_text('{"tokenizer":2}\n')
    second = directory_file_hashes(tmp_path)

    assert set(first) == {
        "chat_template.jinja",
        "config.json",
        "model.safetensors",
        "tokenizer.json",
    }
    assert first["model.safetensors"] == second["model.safetensors"]
    assert first["tokenizer.json"] != second["tokenizer.json"]
