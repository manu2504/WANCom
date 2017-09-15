import os, sys

from graph_tool.all import *
from collections import defaultdict

COLOR_ENDNODE = [0, 0, 0.65, 0.9]
COLOR_HOP = [0, 0.65, 0, 0.9]
COLOR_UNKNOWN = [0.65, 0.65, 0.65, 0.7]
# Missing Alpha! Append it when using coalescence!
COLOR_COAL = [0.65, 0, 0]

EDGE_WIDTH = 15

def deasteriskify(hops):
    ret = []
    previous = None
    power = 0
    for h in hops:
        if h == '*':
            power += 1
            previous = '*'
        else:
            if(previous):
                ret.append("{}*".format(power))
                power = 0
                previous = None
            ret.append(h)
    return ret

vertex_count = 0
def generateHexLabel():
    global vertex_count
    vertex_count += 1
    return hex(vertex_count)[2:]

def getMinWeight(weight):
    minimum = sys.maxint
    for k,v in weight.iteritems():
        if v < minimum:
            minimum = v
    return minimum

def getMaxWeight(weight):
    maximum = -sys.maxint - 1
    for k,v in weight.iteritems():
        if v > maximum:
            maximum = v
    return maximum

def normalize(value, min, max):
    return (value - min) / (max - min)

def normalizeWeights(weight={}, min=None, max=None):
    ret = {}
    for k, v in weight.iteritems():
        ret[k] = normalize(v, min, max)
    return ret

def generateVerteces(g=None, paths=[]):
    uniquePathDict = {}
    for p in paths:
        for n in range(0, len(p.hops)):
            # If it is unknown ip store neighbors
            if '*' in p.hops[n]:
                # It should not goes outside array index as unknown nodes
                # are always between the two end nodes.
                pred = p.hops[n - 1]
                succ = p.hops[n + 1]
                if (pred, succ) not in uniquePathDict:
                    gvertex = g.add_vertex()
                    uniquePathDict[(pred, succ)] = (gvertex, p.hops[n], generateHexLabel())
            else:
                if p.hops[n] not in uniquePathDict:
                    gvertex = g.add_vertex()
                    lbl = ''
                    if n == 0 or n == len(p.hops) - 1:
                        lbl = p.hops[n]
                    else:
                        lbl = generateHexLabel()
                    uniquePathDict[p.hops[n]] = (gvertex, p.hops[n], lbl)
    return uniquePathDict

def generateEdges(g=None, vertices={}, paths={}):
    edgesDict = {}
    for p in paths:
        for n in range(1, len(p.hops)):
            if '*' in p.hops[n]:
                pred = p.hops[n - 1]
                succ = p.hops[n + 1]
                if not g.edge(vertices[(p.hops[n - 1])][0], vertices[(pred, succ)][0]):
                    e = g.add_edge(vertices[(p.hops[n - 1])][0], vertices[(pred, succ)][0])
            elif '*' in p.hops[n - 1]:
                pred = p.hops[n - 2]
                succ = p.hops[n]
                if not g.edge(vertices[(pred, succ)][0], vertices[(p.hops[n])][0]):
                    e = g.add_edge(vertices[(pred, succ)][0], vertices[(p.hops[n])][0])
            else:
                if not g.edge(vertices[p.hops[n - 1]][0], vertices[p.hops[n]][0]):
                    e = g.add_edge(vertices[p.hops[n - 1]][0], vertices[p.hops[n]][0])
    return edgesDict

# Return the top-k paths of a trace direction (selected by id).
def getTopKPaths(dm=None, td=None, k=10):
    return sorted(filter(lambda x: x.idTraceDirection == td, dm.pdm.list),
        key = lambda x: len(x.measurements))[0:k]

def weightEdges(paths=[]):
    weights = defaultdict(float)
    # Assign a weight to the edges
    for p in paths:
        # TODO: This is not responsibility of this method!
        p.hops = deasteriskify(p.hops)
        for n in range(1, len(p.hops)):
            if '*' in p.hops[n]:
                pred = p.hops[n - 1]
                succ = p.hops[n + 1]
                weights[(pred, succ)] += len(p.measurements)
            elif '*' in p.hops[n - 1]:
                pred = p.hops[n - 2]
                succ = p.hops[n]
                weights[(pred, succ)] += len(p.measurements)
            else:
                weights[(p.hops[n - 1], p.hops[n])] += len(p.measurements)
    return weights

