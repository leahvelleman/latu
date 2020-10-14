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

template = env.from_string("""
<style type="text/css">
{}
</style>
{}
""".format(style, bodytext))
text = template.render(**lexicon.__dict__, IMP=IMP, CON=CON, INDEF=INDEF,
        INDIC=INDIC, PSUBJ=PSUBJ)
html = markdown.markdown(text, extensions=['tables', 'admonition', 'smarty'])

with open('latu.html', 'w') as f:
    f.write(html)





