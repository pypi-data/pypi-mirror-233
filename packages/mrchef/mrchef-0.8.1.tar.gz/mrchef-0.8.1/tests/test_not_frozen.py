from textwrap import dedent

import pytest
from git_find_repos import is_git_repo

from mrchef import lib

# Avoid expected warnings because these tests are for an unfrozen kitchen
pytestmark = pytest.mark.filterwarnings("ignore:Freezer file not found.:UserWarning")


@pytest.mark.impure
def test_check(assets_copy):
    """Check must fail when not frozen."""
    lib.Worker(assets_copy).warmup()
    with pytest.raises(lib.MrChefError, match=r"Freezer not found"):
        lib.Worker(assets_copy).check()


@pytest.mark.impure
def test_freeze(assets_copy, assets_orig):
    """Freeze a metarepo that was not frozen before."""
    assert not assets_copy.joinpath(lib.FREEZER_FILE).exists()
    # Download code; there's no freezer
    lib.Worker(assets_copy).warmup()
    assert is_git_repo(assets_copy / "code" / "autopretty1")
    assert is_git_repo(assets_copy / "code" / "autopretty2")
    # Generate freezer for the 1st time
    lib.Worker(assets_copy).freeze()
    new_freezer = assets_copy.joinpath(lib.FREEZER_FILE).read_text()
    expected_freezer = assets_orig.joinpath("expected-freezer.toml").read_text()
    assert new_freezer == expected_freezer


@pytest.mark.impure
def test_spice_add_respects_comments(assets_copy):
    """Auto-adding spice respects comments made by humans in the config file."""
    lib.Worker(assets_copy).warmup()
    lib.Worker(assets_copy).spice_add(
        assets_copy / "code" / "autopretty1",
        "https://github.com/copier-org/autopretty/commit/2a748b2fc8c378746a1f9f796785210e682157d4.patch",
    )
    expected_user_config = dedent(
        """\
        version = 1
        kitchen = 'code'

        [meals.autopretty1]
        url = 'https://github.com/copier-org/autopretty.git'
        branch = "main"
        rev = "56d43ec053fb1969a2450c569d6b8127531942d3" # Hand-pinned forever
        spices = [
          # Allow commit to branch
          'https://github.com/copier-org/autopretty/commit/d46b05b4cff321425e97cc4a04bd1950332a898b.patch',
          "https://github.com/copier-org/autopretty/commit/2a748b2fc8c378746a1f9f796785210e682157d4.patch",
        ]

        [meals.autopretty2]
        url = 'https://github.com/copier-org/autopretty.git'
        branch = "main"
        rev = "eab06b7d666bd6ea59f757d876917f49492acbbd"
        """
    )
    real_user_config = assets_copy.joinpath(lib.CONFIG_FILE).read_text()
    assert expected_user_config == real_user_config


def test_warmup_missing_meal(assets_copy):
    """Fail if the meal you want doesn't exist."""
    with pytest.raises(lib.MrChefError):
        lib.Worker(assets_copy).warmup(assets_copy / "code" / "autopretty")


@pytest.mark.impure
def test_warmup_one_meal(assets_copy):
    """The other meal is not warmed up."""
    wanted = assets_copy / "code" / "autopretty1"
    rejected = assets_copy / "code" / "autopretty2"
    lib.Worker(assets_copy).warmup(wanted / ".." / wanted.name)
    assert is_git_repo(wanted)
    assert not rejected.exists()
