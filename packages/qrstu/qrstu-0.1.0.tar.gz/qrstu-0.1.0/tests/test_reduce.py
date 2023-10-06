# -*- coding: utf-8 -*-

"""

tests.test_resduce

Unit test the reduce module


Copyright (C) 2023 Rainer Schwarzbach

This file is part of qrstu.

qrstu is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

qrstu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


from unittest import TestCase

from qrstu import reduce


#
# Reduction rules as dicts: {source_characters: ascii_replacement, …}
#

LATIN = {
    # Latin characters from the
    # Latin-1 supplement (U0080–U00ff) and
    # Latin extended-A (U0100–U017f) Unicode blocks
    #
    "ÀÁÂÃÄÅĀĂĄ": "A",
    "Æ": "AE",
    "ÇĆĈĊČ": "C",
    "Ď": "D",
    "ÐĐ": "DH",
    "ÈÉÊËĒĔĖĘĚ": "E",
    "ĜĞĠĢ": "G",
    "ĤĦ": "H",
    "ÌÍÎÏĨĪĬĮİ": "I",
    "Ĳ": "IJ",
    "Ĵ": "J",
    "Ķ": "K",
    "ĹĻĽĿŁ": "L",
    "ÑŃŅŇ": "N",
    "Ŋ": "NG",
    "ÒÓÔÕÖŌŎŐØ": "O",
    "Œ": "OE",
    "ŔŖŘ": "R",
    "ŚŜŞŠ": "S",
    "ŢŤŦ": "T",
    "Þ": "TH",
    "ÙÚÛÜŨŪŬŮŰŲ": "U",
    "Ŵ": "W",
    "ÝŶŸ": "Y",
    "ŹŻŽ": "Z",
    "àáâãäåāăą": "a",
    "æ": "ae",
    "çćĉċč": "c",
    "ď": "d",
    "ðđ": "dh",
    "èéêëēĕėęě": "e",
    "ĝğġģ": "g",
    "ĥħ": "h",
    "ìíîïĩīĭįı": "i",
    "ĳ": "ij",
    "ĵ": "j",
    "ķĸ": "k",
    "ĺļľŀł": "l",
    "ñńņň": "n",
    "ŋ": "ng",
    "òóôõöōŏőø": "o",
    "œ": "oe",
    "ŕŗř": "r",
    "śŝşšſ": "s",
    "ß": "ss",
    "ţťŧ": "t",
    "þ": "th",
    "ùúûüũūŭůűų": "u",
    "ŵ": "w",
    "ýŷÿ": "y",
    "źżž": "z",
}

PUNCTUATION = {
    # Punctuation and symbols from the
    # Latin-1 supplement (U0080–U00ff) and
    # General punctuation (U2000–U206f) Unicode blocks
    #
    # Spacing characters → space
    "\u00a0\u2000\u2001\u2002\u2003\u2004"
    "\u2005\u2006\u2007\u2008\u2009\u200a": "\x20",
    # Soft hyphen → hyphen in parentheses
    "\u00ad": "(-)",
    # Hyphen bullet → hyphen
    "\u2043": "-",
    # Dashes → single, double or triple hyphen
    "\u2010\u2011": "-",
    "\u2012\u2013": "--",
    "\u2014\u2015": "---",
    # Double vertical line → double pipe
    "\u2016": "||",
    # Double low line → underscore
    "\u2017": "_",
    # Quotation marks → apostrophe, quotation mark, << or >>
    "\u2018\u2019\u201a\u201b": "\x27",
    "\u201c\u201d\u201e\u201f": '"',
    "«": "<<",
    "»": ">>",
    # Daggers → plus sign(s)
    "\u2020": "+",
    "\u2021": "++",
    # Leader dots, ellipsis → dots
    "\u2024": ".",
    "\u2025": "..",
    "\u2026": "...",
    # Bullets, middle dots, times sign → asterisk
    "\u00b7\u00d7\u2022\u2027\u204c\u204d\u204e": "*",
    # Line and paragraph separators → ASCII LF
    "\u2028": "\n",
    "\u2029": "\n\n",
    # Per mille and per myriad (= per then thousand) signs → {description}
    "\u2030": "{permille}",
    "\u2031": "{permyriad}",
    # Primes → apostrophes, reverse primes → grave accents
    "\u2032": "\x27",
    "\u2033": "\x27\x27",
    "\u2034": "\x27\x27\x27",
    "\u2057": "\x27\x27\x27\x27",
    "\u2035": "\x60",
    "\u2036": "\x60\x60",
    "\u2037": "\x60\x60\x60",
    # Caret, angle quotation marks → circumflex, less-than, greater than
    "\u2038": "^",
    "\u2039": "<",
    "\u203a": ">",
    # Exclamation and question marks, semicolon
    "¡": "!",
    "¿": "?",
    "\u203c": "!!",
    "\u203d": "?!",
    "\u2047": "??",
    "\u2048": "?!",
    "\u2049": "!?",
    "\u204f": ";",
    # Division sign and fraction slash → slash
    "÷\u2044": "/",
    # Tironian sign et → ampersand
    "\u204a": "&",
    # Various punctuation and symbols from the U2000 block
    "\u204b": "{reversed pilcrow}\n",
    "\u2051": "**",
    "\u2052": "./.",
    "\u2053": "~",
    "\u2055": "*",
    # Various punctuation and symbols from the U0080 block
    "¢": "ct",
    "£": "GBP",
    "¤": "{currency}",
    "¥": "JPY",
    "¦": "|",
    "§": "{section sign}",
    "¨": '"',
    "©": "(C)",
    "¬": "{not}",
    "®": "(R)",
    "¯": "{macron}",
    "°": "{degree}",
    "±": "+-",
    "´": "\x27",
    "µ": "{micro}",
    "¶": "{pilcrow}\n",
    "¸": "{cedilla}",
    "¼": "1/4",
    "½": "1/2",
    "¾": "3/4",
    "\u037e": ";",  # GREEK QUESTION MARK
}

ISO_CURRENCY = {
    # ISO 4217 codes for all currency symbols from the
    # Currency symbols (U20a0–U20bf) Unicode block
    # that are clearly attributable
    #
    "₠": "ECU",
    "₣": "FRF",
    "₦": "NGN",
    "₧": "ESP",
    "₪": "ILS",
    "₫": "VND",
    "€": "EUR",
    "₭": "LAK",
    "₮": "MNT",
    "₯": "GRD",
    "₱": "PHP",
    "₲": "PYG",
    "₳": "ARA",
    "₴": "UAH",
    "₵": "GHS",
    "₸": "KZT",
    "₹": "INR",
    "₺": "TRY",
    "₼": "AZN",
    "₽": "RUB",
    "₾": "GEL",
    "₿": "BTC",
    "ƒ": "NLG",
    "฿": "THB",
    "৳": "BDT",
}

NON_ISO_CURRENCY = {
    # Names for all currency symbols from the
    # Currency symbols (U20a0–U20bf) Unicode block that are
    # NOT clearly attributable or do not have a ISO 4217 code
    #
    "₡": "{Colon}",  # CRC and SVC
    "₢": "{Cruzeiro}",  # BRB, BRC, BRN, BRE, BRR
    "₤": "{Lira}",  # ITL, MTL, SML, VAL, possybly also SYP
    "₥": "{Mill}",  # former US currency unit (1/1000 $)
    "₨": "Rs",  # various currencies; Indian Rupee: see INR
    "₩": "{Won}",  # KPW and KRW
    "₰": "{Pfennig}",  # former German curreny unit (1/100 Mark)
    "₶": "{Livre tournois}",  # former French currency, 13th to 18th century
    "₷": "{Spesmilo}",  # historical proposed int'l currency
    "₻": "{Nordic Mark}",  # Danish rigsdaler
}

GERMAN_OVERRIDES = {
    # German-language overrides including U1e9e (ẞ, capital ß)
    #
    "Ä": "AE",
    "Ö": "OE",
    "Ø": "OE",
    "ẞ": "SZ",
    "Ü": "UE",
    "ä": "ae",
    "ö": "oe",
    "ø": "oe",
    "ß": "sz",
    "ü": "ue",
    "\u2030": "{Promille}",
    "¤": "{Waehrung}",
    "§": "Par.",
    "¬": "{nicht}",
    "°": "{Grad}",
    "¶": "{Absatzmarke}\n",
    "¸": "{Cedille}",
    "₰": "Pf.",
}

METAL_UMLAUTS = {
    "Hūsker Dū": "Husker Du",
    "Lȧȧz Rockit": "Laaz Rockit",
    "Leftöver Crack": "Leftover Crack",
    "Spın̈al Tap": "Spinal Tap",
}

PARDON_MY_FRENCH = {
    "Ça va\xa0?": "Ca va ?",
    "Sacre-Cœur": "Sacre-Coeur",
    "«\xa0Père Noël\xa0»": "<< Pere Noel >>",
}


class CombinedCharacters(TestCase):

    """Test the CombinedCharacter class"""

    def test_properties(self) -> None:
        """__init__() function and properties with various inputs"""
        # decomposed into 2 characters
        character = "ï"
        combined = reduce.CombinedCharacter(character)
        with self.subTest(character=character, scope="components"):
            self.assertEqual(combined.components, (0x69, 0x308))
        #
        with self.subTest(character=character, scope="nfc"):
            self.assertEqual(combined.nfc, character)
        #
        # decomposed into a single character
        character = "‼"
        combined = reduce.CombinedCharacter(character)
        with self.subTest(character=character, scope="components"):
            self.assertEqual(combined.components, (0x203C,))
        #
        with self.subTest(character=character, scope="nfc"):
            self.assertEqual(combined.nfc, character)
        #
        # marks at the start of a CombinedCharacter are forbidden
        character = chr(0x301)  # COMBINING ACUTE ACCENT
        with self.subTest(
            character=character, scope="error: mark at beginning"
        ):
            self.assertRaises(ValueError, reduce.CombinedCharacter, character)
        #
        # Simply combining two characters into one
        # is not supported
        text = "ae"  # distinct a and e letters
        with self.subTest(text=text, scope="error: illegal combination"):
            self.assertRaises(
                reduce.NewCharacterRequired,
                reduce.CombinedCharacter,
                text,
            )
        #

    def test_reduce(self) -> None:
        """__reduce__() function with various inputs"""
        for character, expected_result in (
            ("ï", "i"),
            ("æ", "ae"),
            ("‼", "!!"),
        ):
            with self.subTest(
                character=character, expected_result=expected_result
            ):
                combined = reduce.CombinedCharacter(character)
                self.assertEqual(combined.reduce(), expected_result)
            #
        #
        # Non-ASCII-reducable character
        character = "Ж"
        combined = reduce.CombinedCharacter(character)
        with self.subTest(character=character, expected_behavior="exception"):
            self.assertRaises(UnicodeEncodeError, combined.reduce)
        #
        for error_handling, expected_result in (
            ("ignore", ""),
            ("replace", "?"),
            ("backslashreplace", "\\u0416"),
            ("xmlcharrefreplace", "&#1046;"),
            ("namereplace", "\\N{CYRILLIC CAPITAL LETTER ZHE}"),
        ):
            with self.subTest(
                character=character,
                error_handling=error_handling,
                expected_result=expected_result,
            ):
                self.assertEqual(
                    combined.reduce(errors=error_handling), expected_result
                )
            #
        #

    def test_eq(self) -> None:
        """__eq__() special function"""
        self.assertEqual(
            reduce.CombinedCharacter("ï"),
            reduce.CombinedCharacter("i\u0308"),
        )

    def test_add(self) -> None:
        """__add__() special function"""
        self.assertEqual(
            reduce.CombinedCharacter("e") + "\u0308",
            reduce.CombinedCharacter("ë"),
        )

    def test_len(self) -> None:
        """__len__() special function"""
        # eg. vietnamese multi-accent characters
        self.assertEqual(len(reduce.CombinedCharacter("ế")), 3)

    def test_str(self) -> None:
        """__str__() special function"""
        # eg. vietnamese multi-accent characters
        self.assertEqual(str(reduce.CombinedCharacter("ế")), "e\u0302\u0301")


class Functions(TestCase):

    """Test the module functions"""

    def test_tokenize(self) -> None:
        """tokenize() function"""
        self.assertEqual(
            list(reduce.tokenize("Hélène")),
            [
                reduce.CombinedCharacter("H"),
                reduce.CombinedCharacter("e\u0301"),
                reduce.CombinedCharacter("l"),
                reduce.CombinedCharacter("e\u0300"),
                reduce.CombinedCharacter("n"),
                reduce.CombinedCharacter("e"),
            ],
        )

    def test_reduce_characters(self) -> None:
        """reduce_text() function with single characters"""
        for name, collection in (
            ("Latin", LATIN),
            ("Punctuation", PUNCTUATION),
            ("ISO currency", ISO_CURRENCY),
            ("Non-ISO currency", NON_ISO_CURRENCY),
        ):
            # Build test collection
            tested_characters = {}
            for key, value in collection.items():
                for source_character in key:
                    tested_characters[source_character] = value
                #
            #
            for source_character, expected_result in tested_characters.items():
                with self.subTest(
                    name=name,
                    source_character=source_character,
                    expected_result=expected_result,
                ):
                    self.assertEqual(
                        reduce.reduce_text(source_character), expected_result
                    )
                #
            #
        #
        # Build test collection
        tested_characters = {}
        for key, value in GERMAN_OVERRIDES.items():
            for source_character in key:
                tested_characters[source_character] = value
            #
        #
        for source_character, expected_result in tested_characters.items():
            with self.subTest(
                name="Fancy overrides",
                source_character=source_character,
                expected_result=expected_result,
            ):
                self.assertEqual(
                    reduce.reduce_text(
                        source_character, extra_translations=GERMAN_OVERRIDES
                    ),
                    expected_result,
                )
            #
        #

    def test_reduce_longer_texts(self) -> None:
        """reduce_text() function with selected longer text inputs"""
        for title, source_collection in (
            ("Metal Umlauts", METAL_UMLAUTS),
            ("Pardon my French", PARDON_MY_FRENCH),
        ):
            for source_text, expected_result in source_collection.items():
                with self.subTest(
                    title=title,
                    source_text=source_text,
                    expected_result=expected_result,
                ):
                    self.assertEqual(
                        reduce.reduce_text(source_text),
                        expected_result,
                    )
                #
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
