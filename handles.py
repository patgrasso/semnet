
from network import Concept
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

ps = SnowballStemmer("english")


def handle_cop(node, subj, nodes):
    vbz = ps.stem(node["word"])
    cop = get_concept(nodes[node["head"]], nodes)
    subj[vbz] = cop

def handle_dep(node, obj, nodes):
    verb = ps.stem(nodes[node["head"]]["word"])
    dobj = get_concept(node, nodes)
    dobj[verb] = obj

def handle_dobj(node, subj, nodes):
    verb = ps.stem(nodes[node["head"]]["word"])
    dobj = get_concept(node, nodes)
    subj[verb] = dobj


def get_concept(node, nodes):
    amods = None
    if "amod" in node["deps"].keys():
        amods = [ps.stem(nodes[mod]["word"]) for mod in node["deps"]["amod"]]

    return Concept.get(ps.stem(node["word"]), amods)

def from_root(root, nodes, prev_subj=None):
    if "nsubj" in root["deps"]:
        subj = get_concept(nodes[root["deps"]["nsubj"][0]], nodes)
    elif "nsubjpass" in root["deps"]:
        subj = get_concept(nodes[root["deps"]["nsubjpass"][0]], nodes)
    else:
        return

    # Referring to previous sentence's subject
    if subj.name in ["they", "it"]:
        subj = prev_subj or subj

    for key, fn in handles.items():
        if key in root["deps"]:
            for node in root["deps"][key]:
                fn(nodes[node], subj, nodes)

    return subj

handles = {
    "cop"   : handle_cop,
    "dep"   : handle_dep,
    "dobj"  : handle_dobj
}
