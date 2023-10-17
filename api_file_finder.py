from utils import get_filenames
from chroma_db import query_collection_with_strings
from typing import Optional

def find_api_file() -> Optional[str]:
    keywords = ['API', 'Endpoints', 'Routes', 'HTTP', 'GET', 'POST', 'PUT', 'DELETE']
    # Query the collection with the sentences
    results = query_collection_with_strings(keywords, 1)

    filenames = get_filenames(results)

    if len(filenames) > 0:
        return filenames[0]

    return None
