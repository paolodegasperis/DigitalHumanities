
# Text Summarizer and Keyword Extractor

## Description
This Python script automates the process of reading, summarizing, and extracting keywords from text files (.txt). It uses the OpenAI API to generate concise and relevant summaries along with significant keywords.

## Prerequisites
- Python 3.x
- Python modules: `os`, `csv`, `glob`, `openai`, `time`
- OpenAI API key (register at [OpenAI](https://www.openai.com/) to obtain one)

## Configuration
Before running the script, you need to configure your OpenAI API key in the code:
```python
openai.api_key = 'YOUR_API_KEY'
```
Replace `'YOUR_API_KEY'` with your personal API key.

## Folder Structure
The script expects a specific directory structure where the .txt files to be analyzed are placed in a subfolder named 'txt' in the same directory as the script.

## Usage
1. Ensure all .txt files to be analyzed are in the `txt` folder.
2. Run the script from the terminal or IDE:
```bash
python summarize.py
```
3. The results of the summarization and keywords will be saved in a CSV file named `summary_results.csv` in the same directory as the script.

## Output
The script generates a CSV file with three columns: `File_Name`, `Summarization`, and `Keywords`. Each row represents an analyzed text file, with the file name, summarized text, and extracted keywords.

## Note
The script includes a 10-second delay between analyzing each file to avoid overloading the OpenAI API requests.

## License
This project is released under the Creative Commons Attribution-ShareAlike License (CC-BY-SA). For further details on the license, visit the following URL: [CC-BY-SA](https://creativecommons.org/licenses/by-sa/4.0/).
