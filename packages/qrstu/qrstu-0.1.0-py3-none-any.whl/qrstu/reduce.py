# -*- coding: utf-8 -*-

"""

qrstu.reduce

Functions reducing unicode to ASCII


Copyright (C) 2023 Rainer Schwarzbach

This file is part of qrstu.

qrstu is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

qrstu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import codecs
import logging
import unicodedata

from typing import Dict, Iterator, List, Optional, Tuple


ASCII = "ascii"
ERRORS_DEFAULT = "strict"

PRESET_CHARACTER_REDUCTIONS: Dict[int, str] = {
    # Latin characters from the
    # Latin-1 supplement (U0080–U00ff) and
    # Latin extended-A (U0100–U017f) Unicode blocks
    #
    0xC6: "AE",  # "Æ"
    0xD0: "DH",  # "Ð"
    0x110: "DH",  # "Đ"
    0x126: "H",  # "Ħ"
    0x141: "L",  # "Ł"
    0x14A: "NG",  # "Ŋ"
    0xD8: "O",  # "Ø"
    0x152: "OE",  # "Œ"
    0x166: "T",  # "Ŧ"
    0xDE: "TH",  # "Þ"
    0xE6: "ae",  # "æ"
    0xF0: "dh",  # "ð"
    0x111: "dh",  # "đ"
    0x127: "h",  # "ħ"
    0x131: "i",  # "ı"
    0x138: "k",  # "ĸ"
    0x142: "l",  # "ł"
    0x14B: "ng",  # "ŋ"
    0xF8: "o",  # "ø"
    0x153: "oe",  # "œ"
    0xDF: "ss",  # "ß"
    0x167: "t",  # "ŧ"
    0xFE: "th",  # "þ"
    #
    # Punctuation and symbols from the
    # Latin-1 supplement (U0080–U00ff) and
    # General punctuation (U2000–U206f) Unicode blocks
    #
    0xAD: "(-)",  # SOFT HYPHEN
    0x2043: "-",  # HYPHEN BULLET
    0x2010: "-",  # HYPHEN
    0x2011: "-",  # NON-BREAKING HYPHEN
    0x2012: "--",  # FIGURE DASH
    0x2013: "--",  # EN DASH
    0x2014: "---",  # EM DASH
    0x2015: "---",  # HORIZONTAL BAR
    0x2016: "||",  # DOUBLE VERTICAL LINE
    0x2018: "'",  # LEFT SINGLE QUOTATION MARK
    0x2019: "'",  # RIGHT SINGLE QUOTATION MARK
    0x201A: "'",  # SINGLE LOW-9 QUOTATION MARK
    0x201B: "'",  # SINGLE HIGH-REVERSED-9 QUOTATION MARK
    0x201C: '"',  # LEFT DOUBLE QUOTATION MARK
    0x201D: '"',  # RIGHT DOUBLE QUOTATION MARK
    0x201E: '"',  # DOUBLE LOW-9 QUOTATION MARK
    0x201F: '"',  # DOUBLE HIGH-REVERSED-9 QUOTATION MARK
    0xAB: "<<",  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0xBB: ">>",  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x2020: "+",  # DAGGER
    0x2021: "++",  # DOUBLE DAGGER
    0x2024: ".",  # ONE DOT LEADER
    0x2025: "..",  # TWO DOT LEADER
    0x2026: "...",  # HORIZONTAL ELLIPSIS
    0xB7: "*",  # MIDDLE DOT
    0xD7: "*",  # MULTIPLICATION SIGN
    0x2022: "*",  # BULLET
    0x2027: "*",  # HYPHENATION POINT
    0x204C: "*",  # BLACK LEFTWARDS BULLET
    0x204D: "*",  # BLACK RIGHTWARDS BULLET
    0x204E: "*",  # LOW ASTERISK
    0x2028: "\n",  # LINE SEPARATOR
    0x2029: "\n\n",  # PARAGRAPH SEPARATOR
    0x2030: "{permille}",  # PER MILLE SIGN
    0x2031: "{permyriad}",  # PER TEN THOUSAND SIGN
    0x2032: "'",  # PRIME
    0x2035: "`",  # REVERSED PRIME
    0x2038: "^",  # CARET
    0x2039: "<",  # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    0x203A: ">",  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    0xA1: "!",  # INVERTED EXCLAMATION MARK
    0xBF: "?",  # INVERTED QUESTION MARK
    0x203D: "?!",  # INTERROBANG
    0x204F: ";",  # REVERSED SEMICOLON
    0xF7: "/",  # DIVISION SIGN
    0x2044: "/",  # FRACTION SLASH
    0x204A: "&",  # TIRONIAN SIGN ET
    0x204B: "{reversed pilcrow}\n",  # REVERSED PILCROW SIGN
    0x2051: "**",  # TWO ASTERISKS ALIGNED VERTICALLY
    0x2052: "./.",  # COMMERCIAL MINUS SIGN
    0x2053: "~",  # SWUNG DASH
    0x2055: "*",  # FLOWER PUNCTUATION MARK
    0xA2: "ct",  # CENT SIGN
    0xA3: "GBP",  # POUND SIGN
    0xA4: "{currency}",  # CURRENCY SIGN
    0xA5: "JPY",  # YEN SIGN
    0xA6: "|",  # BROKEN BAR
    0xA7: "{section sign}",  # SECTION SIGN
    0xA9: "(C)",  # COPYRIGHT SIGN
    0xAC: "{not}",  # NOT SIGN
    0xAE: "(R)",  # REGISTERED SIGN
    0xB0: "{degree}",  # DEGREE SIGN
    0xB1: "+-",  # PLUS-MINUS SIGN
    0xB6: "{pilcrow}\n",  # PILCROW SIGN
    #
    # ISO 4217 codes for all currency symbols from the
    # Currency symbols (U20a0–U20bf) Unicode block
    # that are clearly attributable
    #
    0x20A0: "ECU",  # "₠" (EURO-CURRENCY SIGN)
    0x20A3: "FRF",  # "₣" (FRENCH FRANC SIGN)
    0x20A6: "NGN",  # "₦" (NAIRA SIGN)
    0x20A7: "ESP",  # "₧" (PESETA SIGN)
    0x20AA: "ILS",  # "₪" (NEW SHEQEL SIGN)
    0x20AB: "VND",  # "₫" (DONG SIGN)
    0x20AC: "EUR",  # "€" (EURO SIGN)
    0x20AD: "LAK",  # "₭" (KIP SIGN)
    0x20AE: "MNT",  # "₮" (TUGRIK SIGN)
    0x20AF: "GRD",  # "₯" (DRACHMA SIGN)
    0x20B1: "PHP",  # "₱" (PESO SIGN)
    0x20B2: "PYG",  # "₲" (GUARANI SIGN)
    0x20B3: "ARA",  # "₳" (AUSTRAL SIGN)
    0x20B4: "UAH",  # "₴" (HRYVNIA SIGN)
    0x20B5: "GHS",  # "₵" (CEDI SIGN)
    0x20B8: "KZT",  # "₸" (TENGE SIGN)
    0x20B9: "INR",  # "₹" (INDIAN RUPEE SIGN)
    0x20BA: "TRY",  # "₺" (TURKISH LIRA SIGN)
    0x20BC: "AZN",  # "₼" (MANAT SIGN)
    0x20BD: "RUB",  # "₽" (RUBLE SIGN)
    0x20BE: "GEL",  # "₾" (LARI SIGN)
    0x20BF: "BTC",  # "₿" (BITCOIN SIGN)
    0x192: "NLG",  # "ƒ" (LATIN SMALL LETTER F WITH HOOK)
    0xE3F: "THB",  # "฿" (THAI CURRENCY SYMBOL BAHT)
    0x9F3: "BDT",  # "৳" (BENGALI RUPEE SIGN)
    #
    # Names for all currency symbols from the
    # Currency symbols (U20a0–U20bf) Unicode block that are
    # NOT clearly attributable or do not have a ISO 4217 code
    #
    0x20A1: "{Colon}",  # "₡" (COLON SIGN)
    0x20A2: "{Cruzeiro}",  # "₢" (CRUZEIRO SIGN)
    0x20A4: "{Lira}",  # "₤" (LIRA SIGN)
    0x20A5: "{Mill}",  # "₥" (MILL SIGN)
    0x20A8: "Rs",  # "₨" (RUPEE SIGN)
    0x20A9: "{Won}",  # "₩" (WON SIGN)
    0x20B0: "{Pfennig}",  # "₰" (GERMAN PENNY SIGN)
    0x20B6: "{Livre tournois}",  # "₶" (LIVRE TOURNOIS SIGN)
    0x20B7: "{Spesmilo}",  # "₷" (SPESMILO SIGN)
    0x20BB: "{Nordic Mark}",  # "₻" (NORDIC MARK SIGN)
}

PRESET_NORMALIZATION_TRANSLATIONS: Dict[str, str] = {
    "¨": '"',  # DIAERESIS, 0xa8
    "¯": "{macron}",  # MACRON, 0xaf
    "´": "'",  # ACUTE ACCENT, 0xb4
    "µ": "{micro}",  # 0xb5
    "¸": "{cedilla}",  # 0xb8
    "Ŀ": "L",  # 0x13f
    "ŀ": "l",  # 0x140
    "‗": "_",  # DOUBLE LOW LINE, 0x2017
}


class NewCharacterRequired(Exception):

    """Raise if a new CombinedCharacter instace is required"""


def get_mark_flags(text: str) -> List[bool]:
    """Return a List of boolean values indicating if
    the character a that position in text is a combier mark
    """
    return [
        unicodedata.category(character).startswith("M") for character in text
    ]


class CombinedCharacter:

    """Represents a combined character"""

    double_combiners: Dict[int, str] = {
        # Mark codepoints cobining the predecessor
        # and the successor character
        # (0x35c–0x363, 0x1dcd, 0x1dfc)
        0x35C: "__",
        0x35D: "__",
        0x35E: "__",
        0x35F: "__",
        0x360: "~~",
        0x361: "__",
        0x362: "->",
        0x1DCD: "^^",
        0x1DFC: "___",
    }

    def __init__(self, normalized_source: str = "") -> None:
        """Initialize"""
        marks = get_mark_flags(normalized_source)
        collector = list(normalized_source)
        if collector and marks[0]:
            raise ValueError("Mark character at start not supported")
        #
        for index, component in enumerate(collector):
            if not index:
                continue
            #
            if (
                not marks[index]
                and ord(collector[index - 1]) not in self.double_combiners
            ):
                raise NewCharacterRequired
            #
        #
        self.__components: Tuple[int, ...] = tuple(
            ord(component)
            for component in unicodedata.normalize("NFD", normalized_source)
        )

    @property
    def components(self):
        """Return the components"""
        return self.__components

    @property
    def nfc(self):
        """Return the NFC form"""
        return unicodedata.normalize("NFC", str(self))

    def reduce(
        self,
        errors: str = ERRORS_DEFAULT,
    ) -> str:
        """Reduce to ascii"""
        decomposed = unicodedata.normalize("NFKD", str(self))
        marks = get_mark_flags(decomposed)
        collector: List[str] = []
        for index, character in enumerate(decomposed):
            codepoint = ord(character)
            if marks[index]:
                # append double combiner replacement
                try:
                    collector.append(self.double_combiners[codepoint])
                except KeyError:
                    break
                #
            #
            try:
                collector.append(PRESET_CHARACTER_REDUCTIONS[codepoint])
            except KeyError:
                encoded = codecs.encode(
                    character, encoding=ASCII, errors=errors
                )
                collector.append(
                    codecs.decode(encoded, encoding=ASCII, errors=errors)
                )
            #
        #
        return "".join(collector)

    def __add__(self, additional_character: str) -> "CombinedCharacter":
        """Return a new CombinedCharacter instance
        from the current instance’s components
        combined with the additional character (if possible)
        """
        return self.__class__(f"{str(self)}{additional_character}")

    def __eq__(self, other) -> bool:
        """Instances compare equal if the have the same components"""
        return self.components == other.components

    def __hash__(self) -> int:
        """Return a hash over the character’s components"""
        return hash(self.__components)

    def __len__(self) -> int:
        """Return the number of components"""
        return len(self.__components)

    def __str__(self) -> str:
        """Return the whole character as a string"""
        return "".join(chr(component) for component in self.__components)


EASTER_EGGS: Dict[CombinedCharacter, str] = {
    CombinedCharacter("a\u20db"): "Punkrock ohne <3 ;-p",
}


def tokenize(text: str) -> Iterator[CombinedCharacter]:
    """Iterate over the NFC normalized text
    and yield CombinedCharacter instances
    """
    normalized_source = unicodedata.normalize("NFC", text)
    current_combination = CombinedCharacter()
    for character in normalized_source:
        try:
            current_combination = current_combination + character
        except NewCharacterRequired:
            yield current_combination
            current_combination = CombinedCharacter(character)
        #
    #
    if current_combination:
        yield current_combination
    #


def reduce_text(
    source: str,
    errors: str = ERRORS_DEFAULT,
    extra_translations: Optional[Dict[str, str]] = None,
) -> str:
    """Reduce a text and return the result"""
    translations: Dict[str, str] = dict(PRESET_NORMALIZATION_TRANSLATIONS)
    if extra_translations:
        translations.update(extra_translations)
    #
    result_components: List[str] = []
    for character in tokenize(source):
        try:
            logging.debug(EASTER_EGGS[character])
        except KeyError:
            pass
        #
        try:
            chunk = translations[character.nfc]
        except KeyError:
            chunk = character.reduce(errors=errors)
        #
        result_components.append(chunk)
    #
    return "".join(result_components)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
