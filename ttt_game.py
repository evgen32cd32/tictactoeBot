from ttt_state import State
from ttt_bot import Bot

def init_states():
    state_dict = {}
    id = 0
    state_dict[0] = {'         ':State('         ',id)}
    for i in range(1,10):
        state_dict[i] = {}
        p = 'O' if (i % 2) == 0 else 'X'
        for s,st in state_dict[i-1].items():
            if st.winner is None:
                for j in range(9):
                    if s[j] == ' ':
                        ns = s[:j]+p+s[j+1:]
                        if ns in state_dict[i]:
                            st.children.add(state_dict[i][ns])
                        else:
                            id = id + 1
                            nst = State(ns, id)
                            state_dict[i][ns] = nst
                            st.children.add(nst)
    return state_dict[0]['         ']

def get_user_action(st: State):
    c = ''
    while (not c.isdigit()) or int(c) == 9:
        c = input(st)
    player = 'O' if (st.s.count(' ') % 2) == 0 else 'X'
    ns = st.s[0:int(c)] + player + st.s[int(c)+1:]
    for nst in st.children:
        if nst.s == ns:
            return nst
    print('cell is not empty')
    return get_user_action(st)

def _recursive_save(st: State, b: Bot, saved: set, f):
    if st.id not in saved:
        saved.add(st.id)
        f.write('{};{};{};{}\n'.format(st.id,st.s,b.d[st],[sc.id for sc in st.children]))
        for sc in st.children:
            _recursive_save(sc,b,saved,f)

def save_game(st: State, b: Bot, file = 'configs/svst.csv'):
    with open(file,'w') as f:
        saved = set()
        _recursive_save(st,b,saved,f)


def load_game(file = 'configs/svst.csv'):
    #assert()
    head = None
    b = None
    d = {}
    bot_d = {}
    with open(file,'r') as f:
        for line in f.readlines():
            split = line.split(';')
            id = int(split[0])
            st = State(split[1],id)
            ar = split[3]
            ar = ar[1:-2]
            ar = ar.split(',')
            if ar[0] == '':
                ar = []
            d[id] = (st,[int(x) for x in ar])
            bot_d[st] = float(split[2])
            if bot_d[st] != 0.5 and bot_d[st] != 1.0:
                print(line)
    head = d[0][0]
    b = Bot(head,bot_d)
    for _, (st, ch_ar) in d.items():
        for sc_id in ch_ar:
            st.children.add(d[sc_id][0])
    print("Loaded successfully")
    return (head, b)

if __name__ == '__main__':
    try:
        (start,b) = load_game()
    except Exception:
        print("Can't load. New initialization")
        start = init_states()
        b = Bot(start,expl_rate=0.5)
    ca = start
    plf = True
    while ca.winner is None:
        if plf:
            #ca = get_user_action(ca)
            ca = b.action(ca)
        else:
            ca = b.action(ca)
        print(ca)
        plf = not plf
    b.get_winner(ca.winner)
    save_game(start, b)
    print(ca.winner)
