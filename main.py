# imports and settings

## kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
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
    def hit_select_cos(self):
        sm.current = "CompanySelection"
    
    def hit_is_scorecard(self):
        # test on how to view tabular data
        # TODO: Modify to make it show the company data returned from DataBase methods
        sm.current = "IsScorecard"

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
    # call parent constructor so we can add dfguik widget to screen and move via ScreenManager
    def __init__(self, **kwargs):
        super(IsScorecard, self).__init__(**kwargs)
        # TODO: Replace with Income Statement info
        self.df = create_dummy_data(1000)
        self.add_widget(DfguiWidget(self.df))

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
            EduInfo(name="EduInfo"), CompanySelection(name="CompanySelection"), 
            IsScorecard(name="IsScorecard")]


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