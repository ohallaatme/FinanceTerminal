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

msft_sga = fin_db.calc_sga_perc("MSFT")
print("-"*100)
print("Microsoft SG&A")
print(msft_sga)


msft_int_exp = fin_db.calc_int_perc("MSFT")
print("-"*100)
print("Microsoft Interest Expense as a % of Operating Income")
print(msft_int_exp)

msft_inc_before_tax, msft_tax_exp, msft_tax_perc = fin_db.tax_exp_test("MSFT")

print("-"*100)
print("Microsoft Income Before Taxes")
print(msft_inc_before_tax)

print("-"*100)
print("Microsoft Tax Expense")
print(msft_tax_exp)


print("-"*100)
print("Microsoft Percent Paid (Taxes)")
print(msft_tax_perc)