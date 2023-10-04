"""Tests related to a kitchen that was already frozen and had spices on some meals."""
import pytest

from mrchef import lib

from .conftest import get_frozen_config, get_user_config

PATCH2 = """
From f6bd49c44dd50a658fd42e0122b96d4bf59bdd92 Mon Sep 17 00:00:00 2001
From: Jairo Llopis <yajo.sk8@gmail.com>
Date: Tue, 7 Feb 2023 13:47:24 +0000
Subject: [PATCH] adding a 2nd patch

---
 testfile | 1 +
 1 file changed, 1 insertion(+)

diff --git a/testfile b/testfile
index d9efd14..0611af9 100644
--- a/testfile
+++ b/testfile
@@ -1 +1,2 @@
 local patch
+2nd local patch
--
2.39.0
"""


@pytest.mark.impure
def test_warmup_check(assets_copy, assets_orig):
    lib.Worker(assets_copy).warmup()
    lib.Worker(assets_copy).check()
    # Nothing changed, so frozen file should stay the same
    new_freezer = get_frozen_config(assets_copy)
    old_freezer = get_frozen_config(assets_orig)
    assert new_freezer == old_freezer


@pytest.mark.impure
def test_spice_rm(assets_copy):
    """Removing a spice works as expected."""
    removed = "https://github.com/copier-org/autopretty/commit/d46b05b4cff321425e97cc4a04bd1950332a898b.patch"
    worker = lib.Worker(assets_copy)
    worker.warmup()
    worker.spice_rm(assets_copy / "code" / "autopretty", removed)
    user_config = get_user_config(assets_copy)
    assert user_config["meals"]["autopretty"]["spices"] == [
        "https://github.com/copier-org/autopretty/commit/2a748b2fc8c378746a1f9f796785210e682157d4.patch",
        "./000-local.patch",
    ]
    freezer = get_frozen_config(assets_copy)
    assert removed not in freezer["spices"]
    assert removed not in freezer["patch2spice"].values()


@pytest.mark.impure
def test_spice_rm_missing(assets_copy):
    """Cannot remove a spice that doesn't exist."""
    lib.Worker(assets_copy).warmup()
    with pytest.raises(lib.MrChefError):
        lib.Worker(assets_copy).spice_rm(
            assets_copy / "code" / "autopretty", "https://foo"
        )


def test_spice_export(assets_copy):
    """Exporting spice content works as expected."""
    expected = assets_copy.joinpath("000-local.patch").read_text()
    assert lib.Worker(assets_copy).spice_export("./000-local.patch") == expected


@pytest.mark.impure
def test_spice_updated(assets_copy):
    # Restore last freeze
    lib.Worker(assets_copy).warmup()
    # Imagine the patch changed because upstream pushed a new commit to the PR
    with assets_copy.joinpath("000-local.patch").open("a") as fd:
        fd.write(PATCH2)
    autopretty = assets_copy / "code" / "autopretty"
    # Remove outdated spice
    lib.Worker(assets_copy).spice_rm(
        autopretty,
        "https://github.com/copier-org/autopretty/commit/2a748b2fc8c378746a1f9f796785210e682157d4.patch",
    )
    # Update the meal
    lib.Worker(assets_copy).update(autopretty)
    assert (
        autopretty.joinpath("testfile").read_text() == "local patch\n2nd local patch\n"
    )
