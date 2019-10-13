"""
This script helps you automating boring stuff applying a function to all the files
present in a directory. You can do something like:
-Renaming all the files or Renaming all csv files
-Merging all the files
-Converting csv to xlsx...

This is still work in progress

"""
__author__      = "Kslash2"


import sys, getopt
import shutil
import os
import csv
import datetime
from xlsxwriter import Workbook
import glob
import argparse

sys.tracebacklimit = 0

def get_file_info():
   f_info_dict = {}
   f_info_dict["files"] = os.listdir()
   f_info_dict["total_files"] = len(f_info_dict["files"])
   f_info_dict["extension_list"] = [os.path.splitext(filename)[1] for filename in f_info_dict["files"]]
   f_info_dict["extension_counts_dict"] = {elem:f_info_dict["extension_list"].count(elem) for elem in f_info_dict["extension_list"]}
   f_info_dict["most_present_extension"] = max(f_info_dict["extension_counts_dict"], key=f_info_dict["extension_counts_dict"].get)
   return f_info_dict

def file_info_log():
   files_info_dict = get_file_info()
   print(f"There are {files_info_dict.get('total_files')} files.")
   print("There are:")
   for key,val in files_info_dict.get("extension_counts_dict").items():
      print(f"{val} files with {key} extension")
   print(f"there are more files with {files_info_dict.get('most_present_extension')} extension")


def csv_to_xlsx():
   for csvfile in glob.glob(os.path.join(".", "*.csv")):
      workbook = Workbook(csvfile[:-4] + "-" + str(datetime.date.today()) + ".xlsx")
      worksheet = workbook.add_worksheet()
      with open(csvfile, "rt", encoding="utf8") as f:
         reader = csv.reader(f)
         for r, row in enumerate(reader):
            for c, col in enumerate(row):
                  worksheet.write(r, c, col)
      workbook.close()
      os.remove(csvfile)


def merge_csv(output_name="merged_csv"):
   writer = csv.writer(open(output_name+".csv", "w", newline=""))
   if csv not in get_file_info().get("extension_list"):
      raise FileNotFoundError("There is no csv files in this directory")
   for csv_file_name in glob.glob(os.path.join(".", "*.csv")):
      if csv_file_name != output_name+".csv":
         with open(csv_file_name) as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader, None)
            writer.writerows(reader)


def merge_files(output_name="merged_files",ext=None):
   if ext is None:
      info_df = get_file_info()
      ext = info_df.get("most_present_extension").replace(".","")
   else:
      files = glob.glob(os.path.join(".", "*."+ext))
   
   merged_file = open(output_name+"."+ext, "a")

   for filename in files:
      if filename != output_name:
         if filename != os.path.basename(sys.argv[0]):
            f = open(filename, "r")
            txt = f.read()
            merged_file.write("\n")
            merged_file.write(txt)
            f.close()
   
   merged_file.close()


def replace_files_name(old, new):
   for filename in os.listdir():
      if old in filename:
         os.rename(filename, filename.replace(old, new))


def rename_files(new_filename):
   files = os.listdir()
   files.remove(str(os.path.basename(__file__)))
   for i,file in enumerate(files):
      os.rename(os.path.join('.', file), os.path.join('.', ''.join(str(new_filename)+str(i))))


def main(argv):
   files = os.listdir()
   parser = argparse.ArgumentParser()
   parser.add_argument("--csv2xlsx",action="store_true")
   parser.add_argument("--mergefiles",action="store_true")
   parser.add_argument("--replacefilenames",nargs=2,action="store",metavar=("<oldpart>", "<newpart>"))
   parser.add_argument("--renamefiles",nargs=1, action="store",metavar="<newname>")
   parser.add_argument("--ext",nargs=1,action="store",metavar="<extension>")
   parser.add_argument("--out",nargs=1,action="store",metavar="<output_name>")
   parser.add_argument("--fileinfo",action="store_true")
   
   args = parser.parse_args()
   args_dict = vars(args)


   if args_dict["csv2xlsx"]:
      csv_to_xlsx()
   elif args_dict["mergefiles"]:
      extension = args_dict["ext"]
      out_name = args_dict.get("out")
      print(out_name)
      if extension is None:
         if out_name is None:
            merge_files()
         else:
            merge_files(output_name=out_name[0])
      else:
         if extension[0] == "csv":
            print("merge csv")
            merge_csv()
         else:
            merge_files(output_name=out_name[0],ext=extension[0])
   elif args_dict["replacefilenames"]:
      old, new = args.replacefilenames
      replace_files_name(old,new)
   elif args_dict["renamefiles"]:
      new_name = args_dict.get("renamefiles")[0]
      rename_files(new_name)
   elif args_dict["fileinfo"]:
      file_info_log()

if __name__ == "__main__":
   main(sys.argv[1:])
