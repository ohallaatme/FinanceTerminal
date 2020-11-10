# imports and settings
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import CoreLabel
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView
import kivy.utils
# TODO: determine whether or not to change colors
# I should, need to create Atlas
# https://kivy.org/doc/stable/api-kivy.atlas.html
def notif_window(message, title):
    # text for popup message
    label = Label(text=message, halign="center", valign="middle")

    label.bind(size=lambda s, w: s.setter("text_size")(s, w))

    content = ScrollView()
    content.add_widget(label)

    pop = Popup(content=content, title=title, 
                size_hint=(None, None), size=(800, 300))

    # return rather than just open so we can dismiss when necessary
    return pop