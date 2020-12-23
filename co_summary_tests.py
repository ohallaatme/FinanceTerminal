# imports and settings
from DataBase import DataBase

# instantiate DataBase class
fin_db = DataBase()

# set company selected 
fin_db.set_co_selected("MSFT")

# call eps method
fin_db.get_eps("MSFT")

# view results
msft_eps = fin_db.eps_company_results["MSFT"]

print("-"*100)
print("MSFT EPS Results: ")
print(msft_eps)

## Test get_co_overview method
fin_db.get_co_overview("MSFT")

print("-"*100)
print("MSFT Company Overview: ")

print("SECTOR: ")
msft_sector = fin_db.co_sector["MSFT"]
print(msft_sector)

print("INDUSTRY: ")
msft_industry = fin_db.co_industry["MSFT"]
print(msft_industry)

print("MARKET CAP: ")
msft_mkt_cap = fin_db.co_market_cap["MSFT"]
print(msft_mkt_cap)

print("EBITA: ")
msft_ebita = fin_db.co_ebita["MSFT"]
print(msft_ebita)

print("PE RATIO: ")
msft_pe_ratio = fin_db.co_pe_ratio["MSFT"]
print(msft_pe_ratio)
