import unittest

import pyparsing
import pytest

import bible_coverage.parser.cfg as cfg


# forms:
# <book><chapter>
# <book><verse range>
# <book><chapter>:<verse range>
# <book><chapter>:<verse range>[<optional verse range>]
# <book><chapter>:<verse range>;<verse range>[<optional verse range>]
# <book><chapter>:[<optional verse range>]<verse range>
# <section> or <section>


class TestVerseParsing(unittest.TestCase):
    def test_genesis(self) -> None:
        result = cfg.parse("Genesis 1:1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Genesis")
        self.assertEqual(result[0].chapter, 1)
        self.assertEqual(result[0].start_verse, 1)

    def test_whole_psalm(self) -> None:
        result = cfg.parse("Psalm 100")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Psalm")
        self.assertEqual(result[0].chapter, 100)
        self.assertFalse(result[0].start_verse)

    def test_whole_book(self) -> None:
        result = cfg.parse("Jude")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Jude")
        self.assertFalse(result[0].chapter)
        self.assertFalse(result[0].start_verse)

    def test_short_book_verse(self) -> None:
        result = cfg.parse("Jude 3")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Jude")
        self.assertFalse(result[0].chapter)
        self.assertEqual(result[0].start_verse, 3)

    def test_invalid(self) -> None:
        with pytest.raises(pyparsing.exceptions.ParseException):
            result = cfg.parse("Enoch 1:1")

    def test_basic_range(self) -> None:
        result = cfg.parse("Genesis 15:1-6")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Genesis")
        self.assertEqual(result[0].chapter, 15)
        self.assertEqual(result[0].start_verse, 1)
        self.assertEqual(result[0].end_verse, 6)

    def test_optional_range(self) -> None:
        result = cfg.parse("Luke 2:1-14 [15-20]")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Luke")
        self.assertEqual(result[0].chapter, 2)
        self.assertEqual(result[0].start_verse, 1)
        self.assertEqual(result[0].end_verse, 20)

    def test_second_disjunct_ranges(self) -> None:
        result = cfg.parse("Isaiah 1:1, 10-20")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].book, "Isaiah")
        self.assertEqual(result[0].chapter, 2)
        self.assertEqual(result[0].start_verse, 1)
        self.assertEqual(result[0].end_verse, 1)
        self.assertEqual(result[1].book, "Isaiah")
        self.assertEqual(result[1].chapter, 2)
        self.assertEqual(result[1].start_verse, 10)
        self.assertEqual(result[1].start_verse, 20)

    def test_disjunct_books(self) -> None:
        result = cfg.parse("Galatians 4:4-7 or Philippians 2:5-11")
        self.assertEqual(len(result), 2)

    def test_verse_a_start(self) -> None:
        result = cfg.parse("Amos 6:1a, 4-7")
        self.assertEqual(len(result), 2)

    def test_verse_a_end(self) -> None:
        result = cfg.parse("Revelation 21:1-6a")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Revelation")
        self.assertEqual(result[0].chapter, 21)
        self.assertEqual(result[0].start_verse, 1)
        self.assertEqual(result[0].end_verse, 6)

    def test_verse_b_start(self) -> None:
        result = cfg.parse("Romans 10:8b-13")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Romans")
        self.assertEqual(result[0].chapter, 10)
        self.assertEqual(result[0].start_verse, 8)
        self.assertEqual(result[0].end_verse, 13)

    def test_verse_b_end(self) -> None:
        result = cfg.parse("Romans 12:9-16b")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].book, "Romans")
        self.assertEqual(result[0].chapter, 12)
        self.assertEqual(result[0].start_verse, 9)
        self.assertEqual(result[0].end_verse, 16)

    def test_multiple_ranges(self) -> None:
        result = cfg.parse("Nehemiah 8:1-3, 5-6, 8-10")
        self.assertEqual(len(result), 3)

    def test_multiple_ranges_multiple_styles(self) -> None:
        result = cfg.parse("Nehemiah 8:1-3, 7, 8-10")
        self.assertEqual(len(result), 3)

if __name__ == "__main__":
    unittest.main()
