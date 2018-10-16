#!/usr/bin/python3

from scorelib import Composition,Edition,Person,Print,Voice,load
# edition year nechat null
import sys, sqlite3


# database name
database = sys.argv[2]

def insert_print(pr, cur):
    # check composers
    composer_ids = [] # ids of composers of current print
    for comp in pr.edition.composition.authors:
        cur.execute("select id from person where name is ?",(comp.name,))
        composers = cur.fetchall()
        if len(composers) == 1:
            # when we have found composer with the same name remember it
            composer_ids.append(composers[0][0])
            # change years if necessary
            # TODO change only to two iffs, update only one field at a time if not none
            if comp.born is not None:
                if comp.died is not None:
                    cur.execute("update person set born = ?, died = ? where id is ?",(comp.born,comp.died,composers[0][0]))
                else:
                    cur.execute("update person set born = ? where id is ?",(comp.born,composers[0][0]))
            else:
                if comp.died is not None:
                    cur.execute("update person set died = ? where id is ?",(comp.died,composers[0][0]))
        #we have to create new composer
        else:
            # if comp.born is not None:
            #     if comp.died is not None:
            #         cur.execute("insert into person (name,died,born) values (?,?,?)",(comp.name,comp.born,comp.died))
            #     else:
            #         cur.execute("insert into person (name,born) values (?,?)",(comp.name, comp.born))
            # else:
            #     if comp.died is not None:
            #         cur.execute("insert into person (name, died) values (?,?)",(comp.name,comp.died))
            #     else:
            #         cur.execute("insert into person (name) values (?)",(comp.name,))
            cur.execute("insert into person (name,born,died) values (?,?,?)",(comp.name,comp.born,comp.died))
            composer_ids.append(cur.lastrowid)
            
    # check composition
    composition = pr.composition()
    # TODO namiesto = daj is
    cur.execute("select id from score where name is ? and genre is ? and key is ? and incipit is ? and year is ?",(composition.name, composition.genre, composition.key, composition.incipit, composition.year))
    compositions = cur.fetchall()
    composition_id = None
    # created_new_composition = False # for similarity in edition purposes, maybe i dont need it TODO
    if len(compositions) > 0:
        for com in compositions:
            current_composition_id = com[0]
            composition_same = True # expect they are same, when i change it to false, i dont have to continue comparing current compositon
            # check composers
            cur.execute("select composer from score_author where score is ?",(current_composition_id,))
            current_compositon_composers = cur.fetchall()
            # magic
            if set(i[0] for i in current_compositon_composers) != set(composer_ids): # if sets of composer ids are not equal
                composition_same = False
            # check voices
            if composition_same: # check only if previous test passed (same composers)
                # if there is some differnt voice, you can break
                cur.execute("select number,name,range from voice where score is ?",(current_composition_id,))
                current_compositon_voices = cur.fetchall()
                for i in range(len(composition.voices)):
                    if not composition_same:
                        break
                    if composition.voices[i] is not None:
                        for local_voice in current_compositon_voices:
                            # they have the same number, check other properties, if either of name or range is different, they are not same
                            if local_voice[0] == i+1 and (local_voice[1] != composition.voices[i].name or local_voice[2] !=composition.voices[i].range):
                                composition_same = False
                                break
                            
                # if set((voice.name,voice.range) for voice in composition.voices) != set(current_compositon_voices):
                #     composition_same = False
                if composition_same:
                    composition_id = current_composition_id
                    break

    #havent found same compositon, create new
    if composition_id is None:
        # created_new_composition = True
        # this is new compostion
        cur.execute("insert into score (name,genre,key,incipit,year) values (?,?,?,?,?)",(composition.name,composition.genre,composition.key,composition.incipit,composition.year))
        composition_id = cur.lastrowid
        # create relacion between composition and composers
        for cid in composer_ids:
            cur.execute("insert into score_author (score,composer) values (?,?)",(composition_id,cid))
        # create new voices, beacause this is new composition
        for i in range(len(composition.voices)):
            voice = composition.voices[i]
            if voice is not None:
                cur.execute("insert into voice (number,score,range,name) values (?,?,?,?)",(i+1, composition_id,voice.range, voice.name))
        # created_new_composition = True


    # check eidtors - same as coposers without born died
    editor_ids = []
    for editor in pr.edition.authors:
        cur.execute("select id from person where name is ?", (editor.name,))
        editors = cur.fetchall()
        if len(editors) == 1:
            # we have found editor in database, we dont have to upadte born,died
            editor_ids.append(editors[0][0])
        else:
            #create new editor
            cur.execute("insert into person (name) values (?)",(editor.name,))
            editor_ids.append(cur.lastrowid)
    # check edition
    edition = pr.edition
    cur.execute("select id from edition where score is ? and name is ?",(composition_id, edition.name))
    # Note: i can just use composition_id, when i created composition now, it wont be there, otherwise it can be there
    # if there is any such edition, check editors
    editions = cur.fetchall()
    edition_id = None
    if len(editions) > 0:
        for ed in editions:
            current_edition_id = ed[0]
            cur.execute("select editor from edition_author where edition is ?", (current_edition_id,))
            current_edition_editors = cur.fetchall()
            if set(i[0] for i in current_edition_editors) == set(editor_ids):
                edition_id = current_edition_id
                break

    if edition_id is None:
        cur.execute("insert into edition (score,name) values (?,?)",(composition_id,edition.name))
        edition_id = cur.lastrowid
        for eid in editor_ids:
            cur.execute("insert into edition_author (edition,editor) values (?,?)",(edition_id,eid))
    # check print
    partiture = 'Y' if pr.partiture else 'N'
    cur.execute("insert into print (id, edition, partiture) values (?,?,?)",(pr.print_id,edition_id,partiture))


# reset file
f = open(database,"w")
f.close()

conn = sqlite3.connect(database)
cur = conn.cursor()
# create tables from sql script
script = open("scorelib.sql","r")
cur.executescript(script.read())
script.close

prints = load(sys.argv[1])

for pr in prints:
    insert_print(pr,cur)

conn.commit()
conn.close()