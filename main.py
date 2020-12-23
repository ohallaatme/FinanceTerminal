# imports and settings

## kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.factory import Factory
from kivy import utils
from kivy.uix.recycleview import RecycleView


# parallel programming
import threading

# my mods
from DataBase import DataBase
from MobileScreens.Popup import notif_window

# df gui from kivy (pulled mainy from git)
from dfguik import DfguiWidget


""" -- Define Main Screens -- """
# Menu
class MenuScreen(Screen):
    # TODO: Add market cap data to finstmtanalysis results
    # can be found via company overview
    def hit_fin_stmt_analysis(self):
        sm.current = "FinStmtAnalysis"

    def hit_co_overview(self):
        sm.current = "CoOverview"

    def hit_ts_analysis(self):
        sm.current = "TimeSeriesAnalysis"

    def hit_edu_info(self):
        # test
        hello_window = notif_window("Hello World!", "First Program")
        hello_window.open()

        sm.current = "EduInfo"

class FinStmtAnalysis(Screen):
    def __init__(self, *args, **kwargs):
        super(FinStmtAnalysis, self).__init__(*args, **kwargs)
        # have to re render scorecard screens each time for dynamic view of data
        self.is_scorecard_run = False
        self.bs_scorecard_run = False
        self.cf_scorecard_run = False

    def hit_select_cos(self):
        sm.current = "CompanySelection"
    
    def hit_is_scorecard(self):
        # test on how to view tabular data
        # TODO: Modify to make it show the company data returned from DataBase methods
        # pull rolling income statements for selected companies


        # delete old scorecard if already run
        if self.is_scorecard_run:
            to_delete = sm.get_screen("IsScorecard")
            sm.clear_widgets([to_delete])

        sm.add_widget(IsScorecard(name="IsScorecard"))
        sm.current = "IsScorecard"

        self.is_scorecard_run = True

    def hit_bs_scorecard(self):
        pass

    def hit_cf_scorecard(self):
        pass
    
    # automate stocks being discussed/
    # w upcoming opportunity and score? top sector menu?
    # TODO: think of idea on what to develop here
    def hit_sector_scorecard(self):
        pass

    def hit_return_menu(self):
        sm.current = "MenuScreen"

class CoOverview(Screen):
    ticker = ObjectProperty(None)

    # define constructor to indicate whether we have instantiated a company
    # summary as this will change depending on what ticker the user enters
    def __init__(self, *args, **kwargs):
        super(CoOverview, self).__init__(*args, **kwargs)
        self.hit_co_summary = False

    
    def hit_set_ticker(self):
        ticker_valid = fin_db.set_co_selected(self.ticker.text)

        # TODO: 12.22.2020 -- INCLUDE LOGIC ON WHETHER OR NOT STATS WERE RUN
        # CREATE SCORECARD SCREEN TO MOCK THIS DESIGN PATTERN
        if ticker_valid:
            print(fin_db.co_selected)

            # run data 
            # TODO: potentially make another button
            co_overview_thread = threading.Thread(target=fin_db.get_co_overview)
            co_overview_thread.start()


    def hit_key_stats(self):
        if self.hit_co_summary:
            to_delete = sm.get_screen("CoStats")
            # clear_widgets takes an array argument
            sm.clear_widgets([to_delete])

        sm.add_widget(CoStats(name="CoStats"))
        sm.current = "CoStats"
        self.hit_co_summary = True
 

    def hit_industry_comparison(self):
        pass

    def hit_proc_3(self):
        pass

    def hit_proc_4(self):
        pass

    def hit_return_menu(self):
        sm.current = "MenuScreen"


class TimeSeriesAnalysis(Screen):
    def hit_proc_1(self):
        pass

    def hit_proc_2(self):
        pass

    def hit_proc_3(self):
        pass

    def hit_proc_4(self):
        pass

    def hit_return_menu(self):
        sm.current = "MenuScreen"


