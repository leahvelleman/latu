from jinja2 import Environment, Template
import markdown

C = "ptk7bdgmnlwsWh"
V = "aeiou1"
onset = "[" + C + " " + "]"
vowel = "[" + V + "]|ja|jo|ju"
S = onset + "?" + vowel

allophony = [("+", ""), 
             ("-", ""), 
             ("ti", "tSi"),
             ("di", "dZi"),
             ("si", "Si"),
             ("tj", "tS"),
             ("dj", "dZ"),
             ("sj", "S"),
             ("7w", "7W"),
             ("hs", "ss"),
             ("hS", "SS"),
             ("hw", "WW"),
             ("hW", "WW"),
             ("hl", "KK"),
             ("hm", "MM"),
             ("hn", "NN")]

IPA = [("W", "ʍ"), ("7", "ʔ"), ("K", "ɬ"), ("S", "ʃ"), ("Z", "ʒ"), ("N", "n̥"),
        ("M", "m̥"), ("y", "ɨ"), (":", "ː") ]

orthography = [
               ("j", "i"),
    ("7p", "pp"),
               ("7t", "tt"),
               ("7k", "kk"),
               ("7b", "bb"),
               ("7d", "dd"),
               ("7g", "gg"),
               ("7s", "ts"),
               ("7S", "tsh"),
               ("7tS", "tch"),
               ("7dZ", "dj"),
               ("7W", "qu"),
               ("7l", "tl"),
               ("7m", "pm"),
               ("7n", "tn"),
               ("tS", "ch"),
               ("S", "sh"),
               ("dZ", "j"),
               ("W", "wh"),
               ("SS", "ssh"),
               ("WW", "wwh"),
               ("KK", "lh"),
               ("MM", "mh"),
               ("NN", "nh"),
               ("a:", "ā"),
               ("e:", "ē"),
               ("i:", "ī"),
               ("o:", "ō"),
               ("u:", "ū"),
               ("y:", "ȳ"),
               ("7", "’")]



class Word():
    def __init__(self, *args):
        if len(args) == 2 and isinstance(args[0], Word):
            self.underlying = args[0].underlying
            self.gloss = args[1]
        elif len(args) == 2:
            self.underlying = args[0]
            self.gloss = args[1]
        else:
            raise TypeError

    def __add__(self, other):
        if isinstance(other, Word):
            return Word(self.underlying + "+" + other.underlying,
                        self.gloss + "+" + other.gloss)

    def __mul__(self, other):
        if isinstance(other, Word):
            return Word(self.underlying + " " + other.underlying,
                        self.gloss + " " + other.gloss)

    def __str__(self):
        abbrstr = ""
        if self.phonemic != self.phonetic:
            abbrstr += "<span class='tooltipline'>[{}]</span> ".format(self.phonetic)
        abbrstr += "<span class='tooltipline'>/{}/</span> ".format(self.phonemic)
        abbrstr += "<span class='tooltipline'>*{}*</span> ".format(self.gloss)
        return "<span class='tooltip'>{0}</span><span class='tooltiptext'>{1}</span>".format(self.surface, abbrstr, self.gloss)
    
    def __repr__(self):
        return "<{} {} {} {}>".format(type(self), self.surface, self.underlying, self.gloss)

    @property
    def surface(self):
        pairs = allophony + orthography
        s = self.underlying
        for p in pairs:
            s = s.replace(p[0], p[1])
        return s

    @property
    def phonemic(self):
        pairs = IPA
        s = self.underlying
        for p in pairs:
            s = s.replace(p[0], p[1])
        return s

    @property
    def phonetic(self):
        pairs = allophony + IPA
        s = self.underlying
        for p in pairs:
            s = s.replace(p[0], p[1])
        return s


class Noun(Word):
    ...

class Adjective(Word):
    ...

class Verb(Word):
    ...

class Suffix():
    def __init__(self, process, gloss, concatenative=None):
        self.process = process
        self.gloss = gloss
        self.concatenative = concatenative

    @classmethod
    def fixed(cls, s, gloss):
        process = lambda stem: s
        concatenative = True
        return cls(process, gloss, concatenative)

    @classmethod
    def variable(cls, f, gloss):
        process = f
        concatenative = True
        return cls(process, gloss, concatenative)

    def __rsub__(self, other):
        if isinstance(other, Word):
            stem = other.underlying + "-" + self.process(other.underlying)
            gloss = other.gloss + "-" + self.gloss
            return Word(stem, gloss)




env = Environment()
env.filters['f'] = lambda w: "{} *{}*".format(str(w), w.gloss)


