from __future__ import annotations

import argparse
from contextlib import ExitStack

from tally_token import merge_io, split_io


def split_main(
    *, source_path: str, dest_paths: str, bufsize: int = 1024
) -> None:
    # ensure closing all the files even if an exception is raised
    with ExitStack() as stack:
        infile = stack.enter_context(open(source_path, "rb"))
        outfiles = [stack.enter_context(open(p, "wb")) for p in dest_paths]
        split_io(infile, list(outfiles), bufsize=bufsize)


def merge_main(
    *, dest_path: str, source_paths: str, bufsize: int = 1024
) -> None:
    # ensure closing all the files even if an exception is raised
    with ExitStack() as stack:
        outfile = stack.enter_context(open(dest_path, "wb"))
        infiles = [stack.enter_context(open(p, "rb")) for p in source_paths]
        merge_io(infiles, outfile, bufsize=bufsize)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        required=True,
        dest="command",
        help=(
            "Commands:\n"
            "split: split a file into multiple files\n"
            "merge: merge multiple files into a file"
            "Example:\n"
            "tally-token split example.bin example.bin.1 example.bin.2 example.bin.3\n"
            "tally-token merge example-merged.bin example.bin.1 example.bin.2 example.bin.3"
        ),
    )
    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("src", help="The source file to be split.")
    split_parser.add_argument("dst", nargs="+", help="The destination files.")
    split_parser.add_argument(
        "--bufsize", type=int, default=1024 * 2, help="The buffer size."
    )

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("dst", help="The destination file.")
    merge_parser.add_argument("src", nargs="+", help="The source files.")
    merge_parser.add_argument(
        "--bufsize", type=int, default=1024**2, help="The buffer size."
    )

    args = parser.parse_args()
    if args.command == "split":
        split_main(source_path=args.src, dest_paths=args.dst)
    elif args.command == "merge":
        merge_main(dest_path=args.dst, source_paths=args.src)


if __name__ == "__main__":
    main()
