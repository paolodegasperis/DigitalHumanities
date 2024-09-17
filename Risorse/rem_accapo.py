import os

def remove_line_breaks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().replace('\n', ' ')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_txt_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            remove_line_breaks(file_path)
            print(f"Processed {filename}")

if __name__ == "__main__":
    directory = 'txt_job'
    if os.path.exists(directory) and os.path.isdir(directory):
        process_txt_files(directory)
    else:
        print(f"The directory '{directory}' does not exist.")
