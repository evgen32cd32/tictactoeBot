from ttt_state import State
import random

class Bot:
    def __init__(self, head: State, expl_rate = 0.5):
        self.d = {}
        self.prev = {}
        self.prev['X'] = None
        self.prev['O'] = None
        self.alfa = 0.1
        self.expl_rate = expl_rate

        self._init_weights(head)

    
    def _init_weights(self, st: State):
        for sc in st.children:
            if sc not in self.d:
                self.d[sc] = 0.5 if sc.winner is None or sc.winner == 'D' else 1.0
                self._init_weights(sc)
    
    def action(self, st:State):
        player = 'O' if (st.s.count(' ') % 2) == 0 else 'X'

        max_v = 0
        max_ac = None
        for sc in st.children:
            if max_v <= self.d[sc]:
                max_v = self.d[sc]
                max_ac = sc
        if self.expl_rate <= random.uniform(0,1):
            self.prev[player] = random.choice(list(st.children))
        else:
            if self.prev[player] is not None:
                self.d[self.prev[player]] = self.d[self.prev[player]] + self.alfa * (self.d[max_ac]-self.d[self.prev[player]])
            self.prev[player] = max_ac
        return self.prev[player]
    
    def get_winner(self, winner):
        if winner == 'X' and self.prev['O'] is not None:
            self.d[self.prev['O']] = (1 - self.alfa) * self.d[self.prev['O']]
        elif winner == 'O' and self.prev['X'] is not None:
            self.d[self.prev['X']] = (1 - self.alfa) * self.d[self.prev['X']]
        elif winner == 'D' and self.prev['O'] is not None:
            self.d[self.prev['O']] = (1 - self.alfa) * self.d[self.prev['O']] + 0.5*self.alfa
        self.prev['X'] = None
        self.prev['O'] = None

    def save_state(self, file = 'svst.pt'):
        with open(file,'w') as f:
            for k in self.d:
                f.write('{}:{}\n'.format(k.s,self.d[k]))
    
    def load_state(self, file = 'svst.pt'):
        try:
            with open(file,'r') as f:
                for line in f.readlines:
                    pass
        except FileNotFoundError:
            print('File {} not found'.format(file))

        
        

