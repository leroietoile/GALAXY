'''
Developed by King Kakatsi
kingweb.pythonanywhere.com
'''

# from kivy.config import Config

# Config.set("graphics", "width", "900")
# Config.set("graphics", "height", "400")
import operator

from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from os import path
import json

from kivy.core.window import Window
from random import choice
from kivy.app import App
from kivy.graphics import Line, Color, Quad, Triangle, Ellipse
from kivy.properties import Clock, ObjectProperty, BooleanProperty, StringProperty, ListProperty, DictProperty
from kivy.uix.widget import Widget


class MainWidget(RelativeLayout):
    from transforms import transform, transform_perspective, transform_2D
    from user_actions import on_touch_up, on_touch_down, on_keyboard_down, on_keyboard_up, _keyboard_closed

    DIMENSION_GRAPH = "3D"
    game_over = False
    game_started = False
    menuscreen = ObjectProperty()
    start_btn_disabled = BooleanProperty(False)
    btn_text = StringProperty("START")
    score = StringProperty("0")
    record = StringProperty("00")
    record_man = StringProperty("--")
    user_choosen = BooleanProperty(False)
    user_bg_source = DictProperty({"LEROI":"images/B1.png", "DELALI": "images/B1.png", "DEFAULT": "images/B1.png", "": "images/B1.png", "+": "images/B4.png"})
    btn_color = DictProperty({"LEROI":[1, 1, 1], "DELALI": [1, 1, 1], "DEFAULT": [1, 1, 1], "": [1, 1, 1], "+": [1, 1, 1]})
    user_list = ListProperty(["LEROI", "DELALI", "DEFAULT"])
    input_window = ObjectProperty()
    text_input = ObjectProperty()
    new_user_added = BooleanProperty(False)

    PERSPECTIVE_POINT = {"x": 0, "y": 0}
    PERSP_OFFSET_Y = .75
    score_historic = []
    data = {"score":[], "users":["DEFAULT", "DEFAULT", "DEFAULT"]}
    user_name = "DEFAULT"
    toggles_state = StringProperty("normal") 
    # name_given_by_user = ""


    NB_VLINES = 8
    vline_list = []
    VSPACING_PERCT = .25

    NB_HLINES = 8
    hline_list = []
    HSPACING_PERCT = .15

    tiles = []
    NB_TILES = 6
    tiles_coord = []

    ship = None
    ship_coord = ["1st coord", "2nd coord", "3rd coord"]
    ship_width_perc = 0.3
    ship_height_perc = 0.3
    ship_bottom_pos_perc = 0.1
    ship_out_marge_perc_x = 0.3
    ship_out_marge_perc_y = 0.3

    FPS = 1/60
    speed_perc = .005
    SPEED_X_PERC = .02
    SPEED = 0
    SPEED_X = 0
    current_h_speed = 0
    v_moving_factor = 0
    v_moving_factor_tile = 0
    h_moving_factor = 0
    nb_loop = 0
    prev_nb_loop = 0
    last_y = 0

    n = 0
    change_speed_score_fact = 0
    speed_fact_divisor = 1
    first_run = True

    begin_sound = None
    galaxy_sound = None
    gameover_impact_sound = None
    gameover_voice_sound = None
    restart_sound = None
    music1_sound = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.init_sounds()
        
        if path.exists('historic.txt'):
            with open('historic.txt', 'r') as h:
                data = h.read()
                self.data = json.loads(data)
        self.score_historic = list(self.data["score"])
        self.user_list = list(self.data["users"])
        for user in self.user_list:
            self.btn_color[user] = [1, 1, 1]  
            self.user_bg_source[user] =  "images/B1.png"

        if len(self.score_historic) > 0:
            record = max(self.score_historic, key=lambda x: x[1])[1]
            self.record = str(record)
            self.record_man = max(self.score_historic, key=lambda x: x[1])[0]

        self.create_graphics()
        self.generate_first_tile_field()

        if len(self.tiles_coord) > 0:
            self.last_y = self.tiles_coord[-1][1]
        self.generate_tiles_index()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        self.galaxy_sound.play()

        Clock.schedule_interval(self.update, self.FPS)

    def on_size(self, *args):
        self.PERSPECTIVE_POINT["x"] = self.width / 2
        self.PERSPECTIVE_POINT["y"] = self.height * self.PERSP_OFFSET_Y
        self.SPEED = self.speed_perc * self.height
        self.SPEED_X = self.SPEED_X_PERC * self.width

    def start_game(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        self.speed_perc = 0.005
        self.current_h_speed = 0
        self.v_moving_factor = 0
        self.h_moving_factor = 0
        self.nb_loop = 0
        self.tiles_coord = []
        self.generate_first_tile_field()
        self.game_over = False
        self.start_btn_disabled = True
        self.menuscreen.game_over_box.opacity = 1

        if len(self.tiles_coord) > 0:
            self.last_y = self.tiles_coord[-1][1]
        
        self.game_started = True
        self.menuscreen.opacity = 0    

        if not self.first_run:
            self.restart_sound.play()
        else:
            self.begin_sound.play()
        self.music1_sound.play() 

        self.user_name = self.user_name.strip().upper()
        if self.user_name in self.user_list:
            self.user_list.remove(self.user_name)
        # self.toggles_state = 'normal'
        self.btn_color[self.user_name] = [1, 1, 1]
        if not self.user_name == 'DEFAULT':
            self.user_list.insert(0, self.user_name)  


    def update(self, dt):
        self.score = str(self.nb_loop)
        self.SPEED = self.speed_perc * self.height
        self.speed_regulator()
        self.update_graphics()
        if not self.game_over and self.game_started:            
            delay_perc = dt/self.FPS
            self.v_moving_factor += self.SPEED * delay_perc
            self.v_moving_factor_tile += self.SPEED * delay_perc
            self.h_moving_factor += self.current_h_speed * delay_perc
            self.check_ship()
        else:
            self.menuscreen.opacity = 1
            self.start_btn_disabled = False
            
        if self.game_over and self.n == 0:
            self.n += 1
            # return False
        


    def create_graphics(self):
        # ..............// INIT OF VERTICAL LINES //...........................
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.NB_VLINES):
                self.vline_list.append(Line())

        # ..............//INIT OF HORIZONTAL LINES //...........................
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.NB_HLINES):
                self.hline_list.append(Line())

        # ..............//INIT OF TILES //...........................
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.NB_TILES):
                self.tiles.append(Quad())

        # ..................// SHIP //...................
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

        # ....................// BOMB //.......................
        # with self.canvas:
        #     self.bomb = Ellipse()

    def update_graphics(self):
        # ..............// VERTICAL LINES //...........................
        start_index = -int(self.NB_VLINES / 2)
        end_index = int(self.NB_VLINES / 2) + 1
        for i in range(start_index, end_index):
            x1 = self.get_x_from_index(i) + self.h_moving_factor
            y1 = 0
            x2 = x1
            y2 = self.height
            x1, y1 = self.transform(x1, y1, dimension=self.DIMENSION_GRAPH)
            x2, y2 = self.transform(x2, y2, dimension=self.DIMENSION_GRAPH)
            self.vline_list[i].points = (int(x1), int(y1), int(x2), int(y2))

        # ..............// HORIZONTAL LINES //...........................

        x_min = self.get_x_from_index(start_index + 1)
        x_max = self.get_x_from_index(end_index - 1)
        spacing_y = self.HSPACING_PERCT * self.height
        for i in range(self.NB_HLINES):
            y = self.get_y_from_index(i) - self.v_moving_factor
            x1 = x_min + self.h_moving_factor
            x2 = x_max + self.h_moving_factor
            x1, y1 = self.transform(x1, y, dimension=self.DIMENSION_GRAPH)
            x2, y2 = self.transform(x2, y, dimension=self.DIMENSION_GRAPH)
            self.hline_list[i].points = (int(x1), int(y1), int(x2), int(y2))

            # ...............// TILES //..................
            for i in range(self.NB_TILES):
                self.tiles[i].points = self.generate_tile_coord(*self.tiles_coord[i])

            # ................. // SHIP //..........................
            spacing = self.VSPACING_PERCT * self.width
            ship_width = self.ship_width_perc * spacing
            ship_height = self.ship_height_perc * spacing_y
            ship_bottom_pos = self.ship_bottom_pos_perc * spacing_y

            x1, y1 = self.transform(self.PERSPECTIVE_POINT["x"] - (ship_width / 2), ship_bottom_pos, dimension="2D")
            x2, y2 = self.transform(self.PERSPECTIVE_POINT["x"], ship_bottom_pos + ship_height, dimension="2D")
            x3, y3 = self.transform(self.PERSPECTIVE_POINT["x"] + (ship_width / 2), ship_bottom_pos, dimension="2D")

            self.ship.points = (x1, y1, x2, y2, x3, y3)
            self.ship_coord[0], self.ship_coord[1], self.ship_coord[2] = (x1, y1), (x2, y2), (x3, y3)

            # ...........// CONDITION POUR CREER UN EFFET DE BOUCLE POUR LE DEPLACEMENT VERS L'AVANT //..............
            while self.v_moving_factor >= spacing_y:
                self.v_moving_factor -= spacing_y
                self.nb_loop += 1
                self.generate_tiles_index()

    def update_bomb(self):
        #..........// BOMB SIZE //............................
        self.bomb.size = (dp(10), dp(5))
        #............// UPDATE BOMB POSITION //....................
        limit_left_down_x, limit_left_down_y, limit_left_top_x, limit_left_top_y, limit_right_top_x, limit_right_top_y, limit_right_down_x, limit_right_down_y = self.tiles[2].points

    def generate_first_tile_field(self):
        for i in range(6):
            self.tiles_coord.append((0, i))

    def get_x_from_index(self, index):
        index -= 0.5
        spacing = self.VSPACING_PERCT*self.width
        x = self.PERSPECTIVE_POINT["x"] + spacing * index
        return x

    def get_y_from_index(self, index):
        spacing = self.HSPACING_PERCT * self.height
        y = index * spacing
        return y

    def generate_tiles_index(self):
        left_border_index = -int(self.NB_VLINES / 2) + 1
        right_border_index = int(self.NB_VLINES / 2) - 1
        last_x = 0
        movements = ("left", "strate", "right")
        choosen_movement = choice(movements)
        #...................// DELETE PASSED TILES //.......................
        for i in range(len(self.tiles_coord) - 1, -1, -1):
            if self.tiles_coord[i][1] < self.nb_loop:
                del self.tiles_coord[i]

        if len(self.tiles_coord) > 0:
            last_x = self.tiles_coord[-1][0]

        for i in range(len(self.tiles_coord), self.NB_TILES):
            self.tiles_coord.append((last_x, self.last_y))

            if choosen_movement == 'left':
                if last_x <= left_border_index:
                    choosen_movement = "right"
                else:
                    last_x -= 1
                    self.tiles_coord.append((last_x, self.last_y))
                    self.last_y += 1
                    self.tiles_coord.append((last_x, self.last_y))

            if choosen_movement == 'right':
                if last_x >= right_border_index:
                    choosen_movement = "left"
                else:
                    last_x += 1
                    self.tiles_coord.append((last_x, self.last_y))
                    self.last_y += 1
                    self.tiles_coord.append((last_x, self.last_y))
            self.last_y += 1

    def generate_tile_coord(self, index_x, index_y):
        spacing_y = self.HSPACING_PERCT * self.height
        x_min = self.get_x_from_index(index_x) + self.h_moving_factor
        y_min = self.get_y_from_index(index_y) - (self.v_moving_factor + (self.nb_loop * spacing_y))
        x_max = self.get_x_from_index(index_x + 1) + self.h_moving_factor
        y_max = self.get_y_from_index(index_y + 1) - (self.v_moving_factor + (self.nb_loop * spacing_y))

        x1, y1 = self.transform(x_min, y_min, dimension=self.DIMENSION_GRAPH)
        x2, y2 = self.transform(x_min, y_max, dimension=self.DIMENSION_GRAPH)
        x3, y3 = self.transform(x_max, y_max, dimension=self.DIMENSION_GRAPH)
        x4, y4 = self.transform(x_max, y_min, dimension=self.DIMENSION_GRAPH)
        return x1, y1, x2, y2, x3, y3, x4, y4

    def check_ship(self):
        first_tile_coord = self.tiles[0].points
        second_tile_coord = self.tiles[2].points

        spacing = self.VSPACING_PERCT * self.width
        spacing_y = self.HSPACING_PERCT * self.height
        ship_width = self.ship_width_perc * spacing
        ship_height = self.ship_height_perc * spacing_y

        x1, y1 = self.ship_coord[0]
        x2, y2 = self.ship_coord[1]
        x3, y3  = self.ship_coord[2]

        marge_x = self.ship_out_marge_perc_x * ship_width
        marge_y = self.ship_out_marge_perc_y * ship_height
        ship_top, ship_bottom = y2 - marge_y, y1 + marge_y
        ship_left, ship_rihgt = x1 + marge_x, x3 - marge_x
        
        if self.tiles_coord[0][0] == self.tiles_coord[1][0]:
            ship_top = -10

        x_min, y_min, x_max, y_max = first_tile_coord[0], first_tile_coord[1], first_tile_coord[6], first_tile_coord[5]
        
        if self.tiles_coord[0][1] == self.tiles_coord[1][1]:
            if first_tile_coord[0] < second_tile_coord[0]: # ---->
                x_max = second_tile_coord[6]
                if ship_left > second_tile_coord[0]:
                    ship_top = -10
            else: # <----                
                x_min = second_tile_coord[0]
                if ship_rihgt < first_tile_coord[0]:
                    ship_top = -10
        
        if (ship_left > x_min) and (ship_rihgt < x_max) and (ship_top < y_max) and (ship_bottom > y_min):
            self.game_over = False
        else:
            self.game_over = True
            self.btn_text = "RESTART"
            self.first_run = False
            # ..................// ENREGISTREMENT DU SCORE //...............
            self.score_historic.insert(0, (self.user_name, int(self.score) + 1))
            self.data["score"] = self.score_historic
            self.data["users"] = self.user_list
            self.user_name = "DEFAULT"
            # _______________// RECHERCHER LE RECORD //________________________
            if len(self.score_historic) > 0:
                record = max(self.score_historic, key=lambda x: x[1])[1]
                self.record = str(record)
                self.record_man = max(self.score_historic, key=lambda x: x[1])[0]
            # _______________// ENREGISTREMENT DE L'HISTORIQUE DANS UN FICHIER //_____________
            with open('historic.txt', 'w') as h:
                h.write(json.dumps(self.data))

            self.gameover_impact_sound.play()
            self.music1_sound.stop()
            self.gameover_voice_sound.play()

    def speed_regulator(self):
        if int(self.score) >= self.change_speed_score_fact:
            self.speed_fact_divisor *= 2
            self.speed_perc += .000001
            self.change_speed_score_fact += int(20 / self.speed_fact_divisor)

    def choose_user(self, widget):
        if widget.state == "down":
            self.user_name = widget.text
            self.user_choosen = True
            self.btn_color[widget.text] = [1, 0, 0]
        else:
            self.user_name = "default"
            self.user_choosen = False
            self.btn_color[widget.text] = [1, 1, 1]

    def add_user(self, widget):
        self.input_window.window_disabled = False
        self.btn_color[widget.text] = [1, 0, 0.4]
        self.widget = widget
        self.input_window.window_disabled = False
        Clock.schedule_once(self.reset_add_user_btn_color, 1/10)

    def reset_add_user_btn_color(self, dt):
        self.btn_color[self.widget.text] = [1, 1, 1]

    def validate_name_given(self, widget):
        self.user_name = self.text_input.text
        self.user_name = self.user_name.strip().upper()
        if self.user_name in self.user_list:
            self.user_list.remove(self.user_name)
            self.new_user_added = False
        else:
            self.new_user_added = True

        temporary_user_list = list(self.user_list)
        temporary_user_list.insert(0, self.user_name) 
        for user in temporary_user_list:
            self.btn_color[user] = [1, 1, 1]  
            self.user_bg_source[user] =  "images/B1.png"
        self.input_window.window_disabled = True
        self.user_list = list(temporary_user_list) 
        # .......................................................... 
        # ............// UPDATE BUTTON COLORS //....................

