# imports and settings
from DataBase import DataBase

# driver code

# TODO: Write unit tests for code

# create instance of DataBase
fin_db = DataBase()

# get balance sheet
fin_db.get_yrly_financials("MSFT", "BALANCE_SHEET")

# income statement
fin_db.get_yrly_financials("MSFT", "INCOME_STATEMENT")


# test refactored method - net rec as % of sales
msft_net_rec_perc_ref = fin_db.calc_net_rec_perc("MSFT")

print("-"*100)
print("MSFT Net Rec as % of Sales: ")
print(msft_net_rec_perc_ref)

# test calc_cash_to_debt method
msft_cash_to_debt = fin_db.calc_cash_to_debt("MSFT")

print("-"*100)
print("MSFT Cash to Debt Ratio: ")
print(msft_cash_to_debt)
