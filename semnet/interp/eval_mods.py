
context_words = ["they", "it", "some", "these", "them", "those", "he", "she"]

def eval_mod(mod, nodes, semnet, prevsubj=None):
    if mod["rel"] == "nmod":
        case = nodes[mod["deps"]["case"][0]]["word"]
        mods = eval_nom(mod, nodes, semnet)
        return [ (mod, case) for mod in mods ]
    if mod["rel"] == "nmod:npmod":
        nummod = nodes[mod["deps"]["nummod"][0]]["word"]
        mods = eval_nom(mod, nodes, semnet)
        return [ mod.decorate(nummod) for mod in mods ]

    return [semnet.get(mod["word"])]


def eval_nom(nom, nodes, semnet, prevsubj=None):
    amods   = [ eval_mod(nodes[amod], nodes, semnet)
                for amod in nom["deps"]["amod"] ]
    nmods   = [ eval_mod(nodes[nmod], nodes, semnet)
                for nmod in nom["deps"]["nmod"] ]
    npmods  = [ eval_mod(nodes[nmod], nodes, semnet)
                for nmod in nom["deps"]["nmod:npmod"] ]
    acls    = [ eval_nom(nodes[acl], nodes, semnet)
                for acl in nom["deps"]["acl"] ]

    conjs   = sum([ eval_nom(nodes[conj], nodes, semnet)
                    for conj in nom["deps"]["conj"] ], [])

    nom = semnet.get(nom["word"])
    noms = [nom] + conjs
    noms = [ prevsubj or nom if nom.name in context_words else nom
             for nom in noms ]

    return [nom._find_child(sum(amods + nmods + npmods + acls, []))
            for nom in noms]


def eval_root(root, nodes, semnet, prevsubj=None):
    subj = nodes[root["deps"]["nsubj"][0]]
    subj = eval_nom(subj, nodes, semnet)[0]

    if subj.name in context_words:
        subj = prevsubj or subj

    if root["tag"] in ["NN", "NNS", "JJ"]:
        cop = nodes[root["deps"]["cop"][0]]["word"]
        preds = eval_nom(root, nodes, semnet, prevsubj)

        for pred in preds:
            subj[cop] = pred

    elif root["tag"] in ["VB", "VBD", "VBN", "VBP", "VBZ"]:
        verb = root["word"]
        dobjs = nodes[root["deps"]["dobj"][0]]
        preds = eval_nom(dobjs, nodes, semnet, prevsubj)

        for pred in preds:
            subj[verb] = pred

    return subj
