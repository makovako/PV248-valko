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
            # TODO create print
            if tmpValues.print_num is not None:
                print("new line found")
                print(tmpValues)
                # for p in tmpValues["composers"]:
                #     print(p)
                # input()
            # if tmpValues.print_num is None:
            #     print("found two new lines")
            tmpValues = Template()


        # TODO change all to elif
        # DONE
        if line.startswith("Print Number"):
            number = line.split(':')[1].strip()
            tmpValues.print_num = None if number == "" else int(number)
        if line.startswith("Composer"):
            r = re.compile(r"Composer: (.*)")
            m = r.match(line)
            if m.group(1) is not None:
                tmpValues.composers.append(Person(m.group(1),None,None))
            continue
            # TODO finnish parsing composers
            if m is None: #  when there is no name
                continue
            rawcomp = m.group(1)
            comp = rawcomp.split(";")
            for c in comp:
                if not c:
                    continue
                s = re.compile(r"(.*) \((.*)\)")
                n = s.match(c)
                if n is None: # doesnt have (years)
                    composer = Person(c,None,None)
                    tmpValues["composers"].append(composer)
                else:
                    o = re.compile(r"\((.*)--(.*)\)").match(n.group(2))
                    # TODO mas 2 roky skonrtoluj ci su cisla a vyrob osobu
                    # meno sooby v n group 1
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
            if m is not None:
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
        
        

        
    

load(sys.argv[1])