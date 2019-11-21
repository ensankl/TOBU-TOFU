import pyxel
import sensor
from time import sleep
from sensor import *

sensor = None

class App:
    '''

    '''
    def __init__(self):
        #initialize list for sceneChanger function.
        # WARNING : Set Same length for both lists.
        self.listOfSCX = [180, 120, 80, 60, 40, 20, 0]
        self.listOfSCY = [135, 90, 60, 45, 30, 15, 0]
        #initialize windowWidth, windowHeight
        #set value to 4:3 aspect ratio
        self.windowWidth = 200
        self.windowHeight = 150
        #make instance of Player(spawnX, spawnY)
        self.player = Player(35,35)
        #make instance of Stage(windowWidth, windowHeight)
        self.stage = Stage(800, 150)
        #initialize pyxel rendering WindowSize
        pyxel.init(200, 150, caption="TouchME", fps=60)
        #make instance of sensor


    def render(self, showMode = "none"):
        if showMode == "showTitle" or showMode == "showDead":
            pyxel.cls(7)
            if showMode == "shodeDead":
                pyxel.text(25, 20, "NEW GAME+", 8)
            #laoding title image is not working in this code
            # pyxel.image(0).load(0, 0, "source/Title.png")
            #intialize what kind of sensor is used to play
            pyxel.text(35, 60, "SELECT SENSORS WHAT YOU WANNA PLAY", 5)
            pyxel.text(50, 80, "D:Distance, T:Temperature,\n", 5)
            pyxel.text(62, 90, "L:Light, P:Pressure", 5)
            if pyxel.btn(pyxel.KEY_D):
                sensor = Sensor.generate(Sensors.DISTANCE, 7)
            elif pyxel.btn(pyxel.KEY_T):
                sensor = Sensor.generate(Sensors.TEMPERATURE, 7)
            elif pyxel.btn(pyxel.KEY_L):
                sensor = Sensor.generate(Sensors.LIGHT, 7)
            elif pyxel.btn(pyxel.KEY_P):
                sensor = Sensor.generate(Sensors.TOUCH, 7)

            pyxel.text(60, 120, "PRESS SPACE TO START", 0)
            if pyxel.btn(pyxel.KEY_SPACE):
                self.scene_changer()
                self.render("game")

        elif showMode == "game":
            pass


    def scene_changer(self):
         ##pyxel.clipで四角が狭くなり暗転してタイトルへ戻る
         thisX = pyxel.width
         thisY = pyxel.height
         w = self.listOfSCX[0]
         h = self.listOfSCY[0]
         for i in range(len(self.listOfSCX)):
            pyxel.clip(x1=thisX, y1=thisY, x2=w, y2=h)
            sleep(0.5)
            thisX = w
            thisY = h
            w = self.listOfSCX[i+1]
            h = self.listOfSCY[i+1]


    def updater(self):
        self.player.update_alive()
        self.player.update_judge_move()

        if not self.player.update_alive():
            self.scene_changer()
            self.render("showDead")


    def make_collision(self):
        pass
    #まず生成し、隣り合っているかを判定してから次にどんどん飛ばすfor文で実装する
    #ブロックの座標から１ブロックあたりの大きさは固定なので
    # ブロックを置いた位置の原点(block.originX, block.originY)から
    # (0, block.height), (block.width, 0), (block.width, (動くのはこっちだけ 中身は空洞で良い)block.height)
    #の座標を参照して当たり判定をつける マップタイルは固定なので1blockあたりの判定を定数倍して使用する

class Stage:
    def __init__(self, width, height):
        pyxel.tilemap(0).set(0, 0, ["abcd"])


class Player:
    '''
    Description of class plyaer
        -Methods-

            act:
                let player does something. it worked by move method.

            move:
                give int value that you want to move the player.

    '''
    def __init__(self, x=0, y=0):
        #initialize player's information
        self.posX = x
        self.posY = y
        self.tall = 25
        self.thickness = 10

        #initialize sensor's threshold
        self.noise = 0
        self.walk = 0
        self.fly = 0
        self.glide = 0


    def update_alive(self):
        if pyxel.height < self.posY:
            return 0
        else :
            return 1


    def update_is_on_ground(self):
        #if (self.posY + self.tall) = block.originY:
            return 1


    def update_judge_move(self):
        if self.update_is_on_ground():
            if self.noise < sensor.mapped_data() <= self.walk:
                self.act("doWalk")
            elif self.walk < sensor.mapped_data() <= self.fly:
                self.act("doFly")
                self.fly = sensor.mapped_data()
                while self.fly < sensor.mapped_data():
                    self.act("doFly")
                    self.fly = sensor.mapped_data()
                self.glide = self.fly * 0.8
                if self.glide < sensor.mapped_data():
                    self.act("doGlide")
                else :
                    self.act("doFall")
            else :
                self.act("none")
        else :
            self.act("doFall")


    def act(self, whatDoing):
        whatTimes = 3
        doTimes = [0] * whatTimes
        if whatDoing == "doWalk":
            for i in range(len(doTimes)):
                self.move(2, 0)
                #render(doWalk)
        elif whatDoing == "doFly":
            for i in range(len(doTimes)):
                self.move(2, 2)
                #render(doFly)
        elif whatDoing == "doGlide":
            for i in range(len(doTimes)):
                self.move(2, -1)
                #render(doGlide)
        elif whatDoing == "doFall":
            for i in range(len(doTimes)):
                self.move(0, 2)
                #render(doFall)
        elif whatDoing == "none":
            for i in range(len(doTimes)):
                pass
                #render(doNone)

    def move(self, dx, dy):
        self.posX += dx
        self.posY += dy