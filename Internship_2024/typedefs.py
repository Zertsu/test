from enum import Enum

class States(Enum):
    NONE = 0
    IDLE = 1
    GO_FORWARD = 2
    GO_BACKWARD = 3
    TURN_LEFT = 4
    TURN_RIGHT = 5
    SHOOT = 6

