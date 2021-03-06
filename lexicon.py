from grammar import Word, Noun, Verb, Adjective, Suffix

class lexicon():
    time = Noun("let", "time")
    day = Noun("iku", "day")
    daytime = Noun(time+day, "daytime")


    sit = Verb("he7te", "sit")
    clawCL = Noun("ka", "claw.CL")
    perch = Verb(sit*clawCL, "perch")

    on = Word("pi", "on")
    and_ = Word("kuy", "and")
    then = Word("’e", "then")
    will = Verb("wo:", "will")
    go = Verb("tys", "go")
    information = Noun("Wjabik", "information")
    more = Adjective("niosah", "more")
    word = Noun("a7at", "word")
    have = Verb("syi", "have")
    line = Noun("tihdinja", "line")
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


lex = {k: getattr(lexicon, k) for k in dir(lexicon) if
        isinstance(getattr(lexicon, k), Word)}

