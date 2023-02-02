import os
from datetime import date


def get_line_count(filepath):
    file = open(filepath, 'r', encoding="utf-8")
    line_count = len(file.readlines())
    return line_count


def get_config_data(filepath):
    file = open(filepath, 'r', encoding="utf-8")
    lines = file.readlines()
    language = lines[0]
    excludes = lines[1].split(' ')
    filetypes = lines[2].split(' ')
    return [language, excludes, filetypes]


def get_relevant_files(filepath):
    files = []
    paths = os.listdir(filepath)

    for path in paths:
        new_path = os.path.join(filepath, path)
        if path not in excludes:
            if os.path.isfile(new_path):
                tokens = path.split('.')
                extension = tokens[-1:][0]
                if extension in filetypes:
                    files.append(new_path)
            else:
                sub_files = get_relevant_files(new_path)
                for file in sub_files:
                    files.append(file)
    return files


total_lines = 0

config_data = get_config_data("config.cfg")

language = config_data[0].strip()
excludes = config_data[1]
filetypes = config_data[2]

filepaths = get_relevant_files('.')

for filepath in filepaths:
    total_lines += get_line_count(filepath)

readme = open("readme.md", 'r+')
identifier = f"### Total lines of {language} source code as of "
string = f"{identifier}{str(date.today())} = {str(total_lines)} lines"
readme_lines = readme.readlines()
chars = 0
for i in range(len(readme_lines)):
    if len(readme_lines[i].split(identifier)) > 1:
        readme.seek(chars)
        readme.truncate()
        readme.write(string + "\n")
        readme.writelines(readme_lines[i+1:])
    chars += len(readme_lines[i]) + 1
