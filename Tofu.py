import pyxel
from enum import Enum, auto
import random
#from sensor import *

sensor = None

class STATE(Enum):
    NONE        = auto()
    WALKING     = auto()
    FLYING      = auto()
    FALL        = auto()
    GLIDE   = auto()

class SELECT(Enum):
    NONE        = auto()
    DISTANCE    = auto()
    TEMPERATURE = auto()
    LIGHT       = auto()
    PRESSURE    = auto()

class SHOWMODE(Enum):
    SceneChange = auto()
    Start       = auto()
    Title       = auto()
    Main        = auto()
    End         = auto()

class SCENECHANGE(Enum):
    FIRST   = auto()
    SECOND  = auto()
    THIRD   = auto()
    FOURTH  = auto()
    FIFTH   = auto()

class App:
    FIELD_Y = 102
    def __init__(self):
        pyxel.init(200, 150, caption="TOBU!TOFU!", fps=60)
        self.init()
        self.init_player()
        pyxel.cls(5)
        pyxel.run(self.update, self.draw)

    def init(self):
        #loading image
        pyxel.load("resource/kogemikan.pyxres")
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
        #initialize status what player does
        self.player_state   =   STATE.NONE
        self.now_gamemode   =   SHOWMODE.Title
        self.was_gamemode   =   None
        self.selected_sensor=   SELECT.NONE
        #initialize count
        self.title_count    =   0
        self.was_data       =   0
        self.sec_count      =   0
        self.now_frame      =   0
        self.scene_change_p =   None
        #initialize flags
        self.is_sensing     =   False
        self.is_dead        =   False
        self.is_on_ground   =   True
        self.is_top_passed  =   False
        self.once_called    =   False
        #initialize colors
        self.BACKGROUND     =   self.COLOR_PALLET["BLACK"]
        self.GAMEMESSAGE    =   self.COLOR_PALLET["GLAY"]
        self.STAGE_GROUND   =   self.COLOR_PALLET["GREEN"]
        self.FLASH          =   self.COLOR_PALLET["YELLOW"]
        self.RECT_COLOR     =   self.COLOR_PALLET["BLACK"]
        self.GRID_COLOR     =   self.COLOR_PALLET["BLACK"]
        #initialize image's constant number
        self.TOFU           =   0
        self.LOGO           =   1
        self.DOT_16         =   0
        self.BLOCK_NONE     =   48
        self.BLOCK_FLY      =   64
        self.BLOCK_GLIDE    =   80
        #initialize array for TEST
        self.TEST_LIST      =   [i for i in range(100)]

    def init_player(self):
        #initialize player information
        self.player_x       =   50
        self.player_y       =   self.FIELD_Y - 16
        self.vector_y       =   1
        self.player_size_x  =   16
        self.player_size_y  =   16
        self.player_colkey  =   self.COLOR_PALLET["BLACK"]
        #initialize threshold value for decide what's going on
        #self.NOSIE should be sensor.mapped_data()
        #bcuz it's default value for sensing
        self.NOISE          =   10
        self.WALK           =   self.NOISE+self.NOISE*3
        self.GLIDE          =   self.WALK+self.WALK*3

    def init_stage(self):
        self.block_size_x   =   16
        self.block_size_y   =   16

    def update(self):
        if self.now_gamemode == SHOWMODE.SceneChange:
            self.update_scenechange()
        elif self.now_gamemode == SHOWMODE.Title:
            self.update_title()
        elif self.now_gamemode == SHOWMODE.Main:
            self.update_main()
        elif self.now_gamemode == SHOWMODE.Start:
            self.update_start()
        elif self.now_gamemode == SHOWMODE.End:
            self.update_ending()

    def update_scenechange(self):
        if not self.once_called:
            self.once_called = True
            self.now_frame   = pyxel.frame_count%180
        if (pyxel.frame_count - self.now_frame)%180 < 30:
            self.scene_change_p = SCENECHANGE.FIRST
        elif (pyxel.frame_count - self.now_frame)%180 < 60:
            self.scene_change_p = SCENECHANGE.SECOND
        elif (pyxel.frame_count - self.now_frame)%180 < 90:
            self.scene_change_p = SCENECHANGE.THIRD
        elif (pyxel.frame_count - self.now_frame)%180 < 120:
            self.scene_change_p = SCENECHANGE.FOURTH
        elif (pyxel.frame_count - self.now_frame)%180 < 150:
            self.scene_change_p = SCENECHANGE.FIFTH
        if (pyxel.frame_count - self.now_frame)%50 == 0:
            self.sec_count += 1
            if self.sec_count == 4:
                self.scene_change_p = None
                self.sec_count      = 0
                self.now_frame      = 0
                self.once_called    = False
                if self.was_gamemode == SHOWMODE.Title:
                    self.now_gamemode = SHOWMODE.Start
                elif self.was_gamemode == SHOWMODE.Main:
                    self.now_gamemode = SHOWMODE.Title
                #add elif self.was_gamemode == SHOWMODE.Main and self.is_game_clear:
                #       self.now_gamemode = SHOWMODE.End

    def update_start(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.was_gamemode == SHOWMODE.Title:
                self.was_gamemode = SHOWMODE.Start
                self.now_gamemode = SHOWMODE.Main
            else:
                self.was_gamemode = SHOWMODE.Start
                self.now_gamemode = SHOWMODE.Title

    def update_title(self):
        self.init_player()
        if pyxel.btn(pyxel.KEY_D):
            self.is_sensing     =   True
            self.selected_sensor=   SELECT.DISTANCE
        elif pyxel.btn(pyxel.KEY_T):
            self.is_sensing     =   True
            self.selected_sensor=   SELECT.TEMPERATURE
        elif pyxel.btn(pyxel.KEY_L):
            self.is_sensing     =   True
            self.selected_sensor=   SELECT.LIGHT
        elif pyxel.btn(pyxel.KEY_P):
            self.is_sensing     =   True
            self.selected_sensor=   SELECT.PRESSURE
        elif pyxel.btn(pyxel.KEY_SPACE) and self.is_sensing:
            self.is_dead = False
            if self.selected_sensor == SELECT.DISTANCE:
                #sensor = Sensor.generate(Sensors.DISTANCE, 7)
                pass
            elif self.selected_sensor == SELECT.TEMPERATURE:
                #sensor = Sensor.generate(Sensors.TEMPERATURE, 7)
                pass
            elif self.selected_sensor == SELECT.LIGHT:
                #sensor = Sensor.generate(Sensors.LIGHT, 7)
                pass
            elif self.selected_sensor == SELECT.PRESSURE:
                #sensor = Sensor.generate(Sensors.TOUCH, 7)
                pass
            self.was_gamemode = SHOWMODE.Title
            self.now_gamemode = SHOWMODE.SceneChange

    def update_main(self):
        this_index = pyxel.frame_count%100
        #FLAG : player is on ground or not
        if self.player_y == self.FIELD_Y - self.player_size_y:
            self.is_on_ground = True
        else:
            self.is_on_ground = False
        #do gravity if player is not on ground
        if not self.is_on_ground:
            self.player_y += self.vector_y
        #FLAG : data is increasing or not
        # if sensor.mapped_data() < self.was_data:
        #     self.is_top_passed = True
        if self.TEST_LIST[this_index] < self.was_data:
            self.is_top_passed = True
        elif self.is_on_ground:
            self.is_top_passed = False
        #codes are below is temporary disable for testing
        # if self.NOISE < sensor.mapped_data():
        #     if sensor.mapped_data() <= self.WALK and self.is_on_ground:
        #         if self.player_x < pyxel.width - self.player_size_x:
        #             self.player_x       +=  1
        #             self.player_state   =   STATE.WALKING
        #     else:
        #         if 0 <= self.player_y and sensor.mapped_data() < self.GLIDE:
        #             self.player_y       -=  2
        #             self.player_x       +=  1
        #             self.player_state   =   STATE.FLYING
        #             if self.GLIDE <= sensor.mapped_data() and self.is_top_passed:
        #                 if self.player_y < self.FIELD_Y - self.player_size_y:
        #                     self.player_y       +=  1
        #                     self.player_x       +=  1
        #                     self.player_state   =   STATE.GLIDING
        #             elif not self.is_on_ground and self.is_top_passed and sensor.mapped_data() < self.GLIDE:
        #                 self.player_y += 2
        # if self.player_state == STATE.WALKING:
        #     if sensor.mapped_data() <= self.NOISE:
        #         self.player_state = STATE.NONE

        #this is temporary code for testing
        #delete or disable after testing
        #input flag
        if self.NOISE < self.TEST_LIST[this_index]:
        #flying flag
            if self.WALK < self.TEST_LIST[this_index] and not self.is_top_passed:
                self.is_on_ground = False
                self.player_state = STATE.FLYING
                if 0 <= self.player_y:
                    #self.player_x += 1
                    self.player_y -= 2
        #glide flag
            elif self.GLIDE < self.TEST_LIST[this_index] and self.is_top_passed:
                self.player_state = STATE.GLIDE
                if self.player_y < self.FIELD_Y - self.player_size_y:
                    #self.player_x += 2
                    self.player_y += 1
            elif self.TEST_LIST[this_index] < self.WALK:
                self.player_state = STATE.WALKING
                #self.player_x += 2
        else:
            if self.is_on_ground:
                self.player_state = STATE.NONE
            else:
                self.player_state = STATE.FALL



        self.was_data = self.TEST_LIST[this_index]
        #RELOAD POSITION TO DEBUG
        if pyxel.btn(pyxel.KEY_R):
            self.init_player()

        #screen transition
        if pyxel.btn(pyxel.KEY_E):
            self.is_dead = True
            #add delete sensor
            self.is_sensing = False
        else:
            self.is_dead = False
        if self.is_dead:
            self.title_count += 1
            self.selected_sensor = SELECT.NONE
            self.was_gamemode = SHOWMODE.Main
            self.now_gamemode = SHOWMODE.SceneChange

    def update_ending(self):
        pass

    def draw(self):
        if self.now_gamemode == SHOWMODE.SceneChange:
            self.draw_scene_change()
        elif self.now_gamemode == SHOWMODE.Title:
            self.draw_title()
        elif self.now_gamemode == SHOWMODE.Main:
            self.draw_main()
        elif self.now_gamemode == SHOWMODE.Start:
            self.draw_start()
        elif self.now_gamemode == SHOWMODE.End:
            self.draw_ending()

    def draw_scene_change(self):
        if self.scene_change_p == SCENECHANGE.FIRST:
            #clipping short side
            pyxel.rect(0, 15, 20, 120, self.RECT_COLOR)
            pyxel.rect(180, 15, 20, 120, self.RECT_COLOR)
            #clipping long side
            pyxel.rect(0, 0, 200, 15, self.RECT_COLOR)
            pyxel.rect(0, 135, 200, 15, self.RECT_COLOR)
        elif self.scene_change_p == SCENECHANGE.SECOND:
            #clipping short side
            pyxel.rect(20, 30, 20, 90, self.RECT_COLOR)
            pyxel.rect(160, 30, 20, 90, self.RECT_COLOR)
            #clipping long side
            pyxel.rect(20, 15, 160, 15, self.RECT_COLOR)
            pyxel.rect(20, 120, 160, 15, self.RECT_COLOR)
        elif self.scene_change_p == SCENECHANGE.THIRD:
            #clipping short side
            pyxel.rect(40, 45, 20, 60, self.RECT_COLOR)
            pyxel.rect(140, 45, 20, 60, self.RECT_COLOR)
            #clipping long side
            pyxel.rect(40, 30, 120, 15, self.RECT_COLOR)
            pyxel.rect(40, 105, 120, 15, self.RECT_COLOR)
        elif self.scene_change_p == SCENECHANGE.FOURTH:
            #clipping short side
            pyxel.rect(60, 60, 20, 30, self.RECT_COLOR)
            pyxel.rect(120, 60, 20, 30, self.RECT_COLOR)
            #clipping long side
            pyxel.rect(60, 45, 80, 15, self.RECT_COLOR)
            pyxel.rect(60, 90, 80, 15, self.RECT_COLOR)
        elif self.scene_change_p == SCENECHANGE.FIFTH:
            #clipping long side
            pyxel.rect(80, 60, 40, 30, self.RECT_COLOR)


    def draw_start(self):
        pyxel.cls(self.BACKGROUND)
        if not self.is_dead:
            pyxel.text(60, 120, "PRESS SPACE TO START", self.COLOR_PALLET["BLUE"])
        else:
            pyxel.text(58, 120, "PRESS SPACE TO RE:SET", self.COLOR_PALLET["RED"])

    def draw_title(self):
        pyxel.cls(self.BACKGROUND)
        if self.was_gamemode == SHOWMODE.Main:
            pyxel.text(25, 20, "NEW GAME+", 8)
        pyxel.blt(80, 20, self.TOFU, 25, 0, 63, 16, self.BACKGROUND)
        #show sentence for introducing
        pyxel.text(35, 50, "SELECT SENSORS WHAT YOU WANNA PLAY", self.random_color(self.GAMEMESSAGE, self.title_count+1, self.BACKGROUND))
        pyxel.text(50, 70, "D:Distance, T:Temperature,", self.random_color(self.GAMEMESSAGE, self.title_count+2, self.BACKGROUND))
        pyxel.text(62, 80, "L:Light, P:Pressure", self.random_color(self.GAMEMESSAGE, self.title_count+2, self.BACKGROUND))
        pyxel.text(60, 95, "PRESS SPACE TO READY", self.random_color(self.GAMEMESSAGE, self.title_count+3, self.BACKGROUND))
        #show images for introducing
        #show candle
        pyxel.blt(110, 113, self.LOGO, 0, 0, 32, 32, self.BACKGROUND)
        if self.selected_sensor == SELECT.LIGHT and pyxel.frame_count%60 >= 30:
            pyxel.blt(110, 108, self.LOGO, 32, 28, 32, 4, self.BACKGROUND)
            pyxel.blt(110, 145, self.LOGO, 32, 28, 32, 4, self.BACKGROUND)
        #show ruler
        pyxel.blt(20, 123, self.LOGO, 0, 40, 32, 16, self.BACKGROUND)
        if self.selected_sensor == SELECT.DISTANCE and pyxel.frame_count%60 >= 30:
            pyxel.blt(20, 108, self.LOGO, 32, 28, 32, 4, self.BACKGROUND)
            pyxel.blt(20, 145, self.LOGO, 32, 28, 32, 4, self.BACKGROUND)
        #show thermometer
        pyxel.blt(70, 113, self.LOGO, 8, 64, 16, 32, self.BACKGROUND)
        if self.selected_sensor == SELECT.TEMPERATURE and pyxel.frame_count%60 >= 30:
            pyxel.blt(66, 108, self.LOGO, 32, 28, 24, 4, self.BACKGROUND)
            pyxel.blt(66, 145, self.LOGO, 32, 28, 24, 4, self.BACKGROUND)
        #show hand
        pyxel.blt(160, 113, self.LOGO, 0, 96, 32, 32, self.BACKGROUND)
        if self.selected_sensor == SELECT.PRESSURE and pyxel.frame_count%60 >= 30:
            pyxel.blt(157, 108, self.LOGO, 32, 28, 32, 4, self.BACKGROUND)
            pyxel.blt(157, 145, self.LOGO, 32, 28, 32, 4, self.BACKGROUND)

    def draw_main(self):
        pyxel.cls(self.BACKGROUND)
        pyxel.rect(0, self.FIELD_Y, pyxel.width, pyxel.height - self.FIELD_Y, self.STAGE_GROUND)
        if self.player_state == STATE.NONE and self.is_on_ground:
            if pyxel.frame_count%60 < 15:
                self.DOT_16 = 0
            elif pyxel.frame_count%60 < 30:
                self.DOT_16 = 1
            elif pyxel.frame_count%60 < 45:
                self.DOT_16 = 2
            elif pyxel.frame_count%60 < 59:
                self.DOT_16 = 3
            pyxel.blt(self.player_x, self.player_y, self.TOFU, 16*self.DOT_16, self.BLOCK_NONE, self.player_size_x, self.player_size_y, self.player_colkey)

        elif self.player_state == STATE.WALKING:
            if pyxel.frame_count%60 < 15:
                self.DOT_16 = 0
            elif pyxel.frame_count%60 < 30:
                self.DOT_16 = 1
            elif pyxel.frame_count%60 < 45:
                self.DOT_16 = 2
            elif pyxel.frame_count%60 < 60:
                self.DOT_16 = 3
            pyxel.blt(self.player_x, self.player_y, self.TOFU, 16*self.DOT_16, self.BLOCK_NONE, self.player_size_x, self.player_size_y, self.player_colkey)

        elif self.player_state == STATE.FLYING:
            if pyxel.frame_count%60 < 20:
                self.DOT_16     =   1
            elif pyxel.frame_count%60 < 40:
                self.DOT_16     =   2
            elif pyxel.frame_count%60 < 60:
                self.DOT_16     =   3
            pyxel.blt(self.player_x, self.player_y, self.TOFU, 16*self.DOT_16, self.BLOCK_FLY, self.player_size_x, self.player_size_y, self.player_colkey)

        elif self.player_state == STATE.GLIDE:
            if not self.is_on_ground:
                if pyxel.frame_count%60 < 20:
                    self.DOT_16     =   0
                elif pyxel.frame_count%60 < 40:
                    self.DOT_16     =   1
                elif pyxel.frame_count%60 < 60:
                    self.DOT_16     =   2
            pyxel.blt(self.player_x, self.player_y, self.TOFU, 16*self.DOT_16, self.BLOCK_GLIDE, self.player_size_x, self.player_size_y, self.player_colkey)

        elif self.player_state == STATE.FALL:
            if pyxel.frame_count%60 < 15:
                self.DOT_16 = 3
            elif pyxel.frame_count%60 < 30:
                self.DOT_16 = 2
            elif pyxel.frame_count%60 < 45:
                self.DOT_16 = 1
            elif pyxel.frame_count%60 < 60:
                self.DOT_16 = 0
            pyxel.blt(self.player_x, self.player_y, self.TOFU, 16*self.DOT_16, 48, 16, 16, self.player_colkey)

    def draw_ending(self):
        pass

    def random_color(self, def_num, rand_index, back_col):
        def_num += rand_index
        if back_col == def_num:
            def_num += 1
            return def_num
        else:
            return def_num


    def block_generate(self, upper_limit, res_x, res_y, moss):
        pass

App()