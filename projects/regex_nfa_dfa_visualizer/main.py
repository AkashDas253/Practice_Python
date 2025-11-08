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
	visualizer.visualize(nfa_dict, automata_type='nfa', input_string=input_str if input_str else None, filename='nfa', view=True)
	
	input("Press Enter to continue to DFA...")
	# Construct DFA from NFA
	dfa = DFA(nfa=nfa_dict)
	print("DFA constructed.")
	dfa.print_definition()
	print("Visualizing DFA...")
	dfa_dict = dfa.to_dict()
	visualizer.visualize(dfa_dict, automata_type='dfa', input_string=input_str if input_str else None, filename='dfa', view=True)

