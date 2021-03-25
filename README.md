# Income Statement

Income Statement is a Python package that takes a transaction and account file as input, processes & aggregates them, and outputs the result. It may be used from the command line or imported into another script or notebook.

## Usage

Command Line:
```bash
>>> python income_statement.py -h   
                        
usage: income_statement.py [-h] [-q] [-f] transaction_file account_file

Create monthly income statement report.

positional arguments:
  transaction_file   path to transaction file
  account_file       path to account file

optional arguments:
  -h, --help         show this help message and exit
  -q, --quiet        suppresses report output to stdout
  -f, --output_file  output report to file


>>> python income_statement.py transactions.csv accounts.csv
              
                       revenue  cost_of_revenue  gross_profit  gross_margin  operational_expenses   net_income
transaction_month                                                                                             
2019-01             1031437.67        626463.14     404974.53          0.39            1986880.79  -1581906.26
2019-02             1179373.21        881038.33     298334.88          0.25            1680709.50  -1382374.62
2019-03             1012066.46        918445.93      93620.53          0.09            1915225.38  -1821604.85
2019-04             1159220.50       1213241.95     -54021.45         -0.05            2129930.87  -2183952.32
2019-05             1053017.97       1063737.56     -10719.59         -0.01            2286592.39  -2297311.98
(cont.)
```

Import:
```python
from income_statement import IncomeStatement

# return DataFrame
monthly_statement = IncomeStatement('transactions.csv', 'accounts.csv').get_report()

# print to stdout
monthly_statement = IncomeStatement('transactions.csv', 'accounts.csv').print_report()

# save to CSV
monthly_statement = IncomeStatement('transactions.csv', 'accounts.csv').save_report('output.csv')
```