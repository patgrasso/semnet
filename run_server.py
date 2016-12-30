
import flask
from flask import Flask, render_template, send_from_directory, request
from network import SemNet
import parser
import interp
import wikipedia

mind = SemNet()
app = Flask(__name__,
            template_folder="web/templates")
#wikipedia.set_lang("simple")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/js/<path:path>")
def static_js(path):
    return send_from_directory("web", path)

@app.route("/parse", methods=["POST"])
def parse():
    dep = next(parser.raw_parse(request.form["sentence"]))
    interp.eval_root(dep.root, dep.nodes, mind)

    relations = mind.to_list()
    ret = {"result": relations}
    return flask.jsonify(**ret)

@app.route("/wiki_page", methods=["POST"])
def wiki_page():
    page = request.form["sentence"]
    page = wikipedia.page(page)

    content = page.content.split('.')
    content = [sent.lower().strip() for sent in content]
    content = [''.join([i if ord(i) < 128 else '' for i in sent])
                for sent in content]

    result = parser.raw_parse_sents(content)

    prev_subj = None
    for parsed_sent in result:
        dep_graph = next(parsed_sent)
        try:
            prev_subj = interp.eval_root(
                dep_graph.root,
                dep_graph.nodes,
                mind,
                prev_subj)
        except:
            pass
    relations = mind.to_list()
    ret = {"result": relations}
    return flask.jsonify(**ret)

@app.route("/get_graph")
def get_graph():
    relations = mind.to_list()
    ret = {"result": relations}
    return flask.jsonify(**ret)

@app.route("/get_graph_vis")
def get_graph_vis():
    relations = mind.to_list()
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
    return mind.to_dot()

app.run(host="0.0.0.0")
