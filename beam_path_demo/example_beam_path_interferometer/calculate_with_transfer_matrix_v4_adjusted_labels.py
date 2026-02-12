#import os
import subprocess
import h5py
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt

#import matplotlib
#matplotlib.use('TkAgg',force=True)
#from matplotlib import pyplot as plt
#print("Switched to:",matplotlib.get_backend())

#os.system('read_nexus --help')
#A=os.system('read_nexus -f "C:/Daten/_Project 4 FAIRmat/NXBeam_path/NXopt_element/interferometer.nxs" ')

def _get_value(hdf_node):
  '''
  Get value from hdl5 node
  '''
  hdf_value = hdf_node[...]
  if str(hdf_value.dtype) == 'bool':
    return bool(hdf_value)
  if hdf_value.dtype.kind in 'iufc':
    return hdf_value
  if len(hdf_value.shape) > 0:
    return hdf_value.astype(str)
  return hdf_node[()].decode()


def get_prev_element(x, instrument, str_replacement = "/entry/instrument/"):
  '''
  Get the path of the previous element with the configuration,
  that for the path >str_replacement< is removed beforehand due to redundancy
  '''

  shorten_path = x.replace(str_replacement,"")

  prev_element_output = _get_value(instrument[shorten_path + '/previous_opt_element'])


  if type(prev_element_output) == str:
    if prev_element_output != ".":
      return prev_element_output
  if type(prev_element_output) == np.ndarray:
    if len(prev_element_output) >= 2:
      prev_element_list_without_dot = []
      for i in range(len(prev_element_output)):
        if prev_element_output[i] != ".":
          prev_element_list_without_dot.append(prev_element_output[i])
      if len(prev_element_list_without_dot) >= 1:
        return np.array(prev_element_list_without_dot)
      else:
        return None
  else:
    print("The previous element is eiher \".\" or incorrect formatted. get_prev_element function aborted.")
    return None


def get_the_edges_from_opt_elem(opt_elem, instrument):
  '''
  Uses specific optical elements from a nexus file and return tuples,
  which are connected via the "previous optical elements" field.
  In this way, edges can be created (connection of nodes). See graph
  theory for more details.
  '''
  prev_elements = get_prev_element(opt_elem, instrument)

  if type(prev_elements) == str:
    if prev_elements == None:
      return None
    else:
      return [(opt_elem, prev_elements)]
  if type(prev_elements) == np.ndarray:
    touple_list = []
    if len(prev_elements) >= 2:
      for i in range(len(prev_elements)):
        if str(prev_elements[i]) != ".":
          touple_list.append((opt_elem,str(prev_elements[i])))
      return touple_list

def get_list_of_all_edges(node_list, instrument):
  edges_list_all = []
  for i in range(len(node_list)):
    #extract the lists, which have one or more tuple elements in it
    edges_list = get_the_edges_from_opt_elem(node_list[i], instrument)
    
    # add all individual touple elements from the list, so that no lists with touples are inside the lists. 
    # LIST[Touple, Touple, Toupe]
    # and not
    # LIST[Touple, Touple, LIST[Touple, Touple], Touple]
    if edges_list != None:
      for k in range(len(edges_list)):
        edges_list_all.append(edges_list[k])
  return edges_list_all



#instr[
def read_opt_elemenet_and_beams(instr_name, path_TMT, instrument):
  '''
  input is a instrument name from a nexus file.
  It ten searches for the transfermatricies, which are connected to the next beams. Returned is the transfer matrix with 
  as well as the beam before the transfermatrix application and the beam after the transfermatrix application
  '''
  sucessful_matrix_list = []
  previous_and_next_beam_list = []
  for m in range(1,8):
    for k in range(1,8):
      total_path = path_TMT + instr_name + "/matrix_" + "beam0" + str(m) + "_beam0" + str(k)
      path_short = total_path.replace('/entry/instrument/','')
      try:
        sucessful_matrix = _get_value(instrument[path_short])
        sucessful_matrix_list.append(sucessful_matrix)
        previous_and_next_beam_list.append(["beam0" + str(m),"beam0" + str(k)])
      except KeyError:
        continue
  return sucessful_matrix_list, previous_and_next_beam_list

