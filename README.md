## Readme

Python script that crawls all my PDF payslips that are in a very specific format from my provider; and creates a summary.

Does a basic sanity check (`S_CHECK`), ie the calculations on the PDF are correct.

### Usage:

```
  python -m venv env
  env\Scripts\activate
  pip install -r requirements.txt

  python timesheets.py c:\path\to\payslips
```

### Sample output:

(The numbers are obviously random)

```
TAX_YEAR      Week    INCOME    PENSION    PENSION_2    HOLIDAY    ER_NI    aLEVY    UMB_MAR    UNITS    RATE    EE_GROSS     PAYE    EENI      BANK    S_CHECK  PAY_DATE
----------  ------  --------  ---------  -----------  ---------  -------  -------  ----------  -------  ------  ----------  -------  ------  --------  ---------  ----------
2019-20         49    1125            0          0       123.12   101.01     0           17.5      5       225      892.32     0      48.55    465.1        0     15/03/2020
2019-20         50    1125            0          0       123.12   101.01     0           17.5      5       225      892.32    24.2    48.55    840.9        0     21/03/2020
2019-20         51    1125            0          0       123.12   101.01     0           17.5      5       225      892.32    74.6    48.55    790.5        0     25/03/2020
2019-20         52    1125            0          0       123.12   101.01     0           17.5      5       225      892.32    74.8    48.55    790.3        0     01/04/2020
2020-21          1    1125          500          0        53.65    80.7      0           17.5      5       225      426.8    130.17   02.78     93.84       0.01  06/04/2020
2020-21          2    1300          500          0        15.92    27.5      0           17.5      4       225      205       41.77   22.64    100.59       0     18/04/2020
2020-21          3    1300          500          0        15.92    27.5      0           17.5      4       225      205       11.06   22.64    591.3       -0.01  20/04/2020
```
