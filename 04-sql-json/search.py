#!/usr/bin/python3

import sys, sqlite3, json

# TODO change to false before commit
debug = False
if debug:
    conn = sqlite3.connect("test.dat")
else:
    conn = sqlite3.connect("scorelib.dat")
cur = conn.cursor()
input_name = "%{}%".format(sys.argv[1])
# this will match all persons: composers and editors
cur.execute("select person.id, person.name from person where person.name like ?",(input_name,))
persons = cur.fetchall()
out = {}
for person in persons:
    composer_id = person[0]
    cur.execute("select print.id, score.id,score.name,score.genre,score.key,score.year,score.incipit,edition.id,edition.name,print.partiture from score_author join score on score.id=score_author.score join edition on edition.score=score.id join print on print.edition=edition.id where score_author.composer = ?",(composer_id,))
    prints = cur.fetchall()
    # if this is matched editor, so he doeasnt have any print, it will skip this if and for loop, and wont add it to output dictionary
    # if the person have some prints, he is a composer
    if prints:
        out[person[1]] = []
    for pr in prints:
        print_dic = {}
        score_id = pr[1]
        edition_id = pr[7]
        cur.execute("select person.name,person.born,person.died from person join score_author on person.id=score_author.composer where score_author.score = ?",(score_id,))
        composers = cur.fetchall()
        cur.execute("select person.name from person join edition_author on person.id=edition_author.editor where edition_author.edition = ?",(edition_id,))
        editors = cur.fetchall()
        cur.execute("select voice.number,voice.range, voice.name from voice where voice.score = ?",(score_id,))
        voices = cur.fetchall()

        print_dic["Print Number"] = pr[0]
        composers_list = []
        for composer in composers:
            comp = {}
            comp["name"] = composer[0]
            if composer[1] is not None:
                comp["born"] = composer[1]
            if composer[2] is not None:
                comp["died"] = composer[2]
            composers_list.append(comp)
        print_dic["Composer"] = composers_list
        if pr[2] is not None:
            print_dic["Title"] = pr[2]
        if pr[3] is not None:
            print_dic["Genre"] = pr[3]
        if pr[4] is not None:
            print_dic["Key"] = pr[4]
        if pr[5] is not None:
            print_dic["Composition Year"] = pr[5]
        if pr[8] is not None:
            print_dic["Edition"] = pr[8]
        editors_list = []
        for editor in editors:
            edit = {}
            edit["name"] = editor[0]
            editors_list.append(edit)
        print_dic["Editor"] = editors_list

        # sort by voice number, not required, but nicer
        voices.sort(key=lambda tup: tup[0])
        for voice in voices:
            voice_dic = {}
            if voice[1] is not None:
                voice_dic["range"] = voice[1]
            if voice[2] is not None:
                voice_dic["name"] = voice[2]
            print_dic["Voice {}".format(voice[0])] = voice_dic

        if pr[9] == "Y":
            print_dic["Partiture"] = True
        else:
            print_dic["Partiture"] = False
        if pr[6] is not None:
            print_dic["Incipit"] = pr[6]
        # add current print dictionary to current processed compsoer(person)
        out[person[1]].append(print_dic)

print(json.dumps(out,indent=4,ensure_ascii=False))
    
conn.commit()
conn.close()