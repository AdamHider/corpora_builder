import os
import pandas as pd
import re
 
# reading the CSV file
class Builder :
    def __init__(self, lang_pair) :
        self.lang_pair = lang_pair
        self.ready_dirs = self.get_ready('./text_ready.txt')
        self.path = './text'
        
        self.source_file = f'./target/{self.lang_pair[0]}-{self.lang_pair[1]}/{self.lang_pair[0]}.txt'
        self.target_file = f'./target/{self.lang_pair[0]}-{self.lang_pair[1]}/{self.lang_pair[1]}.txt'

        self.blacklist = []

    def get_ready(self, filename) : 
        # opening the file in read mode 
        my_file = open(filename, "r", encoding="utf-8") 
        # reading the file 
        data = my_file.read() 
        # replacing end splitting the text  
        # when newline ('\n') is seen. 
        data_into_list = data.split("\n") 
        my_file.close() 
        return data_into_list

    def clean(self) :
        if not os.path.exists('./target'):
            os.mkdir('./target') 
        if not os.path.exists(f'./target/{self.lang_pair[0]}-{self.lang_pair[1]}'):
            os.mkdir(f'./target/{self.lang_pair[0]}-{self.lang_pair[1]}') 
        if os.path.exists(self.source_file):
            os. remove(self.source_file)
        if os.path.exists(self.target_file):
            os. remove(self.target_file)


    def iter_ready(self) :
        for folder in self.ready_dirs :
            self.iter_dir(f"{self.path}/{folder}", 0)

    def iter_dir(self, path, level) :
        file_list = os.listdir(path)
        self.check_dir_langs(file_list)
        obj = os.scandir(path)
        for entry in obj :
            if entry.is_dir() or entry.is_file():
                if entry.is_dir() :
                    in_file_list = os.listdir(entry.path)
                    self.check_dir_langs(in_file_list)
                    new_level = level+1
                    self.iter_dir(entry.path, new_level)
                else :
                    if entry.name in self.blacklist:
                        continue
                    if entry.name.endswith('.md'):
                        regex = r"\.(" + re.escape(self.lang_pair[0]) + r"|" + re.escape(self.lang_pair[1]) + r")\."
                        chap_and_lang = re.search(regex, entry.name) 
                        if chap_and_lang:
                            chap_and_lang = chap_and_lang.group().split('.')
                            lang = chap_and_lang[1]
                            text = self.extract_text(entry.path)
                            self.update_target_file(lang, text)
        obj.close()

    def extract_text(self, filename) :
        result = []
        with open(filename, encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if len(line.strip()) > 0:
                    result.append(line.strip()+'\n')
        f.close()
        return result

    def update_target_file(self, lang, data) :
        filename = f"./target/{self.lang_pair[0]}-{self.lang_pair[1]}/{lang}.txt"
        if os.path.exists(filename):
            with open(filename, encoding="utf-8") as output1:
                lines = output1.readlines()
            output1.close()
        else:
            lines = []
        lines = lines + data
        with open(filename, "w", encoding="utf-8") as output:
            output.writelines(lines)

        output.close()

    #iter_dir(path, 0)
    def check_dir_langs(self, file_list):
        is_source = False
        is_target = False
        for filename in file_list:
            regex = r"\.(" + re.escape(self.lang_pair[0]) + r"|" + re.escape(self.lang_pair[1]) + r")\."
            chap_and_lang = re.search(regex, filename) 
            if chap_and_lang:
                chap_and_lang = chap_and_lang.group().split('.')
                lang = chap_and_lang[1]
                if self.lang_pair[0] == lang:
                    is_source = True
                if self.lang_pair[1] == lang:
                    is_target = True

        if not is_source or not is_target:
            self.blacklist = self.blacklist + file_list

    def build(self):
        self.clean()
        self.iter_ready()
        print(self.blacklist)

# entry.is_file() will check
# if entry is a file or not and
# entry.is_dir() method will
# check if entry is a
# directory or not. 

 
# To Close the iterator and
# free acquired resources
# use scandir.close() method

builder = Builder(['crh-RU', 'uk'])
builder.build()
