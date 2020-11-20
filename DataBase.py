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


        """ fields for companies selected to analyze """
        # incl 10 for now
        self.co_1 = None
        self.co_2 = None
        self.co_3 = None
        self.co_4 = None
        self.co_5 = None
        self.co_6 = None
        self.co_7 = None
        self.co_8 = None
        self.co_9 = None
        self.co_10 = None

        # list to store company symbols
        self.symbols = []
    
    # method (setter) to set list of company symbols to analyze
    def set_symbols(self):
        # create list that is not set as field to loop through logic
        # and only append co fields with values to the company symbol list (self.symbols)
        test_list = []
        test_list.append(self.co_1)
        test_list.append(self.co_2)
        test_list.append(self.co_3)
        test_list.append(self.co_4)
        test_list.append(self.co_5)
        test_list.append(self.co_6)
        test_list.append(self.co_7)
        test_list.append(self.co_8)
        test_list.append(self.co_9)
        test_list.append(self.co_10)
        
        for co in test_list: 
            if co == None or co == "":
                continue
            else:
                self.symbols.append(co)

    
    # Returns dictionary with year and account balance 
    # @acct: The account you want the values for
    # @stmt: The financial statement, three string options: "BALANCE_SHEET", "INCOME_STATEMENT", "CASH_FLOWS"
    # @symbol: the stock ticker for the company desired
    def get_acct_balance(self, acct, stmt, symbol):
        if stmt == "BALANCE_SHEET":
            co_data = self.bs_company_results[symbol]
        elif stmt == "INCOME_STATEMENT":
            co_data = self.is_company_results[symbol]
        elif stmt == "CASH_FLOWS":
            co_data = self.cf_company_results[symbol]
        else:
            # TODO: throw pop up error or raise exception, for now break
            print("Invalid Statement Argument")
            return

        # store results from loop 
        results = {}
        for stmt in co_data:
            
            # get amount from account passed 
            val_line = stmt[stmt.Account == acct]
            val = val_line.iloc[0]["Amount"]

            # get year of financial statement
            date_val = val_line.iloc[0]["Date"]
            yr = date_val.year

            # add to results dictionary
            results[yr] = val

        # TODO: PICKUP 11.16.2020 
        # Refactor KPI Methods to leverage get_acct_balance to make code more DRY
        return results

        
    
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

    """ Income Statement KPIs """
    # Calcs the GMs for the symbol provided for the past 5 years
    # as long as the income statements have already been pulled for it
    # returns a nested dictionary with the symbol as the key for
    # each year with the GM %
    def calc_gm_perc(self, symbol):
        
        # store results, not creating class field as KPI methods
        # do not require a request to the server
        gp_company_results = {}
        print("-"*100)
        print(str(symbol) + " Results")
        print(gp_company_results.keys())
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

    # calc SGA as % of Gross Profit
    def calc_sga_perc(self, symbol):
        
        # store final results
        sga_co_results = {}

        # grab company's past 5 years of income statements
        co_is = self.is_company_results[symbol]

        # store results from loop
        results = {}

        for inc_stmt in co_is:
                    
            # get GP $
            gp_line = inc_stmt[inc_stmt.Account == "grossProfit"]
            gp = gp_line.iloc[0]["Amount"]
            
            # sga $
            sga_line = inc_stmt[inc_stmt.Account == "sellingGeneralAdministrative"]
            sga = sga_line = sga_line.iloc[0]["Amount"]
            
            # get yr, the same for all rows so doesn't matter
            # what line we grab it from
            date_val = gp_line.iloc[0]["Date"]
            yr = date_val.year
            
            # calc sga %
            sga_perc = sga/gp
            results[yr] = sga_perc
        
        sga_co_results[symbol] = results
        return sga_co_results


    def calc_int_perc(self, symbol):

        # store final results
        int_co_results = {}

        # grab company's past 5 years of income statements
        co_is = self.is_company_results[symbol]

        # store results from loop
        results = {}

        for inc_stmt in co_is:

            # get GP $
            op_line = inc_stmt[inc_stmt.Account == "operatingIncome"]
            op_inc = op_line.iloc[0]["Amount"]

            # get Interest Exp $
            int_line = inc_stmt[inc_stmt.Account == "interestExpense"]
            int_exp = int_line.iloc[0]["Amount"]

            # get yr, the same for all rows
            date_val = op_line.iloc[0]["Date"]
            yr = date_val.year

            # calc int_exp %
            int_perc = int_exp/op_inc
            results[yr] = int_perc

        int_co_results[symbol] = results
        return int_co_results

    # method determines if tax expense reported is 35% of income vefore taxes, if it doesn't match, 
    # where is the extra income coming from?
    # calc for the 5 years
    def tax_exp_test(self, symbol):
        
        # store final results
        inc_tax_perc_co_results = {}

        # store tax exp results
        tax_exp_results = {}

        # store inc before taxes
        inc_before_tax_results = {}

        # grab company's past 5 years of income statements
        co_is = self.is_company_results[symbol]

        # store results from loop
        inc_results = {}
        tax_results = {}
        perc_results = {}

        for inc_stmt in co_is:
            
            # get income before tax $
            inc_before_tax_line = inc_stmt[inc_stmt.Account == "incomeBeforeTax"]
            inc_before_tax = inc_before_tax_line.iloc[0]["Amount"]

            # get tax $
            tax_line = inc_stmt[inc_stmt.Account == "incomeTaxExpense"]
            tax_exp = tax_line.iloc[0]["Amount"]

            # get yr
            date_val = tax_line.iloc[0]["Date"]
            yr = date_val.year

            # Try returning tax exp as a percent of income before tax for starter

            inc_results[yr] = inc_before_tax
            tax_results[yr] = tax_exp


            inc_tax_perc = tax_exp/inc_before_tax
            perc_results[yr] = inc_tax_perc

        inc_before_tax_results[yr] = inc_results
        tax_exp_results[symbol] = tax_results

        inc_tax_perc_co_results[symbol] = perc_results
        return inc_before_tax_results, tax_exp_results, inc_tax_perc_co_results

    # only returns the inc tax % paid
    def tax_exp_perc(self, symbol):
        
        # store final results
        inc_tax_perc_co_results = {}    

        # grab company's past 5 years of income statements
        co_is = self.is_company_results[symbol]

        # store results from loop
        perc_results = {}

        for inc_stmt in co_is:
            
            # get income before tax $
            inc_before_tax_line = inc_stmt[inc_stmt.Account == "incomeBeforeTax"]
            inc_before_tax = inc_before_tax_line.iloc[0]["Amount"]

            # get tax $
            tax_line = inc_stmt[inc_stmt.Account == "incomeTaxExpense"]
            tax_exp = tax_line.iloc[0]["Amount"]

            # get yr
            date_val = tax_line.iloc[0]["Date"]
            yr = date_val.year

            # Try returning tax exp as a percent of income before tax for starter

            inc_tax_perc = tax_exp/inc_before_tax
            perc_results[yr] = inc_tax_perc

        inc_tax_perc_co_results[symbol] = perc_results
        return inc_tax_perc_co_results

    """ Balance Sheet KPIs """
    # refactored method to use get_acct_balance method
    def calc_net_rec_perc(self, symbol):

        # store final results
        net_rec_co_results = {}

        # get revenue values
        sales_vals = self.get_acct_balance("totalRevenue", "INCOME_STATEMENT", symbol)
        net_rec_vals = self.get_acct_balance("netReceivables", "BALANCE_SHEET", symbol)

        # get years, doesn't matter which dict we take it from
        # both statements will have the same years
        years = [year for year in sales_vals.keys()]

        # results for year loop
        results = {}

        # calc perc by year
        for year in years:
            sales = sales_vals[year]
            net_rec = net_rec_vals[year]

            net_rec_perc = net_rec/sales
            results[year] = net_rec_perc

        # add to final results by ticker
        net_rec_co_results[symbol] = results
        return net_rec_co_results
        
    def calc_cash_to_debt(self, symbol):

        # store final results
        cash_to_debt_results = {}

        ## get asset values
        # cash
        cash_vals = self.get_acct_balance("cash", "BALANCE_SHEET", symbol)
        # short term investments
        st_inv_values = self.get_acct_balance("shortTermInvestments", "BALANCE_SHEET", symbol)

        ## get liability values
        # short term debt
        st_debt_vals = self.get_acct_balance("shortTermDebt", "BALANCE_SHEET", symbol)
        # long term debt
        lt_debt_vals = self.get_acct_balance("longTermDebt", "BALANCE_SHEET", symbol)

        # get years
        # will be the same for each dict so can use any
        years = [year for year in cash_vals.keys()]

        # results for year loop
        results = {}

        for year in years:
            ## assets
            cash = cash_vals[year]
            st_inv = st_inv_values[year]
            
            # ensure data type reads correctly
            cash = float(cash)
            st_inv = float(st_inv)

            # get total cash & equivilants
            tot_cash_and_equiv = cash + st_inv
            
            ## liabilites (debt)
            st_debt = st_debt_vals[year]
            lt_debt = lt_debt_vals[year]

            # ensure decimal data type
            st_debt = float(st_debt)
            lt_debt = float(lt_debt)

            # get total debt
            tot_debt = st_debt + lt_debt

            # calc ratio of cash & equivilants to debt
            cash_to_debt = tot_cash_and_equiv/tot_debt
            results[year] = cash_to_debt

        # add to final results by ticker
        cash_to_debt_results[symbol] = results
        return cash_to_debt_results
        
    # compare income statement ratios of 5 companies
    # will eventually have to make more dynamic
    def compare_companies(self, symbol_1, symbol_2, symbol_3, symbol_4, symbol_5):
        
        is_results = {}

        companies = [symbol_1, symbol_2, symbol_3, symbol_4, symbol_5]

        ## Gross Margin % Calculation
        gp_results = [self.calc_gm_perc(company) for company in companies]

        ## SGA Percent
        sga_results = [self.calc_sga_perc(company) for company in companies]

        ## Interest Percent
        int_results = [self.calc_int_perc(company) for company in companies]

        ## Tax Expense
        tax_perc_results = [self.tax_exp_perc(company) for company in companies]

        """ --- Convert Results into one consolidated DF """

        # append df of results for final concat to produce final output frame
        is_results = []

        ## GP
        gp_dfs = []

        for co in gp_results:
            df = pd.DataFrame.from_dict(co, orient="index")
            df["KPI"] = "Gross Profit %"
            df["Company"] = df.index
            gp_dfs.append(df)

        gp_frame = pd.concat(gp_dfs).reset_index(drop=True)

        is_results.append(gp_frame)

        ## SGA
        sga_dfs = []


        for co in sga_results:
            df = pd.DataFrame.from_dict(co, orient="index")
            df["KPI"] = "SGA as % of Gross Profit"
            df["Company"] = df.index
            sga_dfs.append(df)

        sga_frame = pd.concat(sga_dfs).reset_index(drop=True)

        is_results.append(sga_frame)

        ## Int Exp
        int_dfs = []

        for co in int_results:
            df = pd.DataFrame.from_dict(co, orient="index")
            df["KPI"] = "Interest Expense as % of OpInc"
            df["Company"] = df.index
            int_dfs.append(df)

        int_frame = pd.concat(int_dfs).reset_index(drop=True)

        is_results.append(int_frame)

        ## Tax Rate
        tax_dfs = []

        for co in tax_perc_results:
            df = pd.DataFrame.from_dict(co, orient="index")
            df["KPI"] = "Tax Rate"
            df["Company"] = df.index
            tax_dfs.append(df)

        tax_frame = pd.concat(tax_dfs).reset_index(drop=True)

        is_results.append(tax_frame)

        is_frame = pd.concat(is_results).reset_index(drop=True)
        
        print(is_frame.columns)
        # below fixes col ordering issue but keeps dynamic considering
        # years are dynamic depending on company/time pulled
        is_frame.set_index(["Company", "KPI"], inplace=True)

        new_col_names = ["Year End " + str(col) for col in is_frame.columns]
        is_frame.columns = new_col_names

        is_frame["Company/KPI"] = is_frame.index
        cols = [x for x in is_frame.columns]

        new_cols = [ele for ele in reversed(cols)]

        is_frame_final = is_frame[new_cols]

        is_frame_final.to_excel("/Users/katherineohalloran/Documents/FinanceKivyApp/TestData/Income Statement Scorecard.xlsx")

        return is_frame_final