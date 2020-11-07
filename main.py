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
        sm.current = "EduInfo"

class FinStmtAnalysis(Screen):
    def hit_select_cos(self):
        pass
    
    def hit_is_scorecard(self):
        pass

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
            EduInfo(name="EduInfo")]

# add screens to screen manager
for screen in screens:
    sm.add_widget(screen)

# set up menu screen as the current screen on launch
sm.current = "MenuScreen"

# TODO: PICKUP - BUILD OUT UI FILE
# build the data app
class FinanceApp(App):
    def build(self):
        return sm
        
if __name__ == '__main__':
    FinanceApp().run()