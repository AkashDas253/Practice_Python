from core.nfa import NFA
from core.dfa import DFA
from core.visualizer import AutomataVisualizer

if __name__ == "__main__":
	
	pattern = input("Enter regex: ")
	input_str = input("Enter input string to test (leave blank for static visualization): ")
	visualizer = AutomataVisualizer()
	
	# Construct NFA from regex
	nfa = NFA(regex=pattern)
	print("NFA constructed.")
	nfa.print_definition()
	print("Visualizing NFA...")
	nfa_dict = nfa.to_dict()
	if input_str:
		nfa_traversal = nfa.traverse(input_str)  # returns dict with steps and accepted
		visualizer.visualize(nfa_dict, automata_type='nfa', input_string=input_str, traversal=nfa_traversal, filename='nfa', view=True)
	else:
		visualizer.visualize(nfa_dict, automata_type='nfa', input_string=None, filename='nfa', view=True)
	
	input("Press Enter to continue to DFA...")
	# Construct DFA from NFA
	dfa = DFA(nfa=nfa_dict)
	print("DFA constructed.")
	dfa.print_definition()
	print("Visualizing DFA...")
	dfa_dict = dfa.to_dict()
	if input_str:
		dfa_traversal = dfa.traverse(input_str)  # returns dict with steps and accepted
		visualizer.visualize(dfa_dict, automata_type='dfa', input_string=input_str, traversal=dfa_traversal, filename='dfa', view=True)
	else:
		visualizer.visualize(dfa_dict, automata_type='dfa', input_string=None, filename='dfa', view=True)