#...............................................................
#.....................// INIT SOUNDS //.........................
    def init_sounds(self):
        self.begin_sound = SoundLoader.load("audio/begin.wav")
        self.begin_sound.volume = .25

        self.galaxy_sound = SoundLoader.load("audio/galaxy.wav")
        self.galaxy_sound.volume = .6

        self.gameover_impact_sound = SoundLoader.load("audio/gameover_impact.wav")
        self.gameover_impact_sound.volume = .25

        self.gameover_voice_sound = SoundLoader.load("audio/gameover_voice.wav")
        self.gameover_voice_sound.volume = .6

        self.restart_sound = SoundLoader.load("audio/restart.wav")
        self.restart_sound.volume = .25

        self.music1_sound = SoundLoader.load("audio/music1.wav")
        self.music1_sound.volume = 1



class InputUserNameWindow(RelativeLayout):
    window_disabled = BooleanProperty(True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.check_to_close, 1/20)

    def close_textinput_window(self, widget):
        self.window_disabled = True

    def check_to_close(self, dt):
        if self.window_disabled:
            self.opacity = .8
            self.pos_hint = {"right": 3, "top": 1}
        else:
            self.opacity = 1
            self.pos_hint = {"center_x": .5, "center_y": .5}

class TextField(TextInput):
    pass
    # def _on_textinput_focused(self, instance, value, *largs):
    #     if not instance.focus:
    #         app = App.get_running_app()



class GalaxyApp(App):
    pass


GalaxyApp().run()
