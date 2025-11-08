class NFA:
	class State:
		def __init__(self):
			self.edges = {}      # symbol -> [State]
			self.epsilon = []    # list of States

	class Fragment:
		def __init__(self, start, accepts):
			self.start = start
			self.accepts = accepts

	def __init__(self, regex):
		self.states = set()
		self.transitions = dict()
		self.start_state = None
		self.accept_states = set()
		self._build_from_regex(regex)

	def _build_from_regex(self, regex):
		postfix = self._to_postfix(regex)
		frag = self._thompson(postfix)
		self.start_state = frag.start
		self.accept_states = set(frag.accepts)
		self.states = self._collect_states(frag.start)
		self.transitions = self._collect_transitions(self.states)

	def _to_postfix(self, pattern):
		precedence = {'*': 3, '.': 2, '|': 1}
		output = []
		stack = []
		pattern = self._add_concat(pattern)
		for c in pattern:
			if c.isalnum():
				output.append(c)
			elif c == '(': 
				stack.append(c)
			elif c == ')':
				while stack and stack[-1] != '(': output.append(stack.pop())
				stack.pop()
			else:
				while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(c, 0):
					output.append(stack.pop())
				stack.append(c)
		while stack: output.append(stack.pop())
		return ''.join(output)

	def _add_concat(self, pattern):
		result = ''
		for i, c in enumerate(pattern):
			result += c
			if i+1 < len(pattern):
				d = pattern[i+1]
				if (c.isalnum() or c == ')' or c == '*') and (d.isalnum() or d == '('):
					result += '.'
		return result

	def _thompson(self, postfix):
		stack = []
		for c in postfix:
			if c.isalnum():
				s1, s2 = self.State(), self.State()
				s1.edges[c] = [s2]
				stack.append(self.Fragment(s1, [s2]))
			elif c == '.':
				frag2 = stack.pop()
				frag1 = stack.pop()
				for a in frag1.accepts:
					a.epsilon.append(frag2.start)
				stack.append(self.Fragment(frag1.start, frag2.accepts))
			elif c == '|':
				frag2 = stack.pop()
				frag1 = stack.pop()
				s = self.State()
				s.epsilon.extend([frag1.start, frag2.start])
				accepts = frag1.accepts + frag2.accepts
				stack.append(self.Fragment(s, accepts))
			elif c == '*':
				frag = stack.pop()
				s = self.State()
				for a in frag.accepts:
					a.epsilon.append(frag.start)
				s.epsilon.append(frag.start)
				stack.append(self.Fragment(s, [s]))
		return stack.pop()

	def _collect_states(self, start):
		visited = set()
		stack = [start]
		while stack:
			state = stack.pop()
			if state not in visited:
				visited.add(state)
				for targets in state.edges.values():
					stack.extend(targets)
				stack.extend(state.epsilon)
		return visited

	def _collect_transitions(self, states):
		transitions = {}
		for s in states:
			transitions[s] = {'edges': s.edges, 'epsilon': s.epsilon}
		return transitions

	def to_dict(self):
		state_list = list(self.states)
		numbered = {s: f'S{i+1}' for i, s in enumerate(state_list)}
		transitions = {}
		for s in state_list:
			sid = numbered[s]
			transitions[sid] = {}
			for symbol, targets in self.transitions[s]['edges'].items():
				transitions[sid][symbol] = [numbered[t] for t in targets]
			if self.transitions[s]['epsilon']:
				transitions[sid]['ε'] = [numbered[t] for t in self.transitions[s]['epsilon']]
		return {
			"states": list(numbered.values()),
			"start_state": numbered[self.start_state],
			"accept_states": [numbered[s] for s in self.accept_states],
			"transitions": transitions
		}

	def print_definition(self):
		nfa_dict = self.to_dict()
		print(f"NFA Start State: {nfa_dict['start_state']}")
		print(f"NFA Accept States: {nfa_dict['accept_states']}")
		print("NFA Transition Table:")
		print(f"{'State':<6} | {'Input':<6} | {'Next State(s)':<15}")
		print("-"*40)
		for state, trans in nfa_dict['transitions'].items():
			for symbol, targets in trans.items():
				print(f"{state:<6} | {symbol:<6} | {targets}")
