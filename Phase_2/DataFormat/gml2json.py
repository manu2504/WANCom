import networkx as nx
import io
import json

graph = nx.read_gml("Uunet.gml") #need .gml file in current folder, read gml file
data = nx.node_link_data(graph) # save the graph into .json format(node link like)
with io.open('Uunet.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, indent=4)) # output the data as json file
