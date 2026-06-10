"""Tests for the flux-local `diff ks` command."""

import pytest

from syrupy.assertion import SnapshotAssertion

from . import run_command


@pytest.mark.parametrize(
    ("args", "env"),
    [
        (["apps", "--path", "tests/testdata/cluster"], {}),
        (["apps", "--path", "tests/testdata/cluster"], {"DIFF": "diff"}),
        (["apps", "--path", "tests/testdata/cluster", "-o", "yaml"], {}),
        (
            [
                "apps",
                "--path",
                "tests/testdata/cluster",
                "-o",
                "yaml",
                "--limit-bytes",
                "20000",
            ],
            {},
        ),
        (
            [
                "apps",
                "--path",
                "tests/testdata/cluster",
                "-o",
                "yaml",
                "--sources",
                "''",
            ],
            {},
        ),
    ],
    ids=["apps", "ks-external", "yaml", "yaml-limit", "yaml-empty-sources"],
)
async def test_diff_ks(
    args: list[str], env: dict[str, str], snapshot: SnapshotAssertion
) -> None:
    """Test test diff ks commands."""
    result = await run_command(["diff", "ks"] + args, env=env)
    assert result == snapshot


async def test_diff_ks_accepts_registry_mirror_flag() -> None:
    """Test diff ks accepts --registry-mirror for shared CLI invocations."""
    result = await run_command(
        [
            "diff",
            "ks",
            "apps",
            "--path",
            "tests/testdata/cluster",
            "--registry-mirror",
            "kind-registry:5000=registry.example.com",
        ]
    )
    assert isinstance(result, str)