def print_all_edges(edges_list):
  '''
  Function to print all edges from an edge list
  '''
  print("##################")
  print("These are all the edges")
  for i in range(len(edges_list)):
    print(edges_list[i])
  print("\n")

def get_pos_vector_from_opt_element(x, instrument, str_replacement = "/entry/instrument/"):
  '''
  Get the path of the previous element with the configuration,
  that for the path >str_replacement< is removed beforehand due to redundancy
  '''
  shorten_path = x.replace(str_replacement,"")
  length = _get_value(instrument[shorten_path + '/geometric_position/axis_position_coordinates'])
  vector = instrument[shorten_path + '/geometric_position/axis_position_coordinates'].attrs['vector']
  vector_norm = np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
  if vector_norm != 0:
    return vector/vector_norm * length
  else:
    return vector * 0

def get_pos_touple_from_pos_vector(pos_vector):
  return (pos_vector[0],pos_vector[1])


def add_note_with_pos(Graph, node, instrument):
  # not needed?
  pos_vec = get_pos_vector_from_opt_element(node, instrument)
  pos_tuple = get_pos_touple_from_pos_vector(pos_vec)
  Graph.add_node(node,pos=pos_tuple)



def check_path_type(nexus_file, target_path):
  with nexus_file as file:
    # Get the item at the specified path
    item = file.get(target_path)

    if item is not None:
      if isinstance(item, h5py.Group):
        #print(f"The path '{target_path}' corresponds to a group.")
        return h5py.Group
      elif isinstance(item, h5py.Dataset):

        #print(f"The path '{target_path}' corresponds to a dataset.")
        return h5py.Dataset
      else:
        #print(f"The path '{target_path}' corresponds to an unknown HDF5 item.")
        return None
    else:
      None
      #print(f"The path '{target_path}' does not exist in the HDF5 file.")


def filter_group_for_NeXus_class(list, file_name, path, class_filter):
  #result = b'INFO: entry/instrument' # for faster purpose, replaced the output by a simple string
  #instr_path=result.splitlines()[0].split(b' ')[1]
  output_list = []
  nexus_file = h5py.File(file_name, "r")
  #instr=nexus_file[instr_path]
  #search_path = path.replace('/entry/instrument/','')
  for i in list:
    class_attribute = nexus_file[path+i].attrs['NX_class']
    if class_attribute == class_filter:
      output_list.append(i)
  return output_list



def get_groups_and_datasets_from_nexus_file(FileName, target_path):

  with h5py.File(FileName, 'r') as file:   
    # check if the element (target path) in the file is a group at all, so that it can return .keys()
    if h5py.Group == check_path_type(h5py.File(FileName, 'r'), target_path):

      # Check if the specified path exists in the HDF5 file
      if target_path in file:
        all_elements = list(file[target_path].keys())
        group_list = []
        data_list = []
        for k in all_elements:
          if check_path_type(h5py.File(FileName, 'r'), target_path  + '/' + k) == h5py.Group:
            group_list.append(k)
          if check_path_type(h5py.File(FileName, 'r'), target_path  + '/' + k) == h5py.Dataset:
            data_list.append(k)
        #print(all_elements, "<------------")
        #print(group_list)
        #print(data_list)
        #print(group_list, data_list)
        return group_list, data_list
      else:
        None
        print(f"Path {target_path} does not exist in the HDF5 file.")
    else:
      None
      print("The element of interest is no group and hence has no item in it to list.")











def check_if_graph_edge_has_attribute(graph_edge, attribute_string):
  try:
    #try to excetue this, if not possible, return keyerror with False
    graph_edge[attribute_string]
    return True
  except KeyError:
    return False


