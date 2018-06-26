import tempfile, os, argparse


def get_file_counts(filename, source_path, lines_only):
    with open(filename) as f:
        lines = 0
        chars = 0
        for line in f:
            lines += 1
            chars += len(line)
        return lines, (chars if lines_only else -1)
    raise Exception("File from {0} named {1} locally could not be opened".format(source_path, filename))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Simple program that counts the characters and lines in S3 files locally")
    parser.add_argument('--lines-only', help='If you only want line counts', action='store_true' )
    parser.add_argument('--output-dir', help='The location where output will be written', required='True')
    parser.add_argument('--file_in_repo', help='This file will be provided from the repository in the code folder')
    parser.add_argument('--file_configured_in_registration', help='This file will be specified during registration time. It should be saved by Kuyil during registration time and made available ')
    parser.add_argument('--file_supplied_by_user', help='The file will be provided by user during execution time. Kuyil has to save to and make it available.')
    parser.add_argument('inputs', help='List of input locations (files only, no directories)',nargs='+')

    args = parser.parse_args()
    tmp_file = tempfile.NamedTemporaryFile().name
    print tmp_file
    lines = 0
    chars = 0
    output = []
    for path in args.inputs:
        print 'path: ', path
        os.system("aws s3 cp {0}sample_file_multiple_lines.txt {1}".format(path, tmp_file))
        lines, chars = get_file_counts(tmp_file, path, args.lines_only)
        output.append("{0},{1},{2}".format(lines, chars, path))
    with open(tmp_file,'w') as f:
        for line in output:
            print >> f, line
    os.system("aws s3 cp {0} {1}counts.txt".format(tmp_file, args.output_dir))
        

