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

Run the autodoc.py script with the target file as an argument:
```bash
python autodoc.py <target_file>
```

Replace `<target_file>` with the path to the file you want to process.
