from jinja2 import Environment, Template
import markdown
from lexicon import lexicon
from grammar import IMP, CON, INDEF, INDIC, PSUBJ

env = Environment()
env.filters['f'] = lambda w: "{} *{}*".format(str(w), w.gloss)

with open("latu.md") as f:
    bodytext = f.read()
with open("style.css") as f:
    style = f.read()

template = env.from_string(bodytext)

text = template.render(**lexicon.__dict__, IMP=IMP, CON=CON, INDEF=INDEF,
        INDIC=INDIC, PSUBJ=PSUBJ)
html = markdown.markdown(text, extensions=['tables', 'admonition', 'smarty'])

fullhtml = """
<html>
<head>
<style type="text/css">
{}
</style>
</head>
<body>
<div class="container">
{}
</div>
</body>
</html>
""".format(style, html)

with open('latu.html', 'w') as f:
    f.write(fullhtml)





