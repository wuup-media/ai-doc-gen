import argparse
from generator import generate
from index_builder import build_index
from api_file_finder import find_api_file

# Initialize argument parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

# create the subparser for the "generate" command
generate_parser = subparsers.add_parser('generate')
generate_parser.add_argument("--target_file", default=None, help="The file to process (optional)")
generate_parser.add_argument(
    "--model", default="gpt-3.5-turbo-16k", help="The model to use for generation")

# create the subparser for the "index" command
index_parser = subparsers.add_parser('index')

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == 'generate':
        if args.target_file:
            target_file = args.target_file
        else:
            target_file = find_api_file()
            print(f"Using {target_file} as target file")

        if target_file is None:
            print("No target file provided and no API file found.")
        else:
            generate(target_file, args.model)
    elif args.command == 'index':
        build_index()
    else:
        print("Invalid command. Use 'generate' or 'index'.")