class lexicon():
    time = Noun("let", "time")
    day = Noun("iku", "day")
    daytime = Noun(time+day, "daytime")

    sit = Verb("hehde", "sit")
    clawCL = Noun("ka", "claw.CL")
    perch = Verb(sit*clawCL, "perch")

    on = Word("pi", "on")
    and_ = Word("kuy", "and")
    then = Word("’e", "then")
    will = Verb("wo:", "will")
    go = Verb("tys", "go")
    information = Noun("Wjabju:", "information")
    more = Adjective("niosah", "more")
    word = Noun("tja7a", "word")
    have = Verb("syi", "have")
    line = Noun("tihdinia", "line")
    dot = Noun("sihlihte", "dot")
    below = Word("We:to:", "below")
    tree = Noun("ak", "tree")
    point_out = Verb("Wjutu", "point.out")
    little = Adjective("tiWi", "little")
    prize = Noun("dana", "prize")
    poison = Noun("a:mala", "poison")
    boot = Noun("wele", "boot")
    music = Noun("te:le:", "music")
    broken = Adjective("i:hki", "broken")
    lake = Noun("mono", "lake")
    soap = Noun("o:mo:", "soap")
    problem = Noun("su7tu", "problem")
    knife = Noun("ulū", "knife")
    bite = Verb("kywy", "bite")
    island = Noun("Wy:7y", "island")
    see = Verb("mjoto", "see")
    _open = Verb("kjala", "open")
    hat = Noun("kju:pu", "hat")
    night = Noun("nja:da", "night")
    village = Noun("wjo:lo", "village")
    drinkN = Noun("tas", "drink")
    path = Noun("kad", "path")
    _not = Word("mi", "not")
    fire = Noun("ah", "fire")
    foot = Noun("We7", "foot")

    IMP = Suffix.fixed("ku", "IMP")
    INDEF = Suffix.fixed("a", "IND")
    INDIC = Suffix.fixed("a", "IND")
    PSUBJ = Suffix.fixed("sa", "POS.SUBJ")
    NSUBJ = Suffix.fixed("si", "POS.SUBJ")
    CON = Suffix.fixed("i", "CON")
    def DEFify(stem):
        if stem[-1] in V:
            return "7"
        else:
            return "iu:"
    DEF = Suffix.variable(DEFify, "DEF")


lex = {k: getattr(lexicon, k) for k in dir(lexicon) if
        isinstance(getattr(lexicon, k), Word)}

template = env.from_string("""
<style type="text/css">
body {
  font-family: "Charter";
  line-height: 1.5;
  width: 500px;
  margin-left: 50px;
}

.admonition {
  margin: 0 -16px;
  border-radius: 6px;
  border: 3px solid #369;
  background-color: #CEF;
}

.admonition p {
  padding: 0 16px;
}

.admonition-title {
    display: block;
font-size: 2em;
margin-top: 0.67em;
margin-bottom: 0.67em;
margin-left: 0;
margin-right: 0;
font-weight: bold;
    }


.tooltip {
  font-weight: bold;
  border-bottom: 1px dotted #369;
  }

/* Tooltip text */
.tooltiptext {
font-family: "Charter";
  visibility: hidden;
  --aside-offset: 1rem;
  --aside-offset-lineheight: 1.5rem;
  margin-bottom: calc(var(--padding) * 2);
  padding: var(--padding);
  position: absolute;
  left: 600px;
  width: var(--aside-width);
  border-radius: calc(var(--padding)/4);
  max-width: 100%;
  padding: 16px;
  margin: -16px;
}

.tooltipline {
  position: relative;
  display: block;
}

.tooltipline::after {
  content: "\a";
  white-space: pre;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover + .tooltiptext  {
  visibility: visible;
}

ul li {
list-style: none;
margin-left: 10px;
}
table {
margin-left: 50px;
}
</style>

# Latu

!!! note
    {{ perch-IMP }} {{ on }} {{ word-CON }} {{ have }} {{ line-CON }} 
    {{ dot-INDEF }} {{ below }} {{ and }} {{ then }} {{ will-INDIC }} 
    {{ go-PSUBJ }} {{ information-CON }} {{ more }}.

    *Hover over words that have a dotted line under them for more information.*

# Phonology
## Vowels 

There are six basic vowels: the five cardinal vowels, spelled **a e i o u,**
and /1/, spelled **y.** All six occur both short and long, and written with
a macron when they are long.

|                  |                  |
|------------------|------------------|
| {{ prize | f }}  | {{ poison | f }} |
| {{ boot | f }}   | {{ music | f }}  |
| {{ little | f }} | {{ broken | f }} |
| {{ lake | f }}   |  {{ soap | f }}  |
| {{ problem | f }}|  {{ knife | f }} |
| {{ bite | f }}   | {{ island | f }} |

There are three diphthongs, **ia io iu**, pronounced /ja jo ju/. Other than in
these diphthongs, the [j]-sound does not occur.

- {{ see | f }}
- {{ _open | f }}
- {{ point_out | f }}

The diphthongs also occur with the second element long.

- {{ hat | f }}
- {{ night | f }}
- {{ village | f }}

Roots often have two identical vowels, like the examples in this section.
Another common pattern is an **i** in the first syllable and a diphthong
in the second.

## Consonants

There are fourteen consonant phonemes. 

|                | Bilabial | Alveolar | Velar | Glottal |
|-|-|-|-|-|
| Voiceless stop | **p** /p/ | **t** /t/ | **k** /k/ | **’** /ʔ/ |
| Voiced stop    | **b** /b/ | **d** /d/ | **g** /g/ |  |
| Fricative | | **s** /s/ | **wh** /ʍ/ | **h** /h/ | 
| Nasal | **m** /m/ | **n** /n/ | | | 
| Liquid | | **l** /l/ | **w** /w/ | |

Before **i**, the consonants **t d s** palatalize to [tʃ dʒ ʃ]. Before a
diphthong, these consonants palatalize and the first element of the diphthong
becomes silent. These changes are reflected in writing: the palatalized
consonants are written **ch j sh**.
""")
text = template.render(**lexicon.__dict__, lex=lex)
html = markdown.markdown(text, extensions=['tables', 'admonition', 'smarty'])

with open('latu.html', 'w') as f:
    f.write(html)





