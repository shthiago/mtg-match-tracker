from textwrap import dedent

import pytest

from tracker.utils.deck_parser import DeckParser


@pytest.fixture
def basic_correct_list() -> str:
    return dedent(
        """
    // Deck: UWr Control (60)

    // Lands
    2 Castle Vantress

    // Creatures
    3 Snapcaster Mage

    // Spells
    2 The Wandering Emperor

    // Sideboard
    SB: 2 Chalice of the Void

    """
    )


@pytest.fixture
def basic_incorrect_list() -> str:
    return dedent(
        """
    // Deck: UWr Control (60)

    // ERROR HERE Missing card quantity
    Castle Vantress

    // Creatures
    3 Snapcaster Mage

    // Spells
    2 The Wandering Emperor

    // Sideboard
    SB: 2 Chalice of the Void

    """
    )


def test_validate_list(basic_correct_list: str):
    assert DeckParser._is_valid_list(basic_correct_list)


def test_invalidate_list(basic_incorrect_list: str):
    assert not DeckParser._is_valid_list(basic_incorrect_list)


@pytest.mark.parametrize(
    "row",
    [
        "2",
        "Castle Vantress",
        "Sideboard",
        "SB:",
        "    LETTERSSSSS   ",
        "    124132     ",
        "SB: Frost Titan",
        "SB:    121432154  ",
    ],
)
def test_invalidate_row(row: str):
    assert not DeckParser._is_valid_list(row)


@pytest.mark.parametrize(
    "row",
    ["2 Castre Vantress", "// Comment", "    ", "", "SB: 2 Teferi, Hero of Dominaria"],
)
def test_validate_row(row: str):
    assert DeckParser._is_valid_list(row)


def test_parse_basic_list(basic_correct_list: str):
    assert DeckParser.parse(basic_correct_list) is not None


def test_parse_basic_incorrect_list(basic_incorrect_list: str):
    assert DeckParser.parse(basic_incorrect_list) is None


@pytest.mark.parametrize(
    "input_deck, expected_maindeck, expected_sideboard",
    [
        (
            dedent(
                """
                1 Teferi
                SB: 2 Narset
            """
            ),
            [(1, "Teferi")],
            [(2, "Narset")],
        ),
        (
            dedent(
                """
                1 Solitude
                // Comment

                1 Jace
                SB: 2 Narset
                SB: 1 Garruk
            """
            ),
            [(1, "Solitude"), (1, "Jace")],
            [(2, "Narset"), (1, "Garruk")],
        ),
    ],
)
def test_parse_results(input_deck, expected_maindeck, expected_sideboard):
    maindeck, sideboard = DeckParser.parse(input_deck)

    assert maindeck == expected_maindeck

    assert sideboard == expected_sideboard
