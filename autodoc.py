import os
import spacy
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
import hashlib
import argparse
import openai
import tiktoken
from gitignore_parser import parse_gitignore


enc = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")

# Initialize argument parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

# create the subparser for the "generate" command
generate_parser = subparsers.add_parser('generate')
generate_parser.add_argument("target_file", help="The file to process")

# create the subparser for the "index" command
index_parser = subparsers.add_parser('index')

args = parser.parse_args()

# Initialize spacy
nlp = spacy.load("en_core_web_sm")

# Initialize ChromaDB
chroma_client = PersistentClient(path="db")
embedder = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"])
collection = chroma_client.get_or_create_collection(
    name="code", embedding_function=embedder)


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def break_into_sentences(text):
    doc = nlp(text)
    return list(doc.sents)


def query_collection(sentences):
    return collection.query(
        query_texts=[sent.text for sent in sentences],
        n_results=5
    )


def print_results(results):
    for result in results:
        print(result)


def get_filenames(results):
    filenames = set()
    for metadata in results['metadatas']:
        for item in metadata:
            filenames.add(item['filename'])
    return filenames


def get_file_contents(filenames):
    file_contents = []
    total_tokens = 0
    for filename in list(filenames):
        file_content = read_file(filename)
        tokens = enc.encode(file_content)
        if total_tokens + len(tokens) > 8000:
            break
        total_tokens += len(tokens)
        file_contents.append(file_content)
    return file_contents


def create_prompt(file_contents, target_file_content):
    prompt = f"""# SYSTEM:
    You are a C# developer and a competant technical writer.

# CONTEXT CODE:
    """

    for file_content in file_contents:
        prompt += f"\n```\n{file_content}\n```\n"

    prompt += f"""
# CURRENT FILE:
```
{target_file_content}
```

# TASK:
given the current file, write api documentation for routes or route handling functions in the file.
use the context code to help you write the documentation.
the documentation should be written in markdown.
each route or route handling function should have its own section.
there should be examples of how to use each route or route handling function with curl.

"""
    return prompt


def get_token_count(prompt):
    tokens = enc.encode(prompt)
    return len(tokens)


def get_response(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )


def build_index():

    # Scan directory for popular language files
    extensions = ['.cs', '.py', '.js', '.java',
                  '.c', '.cpp', '.go', '.rb', '.php', '.swift']
    total_files = sum([len(files) for r, d, files in os.walk(
        ".") if any(f.endswith(tuple(extensions)) for f in files)])
    processed_files = 0

    # Parse .gitignore file
    gitignore_path = os.path.abspath('.gitignore')
    gitignore = parse_gitignore(gitignore_path)

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(tuple(extensions)):
                file_path = os.path.join(root, file)

                # Resolve the absolute path to the file
                absolute_file_path = os.path.abspath(file_path)

                # Skip files that match .gitignore patterns
                if gitignore(absolute_file_path):
                    continue

                print(f"Processing {absolute_file_path}")

                # Read the file
                with open(file_path, 'r') as f:
                    text = f.read()

                # Break the file into chunks using spacy
                doc = nlp(text)
                total_sents = len(list(doc.sents))
                processed_sents = 0
                for i, sent in enumerate(doc.sents):
                    # Add each chunk to the ChromaDB vector store with additional context
                    # Also add an incrementing number to the data to be md5ed, so that each doc is unique
                    unique_id = hashlib.md5(
                        (file_path + str(i)).encode()).hexdigest()
                    collection.add(
                        metadatas=[{"filename": file_path}],
                        documents=[sent.text],
                        ids=[unique_id]
                    )
                    processed_sents += 1
                    print(
                        f"  Processed {processed_sents} out of {total_sents} sentences.")

                processed_files += 1
                print(
                    f"Processed {processed_files} out of {total_files} files.")


def generate():
    # Read the target file
    text = read_file(args.target_file)

    # Break the file into sentences using spacy
    sentences = break_into_sentences(text)

    # Query the collection with the sentences
    results = query_collection(sentences)

    print_results(results)

    filenames = get_filenames(results)

    file_contents = get_file_contents(filenames)

    target_file_content = read_file(args.target_file)

    prompt = create_prompt(file_contents, target_file_content)

    token_count = get_token_count(prompt)

    print(prompt)
    print(f"Token count: {token_count}")

    response = get_response(prompt)

    print(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    if args.command == 'generate':
        generate()
    elif args.command == 'index':
        build_index()
    else:
        print("Invalid command. Use 'generate' or 'index'.")
