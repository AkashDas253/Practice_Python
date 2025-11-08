import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict

class AutomataVisualizer:
    def visualize(self, automata_dict, automata_type='nfa', input_string=None, filename='automata', view=True):
        """
        Visualize and animate automata traversal.
        If input_string is provided, animates traversal and acceptance/rejection.
        automata_type: 'nfa' or 'dfa'
        """
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
        # If input_string is provided, animate traversal
        if input_string:
            if automata_type == 'dfa':
                self.animate_dfa(automata_dict, input_string, filename=filename+'_dfa', view=view)
            else:
                self.animate_nfa(automata_dict, input_string, filename=filename+'_nfa', view=view)
        else:
            # Static visualization (step-by-step highlight)
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
            pos = nx.spring_layout(G)

            # Animation: highlight states step by step
            states = list(G.nodes())
            fig, ax = plt.subplots(figsize=(8, 6))
            def update(frame):
                ax.clear()
                node_colors = ['yellow' if i == frame else ('lightgreen' if n in automata_dict.get("accept_states", []) else 'lightblue') for i, n in enumerate(states)]
                nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1200, font_size=10, arrows=True, ax=ax)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
                ax.set_title(f'Automata Visualization - Step {frame+1}/{len(states)}')
                ax.axis('off')
            anim = FuncAnimation(fig, update, frames=len(states), interval=1000, repeat=False)
            plt.tight_layout()
            anim.save(f'{filename}_animation.gif', writer='pillow')
            if view:
                plt.show()
            plt.close()
            print(f"NetworkX animation saved as {filename}_animation.gif")

    def animate_dfa(self, automata_dict, input_string, filename='dfa_anim', view=True):
        """
        Animate DFA traversal for a given input string.
        Highlights current state, transition, and shows acceptance/rejection.
        """
        import matplotlib as mpl
        mpl.rcParams['toolbar'] = 'None'
        fig, ax = plt.subplots(figsize=(12, 8))
        # Build graph and layout
        G = nx.DiGraph()
        edge_labels = defaultdict(list)
        transitions = automata_dict.get("transitions", {})
        for state in automata_dict.get("states", []):
            G.add_node(state)
        for state, trans in transitions.items():
            for symbol, target in trans.items():
                G.add_edge(state, target)
                edge_labels[(state, target)].append(symbol)
        edge_labels = {k: ','.join(v) for k, v in edge_labels.items()}
        pos = nx.spring_layout(G)
        current_state = automata_dict.get("start_state")
        states_traversed = [current_state]
        stopped_early = False
        for symbol in input_string:
            next_state = transitions.get(current_state, {}).get(symbol)
            if next_state is None:
                stopped_early = True
                break
            states_traversed.append(next_state)
            current_state = next_state
        accepted = current_state in automata_dict.get("accept_states", []) and not stopped_early and len(states_traversed) == len(input_string)+1
        frame_idx = [0]  # Mutable for navigation
        def update(frame):
            ax.clear()
            node_colors = ['yellow' if n == states_traversed[frame] else ('lightgreen' if n in automata_dict.get("accept_states", []) else 'lightblue') for n in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1200, font_size=10, arrows=True, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
            ax.annotate('', xy=pos[automata_dict.get("start_state")], xytext=(pos[automata_dict.get("start_state")][0]-0.15, pos[automata_dict.get("start_state")][1]),
                        arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=8))
            processed = input_string[:frame] if frame > 0 else ''
            remaining = input_string[frame:] if frame < len(input_string) else ''
            # Show input info and result together at the top, with simple status (no extra styling)
            if frame == len(states_traversed)-1:
                if stopped_early:
                    result_msg = "STOPPED"
                else:
                    result_msg = "ACCEPTED" if accepted else "REJECTED"
                input_info = f"DFA Traversal | Input: [{processed}]" + (f" [Next: {remaining[:1]}]" if remaining else '') + f" | State: {states_traversed[frame]} | {result_msg}"
                ax.text(0.5, 1.05, input_info, fontsize=14, ha='center', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
            else:
                ax.text(0.5, 1.05, f"DFA Traversal | Input: [{processed}]" + (f" [Next: {remaining[:1]}]" if remaining else '') + f" | State: {states_traversed[frame]}", fontsize=14, ha='center', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
            ax.axis('off')
            # Remove center and top-right result overlays; only show status in the top info box
            # (No code for center or top-right overlays remains)
            ax.text(0.01, 1.01, "←/→: Step Back/Forward", fontsize=10, ha='left', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))
            plt.draw()
        def on_key(event):
            print(f"Key pressed: {event.key}")  # Debug print
            if event.key == 'right' and frame_idx[0] < len(states_traversed)-1:
                frame_idx[0] += 1
                update(frame_idx[0])
            elif event.key == 'left' and frame_idx[0] > 0:
                frame_idx[0] -= 1
                update(frame_idx[0])
        fig.canvas.mpl_connect('key_press_event', on_key)
        update(0)
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.get_current_fig_manager().window.state('zoomed')
        if view:
            plt.show()
        plt.close()
        print(f"DFA animation shown and saved as {filename}_animation.gif")
        if accepted:
            print(f"Result: Input '{input_string}' is ACCEPTED by DFA.")
        else:
            print(f"Result: Input '{input_string}' is REJECTED by DFA.")

    def animate_nfa(self, automata_dict, input_string, filename='nfa_anim', view=True):
        """
        Animate NFA traversal for a given input string.
        Highlights all possible current states at each step.
        Shows acceptance/rejection at end.
        """
        import matplotlib as mpl
        mpl.rcParams['toolbar'] = 'None'
        fig, ax = plt.subplots(figsize=(12, 8))
        # Build graph and layout
        G = nx.DiGraph()
        edge_labels = defaultdict(list)
        transitions = automata_dict.get("transitions", {})
        for state in automata_dict.get("states", []):
            G.add_node(state)
        for state, trans in transitions.items():
            for symbol, targets in trans.items():
                if isinstance(targets, list):
                    for t in targets:
                        G.add_edge(state, t)
                        edge_labels[(state, t)].append(symbol)
                else:
                    G.add_edge(state, targets)
                    edge_labels[(state, targets)].append(symbol)
        edge_labels = {k: ','.join(v) for k, v in edge_labels.items()}
        pos = nx.spring_layout(G)
        # Helper: epsilon closure
        def epsilon_closure(states):
            closure = set(states)
            stack = list(states)
            while stack:
                state = stack.pop()
                for t in transitions.get(state, {}).get('ε', []):
                    if t not in closure:
                        closure.add(t)
                        stack.append(t)
            return closure
        current_states = epsilon_closure([automata_dict.get("start_state")])
        states_per_step = [set(current_states)]
        stopped_early = False
        for idx, symbol in enumerate(input_string):
            # Move on symbol: collect all possible next states from all current states
            next_states = set()
            for state in current_states:
                # If there are transitions for the symbol, add all targets
                for t in transitions.get(state, {}).get(symbol, []):
                    next_states.add(t)
            # Apply epsilon closure to the union of all next states
            current_states = epsilon_closure(next_states)
            # If there are no possible next states, stop early
            if not current_states:
                stopped_early = True
                break
            states_per_step.append(set(current_states))
        # Accept if any current state is an accept state and traversal was not stopped early
        accepted = any(s in automata_dict.get("accept_states", []) for s in current_states) and not stopped_early
        frame_idx = [0]
        def update(frame):
            ax.clear()
            node_colors = ['yellow' if n in states_per_step[frame] else ('lightgreen' if n in automata_dict.get("accept_states", []) else 'lightblue') for n in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1200, font_size=10, arrows=True, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
            ax.annotate('', xy=pos[automata_dict.get("start_state")], xytext=(pos[automata_dict.get("start_state")][0]-0.15, pos[automata_dict.get("start_state")][1]),
                        arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=8))
            processed = input_string[:frame] if frame > 0 else ''
            remaining = input_string[frame:] if frame < len(input_string) else ''
            # Show input info and result together at the top, with simple status (no extra styling)
            if frame == len(states_per_step)-1:
                if stopped_early:
                    result_msg = "STOPPED"
                else:
                    result_msg = "ACCEPTED" if accepted else "REJECTED"
                input_info = f"NFA Traversal | Input: [{processed}]" + (f" [Next: {remaining[:1]}]" if remaining else '') + f" | States: {sorted(states_per_step[frame])} | {result_msg}"
                ax.text(0.5, 1.05, input_info, fontsize=14, ha='center', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
            else:
                ax.text(0.5, 1.05, f"NFA Traversal | Input: [{processed}]" + (f" [Next: {remaining[:1]}]" if remaining else '') + f" | States: {sorted(states_per_step[frame])}", fontsize=14, ha='center', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
            ax.axis('off')
            ax.text(0.01, 1.01, "←/→: Step Back/Forward", fontsize=10, ha='left', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))
            plt.draw()
        def on_key(event):
            print(f"Key pressed: {event.key}")  # Debug print
            if event.key == 'right' and frame_idx[0] < len(states_per_step)-1:
                frame_idx[0] += 1
                update(frame_idx[0])
            elif event.key == 'left' and frame_idx[0] > 0:
                frame_idx[0] -= 1
                update(frame_idx[0])
        fig.canvas.mpl_connect('key_press_event', on_key)
        update(0)
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.get_current_fig_manager().window.state('zoomed')
        if view:
            plt.show()
        plt.close()
        print(f"NFA animation shown and saved as {filename}_animation.gif")
        if accepted:
            print(f"Result: Input '{input_string}' is ACCEPTED by NFA.")
        else:
            print(f"Result: Input '{input_string}' is REJECTED by NFA.")
