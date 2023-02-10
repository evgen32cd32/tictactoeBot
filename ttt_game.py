from ttt_state import CanonState, stateCanonForm, printableState, Transform
from ttt_bot import Bot

class TTTGame:
    def __init__(self, file = 'configs/svst_v2.csv'):
        self.bot_config = file
        state_dict = {}
        state_dict[0] = {0:CanonState('         ',0)}
        for i in range(1,10):
            state_dict[i] = {}
            p = 'O' if (i % 2) == 0 else 'X'
            for st in state_dict[i-1].values():
                if st.winner is None:
                    for j in range(9):
                        if st.s[j] == ' ':
                            ns = st.s[:j]+p+st.s[j+1:]
                            score, cForm, transform = stateCanonForm(ns)
                            if score not in state_dict[i]:
                                nst = CanonState(cForm, score)
                                state_dict[i][score] = nst
                            else:
                                nst = state_dict[i][score]
                            if nst not in st.children:
                                st.children[nst] = []
                            st.children[nst].append(transform)
        self.state_dict = {k:v for d in state_dict.values() for k,v in d.items()}
        self.bot = None
        # Load
        try:
            with open(file,'r') as f:
                self.bot =  Bot(self.state_dict, {int(line.split(';')[0]):float(line.split(';')[1]) for line in f.readlines()})
            print("Loaded successfully")
        except Exception:
            print("Can't load. New initialization")
            self.bot = Bot(self.state_dict)

    def saveGame(self):
        with open(self.bot_config,'w') as f:
            [f.write(f'{k};{self.bot.d[v]}\n') for k,v in self.state_dict.items()]
    
    def startState(self):
        return self.state_dict[0]

    def checkCorrectMove(self, st: str, prev: CanonState):
        score, _, transform = stateCanonForm(st)
        if self.state_dict[score] not in prev.children:
            return None, None
        return self.state_dict[score], transform

    def toSpiral(state: str):
        return state[:3] + state[5] + state[8:5:-1] + state[3:5]

    def fromSpiral(state: str):
        return state[:3] + state[7:] + state[3] + state[6:3:-1]

if __name__ == '__main__':
    game = TTTGame()
    ca = game.startState()
    b = game.bot
    plf = 'X'
    trans = Transform(0,1)
    prev = {'X':None, 'O':None}
    while ca.winner is None:
        ca, tr = b.action(ca,prev[plf])
        prev[plf] = ca
        trans += tr
        print(printableState(ca.getTransformed(trans)))
        plf = 'X' if plf == 'O' else 'O'
    b.get_winner(ca.winner, prev)
    game.saveGame()
    print(ca.winner)
