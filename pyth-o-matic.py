
import sys, getopt
import shutil
import os
import csv
import datetime
from xlsxwriter import Workbook
import glob
import argparse




def show_help():
   print("Help")


def csv_to_xlsx():
   for csvfile in glob.glob(os.path.join('.', '*.csv')):
      workbook = Workbook(csvfile[:-4] + '-' + str(datetime.date.today()) + '.xlsx')
      worksheet = workbook.add_worksheet()
      with open(csvfile, 'rt', encoding='utf8') as f:
         reader = csv.reader(f)
         for r, row in enumerate(reader):
            for c, col in enumerate(row):
                  worksheet.write(r, c, col)
      workbook.close()
      os.remove(csvfile)


def merge_csv():
   writer = csv.writer(open('appended_output.csv', 'w', newline=''))
   for csv_file_name in glob.glob(os.path.join('.', '*.csv')):
      if csv_file_name != 'appended_output.csv':
         print(csv_file_name)
         with open(csv_file_name) as csv_file:
               reader = csv.reader(csv_file)
               header = next(reader, None)
   writer.writerows(reader)


def merge_files():
   files = os.listdir()
   merged_file_name = input("Please insert the name of the file to save:")
   merged_file = open(merged_file_name, 'a')

   for filename in files:
      if filename != merged_file_name:
         if filename != os.path.basename(sys.argv[0]):
            f = open(filename, 'r')
            txt = f.read()
            merged_file.write("\n")
            merged_file.write(txt)
            f.close()
   
   merged_file.close()
   print("files merged")


def rename_files(old, new):
   for filename in os.listdir("."):
      if old in filename:
         os.rename(filename, filename.replace(old, new))


def main(argv):
   files = os.listdir()
   parser = argparse.ArgumentParser()
   parser.add_argument("--csv2xlsx")
   parser.add_argument("--csvmerge")
   parser.add_argument("--fmerge")
   parser.add_argument("--frename",nargs=2, action="store")
   
   args = parser.parse_args()
   args_dict = vars(args)

   if args_dict["csv2xlsx"]:
      csv_to_xlsx()
   elif args_dict["csvmerge"]:
      merge_csv()
   elif args_dict["fmerge"]:
      merge_files()
   elif args_dict["frename"]:
      old, new = args.frename
      rename_files(old,new)


if __name__ == "__main__":
   main(sys.argv[1:])


