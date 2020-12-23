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
# for testing, remove eventually
from demo import create_dummy_data

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
        for co in fin_db.symbols:
            fin_db.get_yrly_financials(co, "INCOME_STATEMENT")

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

    def hit_back(self):
        sm.current = "FinStmtAnalysis"

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

    # TODO - 12.22.2020 - PICKUP FINISH INTEREST EXPENSE AND TAX RATE, BULD DATA BASE
    # END AND UI
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