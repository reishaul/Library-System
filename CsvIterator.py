import csv
'''
 CSV Iterator class 
'''
class CsvIterator:

    def __init__(self, file_path):

        self.file_path = file_path
        self.file = open(file_path, mode='r', encoding='utf-8')  
        self.reader = csv.DictReader(self.file)  
        self.current_line = None  

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.current_line = next(self.reader)  
            return self.current_line  
        except StopIteration:
            self.file.close()  
            raise StopIteration

    def reset(self):
        self.file.seek(0)  
        self.reader = csv.DictReader(self.file)  

        

