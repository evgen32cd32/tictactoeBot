from collections import namedtuple

# '012345678'
#
# 0|1|2
# -+-+-
# 7|8|3
# -+-+-
# 6|5|4

#Transform = namedtuple('Transform',['corner','direction'])
class Transform:
    def __init__(self, corner, direction):
        assert corner in [0,2,4,6], 'Wrong corner'
        assert direction in [-1,1], 'Wrong direction'
        self.corner = corner
        self.direction = direction
    
    def reverse(self):
        if self.direction == 1:
            if self.corner == 2:
                self.corner = 6
            elif self.corner == 6:
                self.corner = 2
        return self
    
    def __add__(self, other):
        return Transform((self.corner + self.direction*other.corner + 8)%8, self.direction * other.direction)
    
    def __iadd__(self, other):
        self.corner = (self.corner + self.direction*other.corner + 8)%8
        self.direction *= other.direction
        return self

def charScore(ch):
    if ch == 'X':
        return 2
    if ch == 'O':
        return 1
    return 0

def calcStateScore(state: str):
    return sum([charScore(ch) * 3**(8-i) for i, ch in enumerate(state)])

def stateCanonForm(state: str):
    bestTransform = None
    corners = [charScore(x) for x in state[:7:2]]
    # (corner_id, clockwise)
    # (0, 1) - Canonical form already
    potential = [Transform(i*2,1) for i, x in enumerate(corners) if x == max(corners)]
    potential.extend([Transform(x.corner,-1) for x in potential])
    for i in range(1,8):
        scores = [charScore(state[(x.corner + x.direction * i)%8]) for x in potential]
        inds = [i for i, x in enumerate(scores) if x == max(scores)]
        potential = [potential[ind] for ind in inds]
        if len(inds) == 1:
            break
    bestTransform = potential[0]
    state8 = state[:-1]
    canonForm = state8[bestTransform.corner::bestTransform.direction] + state8[:bestTransform.corner:bestTransform.direction] + state[-1]
    return (calcStateScore(canonForm), canonForm, bestTransform.reverse())

def printableState(state: str):
    return state[0]+'|'+state[1]+'|'+state[2]+'\n-+-+-\n'+state[7]+'|'+state[8]+'|'+state[3]+'\n-+-+-\n'+state[6]+'|'+state[5]+'|'+state[4] + '\n'

class CanonState:
    def __init__(self, s:str, score: int):
        self.score = score
        self.s = s
        self.children = {}
        turn = 9 - self.s.count(' ')
        player = 'X' if (turn % 2) == 1 else 'O'
        if (       self.s[0:3] == player*3
                or self.s[2:5] == player*3
                or self.s[4:7] == player*3
                or self.s[0] + self.s[7] + self.s[6] == player*3
                or self.s[1] + self.s[8] + self.s[5] == player*3
                or self.s[7] + self.s[8] + self.s[3] == player*3
                or self.s[0] + self.s[8] + self.s[4] == player*3
                or self.s[6] + self.s[8] + self.s[2] == player*3):
            self.winner = player
        elif turn == 9:
            self.winner = 'D'
        else:
            self.winner = None
    
    def getTransformed(self, tr: Transform):
        state8 = self.s[:-1]
        return state8[tr.corner::tr.direction] + state8[:tr.corner:tr.direction] + self.s[-1]

    def __str__(self):
        return printableState(self.s)
