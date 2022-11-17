from ttt_state import State
from ttt_bot import Bot

def init_states():
    state_dict = {}
    state_dict[0] = set([State('         ')])
    for i in range(1,10):
        state_dict[i] = set()
        p = 'O' if (i % 2) == 0 else 'X'
        for st in state_dict[i-1]:
            if st.winner is None:
                for j in range(9):
                    if st.s[j] == ' ':
                        ns = st.s[:j]+p+st.s[j+1:]
                        nst = State(ns)
                        state_dict[i].add(nst)
                        st.children.add(nst)
    return state_dict[0].pop()

def get_user_action(st: State):
    c = ''
    while not (c.isdigit() and int(c) != 9):
        c = input(st)
    player = 'O' if (st.s.count(' ') % 2) == 0 else 'X'
    ns = st.s[0:int(c)] + player + st.s[int(c)+1:]
    for nst in st.children:
        if nst.s == ns:
            return nst
    print('cell is not empty')
    return get_user_action(st)
        




if __name__ == '__main__':
    start = init_states()
    ca = start
    b = Bot(start,0)
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
    b.save_state()
    print(ca.winner)