def add_beam_to_nexus_file(nexus_file, beam_name):
  nexus_file['/entry/instrument'].create_group(beam_name)
  nexus_file['/entry/instrument/' + beam_name].attrs['NX_class'] = 'NXopt_beam'


List_of_beam_names_to_be_created_later = []





def add_beam_names_to_edges(Graph, all_edges, opt_beams_at_path, NeXus_File_Name, instrument):
  #print(groups_at_path)
  #opt_elements_at_path = filter_group_for_NeXus_class(groups_at_path, NeXus_File_Name,'/entry/instrument/', 'NXopt_element')
  #äopt_beams_at_path = filter_group_for_NeXus_class(groups_at_path, NeXus_File_Name,'/entry/instrument/', 'NXopt_beam')




  if len(opt_beams_at_path) < len(all_edges):
    for i in range(len(all_edges) - len(opt_beams_at_path)):
      print("Beam automatically created:", "NXS_Beam_"+str(i))
      opt_beams_at_path.append("NXS_Beam_"+str(i))
      List_of_beam_names_to_be_created_later.append("NXS_Beam_"+str(i))


  # get if there are beams with specific links to opt elements - i.e. user defined beam names
  all_groups, all_datasets=get_groups_and_datasets_from_nexus_file(NeXus_File_Name, '/entry/instrument/') # with attribute: f['/entry/instrument/beam01'].attrs['NX_class'] = 'NXopt_beam'

  all_beams = filter_group_for_NeXus_class(all_groups, NeXus_File_Name, '/entry/instrument/', 'NXopt_beam')



  for k in range(len(all_beams)):
    groups_in_specific_beam, fields_in_specific_beam = get_groups_and_datasets_from_nexus_file(NeXus_File_Name, '/entry/instrument/' + all_beams[k])

    # only iterate through groups of the hdf5 file - dont include datasets
    if fields_in_specific_beam != None:
      # if there are elements in this group, check if there are a previous and next element given.
      if len(fields_in_specific_beam) >= 1:
        for i in fields_in_specific_beam:
          if i == 'next_opt_element':
            search_string = '/entry/instrument/' + all_beams[k] + "/" + i
            next_beam_element = _get_value(instrument[search_string.replace('/entry/instrument/','')])
          if i == 'prev_opt_element':
            search_string = '/entry/instrument/' + all_beams[k] + "/" + i
            prev_beam_element = _get_value(instrument[search_string.replace('/entry/instrument/','')])

        for m in all_edges:
          #print(m)
          #reverse order, as result from prev element list, so that next and prev element as given as beam field are in "human logic" order
          m_reversed = m[::-1] 
          if m_reversed[0] == prev_beam_element and m_reversed[1] == next_beam_element:
            #print(prev_beam_element,next_beam_element, m_reversed)
            #print(all_beams[k])
            Graph[m[0]][m[1]]['beam_name'] = all_beams[k]
            # remove the beam name which was linked to the graph edge, from the list of elements, which need to be assigned
            opt_beams_at_path.remove(all_beams[k])
            pop_index = all_edges.index(m)
            all_edges.pop(pop_index)
            print("------------------> I have popped an element",m)



  if len(opt_beams_at_path) == len(all_edges):
    for i in range(len(opt_beams_at_path)):
      # assign only the a name from the remaining list, if it the graph node does not have a beam_name attibute
      if not check_if_graph_edge_has_attribute(Graph[all_edges[i][0]][all_edges[i][1]], 'beam_name'): # is this true function unnessecary?
                                                                                                      #because all these beams were already removed, which do not havea beam name?
        # Set properties for the first edge
        #G[all_edges[i][0]][all_edges[i][1]]['weight'] = 3.0
        Graph[all_edges[i][0]][all_edges[i][1]]['beam_name'] = opt_beams_at_path[i]
  else:
    print("The number of edges and beam names is incorrect.")



def plot_labels_of_edges(Graph):
  for properties in Graph.edges(data=True):
      label = properties[2]['beam_name']
      edge_pos = properties[2]['edge_pos']
      x = edge_pos[0]
      y = edge_pos[1]
      plt.text(x, y, label, color='black', fontsize=12, ha='center', va='center')



