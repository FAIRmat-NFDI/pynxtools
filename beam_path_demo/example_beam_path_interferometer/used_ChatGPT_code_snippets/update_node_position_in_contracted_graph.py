import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
G.add_edges_from([(1, 2), (1, 3), (2, 3)])

# Perform contraction
G_contracted = nx.contracted_nodes(G, 1, 2)

# Relabel the contracted node
mapping = {1: 'Contraction (1, 2)'}
G_contracted = nx.relabel_nodes(G_contracted, mapping)

# Remove self-loop if exists
if G_contracted.has_edge('Contraction (1, 2)', 'Contraction (1, 2)'):
    G_contracted.remove_edge('Contraction (1, 2)', 'Contraction (1, 2)')

# Specify initial node positions
initial_node_positions = {'Contraction (1, 2)': (0, 0), 3: (1, 1)}

# Draw the graph with initial positions
nx.draw(G_contracted, pos=initial_node_positions, with_labels=True, node_size=500, node_color='skyblue')
plt.show()

# Update node position
updated_node_positions = initial_node_positions.copy()
updated_node_positions['Contraction (1, 2)'] = (0.5, 0.5)  # Update position of the contracted node

# Clear previous plot
plt.clf()

# Redraw the graph with updated positions
nx.draw(G_contracted, pos=updated_node_positions, with_labels=True, node_size=500, node_color='skyblue')
plt.show()