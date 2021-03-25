import pandas as pd
import re
import argparse


class IncomeStatement:
    """
    This class creates a monthly income statement report based on several inputs.

    :param str transactions_file: Path to file containing transaction records.
    :param str accounts_file: Path to file containing account records.
    """
    def __init__(self, transactions_file: str, accounts_file: str) -> None:
        self.transactions = pd.read_csv(transactions_file)
        self.accounts = pd.read_csv(accounts_file)
        self.income_statement = self.refresh()

    @staticmethod
    def __standardize_name(column: str) -> str:
        """Standardize column naming conventions

        This function takes a column name as input and returns the name standardized to snake case format.

        :param str column: Column name.
        :return: Returns column name in snake case format.
        :rtype: str
        """
        column = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', column)
        column = re.sub('([a-z0-9])([A-Z])', r'\1_\2', column).lower()
        column = re.sub(' +', '', column)
        return column

    def __get_unposted_transactions(self) -> pd.DataFrame:
        """Get unposted transactions

        :return: Returns a dataframe composed of unposted transactions.
        :rtype: str
        """
        return self.transactions[self.transactions.posting == False]

    def __get_posted_transactions(self) -> pd.DataFrame:
        """Get posted transactions

        :return: Returns a dataframe composed of posted transactions.
        :rtype: str
        """
        return self.transactions[self.transactions.posting == True]

    def refresh(self) -> pd.DataFrame:
        """Processes and aggregates input files into a monthly income statement.

        :return: Returns processed and aggregated data as a dataframe.
        :rtype: pd.DataFrame
        """
        # process
        data = pd.merge(left=self.__get_posted_transactions(), right=self.accounts, left_on='account',
                        right_on='Account Number')
        data['transaction_date'] = pd.to_datetime(data['transaction_date'])
        data['transaction_month'] = data['transaction_date'].dt.to_period('m')
        data.columns = map(self.__standardize_name, data.columns)

        # aggregate
        revenue = data[data.account_type == 'Revenue'].groupby('transaction_month')['amount'].sum()
        cost_of_revenue = data[data.account_type == 'Cost of Revenue'].groupby('transaction_month')['amount'].sum()
        stmt = pd.concat([revenue, cost_of_revenue], axis=1)
        stmt.columns = ['revenue', 'cost_of_revenue']
        stmt['gross_profit'] = stmt['revenue'] - stmt['cost_of_revenue']
        stmt['gross_margin'] = stmt['gross_profit'] / stmt['revenue']
        stmt['operational_expenses'] = data[data.account_type == 'Operating Expenses'].groupby('transaction_month')['amount'].sum()
        stmt['net_income'] = stmt['revenue'] - stmt['cost_of_revenue'] - stmt['operational_expenses']

        return stmt.round(2)

    def print_report(self) -> None:
        """Print income statement to standard out.
        """
        print(self.income_statement)

    def get_report(self) -> pd.DataFrame:
        """Get monthly income statement as a dataframe.

        :return: Returns income statement as a dataframe.
        :rtype: pd.DataFrame
        """
        return self.income_statement

    def save_report(self, filename: str = 'monthly_income_report.csv') -> None:
        """Saves income statement into CSV file.
        """
        self.income_statement.to_csv(filename, float_format='%.2f')


if __name__ == '__main__':
    """Command-Line Arguments for Monthly Income Statement Generator
    
    usage: income_statement.py <transaction_file> <account_file>
    help: income_statement.py -h for help
    """
    parser = argparse.ArgumentParser(description='Create monthly income statement report.')
    parser.add_argument('transaction_file', metavar='transaction_file', type=str, help='path to transaction file')
    parser.add_argument('account_file', metavar='account_file', type=str, help='path to account file')
    parser.add_argument('-q', '--quiet', action='store_true', help='suppresses report output to stdout')
    parser.add_argument('-f', '--output_file', action='store_true', help='output report to file')
    args = vars(parser.parse_args())

    statement = IncomeStatement(args['transaction_file'], args['account_file'])

    if args['quiet'] is False:
        statement.print_report()

    if args['output_file'] is True:
        statement.save_report()
