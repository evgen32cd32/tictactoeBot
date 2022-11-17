class State:
    def __init__(self, s:str, id: int):
        self.id = id
        self.s = s
        self.children = set()
        turn = 9 - self.s.count(' ')
        player = 'X' if (turn % 2) == 0 else 'O'
        if (       self.s[0:3] == player*3
                or self.s[3:6] == player*3
                or self.s[6:9] == player*3
                or self.s[0] + self.s[3] + self.s[6] == player*3
                or self.s[1] + self.s[4] + self.s[7] == player*3
                or self.s[2] + self.s[5] + self.s[8] == player*3
                or self.s[0] + self.s[4] + self.s[8] == player*3
                or self.s[2] + self.s[4] + self.s[6] == player*3):
            self.winner = player
            #print(self.s[0]+'|'+self.s[1]+'|'+self.s[2]+'\n-+-+-\n'+self.s[3]+'|'+self.s[4]+'|'+self.s[5]+'\n-+-+-\n'+self.s[6]+'|'+self.s[7]+'|'+self.s[8])
        elif self.s.count(' ') == 0:
            self.winner = 'D'
        else:
            self.winner = None
    
    def __str__(self):
        return self.s[0]+'|'+self.s[1]+'|'+self.s[2]+'\n-+-+-\n'+self.s[3]+'|'+self.s[4]+'|'+self.s[5]+'\n-+-+-\n'+self.s[6]+'|'+self.s[7]+'|'+self.s[8] + '\n'
