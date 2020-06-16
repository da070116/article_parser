import os
from transliterate import translit
ROOT_PATH = os.path.abspath("../../test")


def parse_txt_files(execute_function, directory: str) -> None:
    """
    Apply a function to all .txt files in provided directory (subdirectories included)

    :param execute_function: Function to execute
    :param directory: str - Path to a root directory
    :return: None

    """
    # os.system("find . -type f -name \*txt -exec iconv -f cp1251 -t utf-8 '{}' -o '{}' \;")
    for child_directories in os.walk(directory):
        for _file in child_directories[2]:
            img_name = ''
            if _file.endswith('.jpg'):
                # print(f'{_file=}')
                # print(f'{child_directories[0]=}')
                old_name = os.path.join(child_directories[0], _file)
                img_name = translit(_file.lower(), language_code='ru', reversed=True)
                new_name = os.path.join(child_directories[0], )
                os.rename(old_name, new_name)
            #     print(f'Renamed {old_name} -> {new_name}')
            if _file.endswith(".txt"):
                correct_file = os.path.join(child_directories[0], _file)
                for do_function_ in execute_function:
                    do_function_(correct_file, img_name)


def modify_to_web(file_path: str, img_file='') -> None:
    web_content = []
    if img_file:
        image_ = f'''<img src="{img_file}" style="float: left;" '''
        web_content.append()
    with open(file=file_path, mode='r') as file_reader:
        lines = file_reader.readlines()
        for line in lines:
            line = f'<p>{line[:-1]}</p>\n'
            web_content.append(line)
    php_file = create_php_filename(file_path)
    # with open(file=php_filename, mode='w') as file_writer:
    #     for string in web_content:
    #         file_writer.write(string)

    print(f'File {php_file} was written')


def create_php_filename(raw_path: str) -> str:
    """
    Generates name for inc.php file
    by transliteration of parent folder name
    (and add it to a root path)
    :param raw_path: path to a source file
    :return: full path to .inc.php
    """
    path_root = raw_path.rsplit('/', maxsplit=2)
    parent_folder_name = raw_path.split('/')[-2]
    php_filename = translit(parent_folder_name, "ru", reversed=True)
    for sign in ("'", '(', ')'):
        php_filename = php_filename.replace(sign, '')
    php_filename = php_filename.replace(' ', '-').lower() + '.inc.php'
    return f'{path_root[0]}/{php_filename}'


def fix_file(file_path: str) -> None:
    """
     Remove unnecessary line endings and save result to the SAME file.
        IMPORTANT: file expected to be in utf-8 encoding
    :param file_path: string - Path to a text file
    :return: None
    """
    with open(file=file_path, mode='r') as file_reader:
        content = file_reader.read()
        file_reader.close()
    content = content.replace('\n', ' ')
    content = content.replace('- ', '')
    content = content.replace(' ', '\n', 1)
    with open(file=file_path, mode='w') as file_writer:
        file_writer.write(content)
        file_writer.close()
    print(f" Файл {file_path} успешно изменён")


if __name__ == '__main__':
    parse_txt_files([modify_to_web], ROOT_PATH)
