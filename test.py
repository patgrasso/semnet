
import wikipedia
import sandbox
import sys
import os
import subprocess
from models import Concept

if len(sys.argv) <= 1:
    sys.argv += ["tree"]

pages = ' '.join(sys.argv[1:]).split(',')

for page in pages:
    wikipedia.set_lang("simple")
    page = wikipedia.page(page)
    content = page.content.split('.')

    sandbox.parse_many(content)

output_fname = os.path.basename(page.url)
Concept.to_dot(output_fname + ".dot")
subprocess.call(["dot",
                 "-Tpng", output_fname + ".dot",
                 "-o", output_fname + ".png"])

#sandbox.show_concept()
#sandbox.repl()


