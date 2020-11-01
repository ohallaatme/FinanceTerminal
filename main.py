# imports and settings
from DataBase import DataBase

# driver code

# TODO: Write unit tests for code


# create instance of DataBase
fin_db = DataBase()

fin_db.get_yrly_financials("MSFT", "INCOME_STATEMENT")

print("-"*100)
print("Income Statement Results: ")
print(fin_db.is_company_results)

msft_gp = fin_db.calc_gm_perc("MSFT")

print("-"*100)
print("Microsoft Gross Profit: ")
print(msft_gp)