
from nltk.stem.porter import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser
import sys, time, os
from configparser import ConfigParser

from models import Concept, Thing
import handles


config = ConfigParser()
config.read("config.cfg")
graphs_dir = config.get("graphs", "output-dir")
path_to_jar = config.get("stanford", "jar-path")
path_to_models_jar = config.get("stanford", "model-path")

stemmer = PorterStemmer()
parser = StanfordDependencyParser(
        path_to_jar=path_to_jar,
        path_to_models_jar=path_to_models_jar)


def get_mods(word, trips):
    return [tup[1] for rel, tup in trips.items()
            if tup[0] == word and rel == "amod"]

def parse_many(sentences):
    sentences = [sent.lower() for sent in sentences]
    result = parser.raw_parse_sents(sentences)

    prev_subj = None
    for parsed_sent in result:
        dep = next(parsed_sent)
        prev_subj = handles.from_root(dep.root, dep.nodes, prev_subj)


def parse(sentence, do_print=True):
    sentence = sentence.lower()
    result = parser.raw_parse(sentence)
    dep = next(result)

    f = open(os.path.join(graphs_dir, str(int(time.time())) + ".dot"), "w")
    f.write(dep.to_dot())
    f.close()

    if do_print:
        print(sentence)
        for a, rel, b in dep.triples():
            print("{}({} <- {})".format(rel, a[0], b[0]))
        print()
        for i, node in dep.nodes.items():
            print('#', i)
            for key, val in node.items():
                print(' ', key, ':', val)
        print()

    handles.from_root(dep.root, dep.nodes)
#    for node in dep.nodes.values():
#        rel = node["rel"]
#        if rel in handles.handles:
#            handles.handles[rel](node, dep.nodes)

    return "STOP"

    trips = { stemmer.stem(rel) : (stemmer.stem(a[0]), stemmer.stem(b[0]))
              for a, rel, b in dep.triples() }
#    trips = { rel : (a[0], b[0]) for a, rel, b in dep.triples() }

    if "nsubj" in trips:
        subj = trips["nsubj"][1]
        mods = get_mods(subj, trips)
        subj = Concept.get(subj, mods)

        if "cop" in trips:
            verb = trips["cop"][1]
            adj = trips["cop"][0]
            mods = get_mods(adj, trips)
            subj[verb] = Concept.get(adj, mods)

        if "dobj" in trips:
            verb = trips["dobj"][0]
            dobj = trips["dobj"][1]
            mods = get_mods(dobj, trips)
            subj[verb] = Concept.get(dobj, mods)


def show_concept(concept=None):
    if concept is None:
        for c in Concept.concepts():
            print(c)
            print()
    else:
        print(concept)
        print()
        for child in concept.children:
            show_concept(child)


def repl():
    while True:
        sys.stdout.write("--> ")
        inp = input()
        if inp.startswith("show"):
            query = (inp.split(' ') + [None])[1]
            query = Concept.get(query) if query is not None else None
            show_concept(query)
        elif inp.startswith("dot"):
            fname = (inp.split(' ') + [None])[1]
            if fname is not None:
                Concept.to_dot(fname)
        else:
            parse(inp)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Provide a sentence to parse!")
        exit(1)

    if sys.argv[1] == "-i":
        repl()
    else:
        sentence = ' '.join(sys.argv[1:])
        parse(sentence)
        print()
        show_concept()

