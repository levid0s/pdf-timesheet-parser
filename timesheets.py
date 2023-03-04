import os
import fnmatch
import re
import locale
import sys
from decimal import *
from tabulate import tabulate
from PyPDF2 import PdfReader

dir = sys.argv[1]

class Timesheet:
  def __init__(self, tax_year, week):
    self.tax_year = tax_year
    self.week = week

  def __hash__(self):
    return hash(self.tax_year + self.week)

  @property
  def s_check(self):
    diff = self.gp_f - self.pension_f - self.alevy_f - self.erni_f - self.mar_f - self.paye_f - self.eeni_f - self.pension_2 - self.bank_f
    return diff

  @property
  def ee_gross(self):
    diff = self.gp_f - self.pension_f - self.alevy_f - self.erni_f - self.mar_f
    return diff


def ts_summarize(timesheets):
  header = ["TAX_YEAR", "Week", "INCOME", "PENSION", "PENSION_2", "HOLIDAY", "ER_NI", "aLEVY", "NASA_MAR", "UNITS", "RATE","EE_GROSS", "PAYE", "EENI", "BANK", "S_CHECK", "PAY_DATE"]
  data = []
  for ts in timesheets:
    data += [[ts.tax_year, ts.week, ts.gp_f,ts.pension_f, ts.pension_2, ts.holiday, ts.erni_f, ts.alevy_f, ts.mar_f, ts.units_t, ts.rate_t, ts.ee_gross, ts.paye_f, ts.eeni_f, ts.bank_f, ts.s_check, ts.pay_date]]
  table = tabulate(data, headers=header)
  print(table)

def read_timesheet_data_f(text, key, skips=0, optional=False):
  search_string = key + ("\n.*?"*skips) + "\n(\\(?[\d,.]+)\\)?\\n"
  try:
    value = re.search(search_string, text).group(1)
    value = value.replace('(', '-')
  except:
    value = '0'
    if not optional:
      print("Error searching for " + search_string)
      print(text)
  value = Decimal(value.replace(',', ''))
  return Decimal(f"{value:.2f}")

def read_timesheet_data_s(text, key, skips=0, optional=False):
  search_string = key + ("\n.*?"*skips) + "\n(.*?)\\n"
  try:
    value = re.search(search_string, text).group(1)
  except:
    value = ''
    if not optional:
      print("ERROR: searching for `" + search_string + "`")
      print(text)
  return value


def find_timesheets(root_dir):
  timesheets = []
  for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in fnmatch.filter(filenames, "*Payroll*.pdf"):
      timesheets.append(os.path.join(dirpath, filename))
  return timesheets


Timesheets = []

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

  tax_year = re.search("Payslips\\\\([\d\-]+)\\\\", filepath).group(1)
  tax_period = int(re.search("Tax Period\n([\d,.]+)", text).group(1))

  ts = Timesheet(tax_year, tax_period)

  ts.pension_f = read_timesheet_data_f(text, "Private Pension", optional=True)
  if ts.pension_f == 0 and re.search("Personal[\\s\\n]Pension", text) != None:
    ts.pension_f = abs(read_timesheet_data_f(text, "Weekend[\\s\\n]Date", 7, optional=True))
  ts.pension_2 = read_timesheet_data_f(text, "Employees Pension Deductions", optional=True)
  ts.holiday = read_timesheet_data_f(text, "Holiday Pay",1, optional=True)
  
  if ts.pension_f == 0:
    ts.gp_f = read_timesheet_data_f(text, "Company Income and Costs")
  else:
    ts.gp_f = read_timesheet_data_f(text, "Rate\\nTotal",5, optional=True)
    if ts.gp_f == 0:
      ts.gp_f = read_timesheet_data_f(text, "Rate\\nTotal",4)
  ts.erni_f = read_timesheet_data_f(text, "(?:Employment Costs|Employer's NI)")
  ts.alevy_f = read_timesheet_data_f(text, "Apprenticeship Levy", optional=True)
  ts.mar_f = read_timesheet_data_f(text, "Company Margin")

  ts.units_t = read_timesheet_data_f(text, "Units\nRate", 3, optional=True)
  if(ts.units_t == 0):
    ts.units_t = read_timesheet_data_f(text, "Units\nRate", 4)
  if(ts.pension_f == 0):
    if (read_timesheet_data_f(text, "Units\nRate", 8, optional=True)<=5):
      ts.units_t += read_timesheet_data_f(text, "Units\nRate", 8, optional=True)
  ts.rate_t = read_timesheet_data_f(text, "Rate\nTotal", 3)
  if(ts.rate_t < 100):
    ts.rate_t = read_timesheet_data_f(text, "Rate\nTotal", 4)

  ts.paye_f = read_timesheet_data_f(text, "PAYE\\(Income tax\\)")
  ts.eeni_f = read_timesheet_data_f(text, "Employee's NIC")
  ts.bank_f = read_timesheet_data_f(text, "Total Payment \\(£\\)")
  ts.pay_date = read_timesheet_data_s(text, "Pay Date", 5)
  if ts.pay_date == 'X':
    ts.pay_date = read_timesheet_data_s(text, "Pay Date", 6)

  if abs(ts.s_check) > 1:
    print(text)

  Timesheets.append( ts)

Timesheets.sort(key=lambda x: f"{x.tax_year}:{x.week:02d}")

ts_summarize(Timesheets)

print("done")
