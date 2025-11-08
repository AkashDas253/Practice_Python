import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class AutomataVisualizer:
    def visualize(self, automata_dict, filename='automata', view=True):
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

        # Use DiGraph and merge labels for parallel edges
        G = nx.DiGraph()
        edge_labels = defaultdict(list)
        # Add states
        for state in automata_dict.get("states", []):
            G.add_node(state)
        # Add transitions and merge labels
        for state, trans in transitions.items():
            for symbol, targets in trans.items():
                if isinstance(targets, list):
                    for t in targets:
                        G.add_edge(state, t)
                        edge_labels[(state, t)].append(symbol)
                else:
                    G.add_edge(state, targets)
                    edge_labels[(state, targets)].append(symbol)
        # Merge multiple labels
        edge_labels = {k: ','.join(v) for k, v in edge_labels.items()}
        # Draw graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=[
            'lightgreen' if n in automata_dict.get("accept_states", []) else 'lightblue' for n in G.nodes()
        ], node_size=1200, font_size=10, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        # Highlight start state
        start = automata_dict.get("start_state")
        if start in G:
            nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='yellow', node_size=1400)
        plt.title('Automata Visualization')
        plt.tight_layout()
        plt.savefig(f'{filename}.png')
        if view:
            plt.show()
        plt.close()
        print(f"NetworkX visualization saved as {filename}.png")
