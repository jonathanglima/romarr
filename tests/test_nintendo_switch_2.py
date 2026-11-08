"""Nintendo Switch 2 (switch-2), a platform apart from the Switch."""
import pytest
from test_selection import rel

from romarr.library import import_rom
from romarr.platforms import by_slug, platform_for_file, resolve
from romarr.selection import best_release, infer_platform, judge

SWITCH, SWITCH_2 = by_slug("switch"), by_slug("switch-2")
GAME = "Mario Kart World"
OTHER = "names another platform ({})"


def test_switch_2_names_resolve_to_it():
    for name in ("Nintendo Switch 2", "Switch 2", "switch2", "switch-2"):
        assert resolve(name) is SWITCH_2, name
    assert resolve("Nintendo Switch") is SWITCH


def test_a_nup_package_imports_whole_into_switch_2(tmp_path):
    assert platform_for_file("Mario Kart World.NUP") is SWITCH_2
    assert platform_for_file("Super Mario Odyssey.nsp") is SWITCH
    source = tmp_path / "Mario Kart World.nup"
    source.write_bytes(b"synthetic package for import test")
    [result] = import_rom(source, SWITCH_2, tmp_path / "library")
    assert result.ok and result.destination.read_bytes() == source.read_bytes()
    assert "switch-2" in result.destination.parts


@pytest.mark.parametrize("title,slug", [
    ("Mario Kart World - Nintendo Switch 2", "switch-2"),
    ("Mario Kart World.nup", "switch-2"),
    ("Mario.Kart.World.Switch.2.2025-GRP", "switch-2"),
    ("Super Mario Odyssey - Nintendo Switch", "switch"),
    ("Zelda Switch 2.0 Update NSP", "switch"),
    ("Zelda Switch 2 GB NSP", "switch"),
    ("Zelda [Switch] 2 GB", "switch"),
])
def test_infer_platform_tells_them_apart(title, slug):
    assert infer_platform(rel(title)).slug == slug


def verdict(title, platform, wanted=GAME):
    return judge(rel(title), wanted, platform).verdict or "accepted"


@pytest.mark.parametrize("title,expected", [
    ("Mario Kart World - Nintendo Switch 2", OTHER.format("nintendo switch 2")),
    ("Mario.Kart.World.Nintendo.Switch.2.1080p", OTHER.format("nintendo switch 2")),
    ("Mario.Kart.World.Switch.2.2025-GRP", OTHER.format("switch 2")),
    ("Mario Kart World [NUP]", OTHER.format("nup")),
    ("Mario Kart World Switch2", OTHER.format("switch2")),
    ("Mario Kart World Nintendo Switch 2 Edition NSP", OTHER.format("nintendo switch 2")),
    ("Mario Kart World [Switch] XCI", "accepted"),
    ("Mario Kart World Switch NSZ", "accepted"),
    ("Mario Kart World - Nintendo Switch", "accepted"),
    ("Mario Kart World Switch 2.0 Update NSP", "accepted"),
    ("Mario Kart World Switch_2.0_Update NSP", "accepted"),
    ("Mario Kart World [Switch] 2 GB", "accepted"),
])
def test_a_switch_request(title, expected):
    assert verdict(title, SWITCH) == expected


@pytest.mark.parametrize("title,expected", [
    ("Mario Kart World - Nintendo Switch 2", "accepted"),
    ("Mario.Kart.World.Nintendo.Switch.2.1080p", "accepted"),
    ("Mario Kart World [NUP]", "accepted"),
    ("Mario Kart World Switch2", "accepted"),
    ("Mario Kart World Nintendo Switch 2 Edition NSP", OTHER.format("nsp")),
    ("Mario Kart World Switch 2 XCI", OTHER.format("xci")),
    ("Mario Kart World - Nintendo Switch", OTHER.format("nintendo switch")),
    ("Mario Kart World Switch 2.0 Update NSP", OTHER.format("nsp")),
])
def test_a_switch_2_request(title, expected):
    assert verdict(title, SWITCH_2) == expected


def test_a_package_names_its_machine():
    assert verdict("Super Mario World - Super Nintendo NSP", by_slug("snes"),
                   "Super Mario World") == OTHER.format("nsp")


def test_seeders_do_not_carry_the_other_machine():
    assert best_release([rel("Super Mario Odyssey - Nintendo Switch 2 Edition", seeders=90),
                         rel("Super Mario Odyssey [Switch] XCI", seeders=5)],
                        "Super Mario Odyssey", SWITCH).title == "Super Mario Odyssey [Switch] XCI"
    assert best_release([rel("Mario Kart World Nintendo Switch 2 Edition NSP", seeders=90),
                         rel("Mario Kart World Switch 2 XCI", seeders=90),
                         rel("Mario Kart World [NUP]", seeders=5)],
                        GAME, SWITCH_2).title == "Mario Kart World [NUP]"