def get_edge_position_from_node_touple(node_touple, instrument):
  x_list = []
  y_list = []
  for k in node_touple:
    vec = get_pos_vector_from_opt_element(k, instrument)
    pos_node = get_pos_touple_from_pos_vector(vec)
    x_list.append(pos_node[0])
    y_list.append(pos_node[1])
  x_coordinate = (x_list[0] + x_list[1])/2
  y_coordinate = (y_list[0] + y_list[1])/2
  return x_coordinate, y_coordinate


def get_beam_name_from_graph_properties(Graph, start_node_input, end_node_input):
  for properties in Graph.edges(data=True):
    final_node = properties[0].replace('/entry/instrument/','')
    start_node = properties[1].replace('/entry/instrument/','')
    if final_node == end_node_input and start_node_input == start_node:
      return properties[2]['beam_name'] 
    #print(f"Edge: {properties[0]} - {properties[1]}, Properties: {properties[2]}")


def get_transfer_matrix_entries(NeXus_File, instrument):
  output_list_TMT_entries_only = []
  output_list_not_TMT_entries = []
  target_path_TMT = '/entry/instrument/opt_transfer_matrix_tables/'
  groups_at_path, data_at_path = get_groups_and_datasets_from_nexus_file(NeXus_File, target_path_TMT)
  for i in groups_at_path:
    # iterate through each element in the list, only append it, if the calss can be sucessfully extracted as NX_class = 'NXtransfer_matrix_table'
    try:
      class_type = instrument[target_path_TMT + i].attrs['NX_class']
      if class_type == 'NXtransfer_matrix_table':
        output_list_TMT_entries_only.append(i)
    except KeyError:
      output_list_not_TMT_entries.append(i)
      continue
  return output_list_TMT_entries_only, output_list_not_TMT_entries
  #power_unit = instrument['beamsplitter_1/output_beam_bs1_straight/final_energy'].attrs['units']





def get_the_neigbor_nodes_from_TMT_entries_as_dictionary(NeXus_File, opt_elements_with_TMT_list, instrument):
  target_path_TMT = '/entry/instrument/opt_transfer_matrix_tables/'
  output_dict = {}

  TMT_count = 0
  print("Get the neighbor nodes: \n")
  for i in opt_elements_with_TMT_list:
    goal_nxs_file_path = target_path_TMT + "TMT_" + i
    groups, datas=get_groups_and_datasets_from_nexus_file(NeXus_File, goal_nxs_file_path)
    for k in datas:
      TMT_count = TMT_count + 1
      goal_path_matrix = goal_nxs_file_path + '/' + k
      goal_path_matrix_short = goal_path_matrix.replace('/entry/instrument/','')
      matrix = _get_value(instrument[goal_path_matrix_short])
      neigbor_nodes_string = k.replace('matrix_','')

      if neigbor_nodes_string.__contains__('_'):
        if neigbor_nodes_string.count('_') == 1:
          underscore_pos = neigbor_nodes_string.index('_')
          first_node = neigbor_nodes_string[:underscore_pos]
          second_node = neigbor_nodes_string[underscore_pos+1:]
        else:
          print("The TMT table names are not formatted as desired.")
      else:
          first_node = neigbor_nodes_string[:underscore_pos]
          second_node = None

      # Write the data to a dictionary which is used as output
      dict_key = 'Transfer_Matrix_' + str(TMT_count)  
      output_dict[dict_key] = [i, first_node, second_node, matrix]
  return output_dict





def matrix_multipl_atten_and_div(x,A):
  if len(x) == 2 and len(A) == 2 and len(A[0]) == 2:
  
    # classical multiplication
    #x1_prime = x[0]*A[0,0] + x[1]*A[0,1]
    #x2_prime = x[0]*A[1,0] + x[1]*A[1,1]
    # simplified version as intensity and divergence do not couple
    x1_prime = x[0] * A[0,0] 
    x2_prime = x[1] + A[1,1]
    return np.array([x1_prime,x2_prime])
  else:
    raise TypeError



