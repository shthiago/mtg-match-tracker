import re
from typing import List, Optional, Tuple


DeckCard = Tuple[int, str]


class DeckParser:
    LINE_COMMENT = r"( )*\/\/.+\n?"
    LINE_EMPTY = r"( )*\n?"
    LINE_MAINDECK = r"( )*\d+( )+[A-Za-z0-9].+\n?"
    SIDEBOARD_PREFIX = "SB:"
    LINE_SIDEBOARD = r"( )*SB:( )* \d+( )+[A-Za-z0-9].+\n?"

    @classmethod
    def parse(cls, input_deck: str) -> Optional[Tuple[List[DeckCard], List[DeckCard]]]:
        """Parse deck and return (maindeck, sideboard)"""
        if not cls._is_valid_list(input_deck):
            return None

        maindeck: List[DeckCard] = []
        sideboard: List[DeckCard] = []

        maindeck_rgx = re.compile(cls.LINE_MAINDECK)
        sideboard_rgx = re.compile(cls.LINE_SIDEBOARD)

        for row in input_deck.split("\n"):
            is_maindeck = maindeck_rgx.fullmatch(row) is not None
            if is_maindeck:
                maindeck.append(cls._process_row(row))
                continue

            is_sideboard = sideboard_rgx.fullmatch(row) is not None
            if is_sideboard:
                sideboard.append(cls._process_row(row))

        return maindeck, sideboard

    @classmethod
    def _process_row(cls, row: str) -> Optional[DeckCard]:
        row = row.replace(cls.SIDEBOARD_PREFIX, "").strip()
        quantity, cardname = row.split(" ", maxsplit=1)
        return int(quantity), cardname.strip()

    @classmethod
    def _is_valid_list(cls, input_deck: str) -> bool:
        valid_lines = (
            cls.LINE_COMMENT
            + "|"
            + cls.LINE_EMPTY
            + "|"
            + cls.LINE_MAINDECK
            + "|"
            + cls.LINE_SIDEBOARD
        )
        rgx = re.compile("(" + valid_lines + ")*")
        return rgx.fullmatch(input_deck) is not None
