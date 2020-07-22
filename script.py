from pathlib import Path
import os, re, shutil, subprocess, json

dev_mode = True
working_dir = Path(input('Enter target directory: ')) if not dev_mode else r'C:\Users\lumzh\Desktop\download'
file_regex = re.compile(r'(\d+)\.blv$')

def file_number(file):
    return int(file.split('.')[0])

def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value

for path, folders, files in os.walk(working_dir):
    if folders == []:
        print(f'Current Path: {path}')
        data_file = Path('\\'.join(path.split('\\')[:-1]), 'entry.json')
        show_title = ''
        with open(data_file, encoding="utf8") as f:
            data = json.load(f)
            show_title = remove(data['title'], r'\/:*?"<>|')

        print(f'Movie Title: {show_title}')
        os.chdir(path)
        file_to_be_converted = []
        for file in files:
            match = file_regex.match(file)
            if match:
                new_file = file.split('.')[0] + '.flv'
                print(f'Renaming {file} to {new_file}')
                file_to_be_converted.append(new_file)
                shutil.copyfile(Path(path, file), Path(path, new_file))
        file_to_be_converted = sorted(file_to_be_converted, key=file_number)

        text_file = open('ff.txt', 'w')
        for file in file_to_be_converted:
            text_file.write(f'file \'{file}\'\n')
        text_file.close() 

        print('\n\nExecuting Command')
        cmd = subprocess.Popen('ffmpeg -f concat -i ff.txt -c copy result.mp4')
        cmd.communicate()

        #Create result dir
        os.makedirs(Path(working_dir, show_title), exist_ok=True)

        shutil.move(Path(path, 'result.mp4'), Path(working_dir, show_title, 'result.mp4'))
        print('\n\nSuccess! Video converted and stored in result.mp4\n\n')


            