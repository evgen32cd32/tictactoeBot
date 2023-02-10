from ttt_state import CanonState, stateCanonForm, printableState, Transform
from ttt_bot import Bot

def init_states():
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
    return {k:v for d in state_dict.values() for k,v in d.items()}

def save_game(state_dict: dict, b: Bot, file = 'configs/svst_v2.csv'):
    with open(file,'w') as f:
        [f.write(f'{k};{b.d[v]}\n') for k,v in state_dict.items()]

def load_game(state_dict: dict, file: str = 'configs/svst_v2.csv'):
    with open(file,'r') as f:
        return Bot(state_dict, {int(line.split(';')[0]):float(line.split(';')[1]) for line in f.readlines()})

if __name__ == '__main__':
    state_dict = init_states()
    try:
        b = load_game(state_dict)
        print("Loaded successfully")
    except Exception:
        print("Can't load. New initialization")
        b = Bot(state_dict)
    ca = state_dict[0]
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
    save_game(state_dict, b)
    print(ca.winner)
