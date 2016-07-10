import string

alphabet = [letter for letter in string.ascii_letters] + [' ']

count = 0

def get_next_state_tag():
    global count
    count = count + 1
    return count

def get_final_states(states):
    return [state for state in states if state.isfinal is True]


def get_start_state(states):
    for state in states:
        if state.isstart is True:
            return state


def concat(nfa1, nfa2):
    states = []
    nfa1.states[nfa1.get_final_state_index()].tag = nfa2.states[nfa2.get_start_state_index()].tag
    nfa1.states[nfa1.get_final_state_index()] = nfa2.states[nfa2.get_start_state_index()]
    del nfa2.states[nfa2.get_start_state_index()]
    nfa1.states[nfa1.get_final_state_index()].isstart = False
    states.extend(nfa1.states)
    states.extend(nfa2.states)
    new_nfa = NFA(states)
    return new_nfa


def slash(nfa1, nfa2):
    states = []
    s_beg = State(get_next_state_tag(), isstart=True)
    s_end = State(get_next_state_tag(), isfinal=True)

    t1 = Transition(nfa1.states[nfa1.get_start_state_index()], 'e')
    t2 = Transition(nfa2.states[nfa2.get_start_state_index()], 'e')
    t3 = Transition(s_end, 'e')
    t4 = Transition(s_end, 'e')

    s_beg.add_transition_to(t1)
    s_beg.add_transition_to(t2)
    nfa1.states[nfa1.get_final_state_index()].add_transition_to(t3)
    nfa2.states[nfa2.get_final_state_index()].add_transition_to(t4)

    nfa1.states[nfa1.get_start_state_index()].isstart = False
    nfa2.states[nfa2.get_start_state_index()].isstart = False

    nfa1.states[nfa1.get_final_state_index()].isfinal = False
    nfa2.states[nfa2.get_final_state_index()].isfinal = False

    states.extend(nfa1.states)
    states.extend(nfa2.states)
    states.extend([s_beg])
    states.extend([s_end])

    new_nfa = NFA(states)
    return new_nfa


def star(nfa):
    states = []
    s_beg = State(get_next_state_tag(), isstart=True)
    s_end = State(get_next_state_tag(), isfinal=True)

    t1 = Transition(nfa.states[nfa.get_start_state_index()], 'e')
    t2 = Transition(s_end, 'e')

    s_beg.add_transition_to(t1)
    nfa.states[nfa.get_final_state_index()].add_transition_to(t2)

    t3 = Transition(nfa.states[nfa.get_start_state_index()], 'e')
    nfa.states[nfa.get_final_state_index()].add_transition_to(t3)

    t4 = Transition(s_end, 'e')
    s_beg.add_transition_to(t4)

    nfa.states[nfa.get_start_state_index()].isstart = False
    nfa.states[nfa.get_final_state_index()].isfinal = False

    states.extend(nfa.states)
    states.extend([s_beg])
    states.extend([s_end])

    new_nfa = NFA(states)
    return new_nfa




class NFA:
    def __init__(self, states):
        self.set_states(states)

    def set_states(self, states):
        self.states = states
        self.alphabets = []
        self.transitions = []
        self.start_state = get_start_state(states)
        self.final_states = get_final_states(states)
        self.count = 0
        for state in states:
            [self.transitions.append(str(state) + "----"+str(trans.alphabets)+"---->"+str(trans.state_to)) for trans in state.transitions]
            for trans in state.transitions:
                if not self.alphabets.__contains__(trans.alphabets):
                    self.alphabets.append(trans.alphabets)



    def get_start_state_index(self):
        for i in range(len(self.states)):
            if self.states[i].isstart is True:
                return i
        return -1


    def get_final_state_index(self):
        for i in range(len(self.states)):
            if self.states[i].isfinal is True:
                return i
        return -1


    def __str__(self):
        list = [trans for trans in self.transitions]
        t = "\n" +"\n".join(list)
        return "\nStates = " + str([state for state in self.states]) + \
               "\nAlphabets = " + str([alph for alph in self.alphabets]) + \
               "\nTransitions = " + str(t) + \
               "\nStart State = " + str(self.start_state) + \
               "\nFinal States = " + str([fin for fin in self.final_states])



class Transition:
    def __init__(self, state_to, alphabets):
        self.alphabets = alphabets
        self.state_to = state_to

    def __str__(self):
        return str(self.alphabets) + " to " + str(self.state_to)

    def __repr__(self):
        return str(self.alphabets) + " to " + str(self.state_to)


class State:
    def __init__(self, tag, isstart=False, isfinal=False):
        self.tag = tag
        self.isstart = isstart
        self.isfinal = isfinal
        self.transitions = set()

    def add_transition_to(self, transition):
        self.transitions.add(transition)

    def __str__(self):
        return str(self.tag)

    def __repr__(self):
        return str(self.tag)


