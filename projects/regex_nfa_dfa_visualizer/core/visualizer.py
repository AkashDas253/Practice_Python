class AutomataVisualizer:
	def visualize(self, automata_dict):
		print("\nStates:", automata_dict.get("states", []))
		print("Start State:", automata_dict.get("start_state"))
		print("Accept States:", automata_dict.get("accept_states", []))
		print("Transitions:")
		transitions = automata_dict.get("transitions", {})
		for state, trans in transitions.items():
			for symbol, targets in trans.items():
				if isinstance(targets, list):
					for t in targets:
						print(f"  {state} --{symbol}--> {t}")
				else:
					print(f"  {state} --{symbol}--> {targets}")
