import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Subtitles processor",
                                     description="Auto-process subtitles files")

    parser.add_argument("sub_files", type=str, nargs='*', metavar="FILE",
                        help="Subtitle file(s) to process. Multiple files can be supplied.")
    parser.add_argument("-c", "--config", type=str, metavar="FILE", default="config/default.yaml",
                        help="Path to the configuration file.")
    parser.add_argument("-f", "--file_list", type=str, metavar="FILE", default=None,
                        help="Text file indicating subtitles files to process. "
                             "Can be used besides/instead of providing the file names directly.")
    parser.add_argument("--outfile_pattern", type=str, metavar="PATTERN", default="processed/{}",
                        help="Pattern for the output processed files."
                             "The {} are replaced by the name of the respective input file.")

    return parser.parse_args()
