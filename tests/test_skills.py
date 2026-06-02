"""Tests for fleet_deepagents_export.skills."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from fleet_deepagents_export import StaticSkillsLoader
from fleet_deepagents_export.skills import _scan


SKILL_MD = dedent(
    """\
    ---
    name: demo
    description: a demo skill
    ---
    body
    """
)


def _write_skill(root: Path, name: str = "demo") -> Path:
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(SKILL_MD)
    return skill_dir


# --- _scan ------------------------------------------------------------------


def test_scan_happy_path(tmp_path: Path):
    skill = _write_skill(tmp_path)
    (skill / "support.txt").write_text("hello")
    files, metadata = _scan([(tmp_path, "/skills/x")])

    assert set(files) == {"/skills/x/demo/SKILL.md", "/skills/x/demo/support.txt"}
    assert len(metadata) == 1
    assert metadata[0]["name"] == "demo"
    assert metadata[0]["path"] == "/skills/x/demo/SKILL.md"


def test_scan_skips_top_level_files(tmp_path: Path):
    _write_skill(tmp_path)
    (tmp_path / "README.md").write_text("top-level, should be skipped")
    files, _ = _scan([(tmp_path, "/skills/x")])

    assert "/skills/x/README.md" not in files


def test_scan_skips_undecodable_files(tmp_path: Path):
    skill = _write_skill(tmp_path)
    (skill / "binary.bin").write_bytes(b"\x80\x81\x82")
    files, _ = _scan([(tmp_path, "/skills/x")])

    assert "/skills/x/demo/binary.bin" not in files
    assert "/skills/x/demo/SKILL.md" in files


# --- StaticSkillsLoader.skill_paths -----------------------------------------


def test_skill_paths_filters_missing_keeps_existing(tmp_path: Path):
    real = tmp_path / "real"
    real.mkdir()
    empty = tmp_path / "empty"
    empty.mkdir()
    missing = tmp_path / "missing"  # not created

    loader = StaticSkillsLoader(
        [
            (real, "/skills/real"),
            (empty, "/skills/empty"),
            (missing, "/skills/missing"),
        ]
    )
    assert loader.skill_paths == ["/skills/real", "/skills/empty"]


# --- StaticSkillsLoader.before_agent ----------------------------------------


def _loader_with_one_skill(tmp_path: Path) -> StaticSkillsLoader:
    _write_skill(tmp_path)
    return StaticSkillsLoader([(tmp_path, "/skills/x")])


def test_before_agent_injects_on_empty_state(tmp_path: Path):
    loader = _loader_with_one_skill(tmp_path)
    update = loader.before_agent({}, runtime=None)

    assert update is not None
    assert update["files"] == loader.files
    assert update["skills_metadata"] == loader.metadata


def test_before_agent_injects_when_caller_provided_unrelated_files(tmp_path: Path):
    """Regression: caller-provided files must not suppress injection."""
    loader = _loader_with_one_skill(tmp_path)
    state = {"files": {"/user/notes.txt": {}}, "skills_metadata": []}
    update = loader.before_agent(state, runtime=None)

    assert update is not None
    assert update["files"] == loader.files
    assert update["skills_metadata"] == loader.metadata


def test_before_agent_returns_none_when_fully_injected(tmp_path: Path):
    loader = _loader_with_one_skill(tmp_path)
    state = {"files": dict(loader.files), "skills_metadata": loader.metadata}
    assert loader.before_agent(state, runtime=None) is None
