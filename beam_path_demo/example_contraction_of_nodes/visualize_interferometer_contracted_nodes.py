
import h5py
import networkx as nx
from calculate_with_transfer_matrix_v4 import *


result = b'INFO: entry/instrument' # for faster purpose, replaced the output by a simple string


instr_path=result.splitlines()[0].split(b' ')[1]

NeXus_File_Name = "interferometer_v4.nxs"


f = h5py.File(NeXus_File_Name, "r")
instr=f[instr_path]



G = nx.DiGraph()




# Add nodes
prefix = '/entry/instrument'
#prefix = ''
n0 = prefix + '.'
n1 = prefix + '/source'
n2 = prefix + '/beamsplitter01'
n3 = prefix + '/mirror01'
n4 = prefix + '/mirror02'
n5 = prefix + '/beamsplitter02'
n6 = prefix + '/detector01'
n7 = prefix + '/detector02'

# create the list of nodes. Names are hardcoded above
node_list = [n1,n2,n3,n4,n5,n6,n7]



# from the list of nodes, create all the edges, for the directed graph
edges_list = get_list_of_all_edges(node_list, instr)



# Add edges
for i in edges_list:
    x_pos_edge, y_pos_edge = get_edge_position_from_node_touple(i, instr)
    G.add_edge(i[0],i[1], edge_pos=(x_pos_edge, y_pos_edge))


#create a list, which will be filled with the position of the nodes, from the NXtransformation attributes
node_positions_list=[]

for i in range(len(node_list)):
    pos_vec = get_pos_vector_from_opt_element(node_list[i], instr)
    pos_touple = get_pos_touple_from_pos_vector(pos_vec)
    node_positions_list.append(pos_touple)

# Adding the nodes to the graph
for i in range(len(node_list)):
      G.add_node(node_list[i])  

add_position_and_names_to_graph_nodes(G, instr)

# Assign positions to nodes using a loop
node_positions = {}
for i, pos in enumerate(node_positions_list):
    node_positions[node_list[i]] = pos

# extract the end and start points of a directed graph.
roots = (v for v, d in G.in_degree() if d == 0)
leaves = [v for v, d in G.out_degree() if d == 0]
all_paths = []





target_path_opt_beams = '/entry/instrument/'

groups_at_path, datasets_at_path_at_opt_beams = get_groups_and_datasets_from_nexus_file(NeXus_File_Name, target_path_opt_beams)
opt_beams_at_path = filter_group_for_NeXus_class(groups_at_path, NeXus_File_Name,'/entry/instrument/', 'NXopt_beam')

# Get all edges as a list
all_edges = list(G.edges())


if len(opt_beams_at_path) < len(all_edges):
    # create beams with arbitrary name, so that all edges can be popilated to nexus beams.
    print("Hey, you have to create the beams, which are missing!")



add_beam_names_to_edges(G, all_edges, opt_beams_at_path, NeXus_File_Name, instr)



# Visualize the original graph
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
#nx.draw(G, with_labels=True, font_weight='bold')
nx.draw(G, pos=node_positions,  with_labels=False, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)

# Draw labels with slight tilt
labels = nx.draw_networkx_labels(G, pos=node_positions, font_size=8, font_color='black', font_family='sans-serif')
for _, t in labels.items():
    t.set_rotation(10)  # Set rotation angle to 10 degrees


plt.margins(x=0.2, y=0.2)






def get_node_names():
    return 1


def remove_self_directed_graphs():
    return 2

def change_names_according_to_groupt(): #/ or extract graph copy with element names as group names, if they have group names.
    return 3




# Assign positions to nodes using a loop
node_positions = {}
for i, pos in enumerate(node_positions_list):
    node_positions[node_list[i]] = pos

contracting_nodes_list = [n2,n3,n4,n5]

H = G
Average_position_list = []
New_name = 'Group: Beamsplitters and Mirrors'
for counter, item in enumerate(contracting_nodes_list):
    Average_position_list.append(H.nodes[item]['position'])
    H = nx.contracted_nodes(H, contracting_nodes_list[0], item)
    H.nodes[n2]['name'] = New_name

    # Relabel the contracted node
    mapping = {contracting_nodes_list[0]: New_name}
    H = nx.relabel_nodes(H, mapping)

print("################")
print(Average_position_list)

# calculate the sum of the touple elements

def get_contracted_node_pos(pos_list):
    contracted_pos = [sum(x)/len(pos_list) for x in zip(*pos_list)]
    return (contracted_pos[0],contracted_pos[1])

#contracted_pos = [sum(x)/len(Average_position_list) for x in zip(*Average_position_list)]
contracted_pos = get_contracted_node_pos(Average_position_list)
print(contracted_pos)
H.nodes[New_name]['position'] = contracted_pos
print(contracted_pos)
print("###")
print(H.nodes(data=True))
print("_____________")
print(H.nodes[New_name])
print("\n ")
#print(H.nodes[New_name]['contraction'])
#print(H.nodes[New_name]['contraction'])

# Remove self-loop if exists
if H.has_edge(New_name, New_name):
    H.remove_edge(New_name, New_name)


plt.subplot(1, 2, 2)
#nx.draw(H, with_labels=True, font_weight='bold')
node_positions = {node: data['position'] for node, data in H.nodes(data=True)}
node_labels = {node: data['name'] for node, data in H.nodes(data=True)}
nx.draw(H, pos=node_positions,  with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)


# Adjust margins if needed
plt.margins(x=0.2, y=0.2)

plt.show()


