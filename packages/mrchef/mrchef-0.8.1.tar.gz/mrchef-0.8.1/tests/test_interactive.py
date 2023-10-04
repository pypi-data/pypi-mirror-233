"""Tests that imitate a human chef working in the kitchen."""

from textwrap import dedent

import pytest
from git_find_repos import is_git_repo
from plumbum import local

from mrchef import lib

from .conftest import cli_run, get_frozen_config, get_user_config


def test_update(tmp_path_factory):
    """Update works as expected."""
    # Create a couple of remote repositories
    remote1 = tmp_path_factory.mktemp("remote1")
    remote1.joinpath("file1").write_text("hello 1")
    git1 = lib.git(remote1)
    git1("init")
    git1("switch", "--create", "branch1")
    git1("add", "-A")
    git1("commit", "--message", "hello 1")
    remote1_commit = lib.git_rev(remote1)
    remote2 = tmp_path_factory.mktemp("remote2")
    remote2.joinpath("file2").write_text("hello 2")
    git2 = lib.git(remote2)
    git2("init")
    git2("switch", "--create", "branch2")
    git2("add", "-A")
    git2("commit", "--message", "hello 2")
    remote2_commit = lib.git_rev(remote2)
    # Create a metarepo where we will include those other repositories
    metarepo = tmp_path_factory.mktemp("metarepo")
    metarepo.joinpath(lib.CONFIG_FILE).write_text(
        dedent(
            f"""\
            version = 1
            kitchen = '.'

            [meals.r1]
            url = '{remote1}'
            branch = 'branch1'

            [meals.r2]
            url = "{remote2}"
            branch = "branch2"
            """
        )
    )
    # Assert they get included properly, both hot and cold
    with pytest.warns(UserWarning, match="Freezer file not found."):
        cli_run("-s", metarepo, "warmup")
    r1, r2 = map(metarepo.joinpath, ("r1", "r2"))
    assert r1.joinpath("file1").read_text() == "hello 1"
    assert r2.joinpath("file2").read_text() == "hello 2"
    with pytest.warns(UserWarning, match="Freezer file not found."):
        cli_run(f"-s{metarepo}", "freeze")
    with local.cwd(metarepo):
        cli_run("check")
    freezer = get_frozen_config(metarepo)
    assert lib.git_rev(r1) == remote1_commit == freezer["meals"]["r1"]["rev"]
    assert lib.git_rev(r2) == remote2_commit == freezer["meals"]["r2"]["rev"]
    # Remote 1 gets updated in the same branch
    remote1.joinpath("file1").write_text("bye 1")
    git1("commit", "--all", "--message", "bye 1")
    remote1_commit = lib.git_rev(remote1)
    # Remote 2 gets updated in a separate branch
    git2("switch", "--create", "feature-branch2")
    remote2.joinpath("file2").write_text("bye 2")
    git2("commit", "--all", "--message", "bye 2")
    # Assert metarepo gets properly updated
    cli_run("--starting-folder", metarepo, "update")
    assert r1.joinpath("file1").read_text() == "bye 1"
    assert r2.joinpath("file2").read_text() == "hello 2"
    cli_run(f"--starting-folder={metarepo}", "check")
    freezer = get_frozen_config(metarepo)
    assert lib.git_rev(r1) == remote1_commit == freezer["meals"]["r1"]["rev"]
    assert lib.git_rev(r2) == remote2_commit == freezer["meals"]["r2"]["rev"]
    # Cook local patch in r2
    r2.joinpath("local-patch").write_text("doing local stuff")
    lib.git(r2)("add", "-A")
    lib.git(r2)("commit", "--message", "local patch")
    # Store local patch in freezer
    cli_run("-s", metarepo, "freeze")
    user_config = get_user_config(metarepo)
    assert user_config["meals"]["r2"]["spices"] == ["mrchef-000.patch"]
    freezer = get_frozen_config(metarepo)
    assert lib.git_rev(r2) != remote2_commit
    assert freezer["meals"]["r2"]["rev"] == remote2_commit
    assert "mrchef-000.patch" in freezer["spices"]
    assert (
        freezer["patch2spice"]["a15fab655cfe7a15843560a4d8fa6b082ea4a3ea"]
        == "mrchef-000.patch"
    )


@pytest.mark.impure
def test_init_meal_add_spice_add_meal_rm(tmp_path):
    """Init a kitchen, add meal, spice it up, remove it."""
    initial_user_config = {"version": 1, "kitchen": "kitchen"}
    fork = tmp_path / "kitchen" / "autopretty"
    url = "https://github.com/copier-org/autopretty.git"
    branch = "main"
    rev = "56d43ec053fb1969a2450c569d6b8127531942d3"
    spice_url = "https://github.com/copier-org/autopretty/commit/d46b05b4cff321425e97cc4a04bd1950332a898b.patch"
    patch_id = "c4375da54e7826f0848f9865f02a0abe31e4cf0a"
    with local.cwd(tmp_path):
        # Init kitchen
        cli_run("init")
        user_config = get_user_config(tmp_path)
        assert user_config == initial_user_config
        # Add new meal
        cli_run("meal-add", fork, url, branch, rev)
        assert is_git_repo(fork)
        assert lib.git_rev(fork) == rev
        user_config = get_user_config(tmp_path)
        assert user_config == {
            "version": 1,
            "kitchen": "kitchen",
            "meals": {
                "autopretty": {
                    "url": url,
                    "branch": branch,
                    "rev": rev,
                }
            },
        }
        freezer = get_frozen_config(tmp_path)
        assert freezer == {
            "version": 1,
            "meals": {"autopretty": {"rev": rev}},
            "spices": {},
            "patch2spice": {},
        }
        cli_run("check")
        # Spice up meal
        cli_run("spice-add", fork, spice_url)
        user_config = get_user_config(tmp_path)
        assert user_config == {
            "version": 1,
            "kitchen": "kitchen",
            "meals": {
                "autopretty": {
                    "url": url,
                    "branch": branch,
                    "rev": rev,
                    "spices": [spice_url],
                }
            },
        }
        freezer = get_frozen_config(tmp_path)
        assert freezer["meals"]["autopretty"]["rev"] == rev
        assert spice_url in freezer["spices"]
        assert freezer["patch2spice"][patch_id] == spice_url
        # Remove meal
        cli_run("meal-rm", fork)
        assert not fork.exists()
        user_config = get_user_config(tmp_path)
        assert "autopretty" not in user_config.get("meals", {})
        freezer = get_frozen_config(tmp_path)
        assert freezer == {"meals": {}, "spices": {}, "patch2spice": {}, "version": 1}
