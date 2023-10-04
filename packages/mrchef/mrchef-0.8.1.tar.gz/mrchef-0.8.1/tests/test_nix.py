"""Tests for nix integration."""
import pytest
from plumbum import local

from .conftest import PROJECT_ROOT


@pytest.mark.impure
def test_nix_flake_check():
    """Run `nix flake check` and hope it works."""
    local["nix"](
        "--extra-experimental-features",
        "nix-command flakes",
        "flake",
        "check",
        PROJECT_ROOT,
    )


@pytest.mark.impure
def test_nix_flake_run():
    """Basic run of mrchef from flake."""
    cli_version = local["nix"](
        "--extra-experimental-features",
        "nix-command flakes",
        "run",
        PROJECT_ROOT,
        "--",
        "--version",
    )
    assert cli_version.startswith("mrchef ")
