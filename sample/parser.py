import os
from typing import List
from transliterate import translit
from shutil import copyfile

SEP = os.path.sep
ROOT_PATH = os.path.abspath("../tmp/")


def parse_csv() -> List[tuple]:
    """
    Method reads the csv file and returns a list of tuples like that: (name_in_Russian, path_to_inc_php_file)
    :raises: UnicodeDecodeError if file is not in UTF-8
    :return: a list of tuples
    """
    result_list = []
    print("Start parse 'record.csv'")
    try:
        with open('records.csv', mode='r', encoding='utf-8') as file_open:
            for line in file_open:
                # Sample of line: "21","АМВРОСИЙ I (Орнатский Андрей Антипович)",,"tmp/amvrosiy_i/amvrosiy_i.inc.php"
                records_in_db = line.strip().split(',')
                name_value = clean_record(records_in_db[1].strip('"'))
                result_list.append((name_value, records_in_db[3].strip('"')))
    except UnicodeDecodeError:
        print('Not a Unicode file')
        raise

    return result_list


def clean_record(raw_string: str) -> str:
    """
    Removes all unnecessary signs from a raw_string and returns it
    :param raw_string: folder or file name to manage
    :return: clean value
    """
    for sign in ("'", '(', ')', '"'):
        raw_string = raw_string.replace(sign, '')
    return raw_string.replace(' ', '-').replace('--', '-')


def convert_name(name: str, only_first: bool = False) -> str:
    """
        Returns string in English lowercase. If only_first=True, splits name by whitespace separator
        and returns it.

    """
    if name.startswith('Т3 '):
        name = name[3:]
    if only_first:
        translated_string = translit(name.split(" ")[0].lower().strip(), language_code='ru', reversed=True)
    else:
        translated_string = translit(name.lower(), language_code='ru', reversed=True)
    return clean_record(translated_string)


def create_sql_query(records: List[str]) -> None:
    """
    Write SQL query file
    :param records: Data to add in database

    """
    with open(file='add_new_values.sql', mode='w') as file_writer:
        file_writer.write(""" INSERT INTO records (name, keywords, link) VALUES \n""")
        for index, item in enumerate(records):
            file_writer.write(f'("{item[0]}","", "{item[1]}")')
            if index != len(records) - 1:
                file_writer.write(", \n")


class Parser:

    record_folder_name = ''
    php_name = ''
    article_rus_name = ''
    web_content = []
    csv_content = []
    db_values = []

    def __init__(self):
        self.csv_content = parse_csv()
        self.scan_folders()
        create_sql_query(self.db_values)

    def scan_folders(self) -> None:
        """
        Walks through the folders within ROOT_PATH. For each folder it sets an article_rus_name (that is a
        name of person as it presents in encyclopedia) and record_folder_name (that is an English transliteration).
        If article name presents in csv file then record_folder_name is taken from it else it creates manually

        After all method works with the files in the folder: text file is converted to .inc.php, image is just copied
        to a new directory
        :return:

        """
        print(f"Start check directories in {ROOT_PATH}")
        for directories in os.walk(ROOT_PATH):
            self.article_rus_name = directories[0].rsplit(SEP, 1)[-1]
            # This check allows to skip a record with the root folder content
            if self.article_rus_name != 'tmp':
                self.record_folder_name = convert_name(self.article_rus_name)
                self.php_name = f'{self.record_folder_name}.inc.php'
                _add_this_to_query = True
                for csv_record in self.csv_content:
                    if csv_record[0].lower() == self.article_rus_name.lower():
                        # Split into 'tmp/folder_name' and 'file_name.inc.php'
                        self.record_folder_name, self.php_name = csv_record[1].rsplit('/', 1)
                        self.record_folder_name = self.record_folder_name[4:]  # Remove 'tmp/'
                        _add_this_to_query = False
                        break
                if _add_this_to_query:
                    self.db_values.append((self.article_rus_name, f'tmp/{self.record_folder_name}/{self.php_name}'))
                # Managing content value
                image_name = ''
                for file in directories[2]:
                    if file.endswith('.txt'):
                        self.web_content = []
                        file_path = f"{directories[0]}{os.path.sep}{file}"
                        try:
                            with open(file=file_path, mode='r', encoding='utf-8') as file_reader:
                                lines = file_reader.readlines()
                                for line in lines:
                                    line = f'<p>{line[:-1]}</p>\n'
                                    self.web_content.append(line)
                        except UnicodeDecodeError:
                            print('Not a Unicode file')
                            raise
                    else:
                        image_name = file
                self.create_folder_structure(content=self.web_content, image=image_name)

    def create_folder_structure(self, content: List[str], image: str = '') -> None:
        """
        Create the proper structure of folders and files. For each article it looks like
            person_name_in_lowercase
                person_name_in_lowercase.inc.php
                [img]
                    [person_name_in_lowercase.jpg]
        All that will be created in folder 'READY' while the sources are in folder pointed in self.ROOT_PATH constant

        :param image: name of the related .jpg file
        :param content: Content of article optimized for web display

        """
        location = f"{ROOT_PATH.rsplit(SEP, 1)[0]}{SEP}READY"
        new_folder_name = f'{location}{SEP}{self.record_folder_name}'
        file_name = f'{new_folder_name}{SEP}{self.php_name}'
        try:
            if not os.path.exists(new_folder_name):
                os.makedirs(new_folder_name)
            # checking need for img folder
            if image:
                img_folder = f'{new_folder_name}{SEP}img'
                if not os.path.exists(img_folder):
                    os.makedirs(img_folder)
                    # copying the image itself
                current_image_path = f'{ROOT_PATH}{SEP}{self.article_rus_name}{SEP}{image}'
                new_image_path = f'{img_folder}{SEP}{self.record_folder_name}.jpg'
                copyfile(current_image_path, new_image_path)
                img_tag = f'''<img src="tmp/{self.record_folder_name}/img/{self.record_folder_name}.jpg" 
                                style="float:left; padding:10px;" />
                           '''
                content.insert(0, img_tag)  # insert <img> at the beginning of the inc.php file
                # Write all content to a file
            with open(file=file_name, mode='w') as file_writer:
                for string in content:
                    file_writer.write(string + '\n')
        except OSError:
            print('Something wrong')
            raise


if __name__ == '__main__':
    parser = Parser()
