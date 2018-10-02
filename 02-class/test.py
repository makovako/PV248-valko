#!/usr/bin/python3

import sys
import re
from scorelib import Person, Composition, Voice, Edition, Print

class Template:
    def __init__(self):
        self.print_num = None
        self.composers = []
        self.title = None
        self.genre = None
        self.key = None
        self.comp_year = None
        self.edition = None
        self.editors = []
        self.voices = []
        self.partiture = False # TODO on print yes/no
        self.incipit = None
    
    def __str__(self):
        return "PN: {}\nCOMP: {}\nTitle: {}\nGenre: {}\nKey: {}\nCompYear: {}\nEdition: {}\nEditors: {}\nVoices: {}\nPartiture: {}\nIncipit: {}\n".format(self.print_num,
        self.composers,
        self.title,
        self.genre,
        self.key,
        self.comp_year,
        self.edition,
        self.editors,
        self.voices,
        self.partiture,
        self.incipit
        )
    

def load(filename):
    prints = []
    tmpValues = Template()
    for line in open(filename,"r"):
        if line == '\n':
            # maybe DONE
            if tmpValues.print_num is not None:
                prints.append(Print(Edition(Composition(tmpValues.title
                    ,tmpValues.incipit,tmpValues.key,tmpValues.genre
                    ,tmpValues.comp_year,tmpValues.voices
                    ,tmpValues.composers),tmpValues.editors
                    ,tmpValues.edition),tmpValues.print_num
                    ,tmpValues.partiture))
            tmpValues = Template()
        # DONE
        if line.startswith("Print Number"):
            number = line.split(':')[1].strip()
            tmpValues.print_num = None if number == "" else int(number)
        # DONE
        if line.startswith("Composer"):
            r = re.compile(r"Composer: (.*)")
            m = r.match(line)
            if m is None or m.group(1) == "": #  when there is no name
                continue
            rawcomp = m.group(1)
            comp = rawcomp.split(";")
            for c in comp:
                if not c:
                    continue
                s = re.compile(r"(.*) \((.*)\)") # separete name and years
                n = s.match(c)
                if n is None: # doesnt have (years)
                    composer = Person(c.strip(),None,None)
                    tmpValues.composers.append(composer)
                else:
                    name = n.group(1).strip()
                    n.group(2).strip()
                    t = re.compile(r"\d\d\d\d") # pattern for for digits = year
                    born = None
                    died = None
                    if "-" in n.group(2):
                        # if there is "-", split by "-" or "--"
                        if "--" in n.group(2):
                            years = n.group(2).split("--")
                        else:
                            years = n.group(2).split("-")
                        o = t.match(years[0])
                        if o is not None:
                            born = int(o.group(0))
                        o = t.match(years[1])
                        if o is not None:
                            died = int(o.group(0))
                    else: # otherwise try to find *,+, or there will be only one year
                        if "*" in n.group(2):
                            o = t.match(n.group(2)[1:])
                            if o is not None and o.group(0) != "":
                                born = int(o.group(0))
                        elif "+" in n.group(2):
                            o = t.match(n.group(2)[1:])
                            if o is not None and o.group(0) != "":
                                died = int(o.group(0))
                        else:
                            o = t.match(n.group(2))
                            if o is not None and o.group(0) != "":
                                born = int(o.group(0))
                    tmpValues.composers.append(Person(name, born, died))
        # DONE
        if line.startswith("Title"):
            title = line.split(":")[1].strip()
            tmpValues.title = None if title == "" else title
        # DONE
        if line.startswith("Genre"):
            genre = line.split(":")[1].strip()
            tmpValues.genre = None if genre == "" else genre
        # DONE
        if line.startswith("Key"):
            key = line.split(":")[1].strip()
            tmpValues.key = None if key == "" else key
        # DONE
        if line.startswith("Composition Year"):
            r = re.compile(r"Composition Year: (\d{4})")
            m = r.match(line)
            if m is not None:
                tmpValues.comp_year = int(m.group(1))
        # DONE
        if line.startswith("Edition"):
            edition = line.split(":")[1].strip()
            tmpValues.edition = None if edition == "" else edition
        if line.startswith("Editor"):
            r = re.compile(r"Editor: (.*)")
            m = r.match(line)
            # TODO parse editors
            if m is not None and m.group(1) != "":
                
                tmpValues.editors.append(Person(m.group(1),None,None))
        if line.startswith("Voice"):
            voice = line.split(":")[1].strip()
            #TODO parse voices
            if voice != "":
                tmpValues.voices.append(Voice(voice,None))
        # DONE
        if line.startswith("Partiture"):
            partiture = line.split(":")[1].strip()
            if "yes" in partiture:
                tmpValues.partiture = True
        # DONE
        if line.startswith("Incipit"):
            incipit = line.split(":")[1].strip()
            if incipit != "" and tmpValues.incipit == None:
                tmpValues.incipit = incipit
    return prints

prints = load(sys.argv[1])
input()
for pr in prints:
    pr.format()
    print()