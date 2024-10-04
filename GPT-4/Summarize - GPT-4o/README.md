
# GPT-4o Mini Text Summarizer

This Python script uses the OpenAI GPT-4o model to automatically summarize text files found in a specific folder. The summarized texts are then saved in a CSV file with two columns: the name of the text file and the corresponding summary. This software is especially useful for researchers, academics, and content curators who need to generate concise abstracts for large numbers of text documents.

## Features
- Summarizes text files into a minimum of 2000 characters.
- Extracts 20 relevant keywords from each text.
- Saves the summarized content into a CSV file.

## Requirements
- Python 3.7+
- OpenAI Python library (`openai`)
- An active OpenAI API key with access to the GPT-4o model.

## Installation

1. Clone this repository or download the script:
   ```sh
   git clone https://your-repository-url
   cd your-repository-url
   ```

2. Install the necessary dependencies:
   ```sh
   pip install openai
   ```

3. Add your OpenAI API key in the script:
   ```python
   client = OpenAI(api_key='Your-API-Key-Here')
   ```

4. Prepare your text files:
   - Place your `.txt` files in a folder named `txt` in the same directory as the script.

## Usage

1. Run the script:
   ```sh
   python summarizer.py
   ```

2. The script will:
   - Read all `.txt` files from the `txt` folder.
   - Generate a summary for each file.
   - Save the summaries in a CSV file named `riassunti.csv` in the same directory.

## Example
For example, if you have the following structure:
```
/txt
  |- file1.txt
  |- file2.txt
```
After running the script, a `riassunti.csv` file will be created with summaries for `file1.txt` and `file2.txt`.

## License
This software is released under the [Creative Commons Attribution-ShareAlike (CC-BY-SA)](https://creativecommons.org/licenses/by-sa/4.0/) license.
You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material
for any purpose, even commercially.

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
