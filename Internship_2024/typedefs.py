class States():
    NONE = 0
    IDLE = 1
    GO_FORWARD = 2
    GO_BACKWARD = 3
    TURN_LEFT = 4
    TURN_RIGHT = 5
    SHOOT = 6
    TURN_ANGLE = 7

States_STR = ["NONE", "IDLE", "GO_FORWARD", "GO_BACKWARD", "TURN_LEFT", "TURN_RIGHT", "SHOOT", "TURN_ANGLE"]

class GuardStates():
    SEARCH = 0
    OBSTYCLE = 1
    SHOOTING = 2
    ATTACKING = 3

class TURN():
    RIGHT = 0
    LEFT = 1

class SoundFiles():
    NONE = 0
    CRYING = 1
    OBJECT = 2
    SEARCHING = 3
    HI = 4
    GAMEOVER = 5
