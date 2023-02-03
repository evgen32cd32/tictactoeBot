# '012345678'
#
# 0|1|2
# -+-+-
# 7|8|3
# -+-+-
# 6|5|4

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
    potential = [(i*2,1) for i, x in enumerate(corners) if x == max(corners)]
    potential.extend([(x,-1) for x,_ in potential])
    for i in range(1,8):
        scores = [charScore(state[(x + a*i)%8]) for x,a in potential]
        inds = [i for i, x in enumerate(scores) if x == max(scores)]
        if len(inds) == 1:
            bestTransform = potential[inds[0]]
            break
        potential = [potential[ind] for ind in inds]
    if bestTransform is None:
        bestTransform = potential[0]
    state8 = state[:-1]
    canonForm = state8[bestTransform[0]::bestTransform[1]] + state8[:bestTransform[0]:bestTransform[1]] + state[-1]
    return (calcStateScore(canonForm), canonForm, bestTransform)

class State:
    def __init__(self, s:str, score: int):
        self.score = score
        self.s = s
        self.children = set()
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
            #print(self.s[0]+'|'+self.s[1]+'|'+self.s[2]+'\n-+-+-\n'+self.s[7]+'|'+self.s[8]+'|'+self.s[3]+'\n-+-+-\n'+self.s[6]+'|'+self.s[5]+'|'+self.s[4])
        elif turn == 9:
            self.winner = 'D'
        else:
            self.winner = None
    
    def __str__(self):
        return self.s[0]+'|'+self.s[1]+'|'+self.s[2]+'\n-+-+-\n'+self.s[7]+'|'+self.s[8]+'|'+self.s[3]+'\n-+-+-\n'+self.s[6]+'|'+self.s[5]+'|'+self.s[4] + '\n'
