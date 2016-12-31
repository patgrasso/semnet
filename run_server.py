
import flask
from flask import Flask, render_template, send_from_directory, request
from semnet import interp, parser, SemNet, PickleStore
import wikipedia
import threading
import re

try:
    mind = PickleStore.load("semnet.pickle")
except:
    mind = SemNet()
store = PickleStore(mind, "semnet.pickle")

app = Flask(__name__,
            template_folder="web/templates")

mindlock = threading.Lock()

wikipedia.set_lang("simple")


already_explored = []


def evaluate_wiki_thread(page):
    page = wikipedia.page(page)

    mindlock.acquire()
    if page.title in already_explored:
        print("already parsed", page.title)
        mindlock.release()
        return
    mindlock.release()

    content = page.content.split('.')
    content = [sent.lower().strip() for sent in content]
    content = [''.join([i if ord(i) < 128 else '' for i in sent])
                for sent in content]

    print("parsing", page.title)
    result = parser.raw_parse_sents(content)
    print("parsed", page.title)

    prev_subj = None
    for parsed_sent in result:
        dep_graph = next(parsed_sent)
        mindlock.acquire()
        try:
            prev_subj = interp.eval_root(
                dep_graph.root,
                dep_graph.nodes,
                mind,
                prev_subj)
        except:
            pass
        mindlock.release()

    mindlock.acquire()
    already_explored.append(page.title)
    mindlock.release()


def evaluate_sentence_thread(sentence):
    dep = next(parser.raw_parse(sentence))

    mindlock.acquire()
    interp.eval_root(dep.root, dep.nodes, mind)
    mindlock.release()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/js/<path:path>")
def static_js(path):
    return send_from_directory("web", path)

@app.route("/parse", methods=["POST"])
def parse():
    sentence = request.form["sentence"]

    threading.Thread(
        target=evaluate_sentence_thread,
        args=(sentence,)).start()

    mindlock.acquire()
    relations = mind.to_list()
    mindlock.release()
    ret = {"result": relations}
    return flask.jsonify(**ret)

@app.route("/wiki_page", methods=["POST"])
def wiki_page():
    pages = request.form["sentence"].split(',')

    for page in pages:
        threading.Thread(
            target=evaluate_wiki_thread,
            args=(page,)).start()

    mindlock.acquire()
    relations = mind.to_list()
    mindlock.release()

    ret = {"result": relations}
    return flask.jsonify(**ret)

@app.route("/get_graph")
def get_graph():
    mindlock.acquire()
    relations = mind.to_list()
    mindlock.release()

    ret = {"result": relations}
    return flask.jsonify(**ret)

@app.route("/get_graph_vis")
def get_graph_vis():
    mindlock.acquire()
    relations = mind.to_list()
    mindlock.release()

    i = 0
    nodes = {}
    links = []
    for relation in relations:
        if relation["source"] not in nodes:
            nodes[relation["source"]] = i
            i += 1
        if relation["target"] not in nodes:
            nodes[relation["target"]] = i
            i += 1
        links.append({
            "id": len(links),
            "from": nodes[relation["source"]],
            "to": nodes[relation["target"]],
            "color": "#ccc" if relation["type"] == "<typeof>" else "#000",
            "label": relation["type"] if relation["type"] != "<typeof>" else ""
        })
    nodes = [ {"id": idd, "label": label} for label, idd in nodes.items() ]

    for i in range(len(links)):
        links[i]["id"] = i
    ret = {"nodes": nodes, "edges": links}
    return flask.jsonify(**ret)

@app.route("/to_dot")
def to_dot():
    topics = re.split("[, ]", request.args.get("topics") or '')
    print(topics)
    if "all" in topics:
        topics = None

    mindlock.acquire()
    dotstr = mind.to_dot(topics=topics)
    mindlock.release()

    return dotstr


app.run(host="0.0.0.0")
