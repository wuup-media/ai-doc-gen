import argparse
from generator import generate
from index_builder import build_index

# Initialize argument parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

# create the subparser for the "generate" command
generate_parser = subparsers.add_parser('generate')
generate_parser.add_argument("target_file", help="The file to process")
generate_parser.add_argument(
    "--model", default="gpt-3.5-turbo-16k", help="The model to use for generation")

# create the subparser for the "index" command
index_parser = subparsers.add_parser('index')

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == 'generate':
        generate(args.target_file, args.model)
    elif args.command == 'index':
        build_index()
    else:
        print("Invalid command. Use 'generate' or 'index'.")
