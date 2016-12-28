

def eval_mod(mod, nodes, semnet):
    if mod["rel"] == "nmod":
        case = nodes[mod["deps"]["case"][0]]["word"]
        mod = eval_nom(mod, nodes, semnet)
        return (mod, case)
    if mod["rel"] == "nmod:npmod":
        nummod = nodes[mod["deps"]["nummod"][0]]["word"]
        mod = eval_nom(mod, nodes, semnet)
        return mod.decorate(nummod)

    return semnet.get(mod["word"])


def eval_nom(nom, nodes, semnet):
    amods = [ eval_mod(nodes[amod], nodes, semnet) for amod in nom["deps"]["amod"] ]
    nmods = [ eval_mod(nodes[nmod], nodes, semnet) for nmod in nom["deps"]["nmod"] ]
    npmods = [ eval_mod(nodes[nmod], nodes, semnet) for nmod in nom["deps"]["nmod:npmod"] ]
    acls = [ eval_nom(nodes[acl], nodes, semnet) for acl in nom["deps"]["acl"] ]

    nom = semnet.get(nom["word"])

    return nom._find_child(amods + nmods + npmods + acls)


def eval_root(root, nodes, semnet, prevsubj=None):
    subj = nodes[root["deps"]["nsubj"][0]]
    subj = eval_nom(subj, nodes, semnet)

    if subj.name in ["they", "it"]:
        subj = prevsubj or subj

    if root["tag"] in ["NN", "NNS", "JJ"]:
        cop = nodes[root["deps"]["cop"][0]]["word"]
        pred = eval_nom(root, nodes, semnet)
        subj[cop] = pred

    elif root["tag"] in ["VB", "VBD", "VBN", "VBP", "VBZ"]:
        verb = root["word"]
        pred = eval_nom(nodes[root["deps"]["dobj"][0]], nodes, semnet)
        subj[verb] = pred

    return subj
