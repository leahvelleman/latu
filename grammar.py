
V = "aeiouy:"
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

IPA = [("W", "ʍ"), ("7", "ʔ"), ("KK", "ɬː"), ("SS", "ʃː"), ("ss", "sː"), ("S", "ʃ"), ("Z", "ʒ"), ("NN", "n̥ː"), ("MM", "m̥ː"), ("y", "ɨ"), (":", "ː") ]

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
            self.sources = [source for source in args[0].sources]
            self.gloss = args[1]
            self.citationform = self
        elif len(args) == 2:
            self.underlying = args[0]
            self.sources = []
            self.gloss = args[1]
            self.citationform = self
        else:
            raise TypeError

    def __add__(self, other):
        if isinstance(other, Word):
            out = Word(self.underlying + "+" + other.underlying,
                       self.gloss + "+" + other.gloss)
            out.sources = [self, other]
            return out

    def __mul__(self, other):
        if isinstance(other, Word):
            out = Word(self.underlying + " " + other.underlying,
                       self.gloss + " " + other.gloss)
            out.sources = [self, other]
            return out

    def __str__(self):
        abbrstr = ""
        if self.phonemic != self.phonetic:
            abbrstr += "<span class='tooltipline ipa'>[{}]</span> ".format(self.phonetic)
        abbrstr += "<span class='tooltipline ipa'>/{}/</span> ".format(self.phonemic)
        abbrstr += "<span class='tooltipline ipa'>{}</span> ".format(self.gloss)
        abbrstr += "<span class='tooltipline lexentry'><b>{}</b>".format(self.citationform.citation.capitalize())
        if self.sources:
            abbrstr += " (from "
            for source in self.sources:
                abbrstr += "<b>{}</b> <i>{}</i>, ".format(source.surface, source.gloss)
            abbrstr += ")" 
        abbrstr += " <i>{}</i>.</span>".format(self.citationform.gloss)
        out = "<span class='tooltip'>{0}</span><span class='tooltiptext'>{1}</span>".format(self.surface, abbrstr)
        return out
    
    def __repr__(self):
        return "<{} {} {} {}>".format(type(self), self.surface, self.underlying, self.gloss)

    @property
    def citation(self):
        return self.surface

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
    @property
    def citation(self):
        return (self-INDEF).surface

class Adjective(Word):
    ...

class Verb(Word):
    @property
    def citation(self):
        out = (self-INDIC).surface
        if self.underlying[-1] not in V:
            out += ", " + (self-IMP).surface
        return out

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
            w = Word(stem, gloss)
            w.sources = other.sources
            w.citationform = other.citationform
            return w




IMP = Suffix.fixed("ku7", "IMP")
def INDICify(stem):
    if stem[-1] in V:
        return ""
    else:
        return "a"
INDIC = Suffix.variable(INDICify, "INDIC")
PSUBJ = Suffix.fixed("sa", "POS.SUBJ")
NSUBJ = Suffix.fixed("si", "POS.SUBJ")
CON = Suffix.fixed("i", "CON")
def INDEFify(stem):
    if stem[-1] in V:
        return ""
    else:
        return "a"
INDEF = Suffix.variable(INDEFify, "INDEF")
def DEFify(stem):
    if stem[-1] in V:
        return "7"
    else:
        return "iu:"
DEF = Suffix.variable(DEFify, "DEF")
