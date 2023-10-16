import os
import hashlib
from gitignore_parser import parse_gitignore
from chroma_db import collection
from utils import read_file, break_into_sentences
import spacy

nlp = spacy.load("en_core_web_sm")


def build_index():
    # Scan directory for popular language files
    extensions = ['.cs', '.py', '.js', '.java',
                  '.c', '.cpp', '.go', '.rb', '.php', '.swift', '.mustache']

    # Parse .gitignore file
    gitignore_path = os.path.abspath('.gitignore')
    gitignore = parse_gitignore(gitignore_path)

    # Count total files taking into account the .gitignore
    total_files = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(tuple(extensions)):
                file_path = os.path.join(root, file)
                absolute_file_path = os.path.abspath(file_path)
                if not gitignore(absolute_file_path):
                    total_files += 1

    processed_files = 0

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
                text = read_file(file_path)

                # Break the file into chunks using spacy
                doc = nlp(text)
                total_sents = len(list(doc.sents))
                processed_sents = 0
                for i, sent in enumerate(doc.sents):
                    # Add each chunk to the ChromaDB vector store with additional context
                    # Also add an incrementing number to the data to be md5ed, so that each doc is unique
                    unique_id = hashlib.md5(
                        (file_path + str(i)).encode()).hexdigest()

                    if len(collection.get(unique_id)['ids']) > 0:
                        print(f"  Skipping {unique_id}")
                        continue

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
