from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.lang import Builder

Builder.load_file("menu.kv")

class MenuScreen(RelativeLayout):
    game_over_box = ObjectProperty()