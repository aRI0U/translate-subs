import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Subtitles processor",
                                     description="Auto-processes subtitles files")

    parser.add_argument("sub_files", type=str, nargs='*', metavar="FILE",
                        help="TODO")
    parser.add_argument("-c", "--config", type=str, metavar="FILE", default="config/default.yaml",
                        help="TODO")
    parser.add_argument("-f", "--file_list", type=str, metavar="FILE", default=None,
                        help="TODO")
    parser.add_argument("--outfile_pattern", type=str, default="processed/{}",
                        help="TODO")

    return parser.parse_args()