def plot_all_pahts(dictionary):

  path_names = list(dictionary.keys())


  # Set the number of subplots
  num_subplots = len(dictionary)

  # Create a figure and subplots using subplots
  fig, axes = plt.subplots(num_subplots, 1, figsize=(8, 2*num_subplots), sharey=True)

  # Loop through each subplot
  for i, ax in enumerate(axes):
      selected_path = path_names[i]
      beam_names = []
      for i in range(len(dictionary[selected_path][0])):
        first_node = str(dictionary[selected_path][1][i])
        second_node = str(dictionary[selected_path][1][i+1])
        beam_name=get_beam_name_from_graph_properties(G, first_node, second_node)
        beam_names.append(beam_name)
      
      atten_and_div_array = np.array(dictionary[selected_path][0])

      dictionary[selected_path].append(beam_names)

      atten = atten_and_div_array[:,0]
      div = atten_and_div_array[:,1]


      # Plot different data on each subplot
      ax.plot(beam_names, atten, label='Attentuation',linewidth=5)
      ax.plot(beam_names, div, label='Divergence',linewidth=5)


      # Customize subplot
      ax.set_title(f'Path: {selected_path}')
      ax.legend()
      ax.set_ylabel("Att. / Div.", fontsize=16)
      ax.set_xlabel("NXbeam", fontsize=16)
      ax.legend(fontsize=14)
      ax.grid()

      # Increase the font size for tick labels
      ax.tick_params(axis='both', which='major', labelsize=14)

  # Adjust layout to prevent overlap
  plt.tight_layout()

  # Show the plot
  plt.show()







def get_number_of_equivalent_beams_at_path_location(beam_path_list, beam):
  for i in beam_path_list:
    for k in beam:
      print(i)
      print(k)
      print("____\n ")


def get_number_of_equivalent_words_in_list(list_of_strings):
  result = {}
  for word in set(list_of_strings):
      result[word] = list_of_strings.count(word)  
  return result




def get_number_of_equivalent_words_in_list(list_of_strings):
  result = {}
  for word in set(list_of_strings):
      result[word] = list_of_strings.count(word)  
  return result



def add_position_and_names_to_graph_nodes(Graph,instrument):
  for item in Graph.nodes:
    pos_vec =  get_pos_vector_from_opt_element(item, instrument)
    Graph.nodes[item]['position'] = (pos_vec[0],pos_vec[1])
    Graph.nodes[item]['name'] = item.replace('/entry/instrument/','')



