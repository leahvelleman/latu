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




