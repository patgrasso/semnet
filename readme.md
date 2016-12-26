

# Concept Map

This is an experiment in mapping abstract concepts by parsing natural language.
The goal is to simulate a human intelligence model by interpretting text and
forming logical connections between ideas.


## Setup

The experiment requires the
[Stanford CoreNLP library jar](http://stanfordnlp.github.io/CoreNLP/#download)
and the model jar. A configuration file `config.cfg` needs to be created in the
project's root of the following format:

```
[stanford]
jar-path: path/to/stanford-corenlp.jar
model-path: path/to/stanford-english-model.jar

[graphs]
output-dir: path/of/output/graph/dir
```

With the respective paths replaced with the locations of the downloaded jars and
desired output directories.


## Explanation

Currently, the mapper operates by using Stanford's corenlp library to graph the
dependencies within each sentence (identify subject, direct object, adjectival
modifiers, etc.), then using the structures within the graph, extract and/or
infer logical rules based on the text. Given a set of sentences about one topic,
a reasonable logical model can be generated for that topic.

Concepts follow a hierarchy of specificity. Some concepts are more specific than
others, and the relationship between abstract and more concrete concepts is
captured. For example, `Concept <plant> [tall]` is a child concept of
`Concept <plant>` because they both refer to plants, except that the first one
only refers to tall plants, which is a subset of all plants.


## Example
```
parse("trees are tall plants")

=> Concept <tree>
     are:
       Concept <plant> [tall]
       
parse("plants have green leaves")

=> Concept <tree>
     are:
       Concept <plant> [tall]
         have:
           Concept <leav> [green]
           
   Concept <plant>
     have:
       Concept <leav> [green]
       
   Concept <leav>
   
   Concept <green>
```
