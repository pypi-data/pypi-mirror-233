from pathlib import Path

import pytest

from mrchef import lib

from .conftest import SAMPLE_REPOS

BUNDLE123 = SAMPLE_REPOS / "123.bundle"


def test_warmup(tmp_path):
    """Generate a kitchen and warm it up."""
    tmp_path.joinpath(lib.CONFIG_FILE).write_text(
        f"""
        version = 1
        kitchen = "."

        [meals.one]
        url = "{BUNDLE123}"
        branch = "main"

        [meals.two]
        url = "{BUNDLE123}"
        branch = "main"

        [meals.three]
        url = "{BUNDLE123}"
        branch = "main"
        """
    )
    tmp_path.joinpath(lib.FREEZER_FILE).write_text(
        """
        version = 1
        [meals.one]
        rev = "b72639b17d5882c2ce1448f7ed452e596dbe6acd"
        [meals.two]
        rev = "a6cf33141a9f770967e3c132e0aa0071c3db2d43"
        [meals.three]
        rev = "e757a53dccbb5407994f03dc419651275dc6eacf"
        """
    )
    lib.Worker(tmp_path).warmup()
    assert tmp_path.joinpath("one", "file-1.txt").read_text() == "1\n"
    assert not tmp_path.joinpath("one", "file-2.txt").exists()
    assert not tmp_path.joinpath("one", "file-3.txt").exists()
    assert tmp_path.joinpath("two", "file-1.txt").read_text() == "1\n"
    assert tmp_path.joinpath("two", "file-2.txt").read_text() == "2\n"
    assert not tmp_path.joinpath("two", "file-3.txt").exists()
    assert tmp_path.joinpath("three", "file-1.txt").read_text() == "1\n"
    assert tmp_path.joinpath("three", "file-2.txt").read_text() == "2\n"
    assert tmp_path.joinpath("three", "file-3.txt").read_text() == "3\n"


def test_double_warmup_discards_changes(tmp_path: Path):
    tmp_path.joinpath(lib.CONFIG_FILE).write_text(
        f"""
        version = 1
        kitchen = "code"

        [meals.one]
        url = "{BUNDLE123}"
        branch = "main"
        """
    )
    tmp_path.joinpath(lib.FREEZER_FILE).write_text(
        """
        version = 1
        [meals.one]
        rev = "b72639b17d5882c2ce1448f7ed452e596dbe6acd"
        """
    )
    code = tmp_path / "code"
    one = code / "one"
    thing = one / "thing"
    nothing = one / "nothing"
    # Warmup
    lib.Worker(tmp_path).warmup()
    # Manual edits
    thing.write_text("stuff")
    _git = lib.git(one)
    _git("add", "thing")
    _git("commit", "-m", "Thing & stuff")
    nothing.write_text("emptiness")
    _git("add", "nothing")
    _git("commit", "-m", "Nothing & emptiness")
    # Warmup again
    lib.Worker(tmp_path).warmup()
    # Things are frozen
    assert one.joinpath("file-1.txt").read_text() == "1\n"
    assert not one.joinpath("file-2.txt").exists()
    assert not one.joinpath("file-3.txt").exists()
    assert not thing.exists()
    assert not nothing.exists()
    assert not list(code.glob("*.patch"))


@pytest.mark.parametrize("updated_meal", ("one", "two", "three"))
def test_single_meal_update(tmp_path, updated_meal: str):
    test_warmup(tmp_path)
    expected = lib.Worker(tmp_path).config_frozen
    lib.Worker(tmp_path).update(tmp_path / updated_meal)
    # It is expected that the updated meal contains the same rev as meal "three"
    expected["meals"][updated_meal]["rev"] = "e757a53dccbb5407994f03dc419651275dc6eacf"
    assert expected == lib.Worker(tmp_path).config_frozen


def test_subfolder_add(tmp_path: Path):
    tmp_path.joinpath(lib.CONFIG_FILE).write_text(
        f"""
        version = 1
        kitchen = "kitchen"

        [meals."1/123"]
        url = "{BUNDLE123}"
        branch = "main"
        """
    )
    tmp_path.joinpath(lib.FREEZER_FILE).write_text(
        """
        version = 1
        [meals."1/123"]
        rev = "b72639b17d5882c2ce1448f7ed452e596dbe6acd"
        """
    )
    lib.Worker(tmp_path).warmup()
    lib.Worker(tmp_path).meal_add(
        tmp_path / "kitchen" / "2" / "123", str(BUNDLE123), "main"
    )
    worker = lib.Worker(tmp_path)
    assert worker.config_user["meals"]["1/123"]["url"] == str(BUNDLE123)
    assert worker.config_user["meals"]["1/123"]["branch"] == "main"
    assert worker.config_user["meals"]["2/123"]["url"] == str(BUNDLE123)
    assert worker.config_user["meals"]["2/123"]["branch"] == "main"
    assert (
        worker.config_frozen["meals"]["1/123"]["rev"]
        == "b72639b17d5882c2ce1448f7ed452e596dbe6acd"
    )
    assert (
        worker.config_frozen["meals"]["2/123"]["rev"]
        == "e757a53dccbb5407994f03dc419651275dc6eacf"
    )
