"""Tests for a metarepo that was already frozen in the past."""
from textwrap import dedent

import pytest
from git_find_repos import is_git_repo
from plumbum import ProcessExecutionError
from plumbum.cmd import git

from mrchef import lib

from .conftest import get_frozen_config, get_user_config


@pytest.mark.impure
def test_warmup_check_freeze(assets_copy, assets_orig):
    autopretty_dir = assets_copy / "code" / "autopretty"
    # Warm
    worker = lib.Worker(assets_copy)
    worker.warmup()
    assert is_git_repo(autopretty_dir)
    assert lib.git_branch(autopretty_dir) == "main"
    assert lib.git_rev(autopretty_dir) == "56d43ec053fb1969a2450c569d6b8127531942d3"
    assert (
        lib.git_origin(autopretty_dir) == "https://github.com/copier-org/autopretty.git"
    )
    # Check
    worker.check()
    # Freezing changes nothing
    worker.freeze()
    new_freezer = get_frozen_config(assets_copy)
    old_freezer = get_frozen_config(assets_orig)
    assert new_freezer == old_freezer


@pytest.mark.impure
def test_spice_add(assets_copy):
    autopretty_dir = assets_copy / "code" / "autopretty"
    patch_url = "https://github.com/copier-org/autopretty/commit/2a748b2fc8c378746a1f9f796785210e682157d4.patch"
    patch_id = "3f0f5ee4068db2f5be5ba554035ae44bd0a5647a"
    patch_text = dedent(
        """\
        From 2a748b2fc8c378746a1f9f796785210e682157d4 Mon Sep 17 00:00:00 2001
        From: Jairo Llopis <yajo.sk8@gmail.com>
        Date: Fri, 23 Oct 2020 10:26:23 +0100
        Subject: [PATCH] Pin pre-commit language versions

        It helps prevent https://github.com/prettier/prettier/issues/9459.
        ---
         .pre-commit-config.yaml       | 3 +++
         .pre-commit-config.yaml.jinja | 3 +++
         2 files changed, 6 insertions(+)

        diff --git a/.pre-commit-config.yaml b/.pre-commit-config.yaml
        index 505e718..c08d0f4 100644
        --- a/.pre-commit-config.yaml
        +++ b/.pre-commit-config.yaml
        @@ -1,3 +1,6 @@
        +default_language_version:
        +  python: python3
        +  node: "14.14.0"
         repos:
           # General
           - repo: local
        diff --git a/.pre-commit-config.yaml.jinja b/.pre-commit-config.yaml.jinja
        index 7afddaf..5756970 100644
        --- a/.pre-commit-config.yaml.jinja
        +++ b/.pre-commit-config.yaml.jinja
        @@ -1,3 +1,6 @@
        +default_language_version:
        +  python: python3
        +  node: "14.14.0"
         repos:
           # General
           - repo: local
        """
    )
    # Warm
    worker = lib.Worker(assets_copy)
    worker.warmup()
    # Spice
    worker.spice_add(autopretty_dir, patch_url)
    # Assertions
    user_config = get_user_config(assets_copy)
    assert user_config["meals"]["autopretty"]["spices"] == [patch_url]
    freezer = get_frozen_config(assets_copy)
    assert freezer["spices"][patch_url] == patch_text
    assert freezer["patch2spice"][patch_id] == patch_url


@pytest.mark.impure
def test_manual_spice_add_remove(assets_copy):
    autopretty_dir = assets_copy / "code" / "autopretty"
    thing = autopretty_dir / "thing"
    nothing = autopretty_dir / "nothing"
    # Warmup
    lib.Worker(assets_copy).warmup()
    # Manual edits
    thing.write_text("stuff")
    git("-C", autopretty_dir, "add", "thing")
    git("-C", autopretty_dir, "commit", "-m", "Thing & stuff")
    nothing.write_text("emptiness")
    git("-C", autopretty_dir, "add", "nothing")
    git("-C", autopretty_dir, "commit", "-m", "Nothing & emptiness")
    # Manual freeze
    lib.Worker(assets_copy).freeze()
    # Things are frozen
    assert thing.read_text() == "stuff"
    assert nothing.read_text() == "emptiness"
    assert assets_copy.joinpath("code", "mrchef-000.patch").exists()
    assert assets_copy.joinpath("code", "mrchef-001.patch").exists()
    user_config = get_user_config(assets_copy)
    assert user_config["meals"]["autopretty"]["spices"] == [
        "code/mrchef-000.patch",
        "code/mrchef-001.patch",
    ]
    # Remove a spice
    lib.Worker(assets_copy).spice_rm(autopretty_dir, "code/mrchef-000.patch")
    assert not thing.exists()
    assert nothing.read_text() == "emptiness"
    assert not assets_copy.joinpath("code", "mrchef-000.patch").exists()
    assert assets_copy.joinpath("code", "mrchef-001.patch").exists()
    user_config = get_user_config(assets_copy)
    assert user_config["meals"]["autopretty"]["spices"] == ["code/mrchef-001.patch"]


@pytest.mark.parametrize(
    "spice_url",
    (
        "https://github.com/copier-org/autopretty/commit/276a0941916c6e9fe4184fdd719fdc241dc7ff57.patch",
        "https://github.com/copier-org/autopretty/commit/276a0941916c6e9fe4184fdd719fdc241dc7ff57",
        "https://github.com/copier-org/autopretty/commit/276a0941916c6e9fe4184fdd719fdc241dc7ff57/",
        "https://github.com/copier-org/autopretty/pull/7.patch",
        "https://github.com/copier-org/autopretty/pull/7",
        "https://github.com/copier-org/autopretty/pull/7/",
        "https://gitlab.com/recallstack/recallstack.gitlab.io/-/commit/a06f912857b8c9d47c7b64f89a775f59b0cfc62d.patch",
        "https://gitlab.com/recallstack/recallstack.gitlab.io/-/commit/a06f912857b8c9d47c7b64f89a775f59b0cfc62d",
        "https://gitlab.com/recallstack/recallstack.gitlab.io/-/commit/a06f912857b8c9d47c7b64f89a775f59b0cfc62d/",
        "https://gitlab.com/recallstack/recallstack.gitlab.io/-/merge_requests/34.patch",
        "https://gitlab.com/recallstack/recallstack.gitlab.io/-/merge_requests/34",
        "https://gitlab.com/recallstack/recallstack.gitlab.io/-/merge_requests/34/",
    ),
)
@pytest.mark.impure
def test_spice_add_transform(assets_copy, spice_url):
    """Test several patch URL formats, and see if they all work."""
    worker = lib.Worker(assets_copy)
    worker.warmup()
    worker.spice_add(assets_copy / "code" / "autopretty", spice_url)


@pytest.mark.impure
def test_unreachable(assets_copy):
    """Remote is temporarily unreachable; no garbage left for next runs."""
    config = assets_copy / "mrchef.toml"
    lib.Worker(assets_copy).warmup()
    # Write to non-existing remote, to emulate an unreachable remote
    original_config = config.read_text()
    config.write_text(
        original_config.replace("https://github.com", "https://not-github.example.com")
    )
    with pytest.raises(ProcessExecutionError):
        lib.Worker(assets_copy).update()
    # Restore URL to emulate remote being back online
    config.write_text(original_config)
    lib.Worker(assets_copy).update()
