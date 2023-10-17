from utils import read_file, break_into_sentences, get_filenames, get_files_data, create_prompt, get_token_count
from chroma_db import query_collection
from openai_interaction import get_response


def generate(target_file, model):
    # Read the target file
    text = read_file(target_file)

    # Break the file into sentences using spacy
    sentences = break_into_sentences(text)

    # Query the collection with the sentences
    results = query_collection(sentences)

    filenames = get_filenames(results)

    file_contents = get_files_data(filenames, model)

    target_file_content = read_file(target_file)

    prompt = create_prompt(file_contents, target_file_content)

    token_count = get_token_count(prompt, model)

    # print(prompt)
    print(f"Token count: {token_count}")

    response = get_response(prompt, model)

    print(response['choices'][0]['message']['content'])
