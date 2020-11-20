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
