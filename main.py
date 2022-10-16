from utils import parse_args, parse_config


args = parse_args()

# compute list of subtitles files to be processed
sub_files = args.sub_files
if args.file_list is not None:
    with open(args.file_list, 'r') as f:
        files_list = [fname.strip() for fname in f.readlines() if len(fname.strip()) > 0]

    sub_files.extend(files_list)


# initialize processor
processor = parse_config(args.config)


# process subtitles
for sub_file in sub_files:
    out_file = args.outfile_pattern.format(sub_file)
    processor.process_subtitles(sub_file, out_file)