def coalescence(paths=[]):
    # Appearence of a node in paths
    appearence = defaultdict(set)
    for p in paths:
        for h in p.hops:
            if '*' not in h:
                appearence[p.idTraceDirection].add(h)

    # Occurrencies of a hops in paths
    ret = defaultdict(float)
    for p in paths:
        for h in p.hops:
            if '*' not in h and h not in ret:
                for k, v in appearence.iteritems():
                    if h in v:
                        ret[h] += 1
    ret = {k: v for k, v in ret.iteritems() if v > 1}
    ret = normalizeWeights(weight=ret, min=0, max=getMaxWeight(ret))
    return {k: v * 0.5 + 0.5 for k, v in ret.iteritems()}

def vertexColorProp(g=None, vertices={}, coalescence={}):
    vprop_color = g.new_vertex_property("vector<float>")
    for k, v in vertices.iteritems():
        # Unknown IP address. Key of * is (pred, succ).
        if isinstance(k, tuple):
            vprop_color[v[0]] = COLOR_UNKNOWN
        # FIXME: this is not really nice
        # Exploit the fact that the label is an IP address only for end nodes.
        elif '.' in v[2]:
            vprop_color[v[0]] = COLOR_ENDNODE
        elif v[1] in coalescence:
            vprop_color[v[0]] = COLOR_COAL + [coalescence[v[1]]]
        else:
            vprop_color[v[0]] = COLOR_HOP
    return vprop_color

def vertexSizeProp(g=None, vertices={}, coalescence={}):
    vprop_size = g.new_vertex_property("int")
    for k, v in vertices.iteritems():
        # Unknown IP address. Key of * is (pred, succ).
        if isinstance(k, tuple):
            vprop_size[v[0]] = 25
        # FIXME: this is not really nice
        # Exploit the fact that the label is an IP address only for end nodes.
        elif '.' in v[2]:
            vprop_size[v[0]] = 50
        elif v[1] in coalescence:
            vprop_size[v[0]] = 40
        else:
            vprop_size[v[0]] = 25
    return vprop_size

def vertexLabelProp(dm=None, g=None, vertices={}):
    vprop_label = g.new_vertex_property("string")
    for k, v in vertices.iteritems():
        # FIXME: this is not really nice
        # Exploit the fact that the label is an IP address only for end nodes.
        if '.' in v[2]:
            vprop_label[v[0]] = dm.ndm.getElementByAttribute('ip', v[2]).name
        else:
            vprop_label[v[0]] = ""
    return vprop_label

def edgeWidthProp(g=None, vertices={}, paths={}, weights={}):
    eprop_size = g.new_edge_property("double")
    for p in paths:
        for n in range(1, len(p.hops)):
            if '*' in p.hops[n]:
                pred = p.hops[n - 1]
                succ = p.hops[n + 1]
                e = g.edge(vertices[(p.hops[n - 1])][0], vertices[(pred, succ)][0])
                if e:
                    eprop_size[e] = 1 + weights[(pred, succ)] * EDGE_WIDTH
            elif '*' in p.hops[n - 1]:
                pred = p.hops[n - 2]
                succ = p.hops[n]
                e = g.edge(vertices[(pred, succ)][0], vertices[(p.hops[n])][0])
                if  e:
                    eprop_size[e] = 1 + weights[(pred, succ)] * EDGE_WIDTH
            else:
                e = g.edge(vertices[p.hops[n - 1]][0], vertices[p.hops[n]][0])
                if e:
                    eprop_size[e] = 1 + weights[(p.hops[n - 1], p.hops[n])] * EDGE_WIDTH
    return eprop_size

def generateGraph(dm=None, tds=[], topk=10):
    paths = []
    for i in tds:
        paths = paths + getTopKPaths(dm=dm, td=i, k=topk)

    weights = weightEdges(paths)
    weights = normalizeWeights(weightEdges(paths), min=getMinWeight(weights), max=getMaxWeight(weights))

    g = Graph()

    uniquePathDict = generateVerteces(g=g, paths=paths)
    vprop_color = vertexColorProp(g, uniquePathDict, coalescence(paths))
    vprop_size = vertexSizeProp(g, uniquePathDict, coalescence(paths))
    vprop_label = vertexLabelProp(dm, g, uniquePathDict)

    edges = generateEdges(g=g, vertices=uniquePathDict, paths=paths)
    eprop_size = edgeWidthProp(g=g, vertices=uniquePathDict, paths=paths, weights=weights)

    ep = {}
    vp = {'text_position': "centered"}
    name = ""
    for td in tds:
        name += "{}-".format(td)
    name += "top{}".format(topk)
    if not os.path.exists("../../tectonic-graphs"):
        os.makedirs("../../tectonic-graphs")
    graph_draw(g, vertex_text=vprop_label, vertex_fill_color=vprop_color, vertex_size=vprop_size, vprops=vp, #pos=arf_layout(g, max_iter=0),
            edge_pen_width=eprop_size, edge_color=eprop_size,
            output_size=(2000, 1500), output="../../tectonic-graphs/{}.png".format(name))
