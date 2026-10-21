"""Command-line entry point: `tatbeea "نَصّ"` or `echo "نَصّ" | tatbeea`."""

import argparse
import sys

from . import __version__
from .core import normalize


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="tatbeea",
        description="Normalize Arabic text (remove tashkeel, unify alef/yeh, digits...).",
    )
    parser.add_argument("text", nargs="*", help="text to normalize; reads stdin if omitted")
    parser.add_argument("--keep-tashkeel", action="store_true", help="do not remove harakat")
    parser.add_argument("--keep-digits", action="store_true", help="do not convert digits to 0-9")
    parser.add_argument("--teh-marbuta", action="store_true", help="also fold ة into ه")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    options = dict(
        tashkeel=not args.keep_tashkeel,
        digits=not args.keep_digits,
        teh_marbuta=args.teh_marbuta,
    )

    if args.text:
        print(normalize(" ".join(args.text), **options))
    else:
        for line in sys.stdin:
            print(normalize(line, **options))
    return 0


if __name__ == "__main__":
    sys.exit(main())