class EduInfo(Screen):
    def hit_proc_1(self):
        pass

    def hit_proc_2(self):
        pass

    def hit_proc_3(self):
        pass

    def hit_proc_4(self):
        pass

    def hit_return_menu(self):
        sm.current = "MenuScreen"

""" --- Financial Statement Anaysis SubScreens --- """
class CompanySelection(Screen):
    co_1 = ObjectProperty(None)
    co_2 = ObjectProperty(None)
    co_3 = ObjectProperty(None)
    co_4 = ObjectProperty(None)
    co_5 = ObjectProperty(None)
    co_6 = ObjectProperty(None)
    co_7 = ObjectProperty(None)
    co_8 = ObjectProperty(None)
    co_9 = ObjectProperty(None)
    co_10 = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(CompanySelection, self).__init__(*args, **kwargs)
        self.run_is = False
        self.run_bs = False
        self.run_cf = False

    def hit_back(self):
        sm.current = "FinStmtAnalysis"

    def is_checkbox_click(self, instance, value):
        if value is True:
            self.run_is = True
            print(self.run_is)
        else:
            self.run_is = False
            print(self.run_is)

    def bs_checkbox_click(self, instance, value):
        if value is True:
            self.run_bs = True
            print(self.run_bs)
        else:
            self.run_bs = False
            print(self.run_bs)

    def cf_checkbox_click(self, instance, value):
        if value is True:
            self.run_cf = True
            print(self.run_cf)
        else:
            self.run_cf = False
            print(self.run_cf)

    def hit_save_symbols(self):
        # determine whether or not to have an info
        # screen on the companies selected, for now go back to menu
        # and issue pop up
        sm.current = "FinStmtAnalysis"

        fin_db.co_1 = self.co_1.text.strip()
        fin_db.co_2 = self.co_2.text.strip()
        fin_db.co_3 = self.co_3.text.strip()
        fin_db.co_4 = self.co_4.text.strip()
        fin_db.co_5 = self.co_5.text.strip()
        fin_db.co_6 = self.co_6.text.strip()
        fin_db.co_7 = self.co_7.text.strip()
        fin_db.co_8 = self.co_8.text.strip()
        fin_db.co_9 = self.co_9.text.strip()
        fin_db.co_10 = self.co_10.text.strip()

        fin_db.set_symbols()

        # convert companies selected to a string to include in the popup window
        # to confirm companies the user selected
        popup_co_txt = ' '.join([str(elem) + " " for elem in fin_db.symbols])

        cos_set = notif_window("The following companies have been selected " + 
                                popup_co_txt, "Company Selection Complete")
                            
        cos_set.open()

        if self.run_is:
            # TODO: 12.23.2020 - NEED TO THREAD THE get_yrly_financials, 
            # can use boolean field within fin_db to control when compare_cos_thread
            # kicks off
            # TODO: Include check if company data already exists in results
            # prior to sending request
            for co in fin_db.symbols:
                fin_db.get_yrly_financials(co, "INCOME_STATEMENT")
            
            compare_cos_thread = threading.Thread(target=fin_db.compare_is_companies)
            compare_cos_thread.start()

