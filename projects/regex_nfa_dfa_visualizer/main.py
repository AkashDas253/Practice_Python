from core.nfa import NFA
from core.dfa import DFA
from core.visualizer import AutomataVisualizer

if __name__ == "__main__":
	
	pattern = input("Enter regex: ")
	visualizer = AutomataVisualizer()
	
	# Construct NFA from regex
	nfa = NFA(regex=pattern)
	print("NFA constructed.")
	nfa.print_definition()
	print("Visualizing NFA...")
	nfa_dict = nfa.to_dict()
	visualizer.visualize(nfa_dict)
	
	input("Press Enter to continue to DFA...")
	# Construct DFA from NFA
	dfa = DFA(nfa=nfa_dict)
	print("DFA constructed.")
	dfa.print_definition()
	print("Visualizing DFA...")
	visualizer.visualize(dfa.to_dict())

    