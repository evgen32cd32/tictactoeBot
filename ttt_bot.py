from ttt_state import CanonState
import random

class Bot:
    def __init__(self, states: dict, d: dict = None):
        self.alfa = 0.1
        if d is None:
            self.d = {st:0.5 if st.winner is None or st.winner == 'D' else 1.0 for st in states.values()}
        else:
            self.d = {states[k]:v for k,v in d.items()}
    
    def action(self, st: CanonState, prev_state: CanonState = None, expl_rate: float = 0.5):
        player = 'O' if (st.s.count(' ') % 2) == 0 else 'X'
        # exploration
        if expl_rate < random.uniform(0,1):
            nst = random.choice(list(st.children))
            return nst, random.choice(st.children[nst])
        max_v = max([self.d[sc] for sc in st.children])
        max_ac = [sc for sc in st.children if self.d[sc] == max_v][0]
        if prev_state is not None:
            self.d[prev_state] += self.alfa * (self.d[max_ac] - self.d[prev_state])
        return max_ac, random.choice(st.children[max_ac])
    
    def get_winner(self, winner: str, prev_states: dict):
        if winner == 'X' and prev_states['O'] is not None:
            self.d[prev_states['O']] *= (1 - self.alfa)
        if winner == 'O' and prev_states['X'] is not None:
            self.d[prev_states['X']] *= (1 - self.alfa)
        if winner == 'D' and prev_states['O'] is not None:
            self.d[prev_states['O']] = (1 - self.alfa) * self.d[prev_states['O']] + 0.5*self.alfa
    
    # Only draw and lost
    def get_defeat(self, winner: str, prev: CanonState):
        if winner == 'D':
            self.d[prev] = (1 - self.alfa) * self.d[prev] + 0.5*self.alfa
        else:
            self.d[prev] *= (1 - self.alfa)

        
        

