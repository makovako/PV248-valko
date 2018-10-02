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
            print("Compostion Year: " + str(self.edition.composition.year))
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