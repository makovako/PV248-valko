import re

class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture
    
    # maybe DONE
    def format(self):
        print("Print Number: "+str(self.print_id))
        
        if self.edition.composition.authors:
            persons = ""
            for person in self.edition.composition.authors:
                if person.born is not None:
                    if person.died is not None:
                        persons += "{} ({}--{}); ".format(person.name,person.born,person.died)
                    else:
                        persons += "{} ({}--); ".format(person.name,person.born)
                else:
                    if person.died is not None:
                        persons += "{} (--{}); ".format(person.name,person.died)
                    else:
                        persons += "{}; ".format(person.name)
                
            print("Composer: " + persons[:-2])
        if self.edition.composition.name is not None:
            print("Title: " + self.edition.composition.name)
        if self.edition.composition.genre is not None:
            print("Genre: " + self.edition.composition.genre)
        if self.edition.composition.key is not None:
            print("Key: " + self.edition.composition.key)
        if self.edition.composition.year is not None:
            print("Composition Year: " + str(self.edition.composition.year))
        if self.edition.name is not None:
            print("Edition: " + self.edition.name)
        if self.edition.authors:
            authors = ""
            for author in self.edition.authors:
                authors += "{}, ".format(author.name)
            print("Editor: " + authors[:-2])
        if self.edition.composition.voices:
            for i in range(len(self.edition.composition.voices)):
                voice = self.edition.composition.voices[i]
                if voice is None:
                    continue
                if voice.range is not None and voice.name is not None:
                    print("Voice {}: {}, {}".format(i+1,voice.range,voice.name))
                elif voice.name is not None:
                    print("Voice {}: {}".format(i+1,voice.name))
                else:
                    print("Voice {}: {}".format(i+1,voice.range))
        if self.partiture:
            print("Partiture: yes")
        else:
            print("Partiture: no")
        if self.edition.composition.incipit is not None:
            print("Incipit: " + self.edition.composition.incipit)

    def composition(self):
        return self.edition.composition


class Edition:
    def __init__(self,composition,authors,name):
        self.composition = composition
        self.authors = authors
        self.name = name

class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors

class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range

class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died

    def __str__(self):
        return self.name

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
        self.partiture = False
        self.incipit = None
    
    # helper method for debugging
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
    
# TODO dont split by : because in some title there is :, rather match in all cases
def load(filename):
    prints = []
    tmpValues = Template()
    for line in open(filename,"r"):
        if line == '\n': # save current print, and create blank one from template
            if tmpValues.print_num is not None: # when there are more new lines between prints, ignore second one
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
                    t = re.compile(r"\d\d\d\d") # pattern for four digits = year
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
                        else: # when there is only one year, i assign it to born
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
        # TODO this match doesnt work right, it matches DDDD/DD
        if line.startswith("Composition Year"):
            r = re.compile(r"Composition Year: (\d{4})")
            m = r.match(line)
            if m is not None:
                tmpValues.comp_year = int(m.group(1))
        # DONE
        if line.startswith("Edition"):
            edition = line.split(":")[1].strip()
            tmpValues.edition = None if edition == "" else edition
        # DONE
        if line.startswith("Editor"):
            r = re.compile(r"Editor: (.*)")
            m = r.match(line)
            if m is not None and m.group(1) != "":
                r = re.compile(r"((\w+, \w+.?),?)+") # pattern for word, word = lastname, firstname and there may be comma and other persons
                text = m.group(1)
                if r.match(text) is not None: # if firstname and lastname are separated by comma
                    while text != "":
                        m = r.match(text) # match them
                        tmpValues.editors.append(Person(m.group(2).strip(), None,None))# add them to output
                        text = text.replace(m.group(2), "")[2:] # remove them from string; # [2:] because there is ", " left in the beginning
                else: # if firstname and lastname are together, and persons are separated by comma
                    comps = text.split(",")
                    for comp in comps:
                        tmpValues.editors.append(Person(comp.strip(),None,None))
        # TODO better check by number
        if line.startswith("Voice"):
            voice = line.split(":")[1].strip()
            if voice != "": # if there is some voice
                r = re.compile(r"(\w+--\w+).*") # match two words and "--"" between them
                m = r.match(voice)
                if m is not None: # if there is range
                    range = m.group(1)
                    voice = voice.replace(m.group(1),"")[2:].strip() # strip range and ", "
                    name = None
                    if voice != "":
                        name = voice # if there is anything left for the name, assign it
                    tmpValues.voices.append(Voice(name, range))
                else: # there is no range
                    tmpValues.voices.append(Voice(voice.strip(),None))
            else: # there is no voice, but i need to remember position (Voice Number)
                tmpValues.voices.append(None)
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
    # on last print it doesnt catch new line at the end of the file
    # so after assigning all tmpValues, it ends reading the file in Incipit
    # and doesnt add it to prints
    # till it is still saved in tmValues
    # i can add that print afterwards
    # when there are two new lines at the end
    # then the last print will be added in for loop
    # and this condition catches that option
    # so it wont add new new print with deafalut None print number
    if tmpValues.print_num is not None:
        prints.append(Print(Edition(Composition(tmpValues.title
                        ,tmpValues.incipit,tmpValues.key,tmpValues.genre
                        ,tmpValues.comp_year,tmpValues.voices
                        ,tmpValues.composers),tmpValues.editors
                        ,tmpValues.edition),tmpValues.print_num
                        ,tmpValues.partiture))
    return prints
