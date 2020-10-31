# imports and settings
from DataBase import DataBase

# driver code

# TODO: Write unit tests for code


# create instance of DataBase
fin_db = DataBase()

fin_db.get_yrly_financials("MSFT", "INCOME_STATEMENT")
fin_db.get_yrly_financials("MSFT", "BALANCE_SHEET")
fin_db.get_yrly_financials("MSFT", "CASH_FLOW")


print("-"*100)
print("Income Statements: ")
print(fin_db.is_company_results)

print("-"*100)
print("Balance Sheets: ")
print(fin_db.bs_company_results)

print("-"*100)
print("Cash Flows: ")
print(fin_db.cf_company_results)
