import spacy
import tiktoken
from typing import List, Set

nlp = spacy.load("en_core_web_sm")


def read_file(file_path: str) -> str:
    """
    Reads the content of a file.

    :param file_path: The path to the file.
    """
    with open(file_path, 'r') as f:
        return f.read()


def break_into_sentences(text: str) -> List[str]:
    """
    Breaks a text into sentences.

    :param text: The text to break into sentences.
    """
    doc = nlp(text)
    return list(doc.sents)


def get_filenames(results: dict) -> List[str]:
    """
    Extracts filenames from the results.

    :param results: The results to extract filenames from.
    """
    filenames = []
    for metadata in results['metadatas']:
        for item in metadata:
            if item['filename'] not in filenames:
                filenames.append(item['filename'])
    return filenames


def get_files_data(filenames: List[str], model: str = "gpt-3.5-turbo-16k") -> List[str]:
    """
    Reads the content of the files and encodes them.

    :param filenames: The filenames to read and encode.
    :param model: The model to use for encoding.
    """
    enc = tiktoken.encoding_for_model(model)

    # Set max tokens based on model variant
    if "16k" in model:
        max_tokens = 8000
    else:
        max_tokens = 4000

    file_contents = []
    total_tokens = 0
    for filename in filenames:
        print(f"Reading {filename}")
        file_content = read_file(filename)
        tokens = enc.encode(file_content)
        if total_tokens + len(tokens) > max_tokens:
            break
        total_tokens += len(tokens)
        file_contents.append(file_content)

    return file_contents


def create_prompt(file_contents: List[str], target_file_content: str) -> str:
    """
    Creates a prompt for the API documentation.

    :param file_contents: The contents of the files to include in the prompt.
    :param target_file_content: The content of the target file to include in the prompt.
    """
    prompt = f"""# SYSTEM:
    You are a polyglot programmer and a competant technical writer.

# CONTEXT CODE:
    """

    for file_content in file_contents:
        prompt += f"\n```\n{file_content}\n```\n"

    prompt += f"""
# CURRENT FILE:
{target_file_content}

# TASK:
given the current file, write api documentation for routes or route handling functions in the file.
use the context code to help you write the documentation.
the documentation should be written in markdown.
each route or route handling function should have its own section.
there should be examples of how to use each route or route handling function with curl.
Show examples using the parameters that the route or route handling function accepts.

# Api Documentation:

"""
    return prompt


def get_token_count(prompt: str, model: str = "gpt-3.5-turbo-16k") -> int:
    """
    Counts the number of tokens in a prompt.

    :param prompt: The prompt to count the tokens in.
    :param model: The model to use for token counting.
    """
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(prompt)
    return len(tokens)


def split_tokens(texts: List[str], threshold: int = 4000, model: str = "gpt-3.5-turbo-16k") -> List[List[str]]:
    """
    Splits a list of texts into tokens and if the number of tokens in any text is over a particular threshold, 
    splits the tokens at the threshold mark.

    :param texts: The list of texts to split into tokens.
    :param threshold: The threshold at which to split the tokens.
    :param model: The model to use for token counting.
    """
    enc = tiktoken.encoding_for_model(model)
    split_tokens = []

    for text in texts:
        tokens = enc.encode(text)

        if len(tokens) > threshold:
            for i in range(0, len(tokens), threshold):
                split_tokens.append(tokens[i:i + threshold])
        else:
            split_tokens.append(tokens)

    return split_tokens