""" --- Scorecard Screens ---"""
class IsScorecard(Screen):
    ## V2 - use labels and grid table view instead

    """ ---  Companies --- """
    co_1 = StringProperty('')
    co_2 = StringProperty('')
    co_3 = StringProperty('')
    co_4 = StringProperty('')
    co_5 = StringProperty('')
    co_6 = StringProperty('')
    co_7 = StringProperty('')
    co_8 = StringProperty('')
    co_9 = StringProperty('')
    co_10 = StringProperty('')
    

    """ --- Years --- """
    year_1 = StringProperty('')
    year_2 = StringProperty('')
    year_3 = StringProperty('')
    year_4 = StringProperty('')
    year_5 = StringProperty('')

    """ --- Gross Profit --- """
    # co 1
    gm_co1_y1 = StringProperty('')
    gm_co1_y2 = StringProperty('')
    gm_co1_y3 = StringProperty('')
    gm_co1_y4 = StringProperty('')
    gm_co1_y5 = StringProperty('')

    # co 2
    gm_co2_y1 = StringProperty('')
    gm_co2_y2 = StringProperty('')
    gm_co2_y3 = StringProperty('')
    gm_co2_y4 = StringProperty('')
    gm_co2_y5 = StringProperty('')

    # co 3
    gm_co3_y1 = StringProperty('')
    gm_co3_y2 = StringProperty('')
    gm_co3_y3 = StringProperty('')
    gm_co3_y4 = StringProperty('')
    gm_co3_y5 = StringProperty('')

    # co 4
    gm_co4_y1 = StringProperty('')
    gm_co4_y2 = StringProperty('')
    gm_co4_y3 = StringProperty('')
    gm_co4_y4 = StringProperty('')
    gm_co4_y5 = StringProperty('')

    # co 5
    gm_co5_y1 = StringProperty('')
    gm_co5_y2 = StringProperty('')
    gm_co5_y3 = StringProperty('')
    gm_co5_y4 = StringProperty('')
    gm_co5_y5 = StringProperty('')

    # co 6
    gm_co6_y1 = StringProperty('')
    gm_co6_y2 = StringProperty('')
    gm_co6_y3 = StringProperty('')
    gm_co6_y4 = StringProperty('')
    gm_co6_y5 = StringProperty('')

    # co 7
    gm_co7_y1 = StringProperty('')
    gm_co7_y2 = StringProperty('')
    gm_co7_y3 = StringProperty('')
    gm_co7_y4 = StringProperty('')
    gm_co7_y5 = StringProperty('')

    # co 8
    gm_co8_y1 = StringProperty('')
    gm_co8_y2 = StringProperty('')
    gm_co8_y3 = StringProperty('')
    gm_co8_y4 = StringProperty('')
    gm_co8_y5 = StringProperty('')

    # co 9
    gm_co9_y1 = StringProperty('')
    gm_co9_y2 = StringProperty('')
    gm_co9_y3 = StringProperty('')
    gm_co9_y4 = StringProperty('')
    gm_co9_y5 = StringProperty('')

    # co 10
    gm_co10_y1 = StringProperty('')
    gm_co10_y2 = StringProperty('')
    gm_co10_y3 = StringProperty('')
    gm_co10_y4 = StringProperty('')
    gm_co10_y5 = StringProperty('')

    """ --- SGA as % of GP --- """
    # co 1
    sga_gp_co1_y1 = StringProperty('')
    sga_gp_co1_y2 = StringProperty('')
    sga_gp_co1_y3 = StringProperty('')
    sga_gp_co1_y4 = StringProperty('')
    sga_gp_co1_y5 = StringProperty('')
    
    # co 2
    sga_gp_co2_y1 = StringProperty('')
    sga_gp_co2_y2 = StringProperty('')
    sga_gp_co2_y3 = StringProperty('')
    sga_gp_co2_y4 = StringProperty('')
    sga_gp_co2_y5 = StringProperty('')

    # co 3
    sga_gp_co3_y1 = StringProperty('')
    sga_gp_co3_y2 = StringProperty('')
    sga_gp_co3_y3 = StringProperty('')
    sga_gp_co3_y4 = StringProperty('')
    sga_gp_co3_y5 = StringProperty('')
    
    # co 4
    sga_gp_co4_y1 = StringProperty('')
    sga_gp_co4_y2 = StringProperty('')
    sga_gp_co4_y3 = StringProperty('')
    sga_gp_co4_y4 = StringProperty('')
    sga_gp_co4_y5 = StringProperty('')

    # co 5
    sga_gp_co5_y1 = StringProperty('')
    sga_gp_co5_y2 = StringProperty('')
    sga_gp_co5_y3 = StringProperty('')
    sga_gp_co5_y4 = StringProperty('')
    sga_gp_co5_y5 = StringProperty('')
    
    # co 6
    sga_gp_co6_y1 = StringProperty('')
    sga_gp_co6_y2 = StringProperty('')
    sga_gp_co6_y3 = StringProperty('')
    sga_gp_co6_y4 = StringProperty('')
    sga_gp_co6_y5 = StringProperty('')

    # co 7
    sga_gp_co7_y1 = StringProperty('')
    sga_gp_co7_y2 = StringProperty('')
    sga_gp_co7_y3 = StringProperty('')
    sga_gp_co7_y4 = StringProperty('')
    sga_gp_co7_y5 = StringProperty('')
    
    # co 8
    sga_gp_co8_y1 = StringProperty('')
    sga_gp_co8_y2 = StringProperty('')
    sga_gp_co8_y3 = StringProperty('')
    sga_gp_co8_y4 = StringProperty('')
    sga_gp_co8_y5 = StringProperty('')

    # co 9
    sga_gp_co9_y1 = StringProperty('')
    sga_gp_co9_y2 = StringProperty('')
    sga_gp_co9_y3 = StringProperty('')
    sga_gp_co9_y4 = StringProperty('')
    sga_gp_co9_y5 = StringProperty('')
    
    # co 10
    sga_gp_co10_y1 = StringProperty('')
    sga_gp_co10_y2 = StringProperty('')
    sga_gp_co10_y3 = StringProperty('')
    sga_gp_co10_y4 = StringProperty('')
    sga_gp_co10_y5 = StringProperty('')

    """ --- Interest Expense as % of OpInc --- """
    # co 1
    int_co1_y1 = StringProperty('')
    int_co1_y2 = StringProperty('')
    int_co1_y3 = StringProperty('')
    int_co1_y4 = StringProperty('')
    int_co1_y5 = StringProperty('')

    # co 2
    int_co2_y1 = StringProperty('')
    int_co2_y2 = StringProperty('')
    int_co2_y3 = StringProperty('')
    int_co2_y4 = StringProperty('')
    int_co2_y5 = StringProperty('')

    # co 3
    int_co3_y1 = StringProperty('')
    int_co3_y2 = StringProperty('')
    int_co3_y3 = StringProperty('')
    int_co3_y4 = StringProperty('')
    int_co3_y5 = StringProperty('')

    # co 4
    int_co4_y1 = StringProperty('')
    int_co4_y2 = StringProperty('')
    int_co4_y3 = StringProperty('')
    int_co4_y4 = StringProperty('')
    int_co4_y5 = StringProperty('')

    # co 5
    int_co5_y1 = StringProperty('')
    int_co5_y2 = StringProperty('')
    int_co5_y3 = StringProperty('')
    int_co5_y4 = StringProperty('')
    int_co5_y5 = StringProperty('')

    # co 6
    int_co6_y1 = StringProperty('')
    int_co6_y2 = StringProperty('')
    int_co6_y3 = StringProperty('')
    int_co6_y4 = StringProperty('')
    int_co6_y5 = StringProperty('')

    # co 7
    int_co7_y1 = StringProperty('')
    int_co7_y2 = StringProperty('')
    int_co7_y3 = StringProperty('')
    int_co7_y4 = StringProperty('')
    int_co7_y5 = StringProperty('')

    # co 8
    int_co8_y1 = StringProperty('')
    int_co8_y2 = StringProperty('')
    int_co8_y3 = StringProperty('')
    int_co8_y4 = StringProperty('')
    int_co8_y5 = StringProperty('')

    # co 9
    int_co9_y1 = StringProperty('')
    int_co9_y2 = StringProperty('')
    int_co9_y3 = StringProperty('')
    int_co9_y4 = StringProperty('')
    int_co9_y5 = StringProperty('')

    # co 10
    int_co10_y1 = StringProperty('')
    int_co10_y2 = StringProperty('')
    int_co10_y3 = StringProperty('')
    int_co10_y4 = StringProperty('')
    int_co10_y5 = StringProperty('')

    """ --- Tax Rate --- """
    # co 1
    tr_co1_y1 = StringProperty('')
    tr_co1_y2 = StringProperty('')
    tr_co1_y3 = StringProperty('')
    tr_co1_y4 = StringProperty('')
    tr_co1_y5 = StringProperty('')

    # co 2
    tr_co2_y1 = StringProperty('')
    tr_co2_y2 = StringProperty('')
    tr_co2_y3 = StringProperty('')
    tr_co2_y4 = StringProperty('')
    tr_co2_y5 = StringProperty('')

    # co 3
    tr_co3_y1 = StringProperty('')
    tr_co3_y2 = StringProperty('')
    tr_co3_y3 = StringProperty('')
    tr_co3_y4 = StringProperty('')
    tr_co3_y5 = StringProperty('')

    # co 4
    tr_co4_y1 = StringProperty('')
    tr_co4_y2 = StringProperty('')
    tr_co4_y3 = StringProperty('')
    tr_co4_y4 = StringProperty('')
    tr_co4_y5 = StringProperty('')

    # co 5
    tr_co5_y1 = StringProperty('')
    tr_co5_y2 = StringProperty('')
    tr_co5_y3 = StringProperty('')
    tr_co5_y4 = StringProperty('')
    tr_co5_y5 = StringProperty('')

    # co 6
    tr_co6_y1 = StringProperty('')
    tr_co6_y2 = StringProperty('')
    tr_co6_y3 = StringProperty('')
    tr_co6_y4 = StringProperty('')
    tr_co6_y5 = StringProperty('')

    # co 7
    tr_co7_y1 = StringProperty('')
    tr_co7_y2 = StringProperty('')
    tr_co7_y3 = StringProperty('')
    tr_co7_y4 = StringProperty('')
    tr_co7_y5 = StringProperty('')

    # co 8
    tr_co8_y1 = StringProperty('')
    tr_co8_y2 = StringProperty('')
    tr_co8_y3 = StringProperty('')
    tr_co8_y4 = StringProperty('')
    tr_co8_y5 = StringProperty('')

    # co 9
    tr_co9_y1 = StringProperty('')
    tr_co9_y2 = StringProperty('')
    tr_co9_y3 = StringProperty('')
    tr_co9_y4 = StringProperty('')
    tr_co9_y5 = StringProperty('')

    # co 10
    tr_co10_y1 = StringProperty('')
    tr_co10_y2 = StringProperty('')
    tr_co10_y3 = StringProperty('')
    tr_co10_y4 = StringProperty('')
    tr_co10_y5 = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(IsScorecard, self).__init__(*args, **kwargs)

        # KPIs can just be labels

        """ ---  Years --- """
        # Just take from co_1 for now
        # TODO: Will need to figure out how to handle mix of year ends where there are 6 years
        first_co = fin_db.gp_results[0][fin_db.symbols[0]]
        
        print("-"*100)
        print("First Company Ticker for years results: ")
        print(first_co)

        years = [key for key in first_co]

        print("-"*100)
        print("Years selected: ")
        print(years)

        # will need to make sure these are in the right order!
        # store numerical values seperately to use when querying out of the dictionary
        year_5 = years[0]
        year_4 = years[1]
        year_3 = years[2]
        year_2 = years[3]
        year_1 = years[4]

        # set the UI display properties, must be a String
        self.year_5 = str(year_5)
        self.year_4 = str(year_4)
        self.year_3 = str(year_3)
        self.year_2 = str(year_2)
        self.year_1 = str(year_1)

        """ --- Gross Profit Results --- """
        if len(fin_db.gp_results) >= 1:
            # pull nested dict from json of all companies
            co_1_gp = fin_db.gp_results[0]
            
            print("-"*100)
            print("co_1_gp")
            print(co_1_gp)

            # handle co data store here so data lines up correctly in UI
            # grab co ticker from nested dict
            
            co_1 = [key for key in co_1_gp]
            self.co_1 = co_1[0]

            print("-"*100)
            print("Company 1 Ticker")
            print(self.co_1)

            # grab dict of GM data for company
            gm_data = co_1_gp[self.co_1]
            
            print("-"*100)
            print("Gross Margin Data (should be dict with years as key, # as value")
            print(gm_data)

            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(gm_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(gm_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(gm_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(gm_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(gm_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.gm_co1_y5 = str(gm_data[year_5])
            if incl_yr_4:
                self.gm_co1_y4 = str(gm_data[year_4])
            if incl_yr_3:
                self.gm_co1_y3 = str(gm_data[year_3])
            if incl_yr_2:
                self.gm_co1_y2 = str(gm_data[year_2])
            if incl_yr_1:
                self.gm_co1_y1 = str(gm_data[year_1])

        if len(fin_db.gp_results) >= 2:
            # pull nested dict from json of all companies
            co_2_gp = fin_db.gp_results[1]
            
            print("-"*100)
            print("co_2_gp")
            print(co_2_gp)

            # handle co data store here so data lines up correctly in UI
            # grab co ticker from nested dict
            
            co_2 = [key for key in co_2_gp]
            self.co_2 = co_2[0]

            print("-"*100)
            print("Company 2 Ticker")
            print(self.co_2)

            # grab dict of GM data for company
            gm_data = co_2_gp[self.co_2]
            
            print("-"*100)
            print("Gross Margin Data (should be dict with years as key, # as value")
            print(gm_data)

            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(gm_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(gm_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(gm_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(gm_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(gm_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.gm_co2_y5 = str(gm_data[year_5])
            if incl_yr_4:
                self.gm_co2_y4 = str(gm_data[year_4])
            if incl_yr_3:
                self.gm_co2_y3 = str(gm_data[year_3])
            if incl_yr_2:
                self.gm_co2_y2 = str(gm_data[year_2])
            if incl_yr_1:
                self.gm_co2_y1 = str(gm_data[year_1])
        
        # co 3 gm
        if len(fin_db.gp_results) >= 3:
            # pull nested dict from json of all companies
            co_3_gp = fin_db.gp_results[2]
            
            print("-"*100)
            print("co_3_gp")
            print(co_3_gp)

            # handle co data store here so data lines up correctly in UI
            # grab co ticker from nested dict
            
            co_3 = [key for key in co_3_gp]
            self.co_3 = co_3[0]

            print("-"*100)
            print("Company 3 Ticker")
            print(self.co_3)

            # grab dict of GM data for company
            gm_data = co_3_gp[self.co_3]
            
            print("-"*100)
            print("Gross Margin Data (should be dict with years as key, # as value")
            print(gm_data)

            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(gm_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(gm_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(gm_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(gm_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(gm_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.gm_co3_y5 = str(gm_data[year_5])
            if incl_yr_4:
                self.gm_co3_y4 = str(gm_data[year_4])
            if incl_yr_3:
                self.gm_co3_y3 = str(gm_data[year_3])
            if incl_yr_2:
                self.gm_co3_y2 = str(gm_data[year_2])
            if incl_yr_1:
                self.gm_co3_y1 = str(gm_data[year_1])
        
        # co 4 gm
        if len(fin_db.gp_results) >= 4:
            # pull nested dict from json of all companies
            co_4_gp = fin_db.gp_results[3]
            
            print("-"*100)
            print("co_4_gp")
            print(co_4_gp)

            # handle co data store here so data lines up correctly in UI
            # grab co ticker from nested dict
            
            co_4 = [key for key in co_4_gp]
            self.co_4 = co_4[0]

            print("-"*100)
            print("Company 4 Ticker")
            print(self.co_4)

            # grab dict of GM data for company
            gm_data = co_4_gp[self.co_4]
            
            print("-"*100)
            print("Gross Margin Data (should be dict with years as key, # as value")
            print(gm_data)

            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(gm_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(gm_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(gm_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(gm_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(gm_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.gm_co4_y5 = str(gm_data[year_5])
            if incl_yr_4:
                self.gm_co4_y4 = str(gm_data[year_4])
            if incl_yr_3:
                self.gm_co4_y3 = str(gm_data[year_3])
            if incl_yr_2:
                self.gm_co4_y2 = str(gm_data[year_2])
            if incl_yr_1:
                self.gm_co4_y1 = str(gm_data[year_1])

        # co 5 gm
        if len(fin_db.gp_results) >= 5:
            # pull nested dict from json of all companies
            co_5_gp = fin_db.gp_results[4]
            
            print("-"*100)
            print("co_5_gp")
            print(co_5_gp)

            # handle co data store here so data lines up correctly in UI
            # grab co ticker from nested dict
            
            co_5 = [key for key in co_5_gp]
            self.co_5 = co_5[0]

            print("-"*100)
            print("Company 5 Ticker")
            print(self.co_5)

            # grab dict of GM data for company
            gm_data = co_5_gp[self.co_5]
            
            print("-"*100)
            print("Gross Margin Data (should be dict with years as key, # as value")
            print(gm_data)

            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(gm_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(gm_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(gm_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(gm_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(gm_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.gm_co5_y5 = str(gm_data[year_5])
            if incl_yr_4:
                self.gm_co5_y4 = str(gm_data[year_4])
            if incl_yr_3:
                self.gm_co5_y3 = str(gm_data[year_3])
            if incl_yr_2:
                self.gm_co5_y2 = str(gm_data[year_2])
            if incl_yr_1:
                self.gm_co5_y1 = str(gm_data[year_1])

        """ --- SGA as % of GP --- """
        # co 1 sga
        if len(fin_db.sga_results) >= 1:
            # pull nested dict from json of all companies
            co_1_sga = fin_db.sga_results[0]

            # grab dict of sga data for company
            sga_data = co_1_sga[self.co_1]


            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(sga_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(sga_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(sga_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(sga_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(sga_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.sga_gp_co1_y5 = str(sga_data[year_5])
            if incl_yr_4:
                self.sga_gp_co1_y4 = str(sga_data[year_4])
            if incl_yr_3:
                self.sga_gp_co1_y3 = str(sga_data[year_3])
            if incl_yr_2:
                self.sga_gp_co1_y2 = str(sga_data[year_2])
            if incl_yr_1:
                self.sga_gp_co1_y1 = str(sga_data[year_1])
        
        # co 2
        if len(fin_db.sga_results) >= 2:
            # pull nested dict from json of all companies
            co_2_sga = fin_db.sga_results[1]

            # grab dict of sga data for company
            sga_data = co_2_sga[self.co_2]


            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(sga_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(sga_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(sga_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(sga_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(sga_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.sga_gp_co2_y5 = str(sga_data[year_5])
            if incl_yr_4:
                self.sga_gp_co2_y4 = str(sga_data[year_4])
            if incl_yr_3:
                self.sga_gp_co2_y3 = str(sga_data[year_3])
            if incl_yr_2:
                self.sga_gp_co2_y2 = str(sga_data[year_2])
            if incl_yr_1:
                self.sga_gp_co2_y1 = str(sga_data[year_1])

        if len(fin_db.sga_results) >= 3:
            # pull nested dict from json of all companies
            co_3_sga = fin_db.sga_results[2]

            # grab dict of sga data for company
            sga_data = co_3_sga[self.co_3]

            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(sga_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(sga_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(sga_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(sga_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(sga_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.sga_gp_co3_y5 = str(sga_data[year_5])
            if incl_yr_4:
                self.sga_gp_co3_y4 = str(sga_data[year_4])
            if incl_yr_3:
                self.sga_gp_co3_y3 = str(sga_data[year_3])
            if incl_yr_2:
                self.sga_gp_co3_y2 = str(sga_data[year_2])
            if incl_yr_1:
                self.sga_gp_co3_y1 = str(sga_data[year_1])


        if len(fin_db.sga_results) >= 4:
            # pull nested dict from json of all companies
            co_4_sga = fin_db.sga_results[3]

            # grab dict of sga data for company
            sga_data = co_4_sga[self.co_4]

            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(sga_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(sga_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(sga_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(sga_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(sga_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.sga_gp_co4_y5 = str(sga_data[year_5])
            if incl_yr_4:
                self.sga_gp_co4_y4 = str(sga_data[year_4])
            if incl_yr_3:
                self.sga_gp_co4_y3 = str(sga_data[year_3])
            if incl_yr_2:
                self.sga_gp_co4_y2 = str(sga_data[year_2])
            if incl_yr_1:
                self.sga_gp_co4_y1 = str(sga_data[year_1])
        
        # co 5
        if len(fin_db.sga_results) >= 5:
            # pull nested dict from json of all companies
            co_5_sga = fin_db.sga_results[4]

            # grab dict of sga data for company
            sga_data = co_5_sga[self.co_5]

            # check if each year is included in the gm results, part of 
            # dynamic year end check
            incl_yr_5 = fin_db.check_dict_keys(sga_data, year_5)
            incl_yr_4 = fin_db.check_dict_keys(sga_data, year_4)
            incl_yr_3 = fin_db.check_dict_keys(sga_data, year_3)
            incl_yr_2 = fin_db.check_dict_keys(sga_data, year_2)
            incl_yr_1 = fin_db.check_dict_keys(sga_data, year_1)

            if incl_yr_5:
                # TODO: format text
                self.sga_gp_co5_y5 = str(sga_data[year_5])
            if incl_yr_4:
                self.sga_gp_co5_y4 = str(sga_data[year_4])
            if incl_yr_3:
                self.sga_gp_co5_y3 = str(sga_data[year_3])
            if incl_yr_2:
                self.sga_gp_co5_y2 = str(sga_data[year_2])
            if incl_yr_1:
                self.sga_gp_co5_y1 = str(sga_data[year_1])

    def hit_back(self):
        sm.current = "FinStmtAnalysis"

    def hit_return_menu(self):
        sm.current = "MenuScreen"



""" ---  Company Summary Subscreens --- """
class CoStats(Screen):
    ticker = StringProperty('')
    sector = StringProperty('')
    industry = StringProperty('')
    market_cap = StringProperty('')
    ebita = StringProperty('')
    pe_ratio = StringProperty('')

    # test at adding the object property detail
    def __init__(self, *args, **kwargs):
        super(CoStats, self).__init__(*args, **kwargs)
        self.ticker = fin_db.co_selected
        self.sector = fin_db.co_sector[fin_db.co_selected]
        self.industry = fin_db.co_industry[fin_db.co_selected]
        # TODO: figure out text formatting for #s for display (commas, $ sign, etc.)
        self.market_cap = str(fin_db.co_market_cap[fin_db.co_selected])
        self.ebita = str(fin_db.co_ebita[fin_db.co_selected])

        self.pe_ratio = str(fin_db.co_pe_ratio[fin_db.co_selected])

    def hit_back(self):
        sm.current = "CoOverview"

    def hit_return_menu(self):
        sm.current = "MenuScreen"

    # TODO: Write Export method, leverage original company comparison that 
    # converts data to DataFrame
    def export_to_excel(self):
        pass


# set up ScreenManager
class WindowManager(ScreenManager):
    pass


# create instance of WindowManager class to manage screens
sm = WindowManager()

# load UI
kv = Builder.load_file("FinanceAppUI.kv")

# list of screens
screens = [MenuScreen(name="MenuScreen"), FinStmtAnalysis(name="FinStmtAnalysis"),
            CoOverview(name="CoOverview"), TimeSeriesAnalysis(name="TimeSeriesAnalysis"),
            EduInfo(name="EduInfo"), CompanySelection(name="CompanySelection")]


# add screens to screen manager
for screen in screens:
    sm.add_widget(screen)

# set up menu screen as the current screen on launch
sm.current = "MenuScreen"

# instantiate instance of the DataBase class
# TODO - Address API Key input before publishing,
# for now make people get their own key
fin_db = DataBase()

# TODO: PICKUP - BUILD OUT UI FILE
# build the data app
class FinanceApp(App):
    def build(self):
        return sm
        
if __name__ == '__main__':
    FinanceApp().run()