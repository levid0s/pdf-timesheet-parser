import os
import fnmatch
import re
import locale
from decimal import *
from tabulate import tabulate
from PyPDF2 import PdfReader

dir = sys.argv[1]

def find_timesheets(root_dir):
  timesheets = []
  for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in fnmatch.filter(filenames, "*Payroll*.pdf"):
      timesheets.append(os.path.join(dirpath, filename))
  return timesheets


tsfiles = find_timesheets(dir)

for filename in tsfiles:
  filepath = os.path.join(dir, filename)
  print(filepath)

  try:
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
      text += page.extract_text() + "\n"
  except:
    print("Error reading file: " + filepath)
    continue
  # print(text)
  with open(filename.replace('.pdf','.txt'), 'w') as f:
    f.write(text)

print("done")
