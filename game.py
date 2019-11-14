import pyxel

class App:
    '''

    '''
    def __init__(self):
        self.player = Player(35,35)
        pyxel.init(200, 150, caption="TouchME", fps=60)

    def updater(self):
        self.player.act()
        self.player.updateAlive()

        if not self.player.updateAlive():
            self.sceneChanger()

    def render(self):
        pass

    def isCollision(self):
        pass

    def sceneChanger(self):
         ##pyxel.clipで四角が狭くなり暗転してタイトルへ戻る
        pass


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
        self.posX = x
        self.posY = y

    def updateAlive(self):
        if pyxel.height < self.posY:
            return 0
        else :
            return 1

    def moveJudge(self):
        pass
    ##sensor.pyからconvertedValueをもらって値の大きさで挙動がWalk, Fly, Glideか決める

    def act(self):
        if None:
            pass

    def move(self, dx, dy):
        self.posX += dx
        self.posY += dy