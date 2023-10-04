import pytest

from mrchef import lib

from .conftest import get_frozen_config


@pytest.mark.impure
def test_warmup_check_freeze(assets_copy, assets_orig):
    lib.Worker(assets_copy).warmup()
    with pytest.raises(lib.MrChefError, match=r"Freezer is outdated"):
        lib.Worker(assets_copy).check()
    # Nothing changed, so frozen file should stay the same
    new_freezer = get_frozen_config(assets_copy)
    old_freezer = get_frozen_config(assets_orig)
    assert new_freezer == old_freezer
    # Update freezer, check should pass this time
    lib.Worker(assets_copy).freeze()
    lib.Worker(assets_copy).check()
