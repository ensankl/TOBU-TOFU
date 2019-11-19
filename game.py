import pyxel
import sensor

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
        self.stage = Stage(200, 150)
        #initialize pyxel rendering WindowSize
        pyxel.init(200, 150, caption="TouchME", fps=60)

    def render(self):

        pass

    def scene_changer(self):
         ##pyxel.clipで四角が狭くなり暗転してタイトルへ戻る
         thisX = pyxel.width
         thisY = pyxel.height
         w = self.listOfSCX[0]
         h = self.listOfSCY[0]
         for i in range(len(self.listOfSCX)):
            pyxel.clip(x1=thisX, y1=thisY, x2=w, y2=h)
            thisX = w
            thisY = h
            w = self.listOfSCX[i+1]
            h = self.listOfSCY[i+1]

    def updater(self):
        self.player.update_alive()
        self.player.update_judge_move()

        if not self.player.update_alive():
            self.scene_changer()

    def make_collision(self):
        pass
    #ブロックの座標から１ブロックあたりの大きさは固定なので
    # ブロックを置いた位置の原点(block.originX, block.originY)から
    # (0, block.height), (block.width, 0), (block.width, (動くのはこっちだけ 中身は空洞で良い)block.height)
    #の座標を参照して当たり判定をつける マップタイルは固定なので1blockあたりの判定を定数倍して使用する

class Stage:
    def __init__(self, width, height):
        pass
        pyxel.tilemap(0).set(0, 0, ["abcd"])


class Player:
    '''
    Description of class plyaer
        -Methods-
            updateDeltas:
                judge sensing data. it returns True or False.


            isFlying:
                player's flying Flag. it returns True or False.


            isGliding:
                player's gliding Flag. it returns True or False.


            act:
                let player does something. it worked by move method.

            move:
                give int value that you want to move the player.


        -Parameters-
            isEnd:
                bring back to title because player is dying.
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

        #initialize stage collision

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
            if self.noise < sensor.convertedValue <= self.walk:
                self.act("doWalk")
            elif self.walk < sensor.convertedValue <= self.fly:
                self.act("doFly")
                if self.fly < sensor.convertedValue <= self.glide:
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
        elif whatDoing == "doFly":
            for i in range(len(doTimes)):
                self.move(2, 2)
        elif whatDoing == "doGlide":
            for i in range(len(doTimes)):
                self.move(2, -1)
        elif whatDoing == "doFall":
            for i in range(len(doTimes)):
                self.move(0, 2)


    def move(self, dx, dy):
        self.posX += dx
        self.posY += dy