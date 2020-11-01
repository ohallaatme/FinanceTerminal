# imports and settings
import requests
import pandas as pd

class DataBase:
    def __init__(self, api_key="ZW30ZWIGT28FST2M"):
        self.api_key = api_key

        self.API_URL = "https://www.alphavantage.co/query"
        # store company results with ticker symbol
        # so the same requests aren't sent to the API multiple times
        self.is_company_results = {}
        self.bs_company_results = {}
        self.cf_company_results = {}

    # TODO: find appropriate way to document Python code
    def get_yrly_financials(self, symbol, statement):
        # store results for a particular company, will be added to the 
        # company_results field for class
        co_results = []

        # set parameters for request
        params = {"function": statement, 
                "symbol": symbol,
                "apikey": self.api_key
        }

        # send request for financial statement data
        resp = requests.get(self.API_URL, params)

        # convert into json to parse
        resp_json = resp.json()

        # json response has three k,v dict pairs, the symbol of the company
        # selected, the annualReports, and the quarterlyReports. For this function
        # we will grab annual reports
        annual_rpts = resp_json["annualReports"]

        # now we have a list of the five annual reports, each structured as a dictionary
        # where the first two k/v pairs represent the fiscalDateEnding and reportedCurrency.
        # the remainder is account/amount k/v pairs where the amt is in a string
        for rpt in annual_rpts:
            acct = []
            amt = []
            for k, v in rpt.items():
                acct.append(k)
                amt.append(v)
                
            # trim off the currency/date
            acct = acct[2:]    
            amt = amt[2:]
            
            # get rid of the 'None' values so we won't have conversion issues later
            i = 0
            for val in amt:
                if val == "None":
                    amt[i] = 0
                i+=1
            
            # dictionary to store column-header/value pairs to convert to eventual data frame
            fs_dict = {}
            fs_dict["Account"] = acct
            fs_dict["Amount"] = amt
            
            # turn dictionary into a DataFrame
            fs_df = pd.DataFrame.from_dict(fs_dict)
            
            # now add back the date and the currency as its own individual column
            fs_df["Date"] = rpt["fiscalDateEnding"]
            fs_df["Currency"] = rpt["reportedCurrency"]
            
            # column type conversions
            fs_df["Amount"] = fs_df["Amount"].astype(float)
            fs_df["Date"] = pd.to_datetime(fs_df["Date"])
            # finally, append to results list
            co_results.append(fs_df)
        
        # lastly, add entry to company_results
        if statement == "BALANCE_SHEET":
            self.bs_company_results[symbol] = co_results
        elif statement == "INCOME_STATEMENT":
            self.is_company_results[symbol] = co_results
        elif statement == "CASH_FLOW":
            self.cf_company_results[symbol] = co_results

    # Calcs the GMs for the symbol provided for the past 5 years
    # as long as the income statements have already been pulled for it
    # returns a nested dictionary with the symbol as the key for
    # each year with the GM %
    def calc_gm_perc(self, symbol):
        
        # store results, not creating class field as KPI methods
        # do not require a request to the server
        gp_company_results = {}

        # grab the companies past 5 yr income statements
        co_is = self.is_company_results[symbol]
        print("-"*100)
        print("Income Statements to Calc GM on:")
        
        print(co_is)
        # store results for loop
        results = {}

        for inc_stmt in co_is:

            # get gross profit $
            gp_line = inc_stmt[inc_stmt.Account == "grossProfit"]
            gp = gp_line.iloc[0]["Amount"]

            # get revenue $
            rev_line = inc_stmt.loc[inc_stmt.Account == "totalRevenue"]
            rev = rev_line.iloc[0]["Amount"]

            # get yr, the same for all rows so doesn't matter
            # what line we grab it from
            date_val = gp_line.iloc[0]['Date']
            yr = date_val.year


            # calc gp %
            gp_percent = gp/rev
            results[yr] = gp_percent
        
        gp_company_results[symbol] = results

        return gp_company_results




















