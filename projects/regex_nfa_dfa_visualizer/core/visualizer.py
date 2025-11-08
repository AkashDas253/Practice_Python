import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict

class AutomataVisualizer:
    def visualize(self, automata_dict, automata_type='nfa', input_string=None, traversal=None, filename='automata', view=True):
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
        if input_string and traversal:
            self.animate(automata_dict, input_string, traversal, filename=filename, view=view)
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
                            print(f"Adding edge: {state} --{symbol}--> {t}")  # Debug print
                            G.add_edge(state, t)
                            edge_labels[(state, t)].append(symbol)
                    else:
                        print(f"Adding edge: {state} --{symbol}--> {targets}")  # Debug print
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
    
    def animate(self, automata_dict, input_string, traversal, filename='anim', view=True):
        import matplotlib as mpl
        mpl.rcParams['toolbar'] = 'None'
        fig, ax = plt.subplots(figsize=(12, 8))
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
        steps = traversal['steps']
        accepted = traversal['accepted']
        stopped_early = traversal['stopped_early']
        frame_idx = [0]
        is_dfa = all(isinstance(s, str) for s in steps[0]) if steps and isinstance(steps[0], set) else True
        def update(frame):
            ax.clear()
            # Debug print for NFA step states
            print(f"NFA step {frame}: {steps[frame]}")
            if is_dfa:
                node_colors = ['yellow' if n == steps[frame] else ('lightgreen' if n in automata_dict.get("accept_states", []) else 'lightblue') for n in G.nodes()]
            else:
                step_states = set(str(s) for s in steps[frame])
                # Always highlight at least one state yellow, even if empty
                if not step_states:
                    # If stopped early, highlight all nodes red
                    node_colors = ['red' for n in G.nodes()]
                else:
                    node_colors = ['yellow' if n in step_states else ('lightgreen' if n in automata_dict.get("accept_states", []) else 'lightblue') for n in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1200, font_size=10, arrows=True, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
            ax.annotate('', xy=pos[automata_dict.get("start_state")], xytext=(pos[automata_dict.get("start_state")][0]-0.15, pos[automata_dict.get("start_state")][1]),
                        arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=8))
            processed = input_string[:frame] if frame > 0 else ''
            remaining = input_string[frame:] if frame < len(input_string) else ''
            if frame == len(steps)-1:
                if stopped_early:
                    result_msg = "STOPPED"
                else:
                    result_msg = "ACCEPTED" if accepted else "REJECTED"
                if is_dfa:
                    input_info = f"DFA Traversal | Input: [{processed}]" + (f" [Next: {remaining[:1]}]" if remaining else '') + f" | State: {steps[frame]} | {result_msg}"
                else:
                    input_info = f"NFA Traversal | Input: [{processed}]" + (f" [Next: {remaining[:1]}]" if remaining else '') + f" | States: {sorted(step_states)} | {result_msg}"
                ax.text(0.5, 1.05, input_info, fontsize=14, ha='center', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
            else:
                if is_dfa:
                    ax.text(0.5, 1.05, f"DFA Traversal | Input: [{processed}]" + (f" [Next: {remaining[:1]}]" if remaining else '') + f" | State: {steps[frame]}", fontsize=14, ha='center', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
                else:
                    ax.text(0.5, 1.05, f"NFA Traversal | Input: [{processed}]" + (f" [Next: {remaining[:1]}]" if remaining else '') + f" | States: {sorted(step_states)}", fontsize=14, ha='center', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
            ax.axis('off')
            ax.text(0.01, 1.01, "←/→: Step Back/Forward", fontsize=10, ha='left', va='bottom', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))
            plt.draw()
        def on_key(event):
            if event.key == 'right' and frame_idx[0] < len(steps)-1:
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
        print(f"Animation shown and saved as {filename}_animation.gif")
        if accepted:
            print(f"Result: Input '{input_string}' is ACCEPTED.")
        else:
            print(f"Result: Input '{input_string}' is REJECTED.")
