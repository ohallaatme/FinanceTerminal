# imports and settings
from DataBase import DataBase
import pandas as pd

# driver code

# TODO: Write unit tests for code


# create instance of DataBase
fin_db = DataBase()

fin_db.get_yrly_financials("MSFT", "INCOME_STATEMENT")
fin_db.get_yrly_financials("AAPL", "INCOME_STATEMENT")
fin_db.get_yrly_financials("GOOG", "INCOME_STATEMENT")
fin_db.get_yrly_financials("UBER", "INCOME_STATEMENT")
fin_db.get_yrly_financials("FB", "INCOME_STATEMENT")

is_scorecard = fin_db.compare_companies("MSFT", "AAPL", "GOOG", "UBER", "FB")
is_scorecard.to_excel(r"/Users/katherineohalloran/Documents/FinanceKivyApp/TestData/test-scorecard.xlsx")
print("-"*100)
print("Income Statement Scorecard Results: ")
print(is_scorecard)