from kivy.uix.relativelayout import RelativeLayout


def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None


def on_touch_down(self, touch):
    if not self.game_over and self.game_started: 
        if touch.x >= self.width / 2:
            self.current_h_speed = -self.SPEED_X
        else:
            self.current_h_speed = self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_up(self, touch):
    self.current_h_speed = 0


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'right':
        self.current_h_speed = -self.SPEED_X
    if keycode[1] == 'left':
        self.current_h_speed = self.SPEED_X
    return True


def on_keyboard_up(self, keyboard, keycode):
    self.current_h_speed = 0
