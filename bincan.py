import pyxel
from time import sleep
from enum import Enum, auto

sensor = None

class STATE(Enum):
    NONE    = 0
    WALKING = 1
    FLYING  = 2
    GLIDING = 3
    FALLING = 4


class SHOWMODE(Enum):
    SceneChange = auto()
    Title = auto()
    Main = auto()
    End = auto()


class App:
    FIELD_Y = 120
    def __init__(self):
        pyxel.init(200, 150, caption="SENSING SENSEI", fps=60)
        self.init()
        pyxel.cls(5)
        pyxel.run(self.update, self.draw)

    def init(self):
        #loading image
        pyxel.image(0).load(0, 0, "resource/cat.png")
        #initialize status what player does
        self.player_state = STATE.NONE
        self.my_gamemode = SHOWMODE.Title
        #initialize count for first or not
        self.title_count = 0
        #initialize flags
        self.is_sensing = False
        self.is_dead = False
        #initialize player position
        self.player_x = 0
        self.player_y = self.FIELD_Y - 16
        #initialize dictionary for color pallet
        self.COLOR_PALLET = {
            "BLACK"       :   0,
            "DARK_BLUE"   :   1,
            "RED_PURPLE"  :   2,
            "GREEN"       :   3,
            "BROWN"       :   4,
            "GLAY"        :   5,
            "SILVER"      :   6,
            "WHITE"       :   7,
            "RED"         :   8,
            "ORANGE"      :   9,
            "YELLOW"      :   10,
            "LIGHT_GREEN" :   11,
            "BLUE"        :   12,
            "PURPLE"      :   13,
            "PINK"        :   14,
            "FLESH"       :   15,
        }
        self.BACKGROUND     =   self.COLOR_PALLET["BLACK"]
        self.GAMEMESSAGE    =   self.COLOR_PALLET["GLAY"]
        self.STAGE_GROUND   =   self.COLOR_PALLET["BROWN"]

    def update(self):
        if self.my_gamemode == SHOWMODE.SceneChange:
            self.update_scenechange()
        elif self.my_gamemode == SHOWMODE.Title:
            self.update_title()
        elif self.my_gamemode == SHOWMODE.Main:
            self.update_main()
        elif self.my_gamemode == SHOWMODE.End:
            self.update_ending()

    def update_scenechange(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.title_count += 1
            if self.title_count %2 == 1:
                self.my_gamemode = SHOWMODE.Main
            else:
                self.my_gamemode = SHOWMODE.Title

    def update_title(self):
        if pyxel.btn(pyxel.KEY_D):
            self.is_sensing = True
            #sensor = Sensor.generate(Sensors.DISTANCE, 7)
        elif pyxel.btn(pyxel.KEY_T):
            self.is_sensing = True
            #sensor = Sensor.generate(Sensors.TEMPERATURE, 7)
        elif pyxel.btn(pyxel.KEY_L):
            self.is_sensing = True
            #sensor = Sensor.generate(Sensors.LIGHT, 7)
        elif pyxel.btn(pyxel.KEY_P):
            self.is_sensing = True
            #sensor = Sensor.generate(Sensors.TOUCH, 7)
        elif pyxel.btnp(pyxel.KEY_SPACE) and self.is_sensing:
            self.is_dead = False
            self.my_gamemode = SHOWMODE.SceneChange

    def update_main(self):
        #screen transition
        if pyxel.btnp(pyxel.KEY_E):
            self.is_dead = True
            self.is_sensing = False
        else:
            self.is_dead = False
        if self.is_dead:
            self.my_gamemode = SHOWMODE.SceneChange

    def update_ending(self):
        pass

    def draw(self):
        if self.my_gamemode == SHOWMODE.SceneChange:
            self.draw_scene_change()
        elif self.my_gamemode == SHOWMODE.Title:
            self.draw_title()
        elif self.my_gamemode == SHOWMODE.Main:
            self.draw_main()
        elif self.my_gamemode == SHOWMODE.End:
            self.draw_ending()

    def draw_scene_change(self):
        pyxel.cls(self.BACKGROUND)
        if not self.is_dead:
            pyxel.text(60, 120, "PRESS SPACE TO START", 12)
        else:
            pyxel.text(58, 120, "PRESS SPACE TO RE:SET", 8)

    def draw_title(self):
        pyxel.cls(self.BACKGROUND)
        if self.title_count != 0:
            pyxel.text(25, 20, "NEW GAME+", 8)
        #laoding title image is not working in this code
        #intialize what kind of sensor is used to play
        pyxel.text(35, 60, "SELECT SENSORS WHAT YOU WANNA PLAY", self.random_color(self.GAMEMESSAGE, self.title_count+1, self.BACKGROUND))
        pyxel.text(50, 80, "D:Distance, T:Temperature,\n", self.random_color(self.GAMEMESSAGE, self.title_count+2, self.BACKGROUND))
        pyxel.text(62, 90, "L:Light, P:Pressure", self.random_color(self.GAMEMESSAGE, self.title_count+2, self.BACKGROUND))
        pyxel.text(60, 120, "PRESS SPACE TO READY", self.random_color(self.GAMEMESSAGE, self.title_count+3, self.BACKGROUND))

    def draw_main(self):
        pyxel.cls(self.BACKGROUND)
        pyxel.rect(0, self.FIELD_Y, pyxel.width, pyxel.height - self.FIELD_Y, self.STAGE_GROUND)

    def draw_ending(self):
        pass

    def random_color(self, def_num, rand_index, back_col):
        def_num += rand_index
        if back_col == def_num:
            def_num += 1
            return def_num
        else:
            return def_num

App()