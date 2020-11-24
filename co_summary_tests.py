# imports and settings
from DataBase import DataBase

# instantiate DataBase class
fin_db = DataBase()

# call eps method
fin_db.get_eps("MSFT")

# view results
msft_eps = fin_db.eps_company_results["MSFT"]

print("-"*100)
print("MSFT EPS Results: ")
print(msft_eps)


## Test get_co_overview method
msft_sector, msft_industry, msft_market_cap, msft_ebita, msft_pe_ratio =  fin_db.get_co_overview("MSFT")

print("-"*100)
print("MSFT Company Overview: ")

print("SECTOR: ")
print(msft_sector)

print("INDUSTRY: ")
print(msft_industry)

print("MARKET CAP: ")
print(msft_market_cap)

print("EBITA: ")
print(msft_ebita)

print("PE RATIO: ")
print(msft_pe_ratio)