# Excecute this part only, if the file is excetuted directly. I.e. this part below is not executed if the file is imported
if __name__ == "__main__":




  #result =subprocess.check_output('read_nexus -f "C:/Daten/_Project 4 FAIRmat/NXBeam_path/NXopt_element/interferometer.nxs" -c /NXopt/ENTRY/INSTRUMENT', shell=True)
  result = b'INFO: entry/instrument' # for faster purpose, replaced the output by a simple string




  instr_path=result.splitlines()[0].split(b' ')[1]

  NeXus_File_Name = "interferometer_v4.nxs"



  f = h5py.File(NeXus_File_Name, "r")
  instr=f[instr_path]



  #start hardcoding from here on (=use specific paths of files, which would not work, if something earlier in the line is adjusted)
  if False:
    power = _get_value(instr['beamsplitter01/output_beam_bs1_straight/final_energy'])
    power_unit = instr['beamsplitter01/output_beam_bs1_straight/final_energy'].attrs['units']

    power=1.23456

    print(power)
    print(power_unit)

  if False:
    original_path = '/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter_2/matrix_i1o2'
    path_short = original_path.replace('/entry/instrument/','')
    matrix = _get_value(instr[path_short])
    print('###########')
    print('###########')
    print(matrix)




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



  # Set properties for the first edge
  #G[all_edges[i][0]][all_edges[i][1]]['weight'] = 3.0
  #Graph[all_edges[i][0]][all_edges[i][1]]['pos'] = opt_beams_at_path[i]





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

  for i in edges_list:
    x_pos_edge, y_pos_edge = get_edge_position_from_node_touple(i, instr)
    G.add_edge(i[0],i[1], edge_pos=(x_pos_edge, y_pos_edge))

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

  if True:
    # Print edges and their properties
    for properties in G.edges(data=True):
        print(f"Edge: {properties[0]} - {properties[1]}, Properties: {properties[2]}")

  add_beam_names_to_edges(G, all_edges, opt_beams_at_path, NeXus_File_Name, instr)


  # Modify the labels to remove the specific string ("Node_" in this case)
  
  entry_instrument_removal = "/entry/instrument"
  
  # draw the graph with specific properties. pos= gives the location of the nodes
  nx.draw(G, pos=node_positions,  with_labels=False, node_size=4*700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color="gray", linewidths=4*1, alpha=0.7, arrowstyle='-|>', arrowsize=3*20, width=4*0.5)


    # Draw the labels separately
  labels = nx.draw_networkx_labels(G, pos=node_positions)
  
  #print(labels)
  #keys_list = list(labels.keys())
  #print(labels[keys_list[0]])
  #print(type(labels[keys_list[0]]))
    # Rotate the labels
  #for _, label in labels.items():
  #  label.set_rotation(45)  # Set the rotation angle as needed


  substring_to_remove = entry_instrument_removal
  for _, label in labels.items():
      new_text = label.get_text().replace(substring_to_remove, "")
      label.set_text(new_text)
      label.set_rotation(45)  # Set the rotation angle as needed

  plot_labels_of_edges(G)



  # Show the graph
  plt.show()











  if True:
    # Print edges and their properties
    for properties in G.edges(data=True):
        print(f"Edge: {properties[0]} - {properties[1]}, Properties: {properties[2]}")



  opt_elements_with_TMT_long, non_TMT_entries = get_transfer_matrix_entries(NeXus_File_Name, instr)


  # remove the "TMT_" string from the entries
  opt_elements_with_TMT = []
  for i in opt_elements_with_TMT_long:
    opt_elements_with_TMT.append(i.replace('TMT_',''))



    # f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter_2/matrix_beam04_beam06'] = [[bs2_tsr,0],[0,unity_div]]
  Transfer_matrix_dictionary = get_the_neigbor_nodes_from_TMT_entries_as_dictionary(NeXus_File_Name,opt_elements_with_TMT, instr)

  # now-> get the transfermatrix, that relates the transfermatrix to two edges and one node

  #1 Creation of Beam Elements, if they are missing


  # a) scanning of the existing beams ##check
  # b) detect, which optical beams (related to edges) are missing ## do later
  # c) create new optical beam instances, which fill up the missing ## do later
  # d) Identification: the beams need as edges previous and next elements (two nodes identify an edge)
  #     should this data be given prior?
  # if there are some edges missing, create these
  # the transfer matrix need a link of total 3 nodes or 2 edges. --> 2 beams or 3 optical elements









  print("#######################")
  print("#######################")
  print("#######################")
  print("#######################")
  print("#######################")








  #extract all paths from roots t
  for root in roots:
      paths = nx.all_simple_paths(G, root, leaves)
      all_paths.extend(paths)



  # If the position between two specific elements shall be calculated
  if True:
    target_node_list = [n2]
    source_node_list = [n6, n7]
    # Find all simple paths between source and target nodes
    all_paths = list(nx.all_simple_paths(G, source=source_node_list[0], target=target_node_list[0]))



  # reverse order, so that the beam path is along the beam direction. Had to be reverses, as the beam path is reconstructred in reverse direction via "previous_opt_element"
  for i in all_paths:
    i.reverse()






  path_dict = {}

  for m in range(len(all_paths)):
    starting_beam_state = np.array([0.08,0]) # 100mW power, and 0 degree divergence
    beam_state_list = []
    path_name = "path" + str(m)
    path_element_list = []
    for k in range(len(all_paths[m])):
      path_element_list.append(all_paths[m][k].replace('/entry/instrument/',''))
      if k != 0 and k != len(all_paths[m])-1:
        #prepare the respective needed nodes to select the transfermatrix
        center_opt_elem_name = all_paths[m][k].replace('/entry/instrument/','')
        prev_opt_elem_name = all_paths[m][k-1].replace('/entry/instrument/','') 
        next_opt_elem_name = all_paths[m][k+1].replace('/entry/instrument/','') 
        
        
        # Select the respective Transfer_matrix
        for i in Transfer_matrix_dictionary:
          if Transfer_matrix_dictionary[i][0] == center_opt_elem_name:
            if Transfer_matrix_dictionary[i][1] == prev_opt_elem_name:
              if Transfer_matrix_dictionary[i][2] == next_opt_elem_name:
                #print(Transfer_matrix_dictionary[i][0], center_opt_elem_name)
                #print(Transfer_matrix_dictionary[i][1], prev_opt_elem_name)
                #print(Transfer_matrix_dictionary[i][2], next_opt_elem_name)
                transfer_matrix = Transfer_matrix_dictionary[i][3]

        # define beam state for starting calculations
        if k == 1:
          new_beam_state = starting_beam_state
          beam_state_list.append(new_beam_state)
        
        new_beam_state = matrix_multipl_atten_and_div(new_beam_state, transfer_matrix)
        beam_state_list.append(new_beam_state)

    path_dict[path_name] = [beam_state_list, path_element_list]

    
  plot_all_pahts(path_dict)


  path_names = list(path_dict.keys())



  #print(path_dict[path_names[0]])
  #print(path_dict[path_names[0]][0])
  #print(path_dict[path_names[0]][0])
  #np.array(path_dict[path_names[0]][0])
  #print(path_dict[path_names[0]][0][1])












  if True:
    # Print edges and their properties
    for properties in G.nodes(data=True):
        print(properties)

  print(">>>>>>>>>>>>")
  print(G.nodes)
  print(G.nodes['/entry/instrument/beamsplitter01'])




  # add content to the nxs file

  # Source file name
  source_filename = 'interferometer_v4.nxs'

  # Destination file name (new name for the copy)
  destination_filename = 'interferometer_v4_mod.nxs'

  if True:
    # use os. to create a copy of a file named: "interferometer_v3_mod.nxs"
    import shutil
    # Copy the file
    shutil.copy2(source_filename, destination_filename)
    print(f"File '{source_filename}' copied to '{destination_filename}'.")





  f = h5py.File("interferometer_v4_mod.nxs", "a")

  for i in List_of_beam_names_to_be_created_later:
    add_beam_to_nexus_file(f, i)

  list_of_all_beams = []

  for m in path_dict:
    beam_names = path_dict[m][2]
    for k in beam_names:
      list_of_all_beams.append(k)

  beam_number_counter = get_number_of_equivalent_words_in_list(list_of_all_beams)

  Total_beam_count=0
  for m in path_dict:
    path_str = m
    beam_states = path_dict[m][0]
    opt_elements = path_dict[m][1]
    beam_names = path_dict[m][2]
    print(path_str, beam_names)
    for k in beam_names:
      list_of_all_beams.append(k)




    
    for index, value in enumerate(beam_names):
      weight_of_beam_at_path_pos = 1/float(beam_number_counter[value])
      f['/entry/instrument/' + value + '/vector_atten_div'+'_' + str(Total_beam_count)] = beam_states[index]
      f['/entry/instrument/' + value + '/vector_atten_div'+'_' + str(Total_beam_count)].attrs['path_id'] = path_str
      f['/entry/instrument/' + value + '/vector_atten_div'+'_' + str(Total_beam_count)].attrs['beam_weight'] = weight_of_beam_at_path_pos
      Total_beam_count = Total_beam_count + 1 

