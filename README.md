# ai-doc-gen

This project uses a virtual environment to manage dependencies. Follow the instructions below to set up the project.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/wuup-media/ai-doc-gen.git
cd ai-doc-gen
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
python -m pip install -r requirements.txt
```

4. Download the necessary Spacy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

### generate
Generates API documentation for routes or route handling functions in a file.

Parameters:
- `target_file` (required): The file to process.
- `model`: The model to use for generation. Default value is "gpt-3.5-turbo-16k".

Example usage:

```bash
python main.py generate myfile.py --model=gpt-3.5-turbo-16k
```

### index
Builds an index of code files for efficient searching.

Example usage:

```bash
python main.py index
```

Note: This command needs to be run before using the `generate` command.
