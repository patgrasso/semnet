
# FIXME ignore this file

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
    acls = [ eval_nom(nodes[acl], nodes, semnet) for acl in nom["deps"]["acl"] ]

    nom = semnet.get(nom["word"])

    return nom._find_child(amods + nmods + acls)


def eval_root(root, nodes, semnet):
    if root["tag"] in ["NN", "NNS", "JJ"]:
        subj = nodes[root["deps"]["nsubj"][0]]
        subj = eval_nom(subj, nodes, semnet)

        cop = nodes[root["deps"]["cop"][0]]["word"]
        #cop = semnet.get(cop)

        pred = eval_nom(root, nodes, semnet)

        subj[cop] = pred

        return pred
