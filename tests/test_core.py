import io
import unittest
from contextlib import redirect_stdout

from tatbeea import (
    normalize,
    normalize_alef,
    normalize_digits,
    normalize_teh_marbuta,
    normalize_yeh,
    remove_tashkeel,
    remove_tatweel,
    to_arabic_digits,
)
from tatbeea.cli import main


class TestFunctions(unittest.TestCase):
    def test_remove_tashkeel(self):
        self.assertEqual(remove_tashkeel("مُحَمَّدٌ"), "محمد")
        self.assertEqual(remove_tashkeel("الرَّحْمٰن"), "الرحمن")

    def test_remove_tatweel(self):
        self.assertEqual(remove_tatweel("مـــرحبـا"), "مرحبا")

    def test_normalize_alef(self):
        self.assertEqual(normalize_alef("أحمد إبراهيم آمنة ٱلله"), "احمد ابراهيم امنة الله")

    def test_normalize_yeh(self):
        self.assertEqual(normalize_yeh("مستشفى"), "مستشفي")

    def test_normalize_teh_marbuta(self):
        self.assertEqual(normalize_teh_marbuta("مدرسة"), "مدرسه")

    def test_digits_round_trip(self):
        self.assertEqual(normalize_digits("٢٠٢٦ و ۱۴"), "2026 و 14")
        self.assertEqual(to_arabic_digits("2026"), "٢٠٢٦")

    def test_non_arabic_untouched(self):
        self.assertEqual(normalize("Hello, world!"), "Hello, world!")


class TestNormalize(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(normalize("  أَهْلـــاً   بِكَ فِي ٢٠٢٦  "), "اهلا بك في 2026")

    def test_teh_marbuta_off_by_default(self):
        self.assertEqual(normalize("مدرسة"), "مدرسة")
        self.assertEqual(normalize("مدرسة", teh_marbuta=True), "مدرسه")

    def test_flags_disable_steps(self):
        self.assertEqual(normalize("أَ ١", tashkeel=False, alef=False, digits=False), "أَ ١")

    def test_search_matching(self):
        variants = ["إسلام", "اسلام", "إِسْلَام", "اسـلام"]
        self.assertEqual(len({normalize(v) for v in variants}), 1)


class TestCli(unittest.TestCase):
    def run_cli(self, *argv):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(list(argv))
        return code, out.getvalue().strip()

    def test_argument(self):
        self.assertEqual(self.run_cli("مُحَمَّد", "٣"), (0, "محمد 3"))

    def test_keep_digits(self):
        self.assertEqual(self.run_cli("--keep-digits", "٣"), (0, "٣"))


if __name__ == "__main__":
    unittest.main()
