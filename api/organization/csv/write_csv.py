import csv
import datetime

class CsvFile:
    """
    Writes to a csv file info required, in path ./reports_generated/
    """
    def __init__(self,name_file,fieldnames,path_type):
        path = './hermes/api/organization/csv/reports_generated/'+path_type
        now = datetime.datetime.utcnow()
        self.file_csv_name = path+now.strftime('%H:%M:%S')+" "+now.strftime('%Y-%m-%d')+" "+name_file+'.csv'
        self.fieldnames = fieldnames
        with open(self.file_csv_name, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()
    
    def append_multiple_lines(self,data_list,row_object):
        with open(self.file_csv_name, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            for d in data_list:
                row_csv={i:d[i] for i in self.fieldnames}
                writer.writerow(row_csv)
    
    def append_line(self,row):
        with open(self.file_csv_name, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writerow(row)